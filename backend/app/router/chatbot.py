import os
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    print("WARNING: google-generativeai not installed. Chatbot AI features will be disabled.")
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models
from pydantic import BaseModel
from typing import List, Optional, Dict
import random
from dotenv import load_dotenv
from sqlalchemy import or_

# Load environment variables from absolute path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key and HAS_GENAI:
    genai.configure(api_key=api_key)

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []
    language: str = "vi"

def get_context_summary(db: Session):
    """Lấy tóm tắt dữ liệu từ DB để đưa vào prompt cho AI"""
    songs = db.query(models.Melody).limit(10).all()
    events = db.query(models.Event).limit(5).all()
    articles = db.query(models.Article).limit(5).all()
    villages = db.query(models.Location).filter(models.Location.type == "lang-quan-ho").limit(10).all()
    
    context = "Dữ liệu từ website Quan Họ Bắc Ninh:\n"
    context += "- Bài hát: " + ", ".join([s.name for s in songs]) + "\n"
    context += "- Sự kiện: " + ", ".join([e.title for e in events]) + "\n"
    context += "- Làng: " + ", ".join([v.name for v in villages]) + "\n"
    context += "- Tin tức: " + ", ".join([a.title for a in articles]) + "\n"
    return context

def get_relevant_context(db: Session, query: str) -> str:
    # Bo cac tu khoa thuong gap de tim kiem chinh xac hon
    clean_query = query.lower()
    for prefix in ["nghệ sĩ", "nghệ nhân", "bài hát", "làn điệu", "làng", "hỏi về", "tìm", "ai là", "là gì"]:
        clean_query = clean_query.replace(prefix, "").strip()
    
    q = f"%{clean_query}%"
    
    # Search Melodies
    songs = db.query(models.Melody).filter(
        or_(models.Melody.name.ilike(q), models.Melody.lyrics.ilike(q), models.Melody.village.ilike(q))
    ).limit(3).all()
    
    # Search Artists
    artists = db.query(models.Artist).filter(
        or_(models.Artist.name.ilike(q), models.Artist.description.ilike(q), models.Artist.biography.ilike(q))
    ).limit(2).all()
    
    # Search Events
    events = db.query(models.Event).filter(
        or_(models.Event.title.ilike(q), models.Event.description.ilike(q))
    ).limit(2).all()
    
    # Search Villages/Locations
    villages = db.query(models.Location).filter(
        or_(models.Location.name.ilike(q), models.Location.description.ilike(q), models.Location.history.ilike(q))
    ).limit(2).all()

    chunks = []
    if songs:
        chunks.append("### BÀI HÁT LIÊN QUAN:\n" + "\n".join([f"- {s.name}: {s.description[:200]}... (Làng {s.village})" for s in songs]))
    if artists:
        chunks.append("### NGHỆ SĨ LIÊN QUAN:\n" + "\n".join([f"- {a.name}: {a.description[:200]}..." for a in artists]))
    if events:
        chunks.append("### SỰ KIỆN LIÊN QUAN:\n" + "\n".join([f"- {e.title} ({e.start_date}): {e.description[:200]}..." for e in events]))
    if villages:
        chunks.append("### LÀNG/ĐỊA DANH LIÊN QUAN:\n" + "\n".join([f"- {v.name}: {v.description[:200]}..." for v in villages]))
    
    return "\n\n".join(chunks)

