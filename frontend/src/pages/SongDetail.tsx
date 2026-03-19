import { useParams, Link } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import CommentSection from "@/components/CommentSection";
import { songs } from "@/data/mockData";
import { useAuth } from "@/contexts/AuthContext";
import { ArrowLeft, Play, Music, MapPin, User, Clock, Heart } from "lucide-react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

export default function SongDetail() {
  const { t } = useTranslation();
  const { id } = useParams();
  const { isFavorite, toggleFavorite } = useAuth();
  
  // Tìm bài hát theo ID
  const song = songs.find((s) => s.id === Number(id));

  // Trạng thái không tìm thấy bài hát
  if (!song) {
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
            {/* Banner bài hát */}
            <div className="relative aspect-[21/9] overflow-hidden">
              <img src={song.imageUrl} alt={song.title} className="h-full w-full object-cover" />
              <div className="absolute inset-0 flex items-center justify-center bg-foreground/30">
                <button className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-elevated transition-transform hover:scale-110">
                  <Play className="h-7 w-7 ml-1" />
                </button>
              </div>
            </div>

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

              {/* Trình phát âm thanh (Placeholder) */}
              <div className="mt-6 rounded-lg bg-muted p-4">
                <div className="flex items-center gap-3">
                  <button className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground">
                    <Play className="h-4 w-4 ml-0.5" />
                  </button>
                  <div className="flex-1">
                    <div className="h-2 rounded-full bg-border">
                      <div className="h-2 w-1/3 rounded-full bg-primary" />
                    </div>
                    <div className="mt-1 flex justify-between text-xs text-muted-foreground">
                      <span>1:24</span>
                      <span>{song.duration}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Lời bài hát */}
              <div className="mt-8">
                <h2 className="font-display text-xl font-semibold text-card-foreground">{t("songs_page.lyrics")}</h2>
                <p className="mt-3 whitespace-pre-line leading-relaxed text-muted-foreground italic">
                  {song.lyrics}
                </p>
              </div>

              {/* Phần bình luận */}
              <CommentSection targetType="song" targetId={song.id} />
            </div>
          </motion.div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
