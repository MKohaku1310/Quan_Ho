import { useState, useMemo } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SongCard from "@/components/SongCard";
import SectionTitle from "@/components/SectionTitle";
import { type Song } from "@/data/mockData";
import { Search, Filter } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

interface BackendSong {
  id: number;
  name: string;
  category: string;
  image_url?: string | null;
  audio_url?: string | null;
  video_url?: string | null;
  village?: string | null;
  artist?: { name: string } | string | null;
  artist_id?: number | null;
  lyrics?: string | null;
  duration?: string | null;
}

export default function Songs() {
  const { t } = useTranslation();
  const [search, setSearch] = useState("");
  const [melodyFilter, setMelodyFilter] = useState("");
  const [villageFilter, setVillageFilter] = useState("");

  const { data: rawSongs = [], isLoading } = useQuery<BackendSong[]>({
    queryKey: ["songs"],
    queryFn: async () => {
      const resp = await fetch("/api/melodies/");
      if (!resp.ok) throw new Error("Failed to fetch songs");
      const data = await resp.json();
      return data as BackendSong[];
    }
  });

  const songsData = useMemo(() => {
    return rawSongs.map((s) => {
      const artistName =
        typeof s.artist === "string" ? s.artist : s.artist?.name || "Nghệ nhân Quan họ";

      return {
        id: s.id,
        title: s.name,
        melody: s.category,
        village: s.village ?? "Bắc Ninh",
        artist: artistName,
        artistId: s.artist_id ?? 0,
        lyrics: s.lyrics ?? "",
        imageUrl: s.image_url ?? "",
        audioUrl: s.audio_url ?? undefined,
        videoUrl: s.video_url ?? undefined,
        duration: s.duration ?? "",
      };
    });
  }, [rawSongs]);

  const melodyOptions = useMemo(() => {
    return Array.from(new Set(songsData.map((s) => s.melody))).filter(Boolean);
  }, [songsData]);

  const villageOptions = useMemo(() => {
    return Array.from(new Set(songsData.map((s) => s.village))).filter(Boolean);
  }, [songsData]);

  const filtered = useMemo(() => {
    return songsData.filter((s) => {
      const matchSearch =
        !search ||
        s.title.toLowerCase().includes(search.toLowerCase()) ||
        s.artist.toLowerCase().includes(search.toLowerCase());
      const matchMelody = !melodyFilter || s.melody === melodyFilter;
      const matchVillage = !villageFilter || s.village === villageFilter;
      return matchSearch && matchMelody && matchVillage;
    });
  }, [songsData, search, melodyFilter, villageFilter]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title={t("songs_page.title")}
            subtitle={t("songs_page.subtitle")}
            translate={false}
          />

          <div className="mb-8 flex flex-col gap-4 rounded-lg border border-border bg-card p-4 shadow-card sm:flex-row sm:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder={t("songs_page.search_placeholder")}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full rounded-md border border-input bg-background py-2 pl-9 pr-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
            <div className="flex gap-3">
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-muted-foreground" />
                <select
                  value={melodyFilter}
                  onChange={(e) => setMelodyFilter(e.target.value)}
                  className="rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground"
                >
                  <option value="">{t("songs_page.all_melodies")}</option>
                  {melodyOptions.map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
                </select>
              </div>
              <select
                value={villageFilter}
                onChange={(e) => setVillageFilter(e.target.value)}
                className="rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground"
              >
                <option value="">{t("songs_page.all_villages")}</option>
                {villageOptions.map((v) => (
                  <option key={v} value={v}>
                    {v}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {isLoading && (
            <div className="flex justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
            </div>
          )}

          {!isLoading && filtered.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {filtered.map((song, i) => (
                <SongCard key={song.id} song={song} index={i} />
              ))}
            </div>
          ) : !isLoading && (
            <div className="py-20 text-center text-muted-foreground">
              {t("songs_page.no_songs")}
            </div>
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}
