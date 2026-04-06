import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Calendar, MapPin, ArrowLeft, Clock, Share2, Ticket } from "lucide-react";
import { useTranslation } from "react-i18next";

interface Event {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date?: string;
  image_url: string;
  status: string;
  location?: { name: string; address: string };
}

export default function EventDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();

  const { data: event, isLoading } = useQuery<Event>({
    queryKey: ["event", id],
    queryFn: async () => {
      const resp = await fetch(`/api/events/${id}`);
      if (!resp.ok) throw new Error("Failed to fetch event");
      return resp.json();
    }
  });

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-background text-center px-4">
        <h2 className="text-2xl font-bold mb-4">{t("common.not_found")}</h2>
        <button 
          onClick={() => navigate("/tin-tuc")}
          className="flex items-center gap-2 text-primary hover:underline"
        >
          <ArrowLeft className="h-4 w-4" /> {t("common.back_to_list")}
        </button>
      </div>
    );
  }

  const startDate = new Date(event.start_date);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navbar />

      <main className="py-20">
        <div className="container mx-auto px-4 max-w-5xl">
          <motion.button
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={() => navigate("/tin-tuc")}
            className="mb-8 flex items-center gap-2 text-muted-foreground transition-colors hover:text-primary"
          >
            <ArrowLeft className="h-4 w-4" /> {t("common.back_to_list")}
          </motion.button>

          <div className="flex flex-col lg:flex-row gap-12">
            <div className="lg:w-2/3">
              <motion.header
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-10"
              >
                <div className={`mb-4 inline-flex items-center rounded-full px-3 py-1 text-sm font-medium uppercase tracking-wider ${
                  event.status === 'upcoming' 
                  ? "bg-primary/10 text-primary" 
                  : "bg-muted text-muted-foreground"
                }`}>
                  {t(`event_status.${event.status}`)}
                </div>
                <h1 className="font-display text-4xl font-bold text-foreground md:text-5xl leading-tight">
                  {event.title}
                </h1>
              </motion.header>

              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="mb-12 overflow-hidden rounded-3xl shadow-elevated aspect-video relative"
              >
                 <img 
                  src={event.image_url} 
                  alt={event.title} 
                  className="h-full w-full object-cover" 
                />
              </motion.div>

              <div className="prose prose-lg dark:prose-invert max-w-none text-muted-foreground leading-relaxed">
                <h3 className="text-foreground font-display text-2xl font-bold mb-4">{t("news_page.about_event")}</h3>
                <p>{event.description}</p>
                <p className="mt-4">Đây là cơ hội tuyệt vời để những người yêu mến Quan họ được trực tiếp trải nghiệm không gian văn hóa đặc sắc của vùng Kinh Bắc. Chương trình hứa hẹn mang đến những cung bậc cảm xúc khó quên thông qua những làn điệu mượt mà, sâu lắng.</p>
              </div>
            </div>

            <aside className="lg:w-1/3">
              <motion.div
                 initial={{ opacity: 0, x: 20 }}
                 animate={{ opacity: 1, x: 0 }}
                 className="sticky top-24 rounded-3xl border border-border bg-card p-8 shadow-card"
              >
                <div className="space-y-8">
                  <div className="flex gap-4">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                      <Calendar className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground uppercase tracking-tight">{t("common.date")}</p>
                      <p className="text-lg font-bold">
                        {startDate.toLocaleDateString(i18n.language === 'vi' ? 'vi-VN' : 'en-US', { day: 'numeric', month: 'long', year: 'numeric' })}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                      <Clock className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground uppercase tracking-tight">{t("common.time")}</p>
                      <p className="text-lg font-bold">20:00 - 22:30</p>
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                      <MapPin className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground uppercase tracking-tight">{t("common.location")}</p>
                      <p className="text-lg font-bold">{event.location?.name || "Bắc Ninh"}</p>
                      <p className="text-sm text-muted-foreground">{event.location?.address}</p>
                    </div>
                  </div>

                  <button className="flex w-full items-center justify-center gap-2 rounded-2xl bg-primary px-6 py-4 font-bold text-primary-foreground shadow-elevated transition-all hover:-translate-y-1 hover:shadow-lg active:scale-95">
                    <Ticket className="h-5 w-5" />
                    {t("news_page.register_event")}
                  </button>

                  <button className="flex w-full items-center justify-center gap-2 rounded-2xl bg-transparent border border-border px-6 py-4 font-medium transition-colors hover:bg-muted">
                    <Share2 className="h-4 w-4" />
                    {t("common.share")}
                  </button>
                </div>
              </motion.div>
            </aside>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
