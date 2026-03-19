import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { motion } from "framer-motion";
import heroBanner from "@/assets/hero-banner.jpg";
import { useTranslation } from "react-i18next";

export default function Introduction() {
  const { t } = useTranslation();

  // Dữ liệu dòng thời gian lịch sử
  const timeline = [
    { year: t("intro.timeline.t1_year"), text: t("intro.timeline.t1_text") },
    { year: t("intro.timeline.t2_year"), text: t("intro.timeline.t2_text") },
    { year: t("intro.timeline.t3_year"), text: t("intro.timeline.t3_text") },
    { year: t("intro.timeline.t4_year"), text: t("intro.timeline.t4_text") },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* Phần banner giới thiệu */}
      <section className="relative flex min-h-[40vh] items-center overflow-hidden">
        <img src={heroBanner} alt="" className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-hero-gradient opacity-80" />
        <div className="relative z-10 container mx-auto px-4 py-16 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="font-display text-4xl font-bold text-primary-foreground md:text-5xl"
          >
            {t("intro.hero_title")}
          </motion.h1>
          <p className="mt-3 text-primary-foreground/80">{t("intro.hero_subtitle")}</p>
        </div>
      </section>

      {/* Nội dung giới thiệu chi tiết */}
      <section className="py-16">
        <div className="container mx-auto max-w-3xl px-4">
          <SectionTitle title={t("intro.what_is_title")} translate={false} />
          <div className="prose-custom space-y-4 text-muted-foreground leading-relaxed">
            <p>{t("intro.desc_p1")}</p>
            <p>{t("intro.desc_p2")}</p>
          </div>
        </div>
      </section>

      {/* Dòng thời gian lịch sử */}
      <section className="bg-card py-16">
        <div className="container mx-auto max-w-3xl px-4">
          <SectionTitle title={t("intro.history_title")} translate={false} />
          <div className="space-y-8">
            {timeline.map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="flex gap-6"
              >
                <div className="flex flex-col items-center">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
                    ❀
                  </div>
                  {i < timeline.length - 1 && <div className="w-px flex-1 bg-border" />}
                </div>
                <div className="pb-8">
                  <h3 className="font-display text-lg font-bold text-foreground">{item.year}</h3>
                  <p className="mt-1 text-muted-foreground">{item.text}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Phần UNESCO công nhận */}
      <section className="py-16">
        <div className="container mx-auto max-w-3xl px-4 text-center">
          <SectionTitle
            title={t("intro.unesco_title")}
            subtitle={t("hero.subtitle")}
            translate={false}
          />
          <p className="text-muted-foreground leading-relaxed">
            {t("intro.unesco_desc")}
          </p>
        </div>
      </section>

      <Footer />
    </div>
  );
}
