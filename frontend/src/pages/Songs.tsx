import { useState, useMemo } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SongCard from "@/components/SongCard";
import SectionTitle from "@/components/SectionTitle";
import { melodies, villageNames, type Song } from "@/data/mockData";
import { Search, Filter } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

// Định nghĩa kiểu dữ liệu từ Backend
interface BackendSong {
  id: number;
  name: string;
  category: string;
  image_url: string;
  audio_url?: string;
  video_url?: string;
  village?: string;
  artist?: { name: string } | string;
}

export default function Songs() {
  const { t } = useTranslation();
  const [search, setSearch] = useState("");
  const [melodyFilter, setMelodyFilter] = useState("");
  const [villageFilter, setVillageFilter] = useState("");

  // Lấy dữ liệu bài hát từ API
  const { data: rawSongs = [], isLoading } = useQuery<BackendSong[]>({
    queryKey: ["songs"],
    queryFn: async () => {
      const resp = await fetch("/api/melodies/");
      if (!resp.ok) throw new Error("Failed to fetch songs");
      const data = await resp.json();
      return data as BackendSong[];
    }
  });

  // Chuyển đổi dữ liệu backend sang định dạng frontend (Song interface)
  const songsData = useMemo(() => {
    return rawSongs.map((s) => {
      const artistName =
        typeof s.artist === "string" ? s.artist : s.artist?.name || "Nghệ nhân Quan họ";

      return {
        id: s.id,
        title: s.name,
        melody: s.category,
        village: s.village || "Bắc Ninh",
        artist: artistName,
        artistId: 0, // Dữ liệu backend chưa cung cấp ID nghệ nhân rõ ràng trong list
        lyrics: "", // Lyrics lấy ở trang chi tiết
        imageUrl: s.image_url,
        audioUrl: s.audio_url,
        videoUrl: s.video_url,
        duration: "4:00", // Placeholder duration
      } as Song;
    });
  }, [rawSongs]);

  // Lọc danh sách bài hát
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

          {/* Tìm kiếm & Bộ lọc */}
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
                <option value="">{t("songs_page.all_villages")}</option>
                {villageNames.map((v) => (
                  <option key={v} value={v}>{v}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Trạng thái tải dữ liệu */}
          {isLoading && (
            <div className="flex justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
            </div>
          )}

          {/* Kết quả */}
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
