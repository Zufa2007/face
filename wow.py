import streamlit as st
from PIL import Image
import cv2
import numpy as np
import io
import webbrowser

st.set_page_config(page_title="My PimEyes", layout="wide")
st.title("🔍 My PimEyes")
st.markdown("**My Personal Image Search Tool**")

uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Photo", use_container_width=True)

    # Detection
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    detections = cascade.detectMultiScale(gray, 1.1, 5)

    if len(detections) > 0:
        st.success(f"Found {len(detections)} target(s)")
        draw = ImageDraw.Draw(image.copy())
        for (x,y,w,h) in detections:
            draw.rectangle([x,y,x+w,y+h], outline="red", width=4)
        st.image(image, caption="Detected", use_container_width=True)

    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=95)

    st.download_button("Download Clean Image", buf.getvalue(), "photo.jpg", "image/jpeg")

    st.subheader("Search This Photo")
    if st.button("🔥 Start Search", type="primary"):
        webbrowser.open("https://pimeyes.com/en/")
        webbrowser.open_new_tab("https://yandex.com/images/")
        webbrowser.open_new_tab("https://facecheck.id/")

    st.info("1. Download the photo\n2. Upload it on the opened websites")
