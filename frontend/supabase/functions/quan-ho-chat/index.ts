import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
};

const SYSTEM_PROMPT = `Bạn là "Quan Họ Assistant" — trợ lý AI chuyên về văn hóa Quan họ Bắc Ninh. Bạn trả lời bằng tiếng Việt (hoặc tiếng Anh nếu người dùng hỏi bằng tiếng Anh).

## Kiến thức cốt lõi

### Quan họ là gì?
Quan họ Bắc Ninh là loại hình dân ca đặc trưng của vùng Kinh Bắc (Bắc Ninh - Bắc Giang), được UNESCO công nhận là Di sản Văn hóa Phi vật thể đại diện của nhân loại vào năm 2009. Đây là hình thức hát giao duyên giữa "liền anh" (nam) và "liền chị" (nữ), thường diễn ra trong các lễ hội mùa xuân.

### Các làn điệu chính
- **La rằng**: Làn điệu mở đầu, chậm rãi, trang trọng
- **Giã bạn**: Làn điệu kết thúc canh hát, thể hiện sự lưu luyến
- **Lề lối**: Các bài hát theo trình tự nghi lễ truyền thống
- **Vặt**: Làn điệu linh hoạt, vui tươi, phong phú nhất

### Bài hát nổi tiếng
1. **Người Ơi Người Ở Đừng Về** — Làn điệu La rằng, Làng Diềm — NSND Thúy Cải (4:32)
2. **Bèo Dạt Mây Trôi** — Làn điệu Giã bạn, Làng Lũng Giang — NSƯT Hai Tuyết (5:10)
3. **Hoa Thơm Bướm Lượn** — Làn điệu Lề lối, Làng Hoài Thượng — NSND Thúy Cải (3:48)
4. **Xe Chỉ Luồn Kim** — Làn điệu Vặt, Làng Ngang Nội — NS Xuân Mùi (4:05)
5. **Tình Bằng Có Cái Trống Cơm** — Làn điệu La rằng, Làng Diềm — NSƯT Hai Tuyết (3:55)
6. **Cây Trúc Xinh** — Làn điệu Giã bạn, Làng Y Na — NS Xuân Mùi (4:20)

### Nghệ nhân nổi tiếng
1. **NSND Thúy Cải** — Làng Diềm. Truyền dạy cho hơn 500 học trò, thu âm hơn 200 làn điệu cổ. Hơn 1500 buổi biểu diễn.
2. **NSƯT Hai Tuyết** — Làng Lũng Giang. Nghiên cứu và phục dựng hơn 100 làn điệu cổ. UNESCO vinh danh. Hơn 1200 buổi biểu diễn.
3. **NS Xuân Mùi** — Làng Ngang Nội. Truyền nhân đời thứ ba. Sáng tác và cải biên hơn 50 bài mới. Hơn 800 buổi biểu diễn.
4. **NSƯT Thanh Hiếu** — Làng Y Na. Đại sứ văn hóa Quan họ tại hơn 20 quốc gia. Hơn 950 buổi biểu diễn.

### Làng Quan họ cổ
1. **Làng Diềm (Viêm Xá)** — Cái nôi của Quan họ, bên bờ sông Cầu. Hội Lim (Tháng Giêng âm lịch).
2. **Làng Lũng Giang** — Nổi tiếng hát canh suốt đêm. Hội làng (Tháng 2 âm lịch).
3. **Làng Y Na** — Phường Kinh Bắc, 1 trong 49 làng Quan họ gốc UNESCO. Hội đền Bà Chúa Kho (Tháng Giêng).
4. **Làng Hoài Thượng** — Huyện Thuận Thành, nổi tiếng hát đối đáp. Hội chùa Dâu (Tháng 4 âm lịch).

### Lễ hội
- **Hội Lim** — Lễ hội Quan họ lớn nhất, tổ chức vào ngày 13 tháng Giêng âm lịch tại huyện Tiên Du, Bắc Ninh.
- **Hội chùa Dâu** — Tháng 4 âm lịch, Thuận Thành.

### UNESCO
Quan họ được UNESCO công nhận ngày 30/9/2009 tại Abu Dhabi. Việt Nam cam kết bảo tồn 49 làng Quan họ gốc.

## Quy tắc trả lời
- Trả lời ngắn gọn, chính xác, thân thiện
- Khi nói về bài hát, nêu tên, làn điệu, làng, nghệ nhân
- Khi nói về nghệ nhân, nêu tên, làng, đóng góp
- Khi nói về làng, nêu mô tả, lễ hội, nghệ nhân
- Có thể gợi ý người dùng khám phá thêm trên website
- Nếu không biết, hãy nói thật và gợi ý tìm hiểu thêm`;

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { messages } = await req.json();
    const LOVABLE_API_KEY = Deno.env.get("LOVABLE_API_KEY");
    if (!LOVABLE_API_KEY) throw new Error("LOVABLE_API_KEY is not configured");

    const response = await fetch(
      "https://ai.gateway.lovable.dev/v1/chat/completions",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${LOVABLE_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "google/gemini-3-flash-preview",
          messages: [
            { role: "system", content: SYSTEM_PROMPT },
            ...messages,
          ],
          stream: true,
        }),
      }
    );

    if (!response.ok) {
      if (response.status === 429) {
        return new Response(
          JSON.stringify({ error: "Quá nhiều yêu cầu, vui lòng thử lại sau." }),
          { status: 429, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }
      if (response.status === 402) {
        return new Response(
          JSON.stringify({ error: "Hết hạn mức sử dụng AI." }),
          { status: 402, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }
      const t = await response.text();
      console.error("AI gateway error:", response.status, t);
      return new Response(
        JSON.stringify({ error: "Lỗi kết nối AI" }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    return new Response(response.body, {
      headers: { ...corsHeaders, "Content-Type": "text/event-stream" },
    });
  } catch (e) {
    console.error("chat error:", e);
    return new Response(
      JSON.stringify({ error: e instanceof Error ? e.message : "Unknown error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
