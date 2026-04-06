import urllib.request
import os

images = {
    "female_costume.jpg": "https://images.weserv.nl/?url=upload.wikimedia.org/wikipedia/commons/c/cf/Li%E1%BB%81n_ch%E1%BB%8B_quan_h%E1%BB%8D_%28%C4%91%C3%A3_c%E1%BA%AFt%29.jpg",
    "male_costume.jpg": "https://images.weserv.nl/?url=upload.wikimedia.org/wikipedia/commons/e/e0/Hat_quan_ho_1.jpg",
    "betel.jpg": "https://images.weserv.nl/?url=upload.wikimedia.org/wikipedia/commons/2/23/Betel_leaf_and_areca_nut.jpg"
}

out_dir = r"d:\Quan_Ho\frontend\public\img"
os.makedirs(out_dir, exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0'}

for name, url in images.items():
    filepath = os.path.join(out_dir, name)
    req = urllib.request.Request(url, headers=headers)
    print(f"Downloading {name} via proxy...")
    try:
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"Success: {name}")
    except Exception as e:
        print(f"Error: {name} - {e}")
