import { useParams, Link } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SongCard from "@/components/SongCard";
import { artists, songs } from "@/data/mockData";
import { ArrowLeft, MapPin, Award, Music } from "lucide-react";
import { motion } from "framer-motion";

export default function ArtistDetail() {
  const { id } = useParams();
  const artist = artists.find((a) => a.id === Number(id));

  if (!artist) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="container mx-auto px-4 py-20 text-center">
          <p className="text-muted-foreground">Không tìm thấy nghệ nhân.</p>
          <Link to="/nghe-nhan" className="mt-4 inline-block text-primary hover:underline">← Quay lại</Link>
        </div>
        <Footer />
      </div>
    );
  }

  const artistSongs = songs.filter((s) => s.artistId === artist.id);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto max-w-4xl px-4">
          <Link to="/nghe-nhan" className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary">
            <ArrowLeft className="h-4 w-4" /> Quay lại danh sách
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
                  <span className="flex items-center gap-1"><MapPin className="h-4 w-4" /> Làng {artist.village}</span>
                  <span className="flex items-center gap-1"><Award className="h-4 w-4" /> {artist.performances} buổi diễn</span>
                </div>
                <p className="mt-4 leading-relaxed text-muted-foreground">{artist.biography}</p>
                <div className="mt-4 rounded-lg bg-muted p-4">
                  <h3 className="text-sm font-semibold text-foreground">Đóng góp nổi bật</h3>
                  <p className="mt-1 text-sm text-muted-foreground">{artist.contributions}</p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Related songs */}
          {artistSongs.length > 0 && (
            <div className="mt-12">
              <h2 className="mb-6 flex items-center gap-2 font-display text-2xl font-bold text-foreground">
                <Music className="h-5 w-5 text-primary" /> Bài hát liên quan
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
