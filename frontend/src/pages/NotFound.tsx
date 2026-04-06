import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";

const NotFound = () => {
  const { t } = useTranslation();
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted">
      <div className="text-center">
        <h1 className="mb-4 text-6xl font-bold text-primary">404</h1>
        <p className="mb-6 text-xl text-muted-foreground">{t("notfound_page.title")}</p>
        <Link to="/" className="inline-block rounded-md bg-primary px-6 py-2 text-primary-foreground shadow-card transition-transform hover:scale-105">
          {t("notfound_page.back_home")}
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
