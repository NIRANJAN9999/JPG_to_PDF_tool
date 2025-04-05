import streamlit as st
from PIL import Image
from fpdf import FPDF
import io
import tempfile

# Custom CSS for styling
st.markdown("""
<style>
body {
    color: #fff;
    background-color: #333;
    font-family: 'Arial', sans-serif;
}

.stApp {
    background-color: #2c3e50;
}

h1 {
    color: #ecf0f1;
    text-align: center;
    font-size: 2.5em;
    margin-bottom: 20px;
}

.stFileUploader {
    width: 100%;
    padding: 10px;
    background-color: #34495e;
    border-radius: 5px;
    border: 2px dashed #ecf0f1;
    color: #ecf0f1;
    text-align: center;
}

.stFileUploader::before {
    content: "Drag & Drop or Click to Upload";
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
}

.stButton > button {
    width: 100%;
    padding: 10px;
    color: #fff;
    background-color: #e74c3c;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s;
}

.stButton > button:hover {
    background-color: #c0392b;
}

.stDownloadButton > button {
    width: 100%;
    padding: 10px;
    color: #fff;
    background-color: #27ae60;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s;
}

.stDownloadButton > button:hover {
    background-color: #219a52;
}

.stMarkdown {
    margin-top: 20px;
    text-align: center;
    font-size: 1.2em;
}
</style>
""", unsafe_allow_html=True)

def convert_image_to_pdf(image):
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()

    # Convert the image to RGB if it's not
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Use a temporary file to save the image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        image.save(temp_file, format='JPEG')
        temp_file_path = temp_file.name

    # Add the image to the PDF using the file path
    pdf.image(temp_file_path, x=10, y=10, w=190)

    # Save the PDF to a bytes buffer
    pdf_buffer = io.BytesIO()
    # Get the PDF content as a string and encode it to bytes
    pdf_content = pdf.output(dest='S')
    pdf_buffer.write(pdf_content.encode('latin-1'))
    pdf_buffer.seek(0)

    return pdf_buffer

def main():
    st.title("JPEG/JPG to PDF Converter")

    uploaded_file = st.file_uploader("Choose a JPEG or JPG file", type=["jpeg", "jpg"])

    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)

        # Convert the image to PDF
        pdf_buffer = convert_image_to_pdf(image)

        # Provide a download link for the PDF
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="converted_image.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
