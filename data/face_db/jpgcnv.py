import os
from PIL import Image

db_path = "face_db"
for filename in os.listdir(db_path):
    if filename.endswith(".webp"):
        img = Image.open(os.path.join(db_path, filename)).convert("RGB")
        img.save(os.path.join(db_path, filename.replace(".webp", ".jpg")), "JPEG")
        # Optional: 
        os.remove(os.path.join(db_path, filename)) # Remove old webp