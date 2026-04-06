import { useParams, Link } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SongCard from "@/components/SongCard";
import { ArrowLeft, MapPin, Award, Music } from "lucide-react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";


interface BackendArtist {
  id: number;
  name: string;
  image_url?: string | null;
  biography?: string | null;
  village?: string | null;
  contributions?: string | null;
  performances?: number | null;
}

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

export default function ArtistDetail() {
  const { t } = useTranslation();
  const { id } = useParams();
  

  const { data: rawArtist, isLoading: isLoadingArtist, error: artistError } = useQuery<BackendArtist>({
    queryKey: ["artist", id],
    queryFn: async () => {
      const resp = await fetch(`/api/artists/${id}`);
      if (!resp.ok) {
        if (resp.status === 404) return null;
        throw new Error("Failed to fetch artist");
      }
      return await resp.json();
    },
    enabled: !!id,
  });


  const { data: allSongs = [] } = useQuery<BackendSong[]>({
    queryKey: ["songs"],
    queryFn: async () => {
      const resp = await fetch("/api/melodies/");
      if (!resp.ok) throw new Error("Failed to fetch songs");
      return await resp.json();
    }
  });

  if (isLoadingArtist) {
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


  if (!rawArtist || artistError) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="container mx-auto px-4 py-20 text-center">
          <p className="text-muted-foreground">{t("artists_page.no_artists")}</p>
          <Link to="/nghe-nhan" className="mt-4 inline-block text-primary hover:underline">
            ← {t("common.back")}
          </Link>
        </div>
        <Footer />
      </div>
    );
  }

  const artist = {
    id: rawArtist.id,
    name: rawArtist.name,
    photo: rawArtist.image_url ?? "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800",
    biography: rawArtist.biography ?? "",
    village: rawArtist.village ?? "Bắc Ninh",
    contributions: rawArtist.contributions ?? "",
    performances: rawArtist.performances ?? 0,
  };


  const rawArtistSongs = allSongs.filter((s) => s.artist_id === artist.id);
  const artistSongs = rawArtistSongs.map(s => {
    const artistName = typeof s.artist === "string" ? s.artist : s.artist?.name || artist.name;
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

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto max-w-4xl px-4">
          <Link to="/nghe-nhan" className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary">
            <ArrowLeft className="h-4 w-4" /> {t("artists_page.back_to_list")}
          </Link>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="overflow-hidden rounded-xl border border-border bg-card shadow-elevated"
          >
            <div className="flex flex-col md:flex-row">
              <div className="md:w-1/3">
                <img src={artist.photo} alt={artist.name} className="h-full w-full object-cover" />
              </div>
              <div className="flex-1 p-6 md:p-8">
                <h1 className="font-display text-3xl font-bold text-card-foreground">{artist.name}</h1>
                <div className="mt-3 flex flex-wrap gap-4 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <MapPin className="h-4 w-4" /> {t("artist.village")} {artist.village}
                  </span>
                  <span className="flex items-center gap-1">
                    <Award className="h-4 w-4" /> {artist.performances} {t("artist.performances")}
                  </span>
                </div>
                <p className="mt-4 leading-relaxed text-muted-foreground">{artist.biography}</p>
                <div className="mt-4 rounded-lg bg-muted p-4">
                  <h3 className="text-sm font-semibold text-foreground">{t("artists_page.contributions")}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">{artist.contributions}</p>
                </div>
              </div>
            </div>
          </motion.div>


          {artistSongs.length > 0 && (
            <div className="mt-12">
              <h2 className="mb-6 flex items-center gap-2 font-display text-2xl font-bold text-foreground">
                <Music className="h-5 w-5 text-primary" /> {t("artists_page.famous_songs")}
              </h2>
              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {artistSongs.map((song, i) => (
                  <SongCard key={song.id} song={song} index={i} />
                ))}
              </div>
            </div>
          )}
        </div>
      </section>
      <Footer />
    </div>
  );
}
