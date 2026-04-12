from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatMessage(BaseModel):
    message: str

@router.post("")
async def ask_chatbot(msg: ChatMessage, db: Session = Depends(get_db)):
    text = msg.message.lower()
    
    # Logic for History & Meaning
    if any(k in text for k in ['lịch sử', 'ý nghĩa', 'nguồn gốc', 'tại sao']):
        articles = db.query(models.Article).filter(models.Article.category == "lich-su").limit(1).all()
        if articles:
            return {"response": f"Về lịch sử Quan họ: {articles[0].excerpt or 'Quan họ Bắc Ninh là loại hình dân ca phong phú bậc nhất của Việt Nam.'} Bạn có thể xem thêm tại mục Giới thiệu."}
        return {"response": "Quan họ Bắc Ninh có lịch sử lâu đời, gắn liền với văn hóa lúa nước vùng Kinh Bắc. Theo truyền thuyết, nó bắt nguồn từ những cuộc giao duyên của các làng kết chạ."}

    # Logic for Festivals & Events
    if any(k in text for k in ['lễ hội', 'sự kiện', 'khi nào', 'lịch']):
        events = db.query(models.Event).filter(models.Event.status == "upcoming").limit(3).all()
        if events:
            ev_list = "\n".join([f"- {e.title} (Ngày: {e.start_date})" for e in events])
            return {"response": f"Các lễ hội và sự kiện sắp tới nè:\n{ev_list}\nBạn nhớ đăng ký tham gia nhé!"}
        return {"response": "Hiện tại chưa có lịch lễ hội cụ thể gần đây, nhưng Hội Lim thường diễn ra vào ngày 13 tháng Giêng hàng năm bạn nhé."}

    # Logic for Registration
    if any(k in text for k in ['đăng ký', 'tham gia', 'làm sao']):
        return {"response": "Để đăng ký tham gia sự kiện, bạn chỉ cần vào mục 'Sự kiện', chọn sự kiện yêu thích và nhấn nút 'Đăng ký'. Nếu bạn đã đăng nhập, tôi sẽ tự động điền thông tin cho bạn!"}

    # Logic for Mood-based Song Suggestions
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
        villages = db.query(models.Location).filter(models.Location.type == "lang-quan-ho").limit(5).all()
        v_names = ", ".join([v.name for v in villages])
        return {"response": f"Vùng Kinh Bắc có 49 làng Quan họ gốc được công nhận. Một số làng tiêu biểu có thể kể đến như: {v_names}... Bạn có thể xem bản đồ chi tiết tại mục 'Làng Quan họ'."}

    # Default
    return {"response": "Chào bạn! Tôi có thể giúp bạn tìm hiểu về 49 làng Quan họ gốc, ý nghĩa các làn điệu cổ, hoặc gợi ý bài hát theo tâm trạng của bạn. Bạn muốn bắt đầu từ đâu?"}
