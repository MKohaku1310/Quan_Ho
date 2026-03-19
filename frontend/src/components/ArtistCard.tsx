import { Link } from "react-router-dom";
import { MapPin, Award } from "lucide-react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import type { Artist } from "@/data/mockData";

export default function ArtistCard({ artist, index = 0 }: { artist: Artist; index?: number }) {
  const { t } = useTranslation();
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
    >
      <Link
        to={`/nghe-nhan/${artist.id}`}
        className="group block overflow-hidden rounded-lg border border-border bg-card shadow-card transition-all hover:shadow-elevated"
      >
        <div className="relative aspect-square overflow-hidden">
          <img
            src={artist.photo}
            alt={artist.name}
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
          />
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-foreground/70 to-transparent p-4">
            <h3 className="font-display text-lg font-bold text-primary-foreground">{artist.name}</h3>
          </div>
        </div>
        <div className="p-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <MapPin className="h-3.5 w-3.5" /> {t("artist.village")} {artist.village}
          </div>
          <div className="mt-1.5 flex items-center gap-2 text-sm text-muted-foreground">
            <Award className="h-3.5 w-3.5" /> {artist.performances} {t("artist.performances")}
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
