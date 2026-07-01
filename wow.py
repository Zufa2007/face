import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io
import pickle
import os
from datetime import datetime

DB_FILE = "database.pkl"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "rb") as f:
        database = pickle.load(f)
else:
    database = {}

st.set_page_config(page_title="Scanner Pro", layout="wide")
st.title("Scanner Pro")

uploaded_file = st.file_uploader("Upload image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Use headless version
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    items = cascade.detectMultiScale(gray, 1.1, 5, minSize=(60,60))

    if len(items) > 0:
        st.success(f"Detected {len(items)} item(s)")
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        for (x, y, w, h) in items:
            draw.rectangle([x, y, x+w, y+h], outline="lime", width=5)
        st.image(annotated, caption="Detected", use_container_width=True)

    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=95)
    img_bytes = buf.getvalue()

    st.download_button("Download Image", img_bytes, "image.jpg", "image/jpeg")

    name_input = st.text_input("Label this as:", placeholder="Name")

    if st.button("Save to Collection", type="primary"):
        if name_input:
            database[name_input] = {"added": str(datetime.now())}
            with open(DB_FILE, "wb") as f:
                pickle.dump(database, f)
            st.success(f"Saved: {name_input}")

    if st.button("Search Collection"):
        if database:
            for name in database.keys():
                st.write(f"• {name}")
        else:
            st.write("Collection empty")
