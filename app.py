import streamlit as st
import io
from PIL import Image

# Lazy import to avoid issues during script validation
@st.cache_resource
def get_rembg():
    try:
        from rembg import remove
        return remove
    except Exception as e:
        st.error(f"Failed to load background removal library: {e}")
        return None

st.title("Background Remover")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button('Remove Background'):
            remove_func = get_rembg()
            if remove_func is None:
                st.error("Background removal is not available.")
                return

            with st.spinner('Removing background...'):
                try:
                    # Convert to bytes
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()

                    # Remove background
                    output = remove_func(img_byte_arr)

                    # Convert back to PIL Image
                    output_image = Image.open(io.BytesIO(output))

                    st.success("Background removed successfully!")
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
                except Exception as e:
                    st.error(f"Error removing background: {str(e)}")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")