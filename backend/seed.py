from app.db import engine, Base
from app import models
import datetime

def seed_data():
    # Re-create tables
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)

    print("Opening database session...")
    db = SessionLocal()

    # Artists
    print("Seeding Artists...")
    artists = [
        models.Artist(
            id=1,
            name="NSND Thúy Cải",
            slug="nsnd-thuy-cai",
            biography="Nghệ sĩ Nhân dân Thúy Cải là một trong những giọng ca Quan họ nổi tiếng nhất Bắc Ninh. Bà đã cống hiến cả đời cho việc bảo tồn và phát huy nghệ thuật Quan họ truyền thống.",
            village="Làng Diềm",
            contributions="Truyền dạy Quan họ cho hơn 500 học trò, thu âm hơn 200 làn điệu cổ",
            performances=1500,
            image_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400",
            generation=models.ArtistGeneration.truyen_thong
        ),
        models.Artist(
            id=2,
            name="NSƯT Hai Tuyết",
            slug="nsut-hai-tuyet",
            biography="Nghệ sĩ Ưu tú Hai Tuyết sinh ra và lớn lên tại làng Quan họ cổ Lũng Giang. Bà được UNESCO vinh danh vì những đóng góp cho việc bảo tồn di sản Quan họ.",
            village="Lũng Giang",
            contributions="Nghiên cứu và phục dựng hơn 100 làn điệu Quan họ cổ",
            performances=1200,
            image_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400",
            generation=models.ArtistGeneration.truyen_thong
        ),
        models.Artist(
            id=3,
            name="NS Xuân Mùi",
            slug="ns-xuan-mui",
            biography="Nghệ sĩ Xuân Mùi là truyền nhân đời thứ ba trong gia đình có truyền thống Quan họ tại làng Ngang Nội. Ông nổi tiếng với giọng hát trầm ấm và phong cách biểu diễn đầy cảm xúc.",
            village="Ngang Nội",
            contributions="Sáng tác và cải biên hơn 50 bài Quan họ mới",
            performances=800,
            image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
            generation=models.ArtistGeneration.truyen_thong
        ),
        models.Artist(
            id=4,
            name="Liền chị Minh Thúy",
            slug="minh-thuy",
            biography="Đại diện tiêu biểu cho thế hệ trẻ hát Quan họ, Minh Thúy mang đến hơi thở mới cho những làn điệu cổ với cách xử lý tinh tế và hiện đại.",
            village="Viêm Xá",
            contributions="Giải nhất Tiếng hát Quan họ tỉnh Bắc Ninh 2023",
            performances=200,
            image_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400",
            generation=models.ArtistGeneration.the_he_moi
        )
    ]
    db.add_all(artists)
    db.commit()

    # Locations
    print("Seeding Locations...")
    locations = [
        models.Location(
            id=1,
            name="Làng Diềm (Viêm Xá)",
            slug="lang-diem",
            description="Cái nôi của Quan họ, nơi thờ Thủy tổ Quan họ. Làng còn giữ được nhiều nét kiến trúc cổ và những canh hát đối đáp mượt mà.",
            address="Xã Hòa Long, TP Bắc Ninh",
            festival="Lễ hội đền Cùng - Giếng Ngọc",
            image_url="https://images.unsplash.com/photo-1528164344705-47542687000d?w=400",
            latitude=21.18,
            longitude=106.07,
            type=models.LocationType.lang_quan_ho
        ),
        models.Location(
            id=2,
            name="Thủy Đình - Đền Đô",
            slug="thuy-dinh-den-do",
            description="Nơi diễn ra các buổi biểu diễn Quan họ trên thuyền rồng vào các dịp lễ lớn, đặc biệt là hội Đền Đô.",
            address="Phường Đình Bảng, Từ Sơn, Bắc Ninh",
            festival="Lễ hội Đền Đô (15/3 âm lịch)",
            image_url="https://images.unsplash.com/photo-1598970434795-0c54fe7c0648?w=400",
            latitude=21.10,
            longitude=105.99,
            type=models.LocationType.dien_xuong
        ),
        models.Location(
            id=3,
            name="Đồi Lim",
            slug="doi-lim",
            description="Trung tâm của Hội Lim nổi tiếng, nơi tụ hội của các liền anh, liền chị từ khắp 49 làng Quan họ gốc.",
            address="Thị trấn Lim, Tiên Du, Bắc Ninh",
            festival="Hội Lim (13 tháng Giêng)",
            image_url="https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=400",
            latitude=21.12,
            longitude=106.02,
            type=models.LocationType.le_hoi
        )
    ]
    db.add_all(locations)
    db.commit()

    # Melodies
    print("Seeding Melodies...")
    melodies = [
        models.Melody(
            id=1,
            name="Người Ơi Người Ở Đừng Về",
            slug="nguoi-oi-nguoi-o-dung-ve",
            lyrics="Người ơi người ở đừng về\nNgười về em vẫn khóc thầm\nĐôi bên bạn cũ ân cần\nBõ công em đợi bõ công em chờ...",
            image_url="https://images.unsplash.com/photo-1518639192441-8fce0a366e2e?w=400",
            duration="4:32",
            artist_id=1,
            village="Diềm",
            category=models.MelodyCategory.co,
            difficulty=models.Difficulty.trung_binh
        ),
        models.Melody(
            id=2,
            name="Bèo Dạt Mây Trôi",
            slug="beo-dat-may-troi",
            lyrics="Bèo dạt mây trôi chốn xa xôi\nAnh ơi em vẫn đợi chờ\nBến nước con đò sang ngang...",
            image_url="https://images.unsplash.com/photo-1528164344705-47542687000d?w=400",
            duration="5:10",
            artist_id=2,
            village="Lũng Giang",
            category=models.MelodyCategory.bien_tieu,
            difficulty=models.Difficulty.de
        ),
        models.Melody(
            id=3,
            name="Ngồi Tựa Mạn Thuyền",
            slug="ngoi-tua-man-thuyen",
            lyrics="Ngồi tựa mạn thuyền\nTrăng in đáy nước\nHương đưa gió thoảng\nCâu ca trao gửi tình thân...",
            image_url="https://images.unsplash.com/photo-1550985543-f47f38aee65e?w=400",
            duration="3:45",
            artist_id=3,
            village="Ngang Nội",
            category=models.MelodyCategory.co,
            difficulty=models.Difficulty.kho
        ),
        models.Melody(
            id=4,
            name="Làng Quan Họ Quê Tôi",
            slug="lang-quan-ho-que-toi",
            lyrics="Làng Quan họ quê tôi tháng Giêng mùa hát hội...\nMái đình cong cong, dòng sông Cầu lơ thơ nước chảy...",
            image_url="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400",
            duration="4:15",
            artist_id=4,
            village="Bắc Ninh",
            category=models.MelodyCategory.moi,
            difficulty=models.Difficulty.de
        )
    ]
    db.add_all(melodies)
    db.commit()

    # Articles
    print("Seeding Articles...")
    articles = [
        models.Article(
            id=1,
            title="Nguồn gốc Lễ hội Hội Lim",
            slug="nguon-goc-hoi-lim",
            content="Hội Lim là một lễ hội lớn ở tỉnh Bắc Ninh, được coi là nét kết tinh độc đáo của vùng văn hoá Kinh Bắc. Hội Lim được tổ chức vào ngày 13 tháng Giêng âm lịch hàng năm tại huyện Tiên Du...",
            category=models.ArticleCategory.le_hoi,
            status=models.ArticleStatus.published,
            image_url="https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=400"
        ),
        models.Article(
            id=2,
            title="Cách mặc trang phục Quan họ đúng chuẩn",
            slug="trang-phuc-quan-ho",
            content="Trang phục của các liền anh, liền chị không chỉ là quần áo mà còn là hồn cốt của nghệ thuật Quan họ. Liền chị mặc áo tứ thân, nón quai thao, liền anh mặc áo dài đen, khăn xếp...",
            category=models.ArticleCategory.nghe_thuat,
            status=models.ArticleStatus.published,
            image_url="https://images.unsplash.com/photo-1566737236500-c8ac43014a67?w=400"
        )
    ]
    db.add_all(articles)
    db.commit()

    # Events
    print("Seeding Events...")
    events = [
        models.Event(
            id=1,
            title="Đêm nhạc Quan họ Di sản",
            slug="dem-nhac-quan-ho-di-san",
            description="Chương trình biểu diễn các làn điệu Quan họ cổ do các nghệ sĩ nhân dân thực hiện.",
            start_date=datetime.date(2026, 4, 15),
            location_id=2,
            status=models.EventStatus.upcoming,
            image_url="https://images.unsplash.com/photo-1514525253344-a812dd969dff?w=400"
        ),
        models.Event(
            id=2,
            title="Khóa học hát Quan họ miễn phí cho thanh thiếu niên",
            slug="khoa-hoc-quan-ho-tre",
            description="Tìm hiểu và học hát những câu Quan họ cơ bản cùng các nghệ nhân.",
            start_date=datetime.date(2026, 6, 1),
            location_id=1,
            status=models.EventStatus.upcoming,
            image_url="https://images.unsplash.com/photo-1524178232363-1fb280714572?w=400"
        )
    ]
    db.add_all(events)
    db.commit()

    db.close()
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
