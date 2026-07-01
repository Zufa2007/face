import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io
import webbrowser

st.set_page_config(page_title="Image Scanner", layout="wide")
st.title("Image Scanner")
st.markdown("Upload image for analysis and web lookup")

uploaded_file = st.file_uploader("Upload image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

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

    st.subheader("Web Lookup")

    if st.button("Start Main Search", type="primary"):
        webbrowser.open("https://yandex.com/images/")
        webbrowser.open_new_tab("https://www.google.com/searchbyimage")
        st.success("Opened main search pages - upload the downloaded image there")

    if st.button("Start Additional Search"):
        webbrowser.open("https://tineye.com/")
        st.info("Use the downloaded image on the opened pages")

    st.info("Best results: Download image first, then upload on the opened sites.")
