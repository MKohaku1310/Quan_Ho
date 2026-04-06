import urllib.request
import os

images = {
    "unesco.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/UNESCO_logo.svg/512px-UNESCO_logo.svg.png",
    "female.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Li%E1%BB%81n_ch%E1%BB%8B_quan_h%E1%BB%8D_%28%C4%91%C3%A3_c%E1%BA%AFt%29.jpg/800px-Li%E1%BB%81n_ch%E1%BB%8B_quan_h%E1%BB%8D_%28%C4%91%C3%A3_c%E1%BA%AFt%29.jpg",
    "male.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Hat_quan_ho_1.jpg",
    "betel.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Betel_leaf_and_areca_nut.jpg/800px-Betel_leaf_and_areca_nut.jpg"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/100.0.4896.127 Safari/537.36'}

for name, url in images.items():
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            with open(name, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded {name} successfully.")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
