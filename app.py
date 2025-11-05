import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("Background Remover")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.button('Remove Background'):
        with st.spinner('Removing background...'):
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Remove background
            output = remove(img_byte_arr)

            # Convert back to PIL Image
            output_image = Image.open(io.BytesIO(output))

            st.image(output_image, caption='Image with Background Removed', use_column_width=True)

            # Provide download button
            buf = io.BytesIO()
            output_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Image",
                data=byte_im,
                file_name="background_removed.png",
                mime="image/png"
            )