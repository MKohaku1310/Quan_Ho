import { useState, useRef, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, X, Sun, Moon, Search, LogIn, UserPlus, User, Heart, LogOut } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/contexts/AuthContext";
import lotusOrnament from "@/assets/lotus-ornament.png";
import { useTranslation } from "react-i18next";

const navItems = [
  { path: "/", key: "home" },
  { path: "/gioi-thieu", key: "intro" },
  { path: "/bai-hat", key: "songs" },
  { path: "/nghe-nhan", key: "artists" },
  { path: "/lang-quan-ho", key: "villages" },
  { path: "/tin-tuc", key: "news" },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dark, setDark] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const { user, isAuthenticated, logout, setShowLoginModal } = useAuth();
  const { t, i18n } = useTranslation();

  const toggleLanguage = () => {
    i18n.changeLanguage(i18n.language === "vi" ? "en" : "vi");
  };

  const toggleDark = () => {
    setDark(!dark);
    document.documentElement.classList.toggle("dark");
  };

  // Đóng dropdown khi click ra ngoài
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  // Đóng menu mobile khi chuyển trang
  useEffect(() => {
    setMobileOpen(false);
    setDropdownOpen(false);
  }, [location.pathname]);

  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-background/90 backdrop-blur-md">
      <div className="container mx-auto flex items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2">
          <img src={lotusOrnament} alt="" className="h-8 w-8" />
          <span className="font-display text-xl font-bold text-primary">
            Quan Họ <span className="text-accent">Bắc Ninh</span>
          </span>
        </Link>

        {/* Điều hướng Desktop */}
        <div className="hidden items-center gap-1 lg:flex">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-muted hover:text-primary ${
                location.pathname === item.path
                  ? "bg-muted text-primary font-semibold"
                  : "text-muted-foreground"
              }`}
            >
              {t(`nav.${item.key}`)}
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/bai-hat"
            className="rounded-md p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-primary"
            aria-label="Tìm kiếm"
          >
            <Search className="h-5 w-5" />
          </Link>
          <button
            onClick={toggleDark}
            className="rounded-md p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-primary"
            aria-label="Chuyển giao diện"
          >
            {dark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>

          <button
            onClick={toggleLanguage}
            className="flex h-9 w-9 items-center justify-center rounded-md text-sm font-bold text-muted-foreground transition-colors hover:bg-muted hover:text-primary"
            title={i18n.language === "vi" ? "Switch to English" : "Chuyển sang Tiếng Việt"}
          >
            {i18n.language === "vi" ? "EN" : "VI"}
          </button>

          {/* Phần xác thực người dùng */}
          {isAuthenticated && user ? (
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                className="flex items-center gap-2 rounded-md p-1.5 transition-colors hover:bg-muted"
              >
                <img
                  src={user.avatar}
                  alt={user.username}
                  className="h-7 w-7 rounded-full object-cover"
                />
                <span className="hidden text-sm font-medium text-foreground lg:block">{user.username}</span>
              </button>

              <AnimatePresence>
                {dropdownOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -5 }}
                    className="absolute right-0 top-full mt-2 w-48 overflow-hidden rounded-lg border border-border bg-card shadow-elevated"
                  >
                    <div className="border-b border-border px-4 py-3">
                      <p className="text-sm font-medium text-foreground">{user.username}</p>
                      <p className="text-xs text-muted-foreground">{user.email}</p>
                    </div>
                    <div className="py-1">
                      <Link
                        to="/ho-so"
                        className="flex items-center gap-2 px-4 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
                      >
                        <User className="h-4 w-4" /> Hồ sơ
                      </Link>
                      <Link
                        to="/ho-so"
                        className="flex items-center gap-2 px-4 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
                      >
                        <Heart className="h-4 w-4" /> Yêu thích
                      </Link>
                      <button
                        onClick={logout}
                        className="flex w-full items-center gap-2 px-4 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-destructive"
                      >
                        <LogOut className="h-4 w-4" /> Đăng xuất
                      </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ) : (
            <div className="hidden items-center gap-1 sm:flex">
              <button
                onClick={() => setShowLoginModal(true)}
                className="flex items-center gap-1.5 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-primary"
              >
                <LogIn className="h-4 w-4" /> {t("nav.login")}
              </button>
              <Link
                to="/dang-ky"
                className="flex items-center gap-1.5 rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
              >
                <UserPlus className="h-4 w-4" /> {t("nav.register")}
              </Link>
            </div>
          )}

          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="rounded-md p-2 text-muted-foreground lg:hidden"
            aria-label="Menu"
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Menu Mobile */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden border-t border-border lg:hidden"
          >
            <div className="flex flex-col gap-1 px-4 py-3">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-muted ${
                    location.pathname === item.path
                      ? "bg-muted text-primary font-semibold"
                      : "text-muted-foreground"
                  }`}
                >
                  {t(`nav.${item.key}`)}
                </Link>
              ))}
              {/* Xác thực mobile */}
              <div className="mt-2 border-t border-border pt-2">
                {isAuthenticated && user ? (
                  <>
                    <Link to="/ho-so" className="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted">
                      <User className="h-4 w-4" /> Hồ sơ ({user.username})
                    </Link>
                    <button onClick={logout} className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-destructive">
                      <LogOut className="h-4 w-4" /> Đăng xuất
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      onClick={() => {
                        setMobileOpen(false);
                        setShowLoginModal(true);
                      }}
                      className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted"
                    >
                      <LogIn className="h-4 w-4" /> Đăng nhập
                    </button>
                    <Link to="/dang-ky" className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-primary hover:bg-muted">
                      <UserPlus className="h-4 w-4" /> Đăng ký
                    </Link>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
