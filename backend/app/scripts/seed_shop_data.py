import sys
import os

# Thêm đường dẫn gốc để import được app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models
from app.models import ProductCategory

def seed_shop():
    db: Session = SessionLocal()
    try:
        print("--- Đang nạp dữ liệu Cửa hàng Quan Họ ---")

        products = [
            {
                "name": "Áo Tứ Thân Truyền Thống",
                "slug": "ao-tu-than-truyen-thong",
                "price": 1200000,
                "stock": 10,
                "category": ProductCategory.costume,
                "description": "Bộ áo tứ thân may thủ công từ lụa tơ tằm thượng hạng, dành cho các liền chị biểu diễn Quan họ chuyên nghiệp.",
                "image_url": "/static/products/ao-tu-than.png"
            },
            {
                "name": "Nón Quai Thao Thêu Rồng",
                "slug": "non-quai-thao-theu-rong",
                "price": 450000,
                "stock": 25,
                "category": ProductCategory.costume,
                "description": "Nón quai thao đặc trưng của người Kinh Bắc, được làm tỉ mỉ với họa tiết thêu rồng phượng và tua lụa dài.",
                "image_url": "/static/products/non-quai-thao.png"
            },
            {
                "name": "Bánh Phu Thê Đình Bảng",
                "slug": "banh-phu-the-dinh-bang",
                "price": 150000,
                "stock": 100,
                "category": ProductCategory.specialty,
                "description": "Đặc sản bánh phu thê (bánh xu xê) nổi tiếng của làng Đình Bảng. Hộp 10 chiếc gói lá dừa xanh mướt.",
                "image_url": "/static/products/banh-phu-the.png"
            },
            {
                "name": "Tranh Đông Hồ: Đám Cưới Chuột",
                "slug": "tranh-dong-ho-dam-cuoi-chuot",
                "price": 300000,
                "stock": 15,
                "category": ProductCategory.souvenir,
                "description": "Tranh dân gian Đông Hồ 'Đám Cưới Chuột' in trên giấy điệp truyền thống với màu sắc tự nhiên.",
                "image_url": "/static/products/tranh-dong-ho.png"
            },
            {
                "name": "Mô Hình Liền Anh Liền Chị Gỗ",
                "slug": "mo-hinh-lien-anh-lien-chi",
                "price": 250000,
                "stock": 40,
                "category": ProductCategory.souvenir,
                "description": "Mô hình nghệ nhân Quan họ bằng gỗ sơn mài thủ công, quà lưu niệm ý nghĩa đậm chất Kinh Bắc.",
                "image_url": "https://images.unsplash.com/photo-1513519247352-4d748c214b68?auto=format&fit=crop&q=80&w=800"
            },
            {
                "name": "Vé VIP Hội Lim 2026",
                "slug": "ve-vip-hoi-lim-2026",
                "price": 500000,
                "stock": 50,
                "category": ProductCategory.ticket,
                "description": "Vé mời tham dự khai mạc Hội Lim 2026, bao gồm chỗ ngồi ưu tiên và tham gia canh hát đêm đặc sắc.",
                "image_url": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?auto=format&fit=crop&q=80&w=800"
            }
        ]

        for p_data in products:
            existing = db.query(models.Product).filter_by(slug=p_data["slug"]).first()
            if not existing:
                product = models.Product(**p_data)
                db.add(product)
                print(f"  + Đã thêm sản phẩm: {p_data['name']}")
            else:
                # Cập nhật thông tin nếu đã tồn tại
                for key, value in p_data.items():
                    setattr(existing, key, value)
                print(f"  * Đã cập nhật sản phẩm: {p_data['name']}")

        db.commit()
        print("--- Hoàn thành nạp dữ liệu Cửa hàng! ---")

    except Exception as e:
        print(f"Lỗi khi nạp dữ liệu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_shop()
