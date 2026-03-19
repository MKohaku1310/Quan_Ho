import { useMemo } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { type Village } from "@/data/mockData";
import { motion } from "framer-motion";
import { MapPin, Calendar, Users, Map as MapIcon } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

// Định nghĩa kiểu dữ liệu từ Backend
interface BackendVillage extends Omit<Village, 'imageUrl'> {
  image_url: string;
}

export default function Villages() {
  const { t } = useTranslation();
  
  // Lấy dữ liệu danh sách làng từ API
  const { data: rawVillages = [], isLoading } = useQuery<BackendVillage[]>({
    queryKey: ["locations-list"],
    queryFn: async () => {
      const resp = await fetch("/api/locations/");
      if (!resp.ok) throw new Error("Failed to fetch villages");
      const data = await resp.json();
      return data as BackendVillage[];
    }
  });

  // Chuyển đổi dữ liệu để phù hợp với giao diện (mapping snake_case sang camelCase)
  const villages = useMemo(() => {
    return rawVillages.map((v) => ({
      ...v,
      imageUrl: v.image_url,
      artists: [], // Placeholder nếu chưa được join
    })) as Village[];
  }, [rawVillages]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title={t("villages_page.title")}
            subtitle={t("villages_page.subtitle")}
            translate={false}
          />

          {/* Bản đồ (Placeholder) */}
          <div className="mb-10 overflow-hidden rounded-lg border border-border bg-card shadow-card">
            <div className="flex items-center justify-center bg-muted py-20">
              <div className="text-center">
                <MapPin className="mx-auto h-10 w-10 text-primary" />
                <p className="mt-2 text-muted-foreground">{t("villages_page.map_title")}</p>
                <p className="text-xs text-muted-foreground">({t("villages_page.map_desc")})</p>
              </div>
            </div>
          </div>

          {/* Trạng thái tải dữ liệu */}
          {isLoading && (
            <div className="flex justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
            </div>
          )}

          {/* Danh sách làng */}
          <div className="grid gap-6 md:grid-cols-2">
            {villages.map((village, i) => (
              <motion.div
                key={village.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="group overflow-hidden rounded-lg border border-border bg-card shadow-card transition-all hover:shadow-elevated"
              >
                <div className="relative aspect-[2/1] overflow-hidden">
                  <img
                    src={village.imageUrl}
                    alt={village.name}
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                    loading="lazy"
                  />
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-foreground/60 to-transparent p-4">
                    <h3 className="font-display text-xl font-bold text-primary-foreground">{village.name}</h3>
                  </div>
                </div>
                <div className="p-5">
                  <div className="mb-2 flex items-start gap-2 text-xs text-primary">
                    <MapIcon className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                    <span>{village.address || t("villages_page.updating_address")}</span>
                  </div>
                  <p className="text-sm text-muted-foreground line-clamp-2">{village.description}</p>
                  <div className="mt-4 flex flex-wrap gap-3 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3.5 w-3.5 text-accent" /> {village.festival}
                    </span>
                    <span className="flex items-center gap-1">
                      <Users className="h-3.5 w-3.5 text-primary" />
                      {village.artists?.length || 0} {t("villages_page.artist_count")}
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
