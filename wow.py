import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io
import base64
import webbrowser
import pickle
import os
from datetime import datetime

# Database file
DB_FILE = "eagleeye_database.pkl"

# Load or create database
if os.path.exists(DB_FILE):
    with open(DB_FILE, "rb") as f:
        database = pickle.load(f)
else:
    database = {}  # name -> face_encoding

st.set_page_config(page_title="🦅 EagleEye Pro", layout="wide")
st.title("🦅 EagleEye Pro - Your Private PimEyes")
st.markdown("**Build your own face database + reverse search**")

# Sidebar for database management
with st.sidebar:
    st.header("📁 Your Database")
    st.write(f"Total faces stored: **{len(database)}**")
    
    if st.button("Clear Database"):
        if st.checkbox("Are you sure?"):
            database = {}
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
            st.success("Database cleared!")

# Main uploader
uploaded_file = st.file_uploader("Upload a photo to scan...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Photo", use_container_width=True)

    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    rgb_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    # Face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY), 1.1, 5, minSize=(60,60))

    if len(faces) == 0:
        st.error("No face detected.")
    else:
        st.success(f"✅ Detected {len(faces)} face(s)")

        # For simplicity, use first face
        (x, y, w, h) = faces[0]
        face_crop = rgb_img[y:y+h, x:x+w]

        # Draw
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        draw.rectangle([x, y, x+w, y+h], outline="lime", width=5)
        st.image(annotated, caption="Face Used for Search", use_container_width=True)

        # Save for download
        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=95)
        img_bytes = buf.getvalue()

        st.download_button("📥 Download Image", img_bytes, "scan.jpg", "image/jpeg")

        # === Search in Local Database ===
        st.subheader("🔍 Search in Your Database")
        name_input = st.text_input("Add this face to database as:", placeholder="John Doe")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add to Database", type="primary"):
                if name_input:
                    # Simple placeholder encoding (in real version we'd use deep encoding)
                    database[name_input] = {"crop": face_crop, "added": str(datetime.now())}
                    with open(DB_FILE, "wb") as f:
                        pickle.dump(database, f)
                    st.success(f"✅ {name_input} added to database!")
                else:
                    st.warning("Enter a name first.")

        with col2:
            if st.button("Search Database"):
                if database:
                    st.info("Matching against database...")
                    for name, data in database.items():
                        st.write(f"• **{name}** (added {data['added']})")
                    st.success("Matches shown above (full similarity matching coming next)")
                else:
                    st.warning("Database is empty. Add some faces first.")

        # Quick external search
        st.subheader("🌐 External Reverse Search")
        if st.button("Open PimEyes + Yandex"):
            webbrowser.open("https://pimeyes.com/en/")
            webbrowser.open_new_tab("https://yandex.com/images/")

st.caption("Your database is saved locally on your computer. Private & Free.")
