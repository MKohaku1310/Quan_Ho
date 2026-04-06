import { useMemo, useState, useRef, useEffect } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { type Village } from "@/data/mockData";
import { motion } from "framer-motion";
import { MapPin, Calendar, Users, Map as MapIcon } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";


interface BackendVillage extends Omit<Village, 'imageUrl' | 'lat' | 'lng'> {
  image_url: string;
  latitude: number;
  longitude: number;
}

export default function Villages() {
  const { t } = useTranslation();
  

  const { data: rawVillages = [], isLoading } = useQuery<BackendVillage[]>({
    queryKey: ["locations-list"],
    queryFn: async () => {
      const resp = await fetch("/api/locations/");
      if (!resp.ok) throw new Error("Failed to fetch villages");
      const data = await resp.json();
      return data as BackendVillage[];
    }
  });


  const villages = useMemo(() => {
    return rawVillages.map((v) => ({
      ...v,
      imageUrl: v.image_url,
      lat: v.latitude,
      lng: v.longitude,
      artists: [],
    })) as Village[];
  }, [rawVillages]);

  const [selectedVillageId, setSelectedVillageId] = useState<number | null>(null);
  const mapRef = useRef<HTMLDivElement>(null);

  const selectedVillage = useMemo(() => {
    return villages.find(v => v.id === selectedVillageId) || null;
  }, [villages, selectedVillageId]);

  const mapQuery = selectedVillage 
    ? encodeURIComponent(`${selectedVillage.name}, ${selectedVillage.address}`) 
    : encodeURIComponent("Bắc Ninh, Việt Nam");

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

          <div ref={mapRef} className="mb-10">
            <div className="overflow-hidden rounded-lg border border-border bg-card shadow-card h-[400px]">
              <iframe
                title="Bản đồ Quan họ Bắc Ninh"
                width="100%"
                height="100%"
                style={{ border: 0 }}
                loading="lazy"
                allowFullScreen
                src={`https://maps.google.com/maps?q=${mapQuery}&t=&z=14&ie=UTF8&iwloc=&output=embed`}
              ></iframe>
            </div>

            {selectedVillage && (
              <motion.div 
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 rounded-lg border-2 border-primary/50 bg-primary/5 p-6 shadow-elevated"
              >
                <div className="flex flex-col gap-6 md:flex-row">
                  <div className="md:w-1/3">
                    <img
                      src={selectedVillage.imageUrl}
                      alt={selectedVillage.name}
                      className="h-48 w-full rounded-md object-cover shadow-sm"
                    />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-display text-2xl font-bold text-primary mb-3">
                      {selectedVillage.name}
                    </h3>
                    <div className="mb-4 flex items-start gap-2 text-sm text-primary/80">
                      <MapIcon className="mt-0.5 h-4 w-4 shrink-0" />
                      <span>{selectedVillage.address}</span>
                    </div>
                    <p className="text-foreground leading-relaxed">
                      {selectedVillage.description}
                    </p>
                    {selectedVillage.festival && (
                      <div className="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
                        <Calendar className="h-4 w-4 text-accent" /> Lễ hội: {selectedVillage.festival}
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {isLoading && (
            <div className="flex justify-center py-20">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
            </div>
          )}

          <div className="grid gap-6 md:grid-cols-2">
            {villages.map((village, i) => (
              <motion.div
                key={village.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                onClick={() => {
                  setSelectedVillageId(village.id);
                  const y = mapRef.current ? mapRef.current.getBoundingClientRect().top + window.scrollY - 100 : 0;
                  window.scrollTo({ top: y, behavior: 'smooth' });
                }}
                className={`group cursor-pointer overflow-hidden rounded-lg border bg-card shadow-card transition-all hover:shadow-elevated hover:border-primary/50 ${
                  selectedVillageId === village.id ? "border-primary ring-1 ring-primary" : "border-border"
                }`}
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
                  <p className={`text-sm text-muted-foreground ${selectedVillageId === village.id ? "" : "line-clamp-2"}`}>
                    {village.description}
                  </p>
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
