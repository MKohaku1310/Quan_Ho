import urllib.request
import os

images = {
    "unesco.svg": "https://upload.wikimedia.org/wikipedia/commons/1/18/UNESCO_logo.svg",
    "female.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Hat_quan_ho_1.jpg", 
    "male.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/87/Hat_quan_ho.jpg",
}

out_dir = r"d:\Quan_Ho\frontend\public\img"
os.makedirs(out_dir, exist_ok=True)

headers = {'User-Agent': 'QuanHoApp/1.0 (contact@quanho.vn) bot'}

for name, url in images.items():
    filepath = os.path.join(out_dir, name)
    req = urllib.request.Request(url, headers=headers)
    print(f"Downloading {name}...")
    try:
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"Success: {name}")
    except Exception as e:
        print(f"Error: {name} - {e}")
