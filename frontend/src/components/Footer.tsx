import { Link } from "react-router-dom";
import lotusOrnament from "@/assets/lotus-ornament.png";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-card">
      <div className="container mx-auto px-4 py-12">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <div className="mb-3 flex items-center gap-2">
              <img src={lotusOrnament} alt="" className="h-8 w-8" />
              <span className="font-display text-lg font-bold text-primary">Quan Họ Bắc Ninh</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Bảo tồn và phát huy giá trị di sản văn hóa phi vật thể Quan họ Bắc Ninh - UNESCO 2009.
            </p>
          </div>
          <div>
            <h4 className="mb-3 font-display text-sm font-semibold text-foreground">Khám phá</h4>
            <div className="flex flex-col gap-2">
              <Link to="/gioi-thieu" className="text-sm text-muted-foreground hover:text-primary">Giới thiệu</Link>
              <Link to="/bai-hat" className="text-sm text-muted-foreground hover:text-primary">Bài hát</Link>
              <Link to="/nghe-nhan" className="text-sm text-muted-foreground hover:text-primary">Nghệ nhân</Link>
              <Link to="/lang-quan-ho" className="text-sm text-muted-foreground hover:text-primary">Làng Quan họ</Link>
            </div>
          </div>
          <div>
            <h4 className="mb-3 font-display text-sm font-semibold text-foreground">Liên hệ</h4>
            <p className="text-sm text-muted-foreground">Sở Văn hóa, Thể thao và Du lịch tỉnh Bắc Ninh</p>
            <p className="mt-1 text-sm text-muted-foreground">Email: quanho@bacninh.gov.vn</p>
          </div>
        </div>
        <div className="mt-8 border-t border-border pt-6 text-center text-xs text-muted-foreground">
          © 2026 Quan Họ Bắc Ninh. Di sản văn hóa phi vật thể của nhân loại.
        </div>
      </div>
    </footer>
  );
}
