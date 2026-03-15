import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import heroBanner from "@/assets/hero-banner.jpg";

export default function HeroBanner() {
  return (
    <section className="relative flex min-h-[70vh] items-center overflow-hidden">
      <img
        src={heroBanner}
        alt="Quan họ Bắc Ninh"
        className="absolute inset-0 h-full w-full object-cover"
      />
      <div className="absolute inset-0 bg-hero-gradient opacity-70" />
      <div className="relative z-10 container mx-auto px-4 py-20 text-center">
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-4 text-sm font-medium uppercase tracking-widest text-gold-light"
        >
          Di sản Văn hóa Phi vật thể UNESCO 2009
        </motion.p>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="font-display text-4xl font-bold leading-tight text-primary-foreground md:text-6xl lg:text-7xl"
        >
          Quan Họ <br />
          <span className="text-gradient-gold">Bắc Ninh</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mx-auto mt-6 max-w-xl text-lg text-primary-foreground/80"
        >
          Khám phá vẻ đẹp tinh tế của dân ca Quan họ — tiếng hát giao duyên ngọt ngào bên dòng sông Cầu xứ Kinh Bắc.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mt-8 flex flex-wrap justify-center gap-4"
        >
          <Link
            to="/bai-hat"
            className="rounded-lg bg-accent px-6 py-3 font-semibold text-accent-foreground shadow-elevated transition-transform hover:scale-105"
          >
            Nghe Quan Họ
          </Link>
          <Link
            to="/gioi-thieu"
            className="rounded-lg border border-primary-foreground/30 px-6 py-3 font-semibold text-primary-foreground transition-colors hover:bg-primary-foreground/10"
          >
            Tìm hiểu thêm
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
