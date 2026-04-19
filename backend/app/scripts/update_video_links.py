import sys
import os

# Thêm đường dẫn gốc để import được app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models

def update_links():
    db: Session = SessionLocal()
    try:
        print("--- Updating Youtube links for melodies ---")
        
        # Danh sách slug và link youtube tương ứng
        links = {
            "con-duyen": "https://www.youtube.com/watch?v=_TsIwL40YqM",
            "khach-den-choi-nha": "https://www.youtube.com/watch?v=BNtcLNed-4g",
            "hoa-thom-buom-luon": "https://www.youtube.com/watch?v=2wpLmNUZUM4",
            "beo-dat-may-troi": "https://www.youtube.com/watch?v=LBxXWnloocM",
            "ngoi-tua-man-thuyen": "https://www.youtube.com/watch?v=KCZn0lvdU6A",
            "lang-quan-ho-que-toi": "https://www.youtube.com/watch?v=TQW-ToDzO5U",
            "xe-chi-luon-kim": "https://www.youtube.com/watch?v=faxV33N8uo4",
            "tinh-bang-co-cai-trong-com": "https://www.youtube.com/watch?v=TFyBK3xzswA"
        }

        updated_count = 0
        for slug, url in links.items():
            melody = db.query(models.Melody).filter_by(slug=slug).first()
            if melody:
                melody.video_url = url
                # Tự động tạo link ảnh từ Youtube ID
                import re
                yt_match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', url)
                if yt_match:
                    video_id = yt_match.group(1)
                    melody.image_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                
                print(f"  + Updated video and image for: {slug}")
                updated_count += 1
            else:
                # Nếu không tìm thấy theo slug, thử tìm theo tên (không dấu/thường)
                # Đơn giản nhất là bỏ qua nếu không có trong db hiện tại
                pass

        db.commit()
        print(f"--- Completed updating {updated_count} melodies! ---")

    except Exception as e:
        print(f"Error during update: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_links()
