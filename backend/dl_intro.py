import os
import requests

out_dir = r"d:\Quan_Ho\frontend\public\img"
os.makedirs(out_dir, exist_ok=True)

images = [
    ("female.jpg", "https://vanchuongphuongnam.vn/wp-content/uploads/2019/04/l-3.jpg"),
    ("male.jpg", "https://media.baodantoc.vn/baodantoc/image/files/hoangmai/2022/07/21/ao-dai-2009.jpg"),
    ("betel.jpg", "https://vov-media.vov.vn/sites/default/files/styles/large/public/2021-02/trau_tem_canh_phuong_9.jpg"),
    ("unesco.svg", "https://www.unesco.org/themes/custom/unesco_ui/logo.svg"),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36'}

for filename, url in images:
    filepath = os.path.join(out_dir, filename)
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("All intro images downloaded successfully.")
