import HeroBanner from "@/components/HeroBanner";
import SectionTitle from "@/components/SectionTitle";
import SongCard from "@/components/SongCard";
import ArtistCard from "@/components/ArtistCard";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { songs, artists } from "@/data/mockData";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Calendar, ArrowRight } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useMemo } from "react";

const Index = () => {
  const { data: articles = [] } = useQuery<any[]>({
    queryKey: ["articles-list-home"],
    queryFn: async () => {
      const resp = await fetch("/api/articles/");
      return resp.ok ? await resp.json() : [];
    }
  });

  const { data: events = [] } = useQuery<any[]>({
    queryKey: ["events-list-home"],
    queryFn: async () => {
      const resp = await fetch("/api/events/");
      return resp.ok ? await resp.json() : [];
    }
  });

  const allItems = useMemo(() => {
    const combined = [
      ...articles.map(a => ({ ...a, type: 'article' })),
      ...events.map(e => ({ ...e, type: 'event' }))
    ];
    return combined.sort((a, b) => new Date(b.created_at || b.start_date).getTime() - new Date(a.created_at || a.start_date).getTime());
  }, [articles, events]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <HeroBanner />

      {/* Featured Songs */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title="Bài hát nổi bật"
            subtitle="Những làn điệu Quan họ kinh điển được yêu thích nhất"
          />
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {songs.slice(0, 3).map((song, i) => (
              <SongCard key={song.id} song={song} index={i} />
            ))}
          </div>
          <div className="mt-8 text-center">
            <Link
              to="/bai-hat"
              className="inline-flex items-center gap-2 text-sm font-medium text-primary hover:underline"
            >
              Xem tất cả bài hát <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Introduction strip */}
      <section className="bg-card py-16">
        <div className="container mx-auto px-4">
          <div className="grid items-center gap-10 md:grid-cols-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="font-display text-3xl font-bold text-foreground">
                Dân ca Quan họ — <span className="text-primary">Tinh hoa Kinh Bắc</span>
              </h2>
              <p className="mt-4 leading-relaxed text-muted-foreground">
                Quan họ Bắc Ninh là thể loại dân ca đối đáp giữa nam và nữ, phổ biến ở vùng
                Kinh Bắc xưa. Năm 2009, UNESCO công nhận Quan họ là Di sản Văn hóa Phi vật thể
                của Nhân loại, khẳng định giá trị văn hóa đặc sắc của dân tộc Việt Nam.
              </p>
              <Link
                to="/gioi-thieu"
                className="mt-6 inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground transition-transform hover:scale-105"
              >
                Tìm hiểu lịch sử <ArrowRight className="h-4 w-4" />
              </Link>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="grid grid-cols-2 gap-3"
            >
              <div className="rounded-lg bg-muted p-6 text-center">
                <p className="font-display text-3xl font-bold text-primary">49</p>
                <p className="mt-1 text-sm text-muted-foreground">Làng Quan họ gốc</p>
              </div>
              <div className="rounded-lg bg-muted p-6 text-center">
                <p className="font-display text-3xl font-bold text-accent">300+</p>
                <p className="mt-1 text-sm text-muted-foreground">Làn điệu cổ</p>
              </div>
              <div className="rounded-lg bg-muted p-6 text-center">
                <p className="font-display text-3xl font-bold text-terracotta">2009</p>
                <p className="mt-1 text-sm text-muted-foreground">UNESCO công nhận</p>
              </div>
              <div className="rounded-lg bg-muted p-6 text-center">
                <p className="font-display text-3xl font-bold text-jade">600+</p>
                <p className="mt-1 text-sm text-muted-foreground">Năm lịch sử</p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Featured Artists */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <SectionTitle
            title="Nghệ nhân tiêu biểu"
            subtitle="Những người giữ lửa cho di sản Quan họ"
          />
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {artists.map((artist, i) => (
              <ArtistCard key={artist.id} artist={artist} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* News */}
      <section className="bg-card py-16">
        <div className="container mx-auto px-4">
          <SectionTitle title="Tin tức & Sự kiện" subtitle="Cập nhật mới nhất về Quan họ Bắc Ninh" />
          <div className="grid gap-6 md:grid-cols-2">
            {allItems.slice(0, 4).map((item, i) => (
              <motion.div
                key={`${item.type}-${item.id}`}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="relative overflow-hidden group"
              >
                <Link to={`/tin-tuc/${item.id}`} className="flex gap-4 rounded-lg border border-border bg-background p-4 shadow-card transition-all hover:shadow-elevated hover:border-primary/50">
                  <img
                    src={item.image_url}
                    alt={item.title}
                    className="h-24 w-24 flex-shrink-0 rounded-md object-cover transition-transform duration-500 group-hover:scale-105"
                    loading="lazy"
                  />
                  <div className="min-w-0">
                    <span className="inline-block rounded bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
                      {item.type === 'event' ? 'Sự kiện' : 'Tin tức'}
                    </span>
                    <h3 className="mt-1 line-clamp-2 font-display text-sm font-semibold text-foreground group-hover:text-primary transition-colors">
                      {item.title}
                    </h3>
                    <p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
                      <Calendar className="h-3 w-3" /> {new Date(item.created_at || item.start_date).toLocaleDateString('vi-VN')}
                    </p>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
          <div className="mt-8 text-center">
            <Link to="/tin-tuc" className="inline-flex items-center gap-2 text-sm font-medium text-primary hover:underline">
               Xem tất cả tin tức <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Index;
