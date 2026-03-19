import { useState } from "react";
import { motion } from "framer-motion";
import { useAuth } from "@/contexts/AuthContext";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SongCard from "@/components/SongCard";
import SectionTitle from "@/components/SectionTitle";
import { songs } from "@/data/mockData";
import { Navigate } from "react-router-dom";
import { User, Mail, Calendar, Heart, MessageSquare, Edit2, Check, X } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function Profile() {
  const { t, i18n } = useTranslation();
  const { user, isAuthenticated, updateProfile, favorites, comments } = useAuth();
  const [editingUsername, setEditingUsername] = useState(false);
  const [newUsername, setNewUsername] = useState("");
  const [activeTab, setActiveTab] = useState<"favorites" | "comments" | "activity">("favorites");

  // Chuyển hướng nếu chưa đăng nhập
  if (!isAuthenticated || !user) {
    return <Navigate to="/" replace />;
  }

  // Lọc bài hát yêu thích và bình luận của người dùng
  const favoriteSongs = songs.filter((s) => favorites.includes(s.id));
  const userComments = comments.filter((c) => c.userId === user.id);

  // Lưu tên người dùng mới
  const handleSaveUsername = () => {
    const trimmed = newUsername.trim();
    if (trimmed.length >= 3 && trimmed.length <= 30) {
      updateProfile({ username: trimmed });
      setEditingUsername(false);
    }
  };

  const tabs = [
    { key: "favorites" as const, label: t("nav.favorites"), icon: Heart, count: favoriteSongs.length },
    { key: "comments" as const, label: t("comments.title"), icon: MessageSquare, count: userComments.length },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto max-w-4xl px-4">
          {/* Header hồ sơ người dùng */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="overflow-hidden rounded-xl border border-border bg-card shadow-elevated"
          >
            <div className="bg-hero-gradient px-6 py-10">
              <div className="flex flex-col items-center gap-4 sm:flex-row">
                <img
                  src={user.avatar}
                  alt={user.username}
                  className="h-20 w-20 rounded-full border-4 border-primary-foreground/30 object-cover shadow-elevated"
                />
                <div className="text-center sm:text-left">
                  <div className="flex items-center gap-2">
                    {editingUsername ? (
                      <div className="flex items-center gap-2">
                        <input
                          type="text"
                          value={newUsername}
                          onChange={(e) => setNewUsername(e.target.value)}
                          className="rounded-md border border-primary-foreground/30 bg-primary-foreground/10 px-2 py-1 text-lg font-bold text-primary-foreground placeholder:text-primary-foreground/50"
                          autoFocus
                        />
                        <button onClick={handleSaveUsername} className="text-primary-foreground/80 hover:text-primary-foreground">
                          <Check className="h-5 w-5" />
                        </button>
                        <button onClick={() => setEditingUsername(false)} className="text-primary-foreground/80 hover:text-primary-foreground">
                          <X className="h-5 w-5" />
                        </button>
                      </div>
                    ) : (
                      <>
                        <h1 className="font-display text-2xl font-bold text-primary-foreground">{user.username}</h1>
                        <button
                          onClick={() => {
                            setNewUsername(user.username);
                            setEditingUsername(true);
                          }}
                          className="text-primary-foreground/60 hover:text-primary-foreground"
                          title={t("profile_page.edit_username")}
                        >
                          <Edit2 className="h-4 w-4" />
                        </button>
                      </>
                    )}
                  </div>
                  <div className="mt-2 flex flex-wrap justify-center gap-4 text-sm text-primary-foreground/70 sm:justify-start">
                    <span className="flex items-center gap-1"><Mail className="h-3.5 w-3.5" /> {user.email}</span>
                    <span className="flex items-center gap-1"><Calendar className="h-3.5 w-3.5" /> {t("profile_page.joined")} {user.joinedDate}</span>
                  </div>
                  {user.role === "admin" && (
                    <span className="mt-2 inline-block rounded-full bg-accent px-3 py-0.5 text-xs font-medium text-accent-foreground">
                      {t("profile_page.admin_role")}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Thống kê nhanh */}
            <div className="grid grid-cols-2 border-b border-border">
              <div className="border-r border-border p-4 text-center">
                <p className="font-display text-2xl font-bold text-primary">{favoriteSongs.length}</p>
                <p className="text-xs text-muted-foreground">{t("profile_page.fav_songs_stat")}</p>
              </div>
              <div className="p-4 text-center">
                <p className="font-display text-2xl font-bold text-accent">{userComments.length}</p>
                <p className="text-xs text-muted-foreground">{t("comments.title")}</p>
              </div>
            </div>
          </motion.div>

          {/* Các tab nội dung */}
          <div className="mt-8 flex gap-2 border-b border-border">
            {tabs.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`flex items-center gap-2 border-b-2 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === tab.key
                    ? "border-primary text-primary"
                    : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                <tab.icon className="h-4 w-4" />
                {tab.label}
                <span className="rounded-full bg-muted px-2 py-0.5 text-xs">{tab.count}</span>
              </button>
            ))}
          </div>

          {/* Nội dung chi tiết của tab */}
          <div className="mt-6">
            {activeTab === "favorites" && (
              favoriteSongs.length > 0 ? (
                <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                  {favoriteSongs.map((song, i) => (
                    <SongCard key={song.id} song={song} index={i} />
                  ))}
                </div>
              ) : (
                <div className="py-16 text-center text-muted-foreground">
                  <Heart className="mx-auto mb-3 h-10 w-10 opacity-30" />
                  <p>{t("profile_page.no_favs")}</p>
                  <p className="text-sm">{t("profile_page.fav_hint")}</p>
                </div>
              )
            )}

            {activeTab === "comments" && (
              userComments.length > 0 ? (
                <div className="space-y-4">
                  {userComments.map((comment) => (
                    <div key={comment.id} className="rounded-lg border border-border bg-card p-4 shadow-card">
                      <p className="text-sm text-foreground">{comment.content}</p>
                      <div className="mt-2 flex items-center gap-3 text-xs text-muted-foreground">
                        <span>
                          {comment.targetType === "song" 
                            ? t("nav.songs") 
                            : comment.targetType === "article" 
                              ? t("news_page.news") 
                              : t("news_page.event")} #{comment.targetId}
                        </span>
                        <span>{new Date(comment.createdAt).toLocaleDateString(i18n.language === 'vi' ? 'vi-VN' : 'en-US')}</span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-16 text-center text-muted-foreground">
                  <MessageSquare className="mx-auto mb-3 h-10 w-10 opacity-30" />
                  <p>{t("comments.no_comments")}</p>
                </div>
              )
            )}
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
