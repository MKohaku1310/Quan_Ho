import { useParams, Link } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import CommentSection from "@/components/CommentSection";
import { useAuth } from "@/contexts/AuthContext";
import { ArrowLeft, Play, Music, MapPin, User, Clock, Heart } from "lucide-react";
import { motion } from "framer-motion";
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

export default function SongDetail() {
  const { t } = useTranslation();
  const { id } = useParams();
  const { isFavorite, toggleFavorite } = useAuth();
  

  const { data: rawSong, isLoading, error } = useQuery<BackendSong>({
    queryKey: ["song", id],
    queryFn: async () => {
      const resp = await fetch(`/api/melodies/${id}`);
      if (!resp.ok) {
        if (resp.status === 404) return null;
        throw new Error("Failed to fetch song");
      }
      return await resp.json();
    },
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="flex justify-center py-20">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
        </div>
        <Footer />
      </div>
    );
  }


  if (!rawSong || error) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="container mx-auto px-4 py-20 text-center">
          <p className="text-muted-foreground">{t("songs_page.no_songs")}</p>
          <Link to="/bai-hat" className="mt-4 inline-block text-primary hover:underline">
            ← {t("common.back")}
          </Link>
        </div>
        <Footer />
      </div>
    );
  }

  const artistName = typeof rawSong.artist === "string" ? rawSong.artist : rawSong.artist?.name || "Nghệ nhân Quan họ";
  const song = {
    id: rawSong.id,
    title: rawSong.name,
    melody: rawSong.category,
    village: rawSong.village ?? "Bắc Ninh",
    artist: artistName,
    lyrics: rawSong.lyrics ?? "",
    imageUrl: rawSong.image_url ?? "https://images.unsplash.com/photo-1518639192441-8fce0a366e2e?w=800",
    videoUrl: rawSong.video_url,
    duration: rawSong.duration ?? "",
  };

  const favorited = isFavorite(song.id);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto max-w-4xl px-4">
          <Link to="/bai-hat" className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary">
            <ArrowLeft className="h-4 w-4" /> {t("songs_page.back_to_library")}
          </Link>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="overflow-hidden rounded-xl border border-border bg-card shadow-elevated"
          >

            {song.videoUrl ? (
              <div className="relative aspect-video overflow-hidden">
                <iframe
                  src={song.videoUrl}
                  title={song.title}
                  className="absolute left-0 top-0 h-full w-full border-0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              </div>
            ) : (
              <div className="relative aspect-[21/9] overflow-hidden">
                <img src={song.imageUrl} alt={song.title} className="h-full w-full object-cover" />
                <div className="absolute inset-0 flex items-center justify-center bg-foreground/30">
                  <button className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-elevated transition-transform hover:scale-110">
                    <Play className="h-7 w-7 ml-1" />
                  </button>
                </div>
              </div>
            )}

            <div className="p-6 md:p-8">
              <div className="flex items-start justify-between gap-4">
                <h1 className="font-display text-3xl font-bold text-card-foreground">{song.title}</h1>
                <button
                  onClick={() => toggleFavorite(song.id)}
                  className={`flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full border transition-all ${
                    favorited
                      ? "border-primary bg-primary text-primary-foreground"
                      : "border-border bg-muted text-muted-foreground hover:border-primary hover:text-primary"
                  }`}
                  aria-label={favorited ? t("song.remove_fav") : t("song.add_fav")}
                >
                  <Heart className={`h-5 w-5 ${favorited ? "fill-current" : ""}`} />
                </button>
              </div>
              <div className="mt-3 flex flex-wrap gap-4 text-sm text-muted-foreground">
                <span className="flex items-center gap-1"><User className="h-4 w-4" /> {song.artist}</span>
                <span className="flex items-center gap-1"><Music className="h-4 w-4" /> {song.melody}</span>
                <span className="flex items-center gap-1"><MapPin className="h-4 w-4" /> {t("artist.village")} {song.village}</span>
                <span className="flex items-center gap-1"><Clock className="h-4 w-4" /> {song.duration}</span>
              </div>


              <div className="mt-8">
                <h2 className="font-display text-xl font-semibold text-card-foreground">{t("songs_page.lyrics")}</h2>
                <p className="mt-3 whitespace-pre-line leading-relaxed text-muted-foreground italic">
                  {song.lyrics}
                </p>
              </div>


              <CommentSection targetType="song" targetId={song.id} />
            </div>
          </motion.div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
