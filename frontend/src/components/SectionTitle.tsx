import { motion } from "framer-motion";
import lotusOrnament from "@/assets/lotus-ornament.png";

interface SectionTitleProps {
  title: string;
  subtitle?: string;
}

export default function SectionTitle({ title, subtitle }: SectionTitleProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="mb-8 text-center"
    >
      <img src={lotusOrnament} alt="" className="mx-auto mb-3 h-10 w-10 opacity-70" />
      <h2 className="font-display text-3xl font-bold text-foreground md:text-4xl">{title}</h2>
      {subtitle && (
        <p className="mx-auto mt-2 max-w-2xl text-muted-foreground">{subtitle}</p>
      )}
    </motion.div>
  );
}
