import { Link } from "react-router-dom";
import lotusOrnament from "@/assets/lotus-ornament.png";
import { useTranslation } from "react-i18next";

export default function Footer() {
  const { t } = useTranslation();
  return (
    <footer className="border-t border-border bg-card">
      <div className="container mx-auto px-4 py-12">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <div className="mb-3 flex items-center gap-2">
              <img src={lotusOrnament} alt="" className="h-8 w-8" />
              <span className="font-display text-lg font-bold text-primary">{t("footer.siteName")}</span>
            </div>
            <p className="text-sm text-muted-foreground">
              {t("footer.description")}
            </p>
          </div>
          <div>
            <h4 className="mb-3 font-display text-sm font-semibold text-foreground">{t("footer.explore")}</h4>
            <div className="flex flex-col gap-2">
              <Link to="/gioi-thieu" className="text-sm text-muted-foreground hover:text-primary">{t("footer.about")}</Link>
              <Link to="/bai-hat" className="text-sm text-muted-foreground hover:text-primary">{t("footer.songs")}</Link>
              <Link to="/nghe-nhan" className="text-sm text-muted-foreground hover:text-primary">{t("footer.artists")}</Link>
              <Link to="/lang-quan-ho" className="text-sm text-muted-foreground hover:text-primary">{t("footer.quanHoVillages")}</Link>
            </div>
          </div>
          <div>
            <h4 className="mb-3 font-display text-sm font-semibold text-foreground">{t("footer.contact")}</h4>
            <p className="text-sm text-muted-foreground">{t("footer.contactAddress")}</p>
            <p className="mt-1 text-sm text-muted-foreground">{t("footer.contactEmail")}</p>
          </div>
        </div>
        <div className="mt-8 border-t border-border pt-6 text-center text-xs text-muted-foreground">
          {t("footer.copyright")}
        </div>
      </div>
    </footer>
  );
}
