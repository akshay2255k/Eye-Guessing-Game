from better_bing_image_downloader import downloader
import os
import cv2
import time

# ================= CONFIG =================
actors = [
    "anikha surendran",
    # "Kamal Haasan",
    # "Vijay",
]

SAVE_DIR = "Tollywood_faces"
IMAGES_PER_PERSON = 40
MIN_FACE_SIZE = 100          # face കുറഞ്ഞത് 100x100 pixel വേണം
# ==========================================

os.makedirs(SAVE_DIR, exist_ok=True)

def has_clear_face(image_path):
    """Face detection - face ഇല്ലാത്ത images remove ചെയ്യും"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE))
        return len(faces) >= 1
    except:
        return False


for person in actors:
    print(f"\n{'='*60}")
    print(f"Downloading accurate faces → {person}")
    print(f"{'='*60}")

    folder = os.path.join(SAVE_DIR, person.replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)

    # Multiple good queries
    queries = [
        f"{person} face closeup",
        f"{person} portrait",
        f"{person} actor face",
        f"{person} nude",
    ]

    for query in queries:
        print(f"\n→ Query: {query}")

        try:
            # DuckDuckGo often better for Indian celebrities
            downloader(
                query=query,
                limit=15,
                output_dir=folder,
                engine="duckduckgo",      # or "bing"
                force_replace=False,
                timeout=30,
                verbose=True,
                adult_filter_off=True,
            )
        except Exception as e:
            print(f"  Error: {e}")

        time.sleep(1)

    # ---- Face Filter + Rename ----
    print("\nFiltering faces...")
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    kept = 0
    for file in files:
        path = os.path.join(folder, file)
        
        if not has_clear_face(path):
            os.remove(path)
            continue
        
        ext = os.path.splitext(file)[1].lower()
        new_name = f"Image_ ({kept+1}){ext}"
        new_path = os.path.join(folder, new_name)
        
        if path != new_path:
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(path, new_path)
        
        kept += 1

    print(f"\n✔ Final: {kept} clear face images saved in → {folder}")

print("\n🎉 Done! Now check the folder.")