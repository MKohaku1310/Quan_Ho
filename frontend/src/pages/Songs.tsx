import { useState, useMemo } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SongCard from "@/components/SongCard";
import SectionTitle from "@/components/SectionTitle";
import { melodies, villageNames, type Song } from "@/data/mockData";
import { Search, Filter } from "lucide-react";
import { useQuery } from "@tanstack/react-query";

export default function Songs() {
  const [search, setSearch] = useState("");
  const [melodyFilter, setMelodyFilter] = useState("");
  const [villageFilter, setVillageFilter] = useState("");

  const { data: rawSongs = [], isLoading } = useQuery<Song[]>({
    queryKey: ["songs"],
    queryFn: async () => {
      const resp = await fetch("/api/melodies/");
      if (!resp.ok) throw new Error("Failed to fetch songs");
      const data: unknown = await resp.json();
      return data as Song[];
    }
  });

  const songsData = useMemo(() => {
    return rawSongs.map((s) => ({
      ...s,
      title: s.name, // Map name to title
      imageUrl: s.image_url,
      audioUrl: s.audio_url,
      videoUrl: s.video_url,
      melody: s.category, // Map category to melody
      artist: s.artist?.name || "Nghệ nhân Quan họ", // If relationship is loaded
    })) as Song[];
  }, [rawSongs]);

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
            title="Thư viện bài hát"
            subtitle="Khám phá kho tàng làn điệu Quan họ Bắc Ninh"
          />

          {/* Search & Filters */}
          <div className="mb-8 flex flex-col gap-4 rounded-lg border border-border bg-card p-4 shadow-card sm:flex-row sm:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder="Tìm kiếm bài hát, nghệ nhân..."
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
                  <option value="">Tất cả làn điệu</option>
                  {melodies.map((m) => (
                    <option key={m} value={m}>{m}</option>
                  ))}
                </select>
              </div>
              <select
                value={villageFilter}
                onChange={(e) => setVillageFilter(e.target.value)}
                className="rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground"
              >
                <option value="">Tất cả làng</option>
                {villageNames.map((v) => (
                  <option key={v} value={v}>{v}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Loading state */}
          {isLoading && (
            <div className="flex justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
            </div>
          )}

          {/* Results */}
          {!isLoading && filtered.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {filtered.map((song, i) => (
                <SongCard key={song.id} song={song} index={i} />
              ))}
            </div>
          ) : !isLoading && (
            <div className="py-20 text-center text-muted-foreground">
              Không tìm thấy bài hát nào phù hợp.
            </div>
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}
