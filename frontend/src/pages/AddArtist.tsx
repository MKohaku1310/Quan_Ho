import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { useTranslation } from "react-i18next";

export default function AddArtist() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    name: "",
    biography: "",
    village: "",
    performances: 0,
    contributions: "",
    image_url: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "performances" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/artists/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(t("add_artist.error"));
      }

      navigate("/nghe-nhan");
    } catch (err: any) {
      setError(err.message || t("add_artist.error"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <section className="py-16 flex-1">
        <div className="container mx-auto px-4 max-w-2xl">
          <SectionTitle title={t("add_artist.title")} subtitle={t("add_artist.subtitle")} translate={false} />

          {error && (
            <div className="mb-4 p-4 text-sm text-destructive-foreground bg-destructive rounded-md">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="bg-card p-6 rounded-lg border border-border shadow-card space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">{t("add_artist.name")} <span className="text-destructive">*</span></label>
              <input
                required
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder={t("add_artist.name_placeholder")}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">{t("add_artist.village")}</label>
              <input
                type="text"
                name="village"
                value={formData.village}
                onChange={handleChange}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder={t("add_artist.village_placeholder")}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">{t("add_artist.performances")}</label>
              <input
                type="number"
                name="performances"
                value={formData.performances}
                onChange={handleChange}
                min="0"
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">{t("add_artist.image_url")}</label>
              <input
                type="url"
                name="image_url"
                value={formData.image_url}
                onChange={handleChange}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">{t("add_artist.biography")}</label>
              <textarea
                name="biography"
                value={formData.biography}
                onChange={handleChange}
                rows={4}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder={t("add_artist.biography_placeholder")}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">{t("add_artist.contributions")}</label>
              <textarea
                name="contributions"
                value={formData.contributions}
                onChange={handleChange}
                rows={3}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder={t("add_artist.contributions_placeholder")}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-md bg-primary py-2 px-4 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-50"
            >
              {loading ? t("add_artist.submitting") : t("add_artist.submit")}
            </button>
          </form>
        </div>
      </section>
      <Footer />
    </div>
  );
}
