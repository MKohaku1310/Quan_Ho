import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ArtistCard from "@/components/ArtistCard";
import SectionTitle from "@/components/SectionTitle";
import { type Artist } from "@/data/mockData";
import { useQuery } from "@tanstack/react-query";

export default function Artists() {
  const { data: artists = [], isLoading } = useQuery<Artist[]>({
    queryKey: ["artists"],
    queryFn: async () => {
      const resp = await fetch("/api/artists/");
      if (!resp.ok) throw new Error("Failed to fetch artists");
      const data: unknown = await resp.json();
      return (data as Artist[]).map((a) => ({
        ...a,
        photo: a.image_url, // Map backend image_url to frontend photo
      }));
    }
  });

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title="Nghệ nhân Quan Họ"
            subtitle="Những người nghệ sĩ đã và đang gìn giữ ngọn lửa Quan họ cho muôn đời sau"
          />

          {isLoading && (
            <div className="flex justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
            </div>
          )}

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {artists.map((artist, i) => (
              <ArtistCard key={artist.id} artist={artist} index={i} />
            ))}
          </div>
          
          {!isLoading && artists.length === 0 && (
             <div className="py-20 text-center text-muted-foreground">
               Không tìm thấy nghệ nhân nào.
             </div>
          )}
        </div>
      </section>
      <Footer />
    </div>
  );
}
