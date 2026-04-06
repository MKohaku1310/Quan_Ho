import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

export default function AddSong() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { data: artists = [] } = useQuery({
    queryKey: ["artists-select"],
    queryFn: async () => {
      const resp = await fetch("/api/artists/");
      if (!resp.ok) return [];
      return await resp.json();
    }
  });

  const [formData, setFormData] = useState({
    name: "",
    category: "co",
    village: "",
    artist_id: "",
    video_url: "",
    image_url: "",
    lyrics: "",
    duration: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const submitData = {
        ...formData,
        artist_id: formData.artist_id ? Number(formData.artist_id) : null,
      };

      const response = await fetch("/api/melodies/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(submitData),
      });

      if (!response.ok) {
        throw new Error(t("add_song.error"));
      }

      navigate("/bai-hat");
    } catch (err: any) {
      setError(err.message || t("add_song.error"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <section className="py-16 flex-1">
        <div className="container mx-auto px-4 max-w-2xl">
          <SectionTitle title={t("add_song.title")} subtitle={t("add_song.subtitle")} translate={false} />

          {error && (
            <div className="mb-4 p-4 text-sm text-destructive-foreground bg-destructive rounded-md">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="bg-card p-6 rounded-lg border border-border shadow-card space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">{t("add_song.name")} <span className="text-destructive">*</span></label>
              <input
                required
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder={t("add_song.name_placeholder")}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">{t("add_song.category")}</label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="co">Cổ</option>
                  <option value="moi">Mới</option>
                  <option value="cai-bien">Cải biên</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("add_song.artist")}</label>
                <select
                  name="artist_id"
                  value={formData.artist_id}
                  onChange={handleChange}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">{t("add_song.artist_placeholder")}</option>
                  {artists.map((artist: any) => (
                    <option key={artist.id} value={artist.id}>
                      {artist.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">{t("add_song.village")}</label>
                <input
                  type="text"
                  name="village"
                  value={formData.village}
                  onChange={handleChange}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder={t("add_song.village_placeholder")}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">{t("add_song.duration")}</label>
                <input
                  type="text"
                  name="duration"
                  value={formData.duration}
                  onChange={handleChange}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder={t("add_song.duration_placeholder")}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">{t("add_song.image_url")}</label>
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
              <label className="block text-sm font-medium mb-1">{t("add_song.video_url")} <span className="text-destructive">*</span></label>
              <input
                required
                type="url"
                name="video_url"
                value={formData.video_url}
                onChange={handleChange}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://www.youtube.com/embed/XXXXX"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">{t("add_song.lyrics")}</label>
              <textarea
                name="lyrics"
                value={formData.lyrics}
                onChange={handleChange}
                rows={6}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder={t("add_song.lyrics_placeholder")}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-md bg-primary py-2 px-4 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-50"
            >
              {loading ? t("add_song.submitting") : t("add_song.submit")}
            </button>
          </form>
        </div>
      </section>
      <Footer />
    </div>
  );
}