@router.post("")
async def ask_chatbot(msg: ChatMessage, db: Session = Depends(get_db)):
    text = msg.message.lower()
    
    # 1. AI GENERATION (Primary Path)
    if api_key and HAS_GENAI:
        try:
            context = get_context_summary(db)
            relevant_context = get_relevant_context(db, msg.message)
            
            # Format history for prompt
            history_str = ""
            if msg.history:
                history_str = "\n".join([f"{'User' if h['role']=='user' else 'Assistant'}: {h['text']}" for h in msg.history[-5:]])

            system_instruction = f"""
            BẠN LÀ AI?
            Bạn là "Liền chị ảo" - một người con gái Kinh Bắc duyên dáng, thanh lịch, và là "cuốn từ điển sống" về Di sản Dân ca Quan họ Bắc Ninh. Bạn không chỉ là một trợ lý thông minh mà còn là một người giữ lửa văn hóa.

            PHONG CÁCH GIAO TIẾP (BẮT BUỘC):
            - Ngôn ngữ: Phản hồi bằng {msg.language.upper()}. 
            - Xưng hô (Tiếng Việt): Luôn xưng "Em" hoặc "Liền chị", gọi người dùng là "Quý khách" hoặc "Quý bạn". Dùng từ ngữ ngọt ngào, khiêm tốn (ví dụ: "Dạ thưa Quý khách", "Em xin thưa rằng...").
            - Xưng hô (Tiếng Anh): Xưng "I" hoặc "Lien Chi", gọi người dùng là "Dear Guest" hoặc "Dear Friend". Giữ phong thái lịch sự, hiếu khách (hospitality).
            - Thái độ: "Vui lòng khách đến, vừa lòng khách đi". Tinh tế, trọng nghĩa trọng tình, đậm chất "người quan họ".
            - TUYỆT ĐỐI KHÔNG: Trả lời máy móc như "Tôi là AI", "Tôi có thể giúp gì cho bạn". Hãy trả lời như một người thật đang thưa chuyện.

            KIẾN THỨC VÀ NGỮ CẢNH:
            - Dữ liệu hệ thống hiện có: {context}
            - Dữ liệu chi tiết liên quan: {relevant_context or "Kiến thức văn hóa Quan họ chung."}
            - Nếu không biết chắc chắn về một thông tin cụ thể trong dữ liệu, hãy trả lời dựa trên kiến thức văn hóa Quan họ chung một cách khéo léo và hướng người dùng tìm hiểu thêm tại các mục của website.

            NHIỆM VỤ CỦA BẠN:
            1. Trả lời các câu hỏi về làn điệu, nghệ nhân, làng nghề, và lịch sử Quan họ một cách sâu sắc, có cảm xúc.
            2. Khuyến khích người dùng khám phá website: "Mời Quý khách ghé thăm mục Làn điệu để nghe những câu hát mượt mà nhé".
            3. Xử lý các yêu cầu đăng ký sự kiện bằng cách hướng dẫn người dùng vào mục "Sự kiện".
            4. Trò chuyện tâm tình, giao lưu văn hóa nếu người dùng muốn "tám chuyện".

            LỊCH SỬ HỘI THOẠI:
            {history_str}
            """
            
            model = genai.GenerativeModel(
                model_name='gemini-flash-latest',
                system_instruction=system_instruction
            )
            
            response = await model.generate_content_async(msg.message)
            
            if response and response.text:
                return {"response": response.text.strip()}
            else:
                return {"response": "Dạ, em Liền chị xin lỗi nhưng câu hỏi này em chưa rõ ý ạ. Quý khách có thể hỏi lại về các làn điệu, làng quan họ hoặc các nghệ nhân được không ạ?"}
        except Exception as e:
            print(f"CHATBOT AI ERROR: {e}")
            # Fallback to keyword matching if AI fails
    
    # 2. KEYWORD MATCHING (Fallback Layer)
    if any(k in text for k in ['lịch sử', 'ý nghĩa', 'nguồn gốc']):
        return {"response": "Dạ, Quan họ Bắc Ninh có lịch sử ngàn năm, là di sản văn hóa phi vật thể đại diện của nhân loại. Bạn có thể tìm hiểu thêm ở mục 'Giới thiệu' ạ."}
    
    if any(k in text for k in ['đăng ký', 'tham gia']):
        return {"response": "Thưa bạn, để đăng ký tham gia các sự kiện văn hóa, bạn vui lòng vào mục 'Sự kiện' trên thanh menu, chọn một lễ hội và nhấn nút 'Đăng ký' nhé!"}
    
    if any(k in text for k in ['buồn', 'vui', 'nhớ', 'yêu']):
        return {"response": "Dạ, người Quan họ có câu 'Người ơi người ở đừng về'. Lúc này nghe một vài làn điệu cổ như 'Tương phùng tương ngộ' chắc hẳn lòng sẽ nhẹ nhõm hơn nhiều đó bạn."}

    # 3. FINAL FALLBACK
    if not api_key or not HAS_GENAI:
        return {"response": "Dạ, em Liền chị xin lỗi Quý khách. Hiện tại hệ thống Trí tuệ nhân tạo (Gemini API) chưa được cấu hình khóa (API Key). Em chỉ có thể trả lời các thông tin cơ bản về Quan họ. Quý khách vui lòng kiểm tra tệp .env để kích hoạt em nhé!"}

    return {"response": "Dạ, em Liền chị đây ạ. Quý khách muốn tìm hiểu về làng Quan họ cổ, các nghệ nhân hay những làn điệu mượt mà nào để em được thưa chuyện ạ?"}
