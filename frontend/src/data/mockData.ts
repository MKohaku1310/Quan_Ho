export interface Song {
  id: number;
  title: string;
  melody: string;
  village: string;
  artist: string;
  artistId: number;
  lyrics: string;
  audioUrl?: string;
  videoUrl?: string;
  imageUrl: string;
  duration: string;
}

export interface Artist {
  id: number;
  name: string;
  photo: string;
  biography: string;
  village: string;
  contributions: string;
  performances: number;
}

export interface Village {
  id: number;
  name: string;
  description: string;
  address: string;
  festival: string;
  artists: string[];
  imageUrl: string;
  lat: number;
  lng: number;
}

export interface NewsEvent {
  id: number;
  title: string;
  excerpt: string;
  content: string;
  date: string;
  imageUrl: string;
  category: "news" | "event" | "festival";
}

export const songs: Song[] = [
  {
    id: 1,
    title: "Người Ơi Người Ở Đừng Về",
    melody: "La rằng",
    village: "Diềm",
    artist: "NSND Thúy Cải",
    artistId: 1,
    lyrics: "Người ơi người ở đừng về\nNgười về em vẫn khóc thầm\nĐôi bên bạn cũ ân cần\nBõ công em đợi bõ công em chờ...",
    imageUrl: "https://images.unsplash.com/photo-1518639192441-8fce0a366e2e?w=400",
    duration: "4:32",
  },
  {
    id: 2,
    title: "Bèo Dạt Mây Trôi",
    melody: "Giã bạn",
    village: "Lũng Giang",
    artist: "NSƯT Hai Tuyết",
    artistId: 2,
    lyrics: "Bèo dạt mây trôi chốn xa xôi\nAnh ơi em vẫn đợi chờ\nBến nước con đò sang ngang...",
    imageUrl: "https://images.unsplash.com/photo-1528164344705-47542687000d?w=400",
    duration: "5:10",
  },
  {
    id: 3,
    title: "Hoa Thơm Bướm Lượn",
    melody: "Lề lối",
    village: "Hoài Thượng",
    artist: "NSND Thúy Cải",
    artistId: 1,
    lyrics: "Hoa thơm bướm lượn ngẩn ngơ\nAnh đi qua đây mà ngỡ vào mơ\nĐôi bờ hoa nở tình thơ...",
    imageUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
    duration: "3:48",
  },
  {
    id: 4,
    title: "Xe Chỉ Luồn Kim",
    melody: "Vặt",
    village: "Ngang Nội",
    artist: "NS Xuân Mùi",
    artistId: 3,
    lyrics: "Xe chỉ luồn kim khéo léo tay\nĐêm khuya vẫn ngồi thêu hoa...",
    imageUrl: "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=400",
    duration: "4:05",
  },
  {
    id: 5,
    title: "Tình Bằng Có Cái Trống Cơm",
    melody: "La rằng",
    village: "Diềm",
    artist: "NSƯT Hai Tuyết",
    artistId: 2,
    lyrics: "Tình bằng có cái trống cơm\nKhen ai khéo vỗ ấy mà nên bông nên bông...",
    imageUrl: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400",
    duration: "3:55",
  },
  {
    id: 6,
    title: "Cây Trúc Xinh",
    melody: "Giã bạn",
    village: "Y Na",
    artist: "NS Xuân Mùi",
    artistId: 3,
    lyrics: "Cây trúc xinh tang tình tang\nCây trúc xinh đứng bên đình\nChị Hai xinh đứng một mình cũng xinh...",
    imageUrl: "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=400",
    duration: "4:20",
  },
];

export const artists: Artist[] = [
  {
    id: 1,
    name: "NSND Thúy Cải",
    photo: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400",
    biography: "Nghệ sĩ Nhân dân Thúy Cải là một trong những giọng ca Quan họ nổi tiếng nhất Bắc Ninh. Bà đã cống hiến cả đời cho việc bảo tồn và phát huy nghệ thuật Quan họ truyền thống.",
    village: "Diềm",
    contributions: "Truyền dạy Quan họ cho hơn 500 học trò, thu âm hơn 200 làn điệu cổ",
    performances: 1500,
  },
  {
    id: 2,
    name: "NSƯT Hai Tuyết",
    photo: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400",
    biography: "Nghệ sĩ Ưu tú Hai Tuyết sinh ra và lớn lên tại làng Quan họ cổ Lũng Giang. Bà được UNESCO vinh danh vì những đóng góp cho việc bảo tồn di sản Quan họ.",
    village: "Lũng Giang",
    contributions: "Nghiên cứu và phục dựng hơn 100 làn điệu Quan họ cổ",
    performances: 1200,
  },
  {
    id: 3,
    name: "NS Xuân Mùi",
    photo: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
    biography: "Nghệ sĩ Xuân Mùi là truyền nhân đời thứ ba trong gia đình có truyền thống Quan họ tại làng Ngang Nội. Ông nổi tiếng với giọng hát trầm ấm và phong cách biểu diễn đầy cảm xúc.",
    village: "Ngang Nội",
    contributions: "Sáng tác và cải biên hơn 50 bài Quan họ mới",
    performances: 800,
  },
  {
    id: 4,
    name: "NSƯT Thanh Hiếu",
    photo: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400",
    biography: "Nghệ sĩ Ưu tú Thanh Hiếu là liền anh nổi tiếng của làng Quan họ Y Na. Ông đã tham gia nhiều chương trình biểu diễn quốc tế, mang Quan họ đến gần hơn với bạn bè quốc tế.",
    village: "Y Na",
    contributions: "Đại sứ văn hóa Quan họ tại hơn 20 quốc gia",
    performances: 950,
  },
];

