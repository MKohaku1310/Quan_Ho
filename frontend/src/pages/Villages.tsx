import { useMemo } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { type Village } from "@/data/mockData";
import { motion } from "framer-motion";
import { MapPin, Calendar, Users, Map as MapIcon } from "lucide-react";
import { useQuery } from "@tanstack/react-query";

export default function Villages() {
  const { data: rawVillages = [], isLoading } = useQuery<Village[]>({
    queryKey: ["locations-list"],
    queryFn: async () => {
      const resp = await fetch("/api/locations/");
      if (!resp.ok) throw new Error("Failed to fetch villages");
      const data: unknown = await resp.json();
      return data as Village[];
    }
  });

  const villages = useMemo(() => {
    return rawVillages.map((v) => ({
      ...v,
      imageUrl: v.image_url,
      artists: [], // Placeholder if not joined
    })) as Village[];
  }, [rawVillages]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title="Làng Quan Họ"
            subtitle="49 làng Quan họ gốc – nơi khai sinh nghệ thuật hát giao duyên"
          />

          {/* Map placeholder */}
          <div className="mb-10 overflow-hidden rounded-lg border border-border bg-card shadow-card">
            <div className="flex items-center justify-center bg-muted py-20">
              <div className="text-center">
                <MapPin className="mx-auto h-10 w-10 text-primary" />
                <p className="mt-2 text-muted-foreground">Bản đồ các làng Quan họ gốc</p>
                <p className="text-xs text-muted-foreground">(Tích hợp bản đồ GPS từ dữ liệu Backend)</p>
              </div>
            </div>
          </div>

          {/* Loading state */}
          {isLoading && (
            <div className="flex justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
            </div>
          )}

          {/* Village list */}
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
                    <span>{village.address || "Đang cập nhật địa chỉ"}</span>
                  </div>
                  <p className="text-sm text-muted-foreground line-clamp-2">{village.description}</p>
                  <div className="mt-4 flex flex-wrap gap-3 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3.5 w-3.5 text-accent" /> {village.festival}
                    </span>
                    <span className="flex items-center gap-1">
                      <Users className="h-3.5 w-3.5 text-primary" /> {/* Mocking count based on data if available */}
                      {village.artists?.length || 0} nghệ nhân
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
