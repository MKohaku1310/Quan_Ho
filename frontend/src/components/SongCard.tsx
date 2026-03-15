import { Link } from "react-router-dom";
import { Play, Clock, Music, Heart } from "lucide-react";
import { motion } from "framer-motion";
import type { Song } from "@/data/mockData";
import { useAuth } from "@/contexts/AuthContext";

export default function SongCard({ song, index = 0 }: { song: Song; index?: number }) {
  const { isFavorite, toggleFavorite } = useAuth();
  const favorited = isFavorite(song.id);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      className="relative"
    >
      {/* Favorite button */}
      <button
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          toggleFavorite(song.id);
        }}
        className={`absolute right-3 top-3 z-10 flex h-8 w-8 items-center justify-center rounded-full transition-all ${
          favorited
            ? "bg-primary text-primary-foreground shadow-elevated"
            : "bg-background/80 text-muted-foreground hover:bg-primary hover:text-primary-foreground backdrop-blur-sm"
        }`}
        aria-label={favorited ? "Bỏ yêu thích" : "Thêm yêu thích"}
      >
        <Heart className={`h-4 w-4 ${favorited ? "fill-current" : ""}`} />
      </button>

      <Link
        to={`/bai-hat/${song.id}`}
        className="group block overflow-hidden rounded-lg border border-border bg-card shadow-card transition-all hover:shadow-elevated"
      >
        <div className="relative aspect-[4/3] overflow-hidden">
          <img
            src={song.imageUrl}
            alt={song.title}
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
            loading="lazy"
          />
          <div className="absolute inset-0 flex items-center justify-center bg-foreground/0 transition-colors group-hover:bg-foreground/30">
            <div className="flex h-12 w-12 scale-0 items-center justify-center rounded-full bg-primary text-primary-foreground transition-transform group-hover:scale-100">
              <Play className="h-5 w-5 ml-0.5" />
            </div>
          </div>
        </div>
        <div className="p-4">
          <h3 className="font-display text-base font-semibold text-card-foreground line-clamp-1">
            {song.title}
          </h3>
          <p className="mt-1 text-sm text-muted-foreground">{song.artist}</p>
          <div className="mt-3 flex items-center gap-3 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Music className="h-3 w-3" /> {song.melody}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" /> {song.duration}
            </span>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
