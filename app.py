import streamlit as st
import qrcode 
import json
from streamlit_lottie import st_lottie
import io
from PIL import Image

st.set_page_config(page_title='QR Code Generator',page_icon='📱')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
	content:''; 
	visibility: visible ;
}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# SIDEBAR
st.sidebar.header('Customize QR Code')
back_color = st.sidebar.color_picker('Pick Background Color', '#ffffff')
# st.sidebar.write('The current color is', back_color)
fill_color = st.sidebar.color_picker('Pick Fill Color', '#000000')
st.sidebar.warning('Attention! Keep a high contrast between the colors because the code can be misread by the camera.')
box_size = st.sidebar.slider('The size of the QR code', 0, 100, 20)
border = st.sidebar.slider('Border of the QR code', 0, 20, 2)



def load_lottiefile(filepath: str):
        with open(filepath, "r") as f :
            return json.load(f)

lottie_coding = load_lottiefile("qrcode.json")

col1, col2 = st.columns(2)
with col1:
     st.write("# QR CODE GENERATOR")
with col2:
      st_lottie(
        lottie_coding,
        speed= 1,
        reverse=False,
        loop=True,
        height=350,
        width= 350,
        key=None
    )

def gen_qr_code(textQR, fill_color=fill_color, back_color=back_color, box_size=box_size, border=border):
    """Generete image QR Code"""
    qr = qrcode.QRCode( version=1, 
                error_correction=qrcode.ERROR_CORRECT_L,
                box_size=box_size,
                border=border )
    qr.add_data(textQR)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img


st.write("---")
st.write("### Enter the web address, text, phone etc... that you want to encode into a QR code")
form = st.form("my_form")
textQR=form.text_input("Your text:", placeholder="https://100pa.com")
submit=form.form_submit_button("Generate QR code")

if submit:
    if textQR=="":
        img = gen_qr_code("https://100pa.com")
        st.write(f"Your QR from https://100pa.com:")
        # Convert PIL image object to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
    else:
        img = gen_qr_code(textQR)
        st.write(f"Your QR from {textQR}:")
        # Convert PIL image object to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")

    # Display image in Streamlit
    qr_image = img_bytes.getvalue()
    st.image(qr_image)
    st.download_button(label="Download your codeQR.png",
                        data=qr_image,
                        file_name='codeQR.png',
                        mime="image/png",
                    )




# FOOTER
st.write("")
st.write("")
st.markdown("Made with ❤️ [100pa.com](https://100pa.com)")