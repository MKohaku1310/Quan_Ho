import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { motion } from "framer-motion";
import { Calendar } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

interface NewsItem {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  category: string;
  created_at: string;
  image_url: string;
  type: 'article' | 'event';
}

export default function News() {
  const { t, i18n } = useTranslation();
  const [activeTab, setActiveTab] = useState(t("common.all"));

  // Lấy dữ liệu bài báo từ API
  const { data: articles = [] } = useQuery<any[]>({
    queryKey: ["articles-list"],
    queryFn: async () => {
      const resp = await fetch("/api/articles/");
      return resp.ok ? await resp.json() : [];
    }
  });

  // Lấy dữ liệu sự kiện từ API
  const { data: events = [] } = useQuery<any[]>({
    queryKey: ["events-list"],
    queryFn: async () => {
      const resp = await fetch("/api/events/");
      return resp.ok ? await resp.json() : [];
    }
  });

  // Kết hợp và sắp xếp dữ liệu
  const allItems = useMemo(() => {
    const combined = [
      ...articles.map(a => ({ ...a, type: 'article' })),
      ...events.map(e => ({ ...e, type: 'event', category: 'event' }))
    ];
    return combined.sort((a, b) => new Date(b.created_at || b.start_date).getTime() - new Date(a.created_at || a.start_date).getTime());
  }, [articles, events]);

  // Bộ lọc dữ liệu theo tab
  const filteredItems = useMemo(() => {
    if (activeTab === t("common.all")) return allItems;
    if (activeTab === t("news_page.news")) return allItems.filter(i => i.type === 'article' && (i.category === 'tin-tuc' || i.category === 'nghe-thuat' || i.category === 'lich-su'));
    if (activeTab === t("news_page.event")) return allItems.filter(i => i.type === 'event');
    if (activeTab === t("news_page.festival")) return allItems.filter(i => i.category === 'le-hoi');
    return allItems;
  }, [allItems, activeTab, t]);

  const tabs = [t("common.all"), t("news_page.news"), t("news_page.event"), t("news_page.festival")];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title={t("sections.news_events")}
            subtitle={t("sections.news_events_sub")}
            translate={false}
          />

          {/* Danh mục tab */}
          <div className="mb-8 flex gap-2">
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`rounded-full border border-border px-4 py-1.5 text-sm transition-colors hover:bg-primary hover:text-primary-foreground ${
                  activeTab === tab ? "bg-primary text-primary-foreground" : "bg-card text-muted-foreground"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Danh sách tin tức và sự kiện */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredItems.map((item, i) => (
              <motion.article
                key={`${item.type}-${item.id}`}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="group overflow-hidden rounded-lg border border-border bg-card shadow-card transition-all hover:shadow-elevated"
              >
                <Link to={`/tin-tuc/${item.id}`} className="block">
                  <div className="relative aspect-[16/9] overflow-hidden">
                    <img
                      src={item.image_url}
                      alt={item.title}
                      className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                      loading="lazy"
                    />
                    <span className="absolute left-3 top-3 rounded bg-primary px-2 py-0.5 text-xs font-medium text-primary-foreground">
                      {item.type === 'event' ? t("news_page.event") : t("news_page.news")}
                    </span>
                  </div>
                  <div className="p-5">
                    <h3 className="font-display text-lg font-semibold text-card-foreground line-clamp-2 group-hover:text-primary transition-colors">
                      {item.title}
                    </h3>
                    <p className="mt-2 text-sm text-muted-foreground line-clamp-2">{item.excerpt || item.description}</p>
                    <p className="mt-3 flex items-center gap-1 text-xs text-muted-foreground">
                      <Calendar className="h-3 w-3" /> {new Date(item.created_at || item.start_date).toLocaleDateString(i18n.language === 'vi' ? 'vi-VN' : 'en-US')}
                    </p>
                  </div>
                </Link>
              </motion.article>
            ))}
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
