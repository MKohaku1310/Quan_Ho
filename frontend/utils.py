import re
from typing import Optional

def get_embed_url(video_url: str) -> Optional[str]:
    """Extract YouTube video ID and return embed URL."""
    if not video_url: return None
    video_url = video_url.strip()
    
    # Regex YouTube chuẩn cho nhiều định dạng
    yt_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(yt_regex, video_url)
    
    if match:
        video_id = match.group(1)
        return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0"
    
    # Trả về nguyên vẹn nếu không khớp mẫu YouTube
    return video_url
