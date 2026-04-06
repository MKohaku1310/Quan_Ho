import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ArtistCard from "@/components/ArtistCard";
import SectionTitle from "@/components/SectionTitle";
import { type Artist } from "@/data/mockData";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

interface BackendArtist extends Omit<Artist, 'photo'> {
  image_url: string;
}

export default function Artists() {
  const { t } = useTranslation();
  
  const { data: artists = [], isLoading } = useQuery<Artist[]>({
    queryKey: ["artists"],
    queryFn: async () => {
      const resp = await fetch("/api/artists/");
      if (!resp.ok) throw new Error("Failed to fetch artists");
      const data = await resp.json();
      return (data as BackendArtist[]).map((a) => ({
        ...a,
        photo: a.image_url, // Ánh xạ image_url từ backend sang photo của frontend
      })) as Artist[];
    }
  });

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title={t("artists_page.title")}
            subtitle={t("artists_page.subtitle")}
            translate={false}
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
               {t("artists_page.no_artists")}
             </div>
          )}
        </div>
      </section>
      <Footer />
    </div>
  );
}
