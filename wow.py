import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io
import webbrowser

st.set_page_config(page_title="Scanner Pro", layout="wide")
st.title("Scanner Pro")
st.markdown("Upload image → Detect + Web search links")

uploaded_file = st.file_uploader("Upload image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    items = cascade.detectMultiScale(gray, 1.1, 5, minSize=(60,60))

    if len(items) > 0:
        st.success(f"✅ Detected {len(items)} item(s)")
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        for (x, y, w, h) in items:
            draw.rectangle([x, y, x+w, y+h], outline="lime", width=5)
        st.image(annotated, caption="Detected", use_container_width=True)
    else:
        st.warning("No item detected — will still search full image.")

    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=95)
    img_bytes = buf.getvalue()

    st.download_button("📥 Download Image", img_bytes, "search_image.jpg", "image/jpeg")

    st.subheader("🔍 Search on Web Platforms")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("PimEyes (Best for People)", type="primary"):
            webbrowser.open("https://pimeyes.com/en/")
        if st.button("Yandex Images"):
            webbrowser.open("https://yandex.com/images/")

    with col2:
        if st.button("Google Reverse Search"):
            webbrowser.open("https://www.google.com/searchbyimage")
        if st.button("FaceCheck.ID"):
            webbrowser.open("https://facecheck.id/")

    st.subheader("Social Media Quick Search")
    if st.button("Instagram / Facebook Search"):
        st.info("After reverse search, try Google with: site:instagram.com [name]")
    if st.button("Twitter / X"):
        webbrowser.open("https://twitter.com/explore")
    if st.button("VK Search"):
        webbrowser.open("https://vk.com/search")

    st.info("Download the image and upload it on the sites above for best results.")