export const villages: Village[] = [
  {
    id: 1,
    name: "Làng Diềm (Viêm Xá)",
    description: "Được coi là cái nôi của Quan họ, làng Diềm nằm bên bờ sông Cầu, nơi khởi nguồn của nghệ thuật hát Quan họ từ hàng trăm năm trước.",
    festival: "Hội Lim (Tháng Giêng âm lịch)",
    artists: ["NSND Thúy Cải", "NS Văn Hùng"],
    imageUrl: "https://images.unsplash.com/photo-1528164344705-47542687000d?w=400",
    lat: 21.18,
    lng: 106.07,
  },
  {
    id: 2,
    name: "Làng Lũng Giang",
    description: "Làng Quan họ cổ nổi tiếng với truyền thống hát canh suốt đêm. Nơi đây còn lưu giữ nhiều phong tục Quan họ nguyên bản nhất.",
    festival: "Hội làng Lũng Giang (Tháng 2 âm lịch)",
    artists: ["NSƯT Hai Tuyết", "NS Minh Thu"],
    imageUrl: "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=400",
    lat: 21.15,
    lng: 106.10,
  },
  {
    id: 3,
    name: "Làng Y Na",
    description: "Làng Y Na thuộc phường Kinh Bắc, thành phố Bắc Ninh, là một trong 49 làng Quan họ gốc được UNESCO công nhận.",
    festival: "Hội đền Bà Chúa Kho (Tháng Giêng)",
    artists: ["NSƯT Thanh Hiếu"],
    imageUrl: "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=400",
    lat: 21.19,
    lng: 106.05,
  },
  {
    id: 4,
    name: "Làng Hoài Thượng",
    description: "Nằm ở huyện Thuận Thành, Bắc Ninh, làng Hoài Thượng nổi tiếng với lối hát đối đáp tinh tế giữa liền anh và liền chị.",
    festival: "Hội chùa Dâu (Tháng 4 âm lịch)",
    artists: ["NS Ngọc Lan", "NS Thu Hương"],
    imageUrl: "https://images.unsplash.com/photo-1518639192441-8fce0a366e2e?w=400",
    lat: 21.10,
    lng: 106.12,
  },
];

export const newsEvents: NewsEvent[] = [
  {
    id: 1,
    title: "Hội Lim 2026 - Lễ hội Quan họ lớn nhất trong năm",
    excerpt: "Hội Lim năm nay thu hút hơn 100.000 du khách trong và ngoài nước đến tham dự và thưởng thức các làn điệu Quan họ cổ.",
    content: "",
    date: "2026-02-15",
    imageUrl: "https://images.unsplash.com/photo-1528164344705-47542687000d?w=400",
    category: "festival",
  },
  {
    id: 2,
    title: "UNESCO đánh giá cao công tác bảo tồn Quan họ",
    excerpt: "Đoàn chuyên gia UNESCO đã có chuyến khảo sát và đánh giá rất tích cực về công tác bảo tồn và phát huy giá trị Quan họ Bắc Ninh.",
    content: "",
    date: "2026-01-20",
    imageUrl: "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=400",
    category: "news",
  },
  {
    id: 3,
    title: "Khai mạc lớp truyền dạy Quan họ cho thế hệ trẻ",
    excerpt: "Sở Văn hóa tỉnh Bắc Ninh phối hợp với các nghệ nhân tổ chức lớp truyền dạy Quan họ miễn phí cho thanh thiếu niên.",
    content: "",
    date: "2026-03-01",
    imageUrl: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400",
    category: "event",
  },
  {
    id: 4,
    title: "Quan họ Bắc Ninh trình diễn tại Festival Huế",
    excerpt: "Đoàn nghệ sĩ Quan họ Bắc Ninh tham gia trình diễn tại Festival Huế 2026, mang đến những làn điệu đặc sắc.",
    content: "",
    date: "2026-04-10",
    imageUrl: "https://images.unsplash.com/photo-1518639192441-8fce0a366e2e?w=400",
    category: "event",
  },
];

export const melodies = ["La rằng", "Giã bạn", "Lề lối", "Vặt"];
export const villageNames = ["Diềm", "Lũng Giang", "Hoài Thượng", "Ngang Nội", "Y Na"];
