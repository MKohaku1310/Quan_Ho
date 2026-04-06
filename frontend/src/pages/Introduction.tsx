import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { motion } from "framer-motion";
import heroBanner from "@/assets/hero-banner.jpg";
import { useTranslation } from "react-i18next";
import { ChevronDown, Music, Heart, Users, CheckCircle2, Leaf } from "lucide-react";

export default function Introduction() {
  const { t } = useTranslation();

  const timeline = [
    { year: t("intro.timeline.t1_year"), text: t("intro.timeline.t1_text") },
    { year: t("intro.timeline.t2_year"), text: t("intro.timeline.t2_text") },
    { year: t("intro.timeline.t3_year"), text: t("intro.timeline.t3_text") },
    { year: t("intro.timeline.t4_year"), text: t("intro.timeline.t4_text") },
  ];

  const features = [
    {
      icon: <Music className="h-6 w-6 text-primary" />,
      title: t("intro.id_singing_title"),
      desc: t("intro.id_singing_desc"),
    },
    {
      icon: <Users className="h-6 w-6 text-primary" />,
      title: t("intro.id_custom_title"),
      desc: t("intro.id_custom_desc"),
    },
    {
      icon: <Heart className="h-6 w-6 text-primary" />,
      title: t("intro.id_manner_title"),
      desc: t("intro.id_manner_desc"),
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <section className="relative flex min-h-[70vh] items-center justify-center overflow-hidden">
        <img src={heroBanner} alt="Hero" className="absolute inset-0 h-full w-full object-cover scale-105 animate-slow-pan" />
        <div className="absolute inset-0 bg-hero-gradient opacity-90" />
        <div className="relative z-10 container mx-auto px-4 text-center mt-12">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="font-display text-5xl font-bold text-primary-foreground md:text-7xl tracking-wide drop-shadow-lg"
          >
            {t("intro.hero_title")}
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="mt-6 text-lg md:text-xl text-primary-foreground/90 max-w-2xl mx-auto font-light"
          >
            {t("intro.hero_subtitle")}
          </motion.p>
        </div>
        
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 1 }}
          className="absolute inset-x-0 bottom-10 flex flex-col items-center justify-center animate-bounce text-primary-foreground/70"
        >
          <span className="text-xs uppercase tracking-widest mb-2">{t("intro.scroll_down")}</span>
          <ChevronDown className="h-5 w-5" />
        </motion.div>
      </section>

      <section className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <SectionTitle title={t("intro.what_is_title")} translate={false} />
          <div className="mx-auto max-w-4xl text-center prose-custom space-y-6 text-muted-foreground leading-relaxed text-lg">
            <p>{t("intro.desc_p1")}</p>
            <p>{t("intro.desc_p2")}</p>
          </div>
        </div>
      </section>

      <section className="py-20 bg-card">
        <div className="container mx-auto px-4">
          <SectionTitle title={t("intro.identity_title")} subtitle={t("intro.identity_desc")} translate={false} />
          
          <div className="grid gap-8 md:grid-cols-3 mt-12">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2 }}
                className="group relative overflow-hidden rounded-2xl border border-border bg-background p-8 shadow-card transition-all hover:-translate-y-1 hover:shadow-elevated hover:border-primary/50"
              >
                <div className="mb-6 inline-flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10 transition-colors group-hover:bg-primary/20">
                  {feature.icon}
                </div>
                <h3 className="mb-4 font-display text-2xl font-bold text-foreground">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="overflow-hidden py-24 bg-background">
        <div className="container mx-auto px-4">
          <SectionTitle title={t("intro.costume_title")} subtitle={t("intro.costume_desc")} translate={false} />

          <div className="mt-16 flex flex-col gap-20">
            <motion.div 
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="flex flex-col items-center gap-10 md:flex-row"
            >
              <div className="md:w-1/2 relative">
                <div className="absolute -inset-4 rounded-2xl bg-gradient-to-r from-primary/20 to-transparent blur-xl"></div>
                <img src="https://vanchuongphuongnam.vn/wp-content/uploads/2019/04/l-3.jpg" alt="Female Costume" className="relative rounded-2xl shadow-elevated object-cover aspect-video" />
              </div>
              <div className="md:w-1/2 space-y-4 px-4">
                <h3 className="font-display text-4xl font-bold text-primary">{t("intro.female_costume_title")}</h3>
                <p className="text-lg text-muted-foreground leading-relaxed">{t("intro.female_costume_desc")}</p>
                <ul className="space-y-2 mt-4 text-muted-foreground">
                  <li className="flex items-center gap-2"><CheckCircle2 className="h-5 w-5 text-accent" /> Áo mớ ba mớ bảy</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="h-5 w-5 text-accent" /> Nón quai thao</li>
                  <li className="flex items-center gap-2"><CheckCircle2 className="h-5 w-5 text-accent" /> Khăn mỏ quạ</li>
                </ul>
              </div>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="flex flex-col items-center gap-10 md:flex-row-reverse"
            >
              <div className="md:w-1/2 relative">
                <div className="absolute -inset-4 rounded-2xl bg-gradient-to-l from-primary/20 to-transparent blur-xl"></div>
                <img src="https://media.baodantoc.vn/baodantoc/image/files/hoangmai/2022/07/21/ao-dai-2009.jpg" alt="Male Costume" className="relative rounded-2xl shadow-elevated object-cover aspect-video" />
              </div>
              <div className="md:w-1/2 space-y-4 px-4">
                <h3 className="font-display text-4xl font-bold text-foreground">{t("intro.male_costume_title")}</h3>
                <p className="text-lg text-muted-foreground leading-relaxed">{t("intro.male_costume_desc")}</p>
              </div>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="mx-auto max-w-4xl overflow-hidden rounded-3xl bg-card border border-border shadow-card flex flex-col md:flex-row mt-10"
            >
              <div className="md:w-2/5 shrink-0">
                <img src="https://vov-media.vov.vn/sites/default/files/styles/large/public/2021-02/trau_tem_canh_phuong_9.jpg" alt="Betel" className="h-full w-full object-cover min-h-[250px]" />
              </div>
              <div className="p-8 md:p-12 self-center flex-1">
                <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-accent/10 px-3 py-1 text-sm font-medium text-accent">
                  <Leaf className="h-4 w-4" /> Truyền thống
                </div>
                <h3 className="font-display text-3xl font-bold mb-4 text-foreground">{t("intro.betel_title")}</h3>
                <p className="text-muted-foreground leading-relaxed">{t("intro.betel_desc")}</p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="bg-card py-24">
        <div className="container mx-auto px-4 max-w-5xl">
          <SectionTitle title={t("intro.history_title")} translate={false} />
          <div className="mt-16 space-y-12">
            {timeline.map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="group relative flex flex-col md:flex-row gap-8"
              >
                <div className="md:w-1/3 text-left md:text-right shrink-0 pt-1">
                  <h3 className="font-display text-3xl font-bold text-primary group-hover:text-accent transition-colors">{item.year}</h3>
                </div>
                
                <div className="hidden md:flex flex-col items-center">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full border-4 border-background bg-primary text-primary-foreground shadow-sm group-hover:scale-110 transition-transform">
                    <span className="h-2 w-2 rounded-full bg-white"></span>
                  </div>
                  {i < timeline.length - 1 && <div className="w-0.5 flex-1 bg-gradient-to-b from-primary/50 to-transparent mt-2 opacity-50" />}
                </div>

                <div className="md:w-2/3 pb-8 md:pb-0">
                  <div className="rounded-xl bg-background p-6 border border-border shadow-sm group-hover:shadow-md transition-shadow">
                    <p className="text-muted-foreground leading-relaxed text-lg">{item.text}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-primary/5 pointer-events-none"></div>
        <div className="container mx-auto max-w-4xl px-4 text-center relative z-10">
          <div className="mx-auto w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mb-8">
             <img src="/img/unesco.svg" alt="UNESCO" className="w-16 opacity-80" />
          </div>
          <SectionTitle
            title={t("intro.unesco_title")}
            subtitle={t("hero.subtitle")}
            translate={false}
          />
          <blockquote className="mt-10 text-xl font-light italic leading-loose text-muted-foreground px-8 border-l-4 border-primary bg-background/50 py-6 rounded-r-xl shadow-sm">
            "{t("intro.unesco_desc")}"
          </blockquote>
        </div>
      </section>

      <Footer />
    </div>
  );
}

