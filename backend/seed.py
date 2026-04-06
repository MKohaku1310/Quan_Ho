from app.db import engine, Base, SessionLocal
from app import models
from app.security import get_password_hash
import datetime

def seed_data():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)

    print("Opening database session...")
    db = SessionLocal()

    print("Seeding Users...")
    users = [
        models.User(
            id=1,
            name="Quản trị viên",
            email="admin@quanho.vn",
            hashed_password=get_password_hash("admin123"),
            role=models.UserRole.admin
        ),
        models.User(
            id=2,
            name="Nguyễn Văn Hoan",
            email="hoan.nv@gmail.com",
            hashed_password=get_password_hash("user123"),
            role=models.UserRole.user
        ),
        models.User(
            id=3,
            name="Trần Thị Mai",
            email="mai.tt@gmail.com",
            hashed_password=get_password_hash("user123"),
            role=models.UserRole.user
        )
    ]
    db.add_all(users)
    db.commit()

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
            image_url="/img/artist1.jpg",
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
            image_url="/img/artist2.jpg",
            generation=models.ArtistGeneration.truyen_thong
        ),
        models.Artist(
            id=3,
            name="NS Xuân Mùi",
            slug="ns-xuan-mui",
            biography="Nghệ sĩ Xuân Mùi là truyền nhân đời thứ ba trong gia đình có truyền thống Quan họ tại làng Ngang Nội. Ông nổi tiếng with giọng hát trầm ấm và phong cách biểu diễn đầy cảm xúc.",
            village="Ngang Nội",
            contributions="Sáng tác và cải biên hơn 50 bài Quan họ mới",
            performances=800,
            image_url="/img/artist3.jpg",
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
            image_url="/img/artist4.jpg",
            generation=models.ArtistGeneration.the_he_moi
        )
    ]
    db.add_all(artists)
    db.commit()

    print("Seeding Locations...")
    locations = [
        models.Location(
            id=1,
            name="Làng Diềm (Viêm Xá)",
            slug="lang-diem",
            description="Cái nôi của Quan họ, nơi thờ Thủy tổ Quan họ. Làng còn giữ được nhiều nét kiến trúc cổ và những canh hát đối đáp mượt mà.",
            address="Thôn Viêm Xá, xã Hòa Long, thành phố Bắc Ninh",
            festival="Lễ hội đền Cùng - Giếng Ngọc",
            image_url="/img/loc1.jpg",
            latitude=21.217222,
            longitude=106.0125,
            type=models.LocationType.lang_quan_ho
        ),
        models.Location(
            id=2,
            name="Thủy Đình - Đền Đô",
            slug="thuy-dinh-den-do",
            description="Nơi diễn ra các buổi biểu diễn Quan họ trên thuyền rồng vào các dịp lễ lớn, đặc biệt là hội Đền Đô.",
            address="Phường Đình Bảng, thành phố Từ Sơn, Bắc Ninh",
            festival="Lễ hội Đền Đô (15/3 âm lịch)",
            image_url="/img/loc2.jpg",
            latitude=21.104167,
            longitude=105.955556,
            type=models.LocationType.dien_xuong
        ),
        models.Location(
            id=3,
            name="Đồi Lim",
            slug="doi-lim",
            description="Trung tâm của Hội Lim nổi tiếng, nơi tụ hội của các liền anh, liền chị từ khắp 49 làng Quan họ gốc.",
            address="Núi Hồng Vân, thị trấn Lim, huyện Tiên Du, Bắc Ninh",
            festival="Hội Lim (13 tháng Giêng)",
            image_url="/img/loc3.jpg",
            latitude=21.134722,
            longitude=106.027778,
            type=models.LocationType.le_hoi
        )
    ]
    db.add_all(locations)
    db.commit()

    print("Seeding Melodies...")
    melodies = [
        models.Melody(
            id=1,
            name="Người Ơi Người Ở Đừng Về",
            slug="nguoi-oi-nguoi-o-dung-ve",
            lyrics="Người ơi người ở đừng về\nNgười về em vẫn khóc thầm\nĐôi bên bạn cũ ân cần\nBõ công em đợi bõ công em chờ...",
            image_url="https://img.youtube.com/vi/Nflsf3SytYc/hqdefault.jpg",
            video_url="https://www.youtube.com/embed/Nflsf3SytYc",
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
            image_url="https://img.youtube.com/vi/LBxXWnloocM/hqdefault.jpg",
            video_url="https://www.youtube.com/embed/LBxXWnloocM",
            duration="5:10",
            artist_id=2,
            village="Lũng Giang",
            category=models.MelodyCategory.cai_bien,
            difficulty=models.Difficulty.de
        ),
        models.Melody(
            id=3,
            name="Ngồi Tựa Mạn Thuyền",
            slug="ngoi-tua-man-thuyen",
            lyrics="Ngồi tựa mạn thuyền\nTrăng in đáy nước\nHương đưa gió thoảng\nCâu ca trao gửi tình thân...",
            image_url="https://img.youtube.com/vi/uW6k0g5iQ1I/hqdefault.jpg",
            video_url="https://www.youtube.com/embed/uW6k0g5iQ1I",
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
            image_url="https://img.youtube.com/vi/TQW-ToDzO5U/hqdefault.jpg",
            video_url="https://www.youtube.com/embed/TQW-ToDzO5U",
            duration="4:15",
            artist_id=4,
            village="Bắc Ninh",
            category=models.MelodyCategory.moi,
            difficulty=models.Difficulty.de
        ),
        models.Melody(
            id=5,
            name="Hoa Thơm Bướm Lượn",
            slug="hoa-thom-buom-luon",
            lyrics="Hoa thơm bướm lượn ngẩn ngơ\nAnh đi qua đây mà ngỡ vào mơ\nĐôi bờ hoa nở tình thơ...",
            image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800",
            duration="3:48",
            artist_id=1,
            village="Hoài Thượng",
            category=models.MelodyCategory.co,
            difficulty=models.Difficulty.trung_binh
        ),
        models.Melody(
            id=6,
            name="Xe Chỉ Luồn Kim",
            slug="xe-chi-luon-kim",
            lyrics="Xe chỉ luồn kim khéo léo tay\nĐêm khuya vẫn ngồi thêu hoa...",
            image_url="https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=800",
            duration="4:05",
            artist_id=3,
            village="Ngang Nội",
            category=models.MelodyCategory.cai_bien,
            difficulty=models.Difficulty.de
        ),
        models.Melody(
            id=7,
            name="Tình Bằng Có Cái Trống Cơm",
            slug="tinh-bang-co-cai-trong-com",
            lyrics="Tình bằng có cái trống cơm\nKhen ai khéo vỗ ấy mà nên bông nên bông...",
            image_url="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800",
            duration="3:55",
            artist_id=2,
            village="Diềm",
            category=models.MelodyCategory.co,
            difficulty=models.Difficulty.de
        ),
        models.Melody(
            id=8,
            name="Cây Trúc Xinh",
            slug="cay-truc-xinh",
            lyrics="Cây trúc xinh tang tình tang\nCây trúc xinh đứng bên đình\nChị Hai xinh đứng một mình cũng xinh...",
            image_url="https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=800",
            duration="4:20",
            artist_id=3,
            village="Y Na",
            category=models.MelodyCategory.co,
            difficulty=models.Difficulty.de
        )
    ]
    db.add_all(melodies)
    db.commit()

    print("Seeding Articles...")
    articles = [
        models.Article(
            id=1,
            title="Kỷ niệm 15 năm Quan họ Bắc Ninh là Di sản Văn hóa Phi vật thể UNESCO",
            slug="ky-niem-15-nam-unesco",
            excerpt="Nhìn lại chặng đường 15 năm bảo tồn và phát huy giá trị di sản dân ca Quan họ Bắc Ninh trên trường quốc tế.",
            content="""<p>Vào ngày 30 tháng 9 năm 2009, tại phiên họp lần thứ tư của Ủy ban Liên Chính phủ Công ước UNESCO về bảo vệ di sản văn hóa phi vật thể, dân ca Quan họ Bắc Ninh đã chính thức được ghi danh vào Danh sách Di sản văn hóa phi vật thể đại diện của nhân loại.</p>
<p>Kể từ đó đến nay, tỉnh Bắc Ninh đã không ngừng nỗ lực trong việc truyền dạy, quảng bá và bảo tồn loại hình nghệ thuật độc đáo này. Với hơn 49 làng Quan họ gốc và hàng trăm CLB trên khắp cả nước, dân ca Quan họ vẫn đang tràn đầy sức sống trong dòng chảy hiện đại.</p>
<p>Các hoạt động kỷ niệm bao gồm các buổi biểu diễn nghệ thuật quy mô lớn, hội thảo quốc tế và vinh danh các nghệ nhân ưu tú đã có công truyền dạy di sản cho thế hệ trẻ.</p>""",
            category=models.ArticleCategory.lich_su,
            status=models.ArticleStatus.published,
            image_url="/img/article1.jpg",
            author_id=1
        ),
        models.Article(
            id=2,
            title="Làng Diềm - Điểm đến linh thiêng của những câu hát Quan họ cổ",
            slug="lang-diem-chiec-noi-quan-ho",
            excerpt="Khám phá ngôi làng cổ nhất - nơi thờ thủy tổ của dân ca Quan họ Bắc Ninh.",
            content="""<p>Làng Diềm (xã Hòa Long, TP Bắc Ninh) được coi là thủy tổ của dân ca Quan họ. Đây là nơi duy nhất có đền thờ Đức Vua Bà - người đã có công sáng tạo và truyền dạy những câu hát giao duyên cho dân làng.</p>
<p>Đến với làng Diềm, du khách không chỉ được thưởng thức những làn điệu cổ 'nguyên bản' mà còn được tham quan những kiến trúc đình chùa cổ kính, nơi diễn ra các canh hát thâu đêm suốt sáng của các liền anh, liền chị.</p>
<p>Hiện nay, làng Diềm vẫn duy trì lối hát đối đáp mộc mạc, không cần nhạc đệm, giữ đúng phong thái cốt cách của người Quan họ xưa.</p>""",
            category=models.ArticleCategory.tin_tuc,
            status=models.ArticleStatus.published,
            image_url="https://img.youtube.com/vi/Nflsf3SytYc/hqdefault.jpg",
            author_id=1
        ),
        models.Article(
            id=3,
            title="Hướng dẫn cách mặc trang phục Quan họ đúng chuẩn Kinh Bắc",
            slug="huong-dan-trang-phuc-quan-ho",
            excerpt="Tìm hiểu ý nghĩa của áo mớ ba mớ bảy, nón quai thao và khăn mỏ quạ trong văn hóa Quan họ.",
            content="""<p>Trang phục Quan họ không chỉ là trang phục biểu diễn mà còn chứa đựng triết lý nhân sinh của người Kinh Bắc. Với nữ giới, quan trọng nhất là bộ áo mớ ba mớ bảy, tượng trưng cho sự dịu dàng và kín đáo.</p>
<p>Bộ trang phục bao gồm: Áo trong cùng là áo yếm, tiếp đến là các lớp áo lụa nhiều màu tầng tầng lớp lớp. Chiếc nón quai thao che nghiêng gương mặt, cùng chiếc khăn mỏ quạ thắt gọn gàng tạo nên nét duyên dáng đặc trưng.</p>
<p>Với nam giới, trang phục gồm áo dài đen, quần trắng, khăn xếp và chiếc ô đen, thể hiện sự lịch lãm, trọng nghĩa trọng tình của các liền anh.</p>""",
            category=models.ArticleCategory.nghe_thuat,
            status=models.ArticleStatus.published,
            image_url="https://images.unsplash.com/photo-1528164344705-47542687000d?w=800",
            author_id=1
        )
    ]
    db.add_all(articles)
    db.commit()

    print("Seeding Events...")
    events = [
        models.Event(
            id=1,
            title="Hát Quan họ trên thuyền Rồng - Hồ Nguyên Phi Ỷ Lan",
            slug="hat-quan-ho-thuyen-rong-2026",
            description="Chương trình biểu diễn định kỳ hàng tuần. Du khách sẽ được hòa mình vào không gian sông nước Kinh Bắc, nghe những lời ca đối đáp mượt mà, đằm thắm của các nghệ nhân tên tuổi trên những chiếc thuyền rồng lộng lẫy.",
            start_date=datetime.date(2026, 4, 15),
            location_id=2,
            status=models.EventStatus.upcoming,
            image_url="https://img.youtube.com/vi/LBxXWnloocM/hqdefault.jpg"
        ),
        models.Event(
            id=2,
            title="Đại lễ hội Hội Lim - Tiên Du 2026",
            slug="le-hoi-hoi-lim-2026",
            description="Lễ hội lớn nhất vùng Kinh Bắc với các hoạt động: Rước sắc, hát đối đáp tại lán trại, thi các trò chơi dân gian (đập niêu, vật, chọi gà) và đặc biệt là canh hát thâu đêm tại nhà các nghệ nhân Quan họ.",
            start_date=datetime.date(2026, 2, 28),
            location_id=1,
            status=models.EventStatus.upcoming,
            image_url="https://img.youtube.com/vi/uW6k0g5iQ1I/hqdefault.jpg"
        ),
        models.Event(
            id=3,
            title="Khóa đào tạo Nghệ nhân Quan họ nhí hè 2026",
            slug="dao-tao-quan-ho-nhi",
            description="Lớp học miễn phí dành cho học sinh từ 8-15 tuổi yêu thích quan họ. Các em sẽ được học cách luyến láy, nhả chữ và phong thái biểu diễn từ những nghệ nhân ưu tú nhất của 49 làng quan họ gốc.",
            start_date=datetime.date(2026, 6, 1),
            location_id=3,
            status=models.EventStatus.upcoming,
            image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800"
        )
    ]
    db.add_all(events)
    db.commit()

    print("Seeding Media...")
    media_items = [
        models.Media(
            url="/img/artist1.jpg",
            type=models.MediaType.image,
            artist_id=1
        ),
        models.Media(
            url="/img/loc1.jpg",
            type=models.MediaType.image,
            location_id=1
        )
    ]
    db.add_all(media_items)
    db.commit()

    print("Seeding Comments...")
    comments = [
        models.Comment(
            content="Làn điệu này thực sự rất hay và mượt mà!",
            user_id=2,
            melody_id=1
        ),
        models.Comment(
            content="Cảm ơn tác giả đã chia sẻ bài viết rất hữu ích.",
            user_id=3,
            article_id=1
        )
    ]
    db.add_all(comments)
    db.commit()

    db.close()
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
