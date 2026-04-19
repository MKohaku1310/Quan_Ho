import sys
import os

# Thêm đường dẫn gốc để import được app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app import models
from app.models import MelodyCategory, ArtistGeneration, LocationType

def seed_data():
    db: Session = SessionLocal()
    try:
        print("--- Đang nạp dữ liệu Quan Họ thực tế ---")

        # 1. THÊM LÀNG QUAN HỌ (LOCATIONS)
        villages = [
            {
                "name": "Làng Khả Lễ",
                "slug": "lang-kha-le",
                "address": "Phường Võ Cường, Thành phố Bắc Ninh",
                "district": "TP Bắc Ninh",
                "latitude": 21.1654,
                "longitude": 106.0521,
                "artist_count": 12,
                "featured_songs": "Vào chùa, Ngồi tựa mạn thuyền",
                "badges": "Làng cổ, Di sản UNESCO",
                "description": "Làng Khả Lễ là một trong những cái nôi của dân ca Quan họ Bắc Ninh. Làng nổi tiếng với phong cách chơi Quan họ 'phong lưu', trọng tình trọng nghĩa.",
                "history": "Khả Lễ có truyền thống văn hiến lâu đời. Đình Khả Lễ là nơi diễn ra các buổi hát đối đáp quan trọng của các liền anh, liền chị từ xa xưa.",
                "culture": "Người dân Khả Lễ nổi tiếng với tục kết chạ và các quy định nghiêm ngặt trong cách chơi Quan họ truyền thống.",
                "image_url": "https://images.unsplash.com/photo-1621259182978-f09e5e2ca845?auto=format&fit=crop&q=80&w=1200",
                "type": LocationType.lang_quan_ho
            },
            {
                "name": "Làng Bồ Sơn",
                "slug": "lang-bo-son",
                "address": "Phường Võ Cường, Thành phố Bắc Ninh",
                "district": "TP Bắc Ninh",
                "latitude": 21.1782,
                "longitude": 106.0615,
                "artist_count": 15,
                "featured_songs": "Còn duyên, Khách đến chơi nhà",
                "badges": "Làng gốc, Nghệ nhân ưu tú",
                "description": "Làng Bồ Sơn (núi Bồ) là làng Quan họ gốc nổi tiếng với những giọng ca mộc mạc nhưng đầy nội lực.",
                "history": "Truyền thuyết kể rằng tiếng hát Quan họ Bồ Sơn đã có từ thời nhà Lý, gắn liền với các lễ hội cầu mùa của vùng Kinh Bắc.",
                "image_url": "https://images.unsplash.com/photo-1590001158193-79037ca0869d?auto=format&fit=crop&q=80&w=1200",
                "type": LocationType.lang_quan_ho
            },
            {
                "name": "Làng Hòa Đình",
                "slug": "lang-hoa-dinh",
                "address": "Phường Võ Cường, Thành phố Bắc Ninh",
                "district": "TP Bắc Ninh",
                "latitude": 21.1715,
                "longitude": 106.0583,
                "artist_count": 8,
                "featured_songs": "Thân lươn bao quản lấm đầu",
                "badges": "Làng Quan họ gốc",
                "description": "Làng Hòa Đình (tên nôm là làng Nhồi) là một trong những làng Quan họ tiêu biểu của vùng đất Võ Cường.",
                "image_url": "https://images.unsplash.com/photo-1596402184320-417d7178b2cd?auto=format&fit=crop&q=80&w=1200",
                "type": LocationType.lang_quan_ho
            }
        ]

        for v_data in villages:
            existing = db.query(models.Location).filter_by(slug=v_data["slug"]).first()
            if not existing:
                village = models.Location(**v_data)
                db.add(village)
                print(f"  + Đã thêm làng: {v_data['name']}")

        db.commit()

        # 2. THÊM NGHỆ NHÂN (ARTISTS)
        artists = [
            {
                "name": "Nghệ nhân ưu tú Nguyễn Thị Bàn",
                "slug": "nguyen-thi-ban",
                "birth_year": 1952,
                "description": "Nghệ nhân nòng cốt của làng Quan họ Diềm (Viêm Xá). Bà được biết đến với kỹ thuật vang, rền, nền, nảy bậc thầy.",
                "biography": "Sinh ra trong một gia đình có truyền thống ca hát tại làng Diềm, bà đã dành cả đời để sưu tầm và truyền dạy các làn điệu Quan họ cổ cho thế hệ mai sau.",
                "village": "Làng Diềm",
                "image_url": "https://images.unsplash.com/photo-1566753323558-f4e0952af115?auto=format&fit=crop&q=80&w=400",
                "generation": ArtistGeneration.truyen_thong
            },
            {
                "name": "NSND Quý Tráng",
                "slug": "quy-trang",
                "birth_year": 1955,
                "description": "Cựu Giám đốc Nhà hát Dân ca Quan họ Bắc Ninh, người có công lớn trong việc đưa Quan họ ra thế giới.",
                "biography": "Ông là một trong những giọng ca nam tiêu biểu, góp phần định hình phong cách biểu diễn Quan họ hiện đại trên sân khấu.",
                "village": "Bắc Ninh",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=400",
                "generation": ArtistGeneration.the_he_moi
            }
        ]

        for a_data in artists:
            existing = db.query(models.Artist).filter_by(slug=a_data["slug"]).first()
            if not existing:
                artist = models.Artist(**a_data)
                db.add(artist)
                print(f"  + Đã thêm nghệ nhân: {a_data['name']}")

        db.commit()

        # 3. THÊM LÀN ĐIỆU (MELODIES)
        # Lấy artist ID để gán
        artist_ban = db.query(models.Artist).filter_by(slug="nguyen-thi-ban").first()
        artist_trang = db.query(models.Artist).filter_by(slug="quy-trang").first()

        melodies = [
            {
                "name": "Còn duyên",
                "slug": "con-duyen",
                "category": MelodyCategory.co,
                "duration": "04:12",
                "image_url": "https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800",
                "description": "Làn điệu Quan họ cổ nổi tiếng nhất, ca ngợi vẻ đẹp và sự duyên dáng của người con gái trong độ tuổi thanh xuân.",
                "artist_id": artist_ban.id if artist_ban else None,
                "village": "Làng Diềm"
            },
            {
                "name": "Khách đến chơi nhà",
                "slug": "khach-den-choi-nha",
                "category": MelodyCategory.co,
                "duration": "03:45",
                "image_url": "https://images.unsplash.com/photo-1517230814606-2e129f553d43?auto=format&fit=crop&q=80&w=800",
                "description": "Một bài hát thể hiện lòng hiếu khách đặc trưng của người dân Kinh Bắc.",
                "artist_id": artist_ban.id if artist_ban else None,
                "village": "Vùng Kinh Bắc"
            },
            {
                "name": "Hoa thơm bướm lượn",
                "slug": "hoa-thom-buom-luon",
                "category": MelodyCategory.moi,
                "duration": "03:20",
                "image_url": "https://images.unsplash.com/photo-1490750967868-886a5a07aa99?auto=format&fit=crop&q=80&w=800",
                "description": "Làn điệu vui tươi, rộn ràng, miêu tả cảnh sắc thiên nhiên và tình yêu đôi lứa.",
                "artist_id": artist_trang.id if artist_trang else None,
                "village": "Bắc Ninh"
            }
        ]

        for m_data in melodies:
            existing = db.query(models.Melody).filter_by(slug=m_data["slug"]).first()
            if not existing:
                melody = models.Melody(**m_data)
                db.add(melody)
                print(f"  + Đã thêm làn điệu: {m_data['name']}")

        db.commit()
        print("--- Hoàn thành nạp dữ liệu! ---")

    except Exception as e:
        print(f"Lỗi khi nạp dữ liệu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
