import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Loader2, Eye, EyeOff } from "lucide-react";
import { motion } from "framer-motion";
import { z } from "zod";
import { useAuth } from "@/contexts/AuthContext";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useTranslation } from "react-i18next";

export default function Register() {
  const { t } = useTranslation();
  
  const registerSchema = z
    .object({
      username: z
        .string()
        .trim()
        .min(3, t("auth.errors.username_min"))
        .max(30, t("auth.errors.username_max"))
        .regex(/^[a-zA-Z0-9_]+$/, t("auth.errors.username_regex")),
      email: z.string().trim().email(t("auth.errors.invalid_email")).max(255),
      password: z.string().min(6, t("auth.errors.password_min")).max(100),
      confirmPassword: z.string(),
    })
    .refine((data) => data.password === data.confirmPassword, {
      message: t("auth.errors.password_mismatch"),
      path: ["confirmPassword"],
    });

  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Cập nhật giá trị form
  const handleChange = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: "" }));
  };

  // Xử lý đăng ký
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    const result = registerSchema.safeParse(form);
    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.errors.forEach((err) => {
        if (err.path[0]) fieldErrors[err.path[0] as string] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    setLoading(true);
    const success = await register(result.data.username, result.data.email, result.data.password);
    setLoading(false);
    if (success) {
      navigate("/ho-so");
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <section className="py-16">
        <div className="container mx-auto max-w-md px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="overflow-hidden rounded-xl border border-border bg-card shadow-elevated"
          >
            <div className="border-b border-border bg-muted px-6 py-4">
              <h1 className="font-display text-2xl font-bold text-card-foreground">{t("auth.register_title")}</h1>
              <p className="mt-1 text-sm text-muted-foreground">{t("auth.register_subtitle")}</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 p-6">
              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">{t("auth.username")}</label>
                <input
                  type="text"
                  value={form.username}
                  onChange={(e) => handleChange("username", e.target.value)}
                  placeholder="vd: quanho_fan"
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
                {errors.username && <p className="mt-1 text-xs text-destructive">{errors.username}</p>}
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">{t("auth.email")}</label>
                <input
                  type="email"
                  value={form.email}
                  onChange={(e) => handleChange("email", e.target.value)}
                  placeholder="email@example.com"
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
                {errors.email && <p className="mt-1 text-xs text-destructive">{errors.email}</p>}
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">{t("auth.password")}</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={form.password}
                    onChange={(e) => handleChange("password", e.target.value)}
                    placeholder={t("auth.errors.password_min")}
                    className="w-full rounded-md border border-input bg-background px-3 py-2 pr-10 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.password && <p className="mt-1 text-xs text-destructive">{errors.password}</p>}
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-foreground">{t("auth.confirm_password")}</label>
                <input
                  type={showPassword ? "text" : "password"}
                  value={form.confirmPassword}
                  onChange={(e) => handleChange("confirmPassword", e.target.value)}
                  placeholder={t("auth.confirm_password")}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
                {errors.confirmPassword && <p className="mt-1 text-xs text-destructive">{errors.confirmPassword}</p>}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="flex w-full items-center justify-center gap-2 rounded-md bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-50"
              >
                {loading && <Loader2 className="h-4 w-4 animate-spin" />}
                {t("auth.register_btn")}
              </button>

              <div className="text-center text-sm text-muted-foreground">
                {t("auth.have_account")}{" "}
                <button
                  type="button"
                  onClick={() => {
                    navigate("/");
                  }}
                  className="font-medium text-primary hover:underline"
                >
                  {t("auth.login_btn")}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
