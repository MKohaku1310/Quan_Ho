import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import SectionTitle from "@/components/SectionTitle";
import { motion } from "framer-motion";
import heroBanner from "@/assets/hero-banner.jpg";

export default function Introduction() {
  const timeline = [
    { year: "Thế kỷ 15", text: "Quan họ bắt đầu hình thành tại vùng Kinh Bắc, gắn liền với đời sống làng xã và tín ngưỡng thờ thành hoàng." },
    { year: "Thế kỷ 17-18", text: "Thời kỳ phát triển rực rỡ nhất, 49 làng Quan họ gốc được xác lập, hình thành nét sinh hoạt văn hóa đặc sắc." },
    { year: "Thế kỷ 19", text: "Quan họ dần được ghi chép, nghiên cứu và trở thành biểu tượng văn hóa tiêu biểu của vùng Bắc Ninh - Bắc Giang." },
    { year: "2009", text: "UNESCO chính thức công nhận Quan họ Bắc Ninh là Di sản Văn hóa Phi vật thể đại diện của Nhân loại." },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* Hero */}
      <section className="relative flex min-h-[40vh] items-center overflow-hidden">
        <img src={heroBanner} alt="" className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-hero-gradient opacity-80" />
        <div className="relative z-10 container mx-auto px-4 py-16 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="font-display text-4xl font-bold text-primary-foreground md:text-5xl"
          >
            Giới thiệu Quan Họ
          </motion.h1>
          <p className="mt-3 text-primary-foreground/80">Lịch sử, nguồn gốc và giá trị văn hóa</p>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="container mx-auto max-w-3xl px-4">
          <SectionTitle title="Quan họ là gì?" />
          <div className="prose-custom space-y-4 text-muted-foreground leading-relaxed">
            <p>
              Quan họ Bắc Ninh là một hình thức hát giao duyên đối đáp giữa nam (liền anh) và nữ (liền chị),
              phổ biến tại vùng Kinh Bắc xưa, nay là tỉnh Bắc Ninh và Bắc Giang. Đây không chỉ là một thể loại
              dân ca mà còn là cả một hệ thống phong tục, tập quán, lễ nghi gắn liền với đời sống tinh thần
              của người dân nơi đây.
            </p>
            <p>
              Quan họ có hơn 300 làn điệu cổ, mỗi làn điệu mang một sắc thái tình cảm khác nhau — từ lời
              mời chào, gặp gỡ, đến giã bạn, tiễn biệt. Nghệ thuật hát Quan họ đòi hỏi kỹ thuật thanh nhạc
              tinh tế như luyến láy, rung, nảy hạt — tạo nên âm sắc đặc trưng không lẫn vào đâu được.
            </p>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="bg-card py-16">
        <div className="container mx-auto max-w-3xl px-4">
          <SectionTitle title="Dòng chảy lịch sử" />
          <div className="space-y-8">
            {timeline.map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="flex gap-6"
              >
                <div className="flex flex-col items-center">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
                    ❀
                  </div>
                  {i < timeline.length - 1 && <div className="w-px flex-1 bg-border" />}
                </div>
                <div className="pb-8">
                  <h3 className="font-display text-lg font-bold text-foreground">{item.year}</h3>
                  <p className="mt-1 text-muted-foreground">{item.text}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* UNESCO */}
      <section className="py-16">
        <div className="container mx-auto max-w-3xl px-4 text-center">
          <SectionTitle
            title="UNESCO 2009"
            subtitle="Di sản Văn hóa Phi vật thể đại diện của Nhân loại"
          />
          <p className="text-muted-foreground leading-relaxed">
            Ngày 30 tháng 9 năm 2009, tại phiên họp Ủy ban liên chính phủ Công ước UNESCO tại Abu Dhabi,
            Quan họ Bắc Ninh đã được chính thức công nhận là Di sản Văn hóa Phi vật thể đại diện của Nhân loại.
            Đây là niềm tự hào to lớn của người dân Bắc Ninh nói riêng và dân tộc Việt Nam nói chung.
          </p>
        </div>
      </section>

      <Footer />
    </div>
  );
}
