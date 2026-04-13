import os
import google.generativeai as genai
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models
from pydantic import BaseModel
from typing import List, Optional
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class ChatMessage(BaseModel):
    message: str

def get_context_summary(db: Session):
    """Lấy tóm tắt dữ liệu từ DB để đưa vào prompt cho AI"""
    songs = db.query(models.Melody).limit(10).all()
    events = db.query(models.Event).limit(5).all()
    articles = db.query(models.Article).limit(5).all()
    villages = db.query(models.Location).filter(models.Location.type == "lang_quan_ho").limit(10).all()
    
    context = "Dữ liệu từ website Quan Họ Bắc Ninh:\n"
    context += "- Bài hát: " + ", ".join([s.name for s in songs]) + "\n"
    context += "- Sự kiện: " + ", ".join([e.title for e in events]) + "\n"
    context += "- Làng: " + ", ".join([v.name for v in villages]) + "\n"
    context += "- Tin tức: " + ", ".join([a.title for a in articles]) + "\n"
    return context

@router.post("")
async def ask_chatbot(msg: ChatMessage, db: Session = Depends(get_db)):
    text = msg.message.lower()
    
    # Nếu có API Key, dùng Gemini
    if api_key:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            context = get_context_summary(db)
            
            prompt = f"""
            Bạn là Trợ lý Quan Họ AI, một chuyên gia về văn hóa Quan họ Bắc Ninh.
            Nhiệm vụ của bạn là trả lời các câu hỏi của người dùng một cách lịch sự, thân thiện và chính xác dựa trên dữ liệu trang web.
            
            {context}
            
            Hướng dẫn trả lời:
            1. Nếu người dùng hỏi về bài hát, sự kiện hoặc làng đang có trong dữ liệu trên, hãy nhắc đến chúng và gợi ý họ xem chi tiết.
            2. Trả lời bằng Tiếng Việt, giọng điệu truyền thống nhưng gần gũi (dùng 'vâng', 'dạ', 'người ơi', 'quý khách').
            3. Trả lời ngắn gọn, súc tích (dưới 100 chữ).
            
            Câu hỏi của người dùng: {msg.message}
            """
            
            response = model.generate_content(prompt)
            return {"response": response.text}
        except Exception as e:
            print(f"CHATBOT AI ERROR: {e}")
            # Fallback to keyword logic below if AI fails

    # --- KEYWORD FALLBACK LOGIC ---
    
    # Logic cho Lịch sử và Ý nghĩa
    if any(k in text for k in ['lịch sử', 'ý nghĩa', 'nguồn gốc', 'tại sao']):
        articles = db.query(models.Article).filter(models.Article.category == "lich-su").limit(1).all()
        if articles:
            return {"response": f"Về lịch sử Quan họ: {articles[0].excerpt or 'Quan họ Bắc Ninh là loại hình dân ca phong phú bậc nhất của Việt Nam.'} Bạn có thể xem thêm tại mục Giới thiệu."}
        return {"response": "Quan họ Bắc Ninh có lịch sử lâu đời, gắn liền với văn hóa lúa nước vùng Kinh Bắc. Theo truyền thuyết, nó bắt nguồn từ những cuộc giao duyên của các làng kết chạ."}

    # Logic cho Lễ hội và Sự kiện
    if any(k in text for k in ['lễ hội', 'sự kiện', 'khi nào', 'lịch']):
        events = db.query(models.Event).filter(models.Event.status == "upcoming").limit(3).all()
        if events:
            ev_list = "\n".join([f"- {e.title} (Ngày: {e.start_date})" for e in events])
            return {"response": f"Các lễ hội và sự kiện sắp tới nè:\n{ev_list}\nBạn nhớ đăng ký tham gia nhé!"}
        return {"response": "Hiện tại chưa có lịch lễ hội cụ thể gần đây, nhưng Hội Lim thường diễn ra vào ngày 13 tháng Giêng hàng năm bạn nhé."}

    # Logic cho Đăng ký
    if any(k in text for k in ['đăng ký', 'tham gia', 'làm sao']):
        return {"response": "Để đăng ký tham gia sự kiện, bạn chỉ cần vào mục 'Sự kiện', chọn sự kiện yêu thích và nhấn nút 'Đăng ký'. Nếu bạn đã đăng nhập, tôi sẽ tự động điền thông tin cho bạn!"}

    # Logic cho Gợi ý bài hát theo tâm trạng
    mood_map = {
        "buồn": ["Người ơi người ở đừng về", "Khách đến chơi nhà", "Ngồi tựa mạn thuyền"],
        "vui": ["Trống cơm", "Lên chùa", "Hội Lim", "Mời nước mời trầu"],
        "nhớ": ["Tương phùng tương ngộ", "Hoa thơm bướm lượn"],
        "yêu": ["Gái đảm trai tài", "Đôi ta như thể con ong"]
    }
    
    for mood, songs in mood_map.items():
        if mood in text:
            song = random.choice(songs)
            return {"response": f"Nghe vẻ bạn đang thấy {mood}. Tôi gợi ý bạn nghe bài '{song}' để cảm nhận rõ hơn cái tình của người Quan họ nhé."}

    # 49 Làng Quan Họ
    if '49 làng' in text or 'danh sách làng' in text:
        villages = db.query(models.Location).filter(models.Location.type == "lang_quan_ho").limit(5).all()
        v_names = ", ".join([v.name for v in villages])
        return {"response": f"Vùng Kinh Bắc có 49 làng Quan họ gốc được công nhận. Một số làng tiêu biểu có thể kể đến như: {v_names}... Bạn có thể xem bản đồ chi tiết tại mục 'Làng Quan họ'."}

    # Mặc định
    return {"response": "Chào bạn! Tôi có thể giúp bạn tìm hiểu về 49 làng Quan họ gốc, ý nghĩa các làn điệu cổ, hoặc gợi ý bài hát theo tâm trạng của bạn. Bạn muốn bắt đầu từ đâu?"}
