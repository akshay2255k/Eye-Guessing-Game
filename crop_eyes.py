import cv2
import os
import glob
import urllib.request
import numpy as np

print("📁 Snooping around in your directory:", os.getcwd())

# Secret stash links for our AI models
prototxt_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"
caffemodel_url = "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"

prototxt_path = "deploy.prototxt"
caffemodel_path = "res10_300x300_ssd_iter_140000.caffemodel"

# Steal... I mean, legally download the files if they are missing
if not os.path.exists(prototxt_path):
    print("⏳ Hold your horses... Fetching the AI Prototxt file...")
    urllib.request.urlretrieve(prototxt_url, prototxt_path)

if not os.path.exists(caffemodel_path):
    print("⏳ Grab a coffee... Downloading the heavy Caffe model...")
    urllib.request.urlretrieve(caffemodel_url, caffemodel_path)

print("✅ AI models are locked and loaded! Booting up the matrix...")
# Ditching MediaPipe for OpenCV's badass Deep Learning model
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
print("🚀 Engine started! Let's hunt some faces...")

images = glob.glob("mollywood_faces/*/*.jpg")
if not images:
    images = glob.glob("mollywood_faces/*.jpg")

print(f"🔍 Target acquired: {len(images)} photos found!")

if not images:
    print("❌ Bro, there are NO photos here! Are you testing me?")
else:
    success_count = 0
    for i, img_path in enumerate(images):
        if "_eyes.jpg" in img_path: 
            continue
            
        img = cv2.imread(img_path)
        if img is None:
            continue
        
        h, w = img.shape[:2]
        
        # Transforming the image into a 'blob' (AI loves blobs)
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        
        # Picking the most confident face from the crowd
        for j in range(0, detections.shape[2]):
            confidence = detections[0, 0, j, 2]
            
            # Only proceed if we are at least 50% sure it's not a potato
            if confidence > 0.5:
                box = detections[0, 0, j, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                
                # Keeping the box inside the photo (no out-of-bounds magic)
                startX, startY = max(0, startX), max(0, startY)
                endX, endY = min(w, endX), min(h, endY)
                
                face_h = endY - startY
                face_w = endX - startX
                
                if face_h > 0 and face_w > 0:
                    # Time for some virtual eye surgery (calculating coordinates)
                    eye_y = startY + int(face_h * 0.20)
                    eye_h = int(face_h * 0.35)
                    
                    eyes_cropped = img[eye_y : eye_y + eye_h, startX : startX + face_w]
                    
                    if eyes_cropped.size != 0:
                        new_eye_path = img_path.replace(".jpg", "_eyes.jpg")
                        cv2.imwrite(new_eye_path, eyes_cropped)
                        print(f"✅ [{success_count+1}] Snip snip! Eye extracted: {os.path.basename(new_eye_path)}")
                        success_count += 1
                    
                break # One face per photo is enough, we ain't greedy
                
    print(f"🔥 BOOM! Mission accomplished! Extracted eyes from {success_count} photos, boss!")