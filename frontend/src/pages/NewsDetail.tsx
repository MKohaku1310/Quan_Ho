import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Calendar, User, ArrowLeft, Share2, MessageSquare } from "lucide-react";
import { useTranslation } from "react-i18next";

interface Article {
  id: number;
  title: string;
  content: string;
  excerpt: string;
  image_url: string;
  category: string;
  created_at: string;
  author?: { name: string };
}

export default function NewsDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();

  const { data: article, isLoading } = useQuery<Article>({
    queryKey: ["article", id],
    queryFn: async () => {
      const resp = await fetch(`/api/articles/${id}`);
      if (!resp.ok) throw new Error("Failed to fetch article");
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

  if (!article) {
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

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <main className="py-20">
        <div className="container mx-auto px-4 max-w-4xl">
          <motion.button
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={() => navigate("/tin-tuc")}
            className="mb-8 flex items-center gap-2 text-muted-foreground transition-colors hover:text-primary"
          >
            <ArrowLeft className="h-4 w-4" /> {t("common.back_to_list")}
          </motion.button>

          <article>
            <motion.header
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-10"
            >
              <div className="mb-4 inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary uppercase tracking-wider">
                {article.category}
              </div>
              <h1 className="font-display text-4xl font-bold text-foreground md:text-5xl lg:text-6xl leading-tight">
                {article.title}
              </h1>
              <div className="mt-6 flex flex-wrap items-center gap-6 text-muted-foreground border-b border-border pb-8">
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4" /> 
                  <span>{article.author?.name || "Bắc Ninh News"}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" /> 
                  <span>{new Date(article.created_at).toLocaleDateString(i18n.language === 'vi' ? 'vi-VN' : 'en-US', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
                </div>
                <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors">
                  <Share2 className="h-4 w-4" /> 
                  <span>{t("common.share")}</span>
                </div>
              </div>
            </motion.header>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="mb-12 overflow-hidden rounded-3xl shadow-elevated aspect-video relative"
            >
               <img 
                src={article.image_url} 
                alt={article.title} 
                className="h-full w-full object-cover" 
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="prose prose-lg dark:prose-invert max-w-none prose-custom text-muted-foreground leading-relaxed space-y-6"
              dangerouslySetInnerHTML={{ __html: article.content }}
            />
            
            <div className="mt-16 pt-10 border-t border-border flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center">
                        <MessageSquare className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                        <p className="font-medium text-foreground">{t("news_page.discussion")}</p>
                        <p className="text-sm text-muted-foreground">{t("news_page.discussion_sub")}</p>
                    </div>
                </div>
                <button className="px-6 py-2 bg-background border border-primary text-primary rounded-full hover:bg-primary hover:text-primary-foreground transition-all">
                    {t("news_page.join_comment")}
                </button>
            </div>
          </article>
        </div>
      </main>

      <Footer />
    </div>
  );
}
