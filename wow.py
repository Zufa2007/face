import streamlit as st
from PIL import Image
import io
import webbrowser

st.set_page_config(page_title="Web Scanner", layout="wide")
st.title("🕵️ Web Scanner Pro")
st.markdown("Upload image → Get links to search on social media & major platforms")

uploaded_file = st.file_uploader("Upload image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=95)
    st.download_button("📥 Download Image (Recommended)", buf.getvalue(), "image_for_search.jpg", "image/jpeg")

    st.subheader("🔍 Best Places to Search This Image")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Best for People / Celebrities**")
        if st.button("PimEyes", type="primary"):
            webbrowser.open("https://pimeyes.com/en/")
        if st.button("FaceCheck.ID"):
            webbrowser.open("https://facecheck.id/")

    with col2:
        st.markdown("**Best General Search**")
        if st.button("Yandex Images"):
            webbrowser.open("https://yandex.com/images/")
        if st.button("Google Reverse"):
            webbrowser.open("https://www.google.com/searchbyimage")

    st.subheader("📱 Social Media & Other Platforms")
    
    if st.button("Search on Instagram / Facebook"):
        st.info("Go to Google → search: \"site:instagram.com\" or \"site:facebook.com\" after doing reverse search")
    
    if st.button("Search on X / Twitter"):
        webbrowser.open("https://twitter.com/explore")
    
    if st.button("Search on VK (good for faces)"):
        webbrowser.open("https://vk.com/search?c%5Bphoto%5D=1")

    st.subheader("Extra Useful Links")
    st.markdown("""
    - [TinEye](https://tineye.com/) - Exact match search
    - [Bing Visual Search](https://www.bing.com/visualsearch)
    - [Social Catfish](https://socialcatfish.com/) - People search
    - [BeenVerified](https://www.beenverified.com/) - Public records
    """)

    st.info("""
    **Best Workflow:**
    1. Download the image
    2. Start with **PimEyes** or **Yandex**
    3. Then search the name you find on Instagram, Facebook, Twitter, etc.
    """)
