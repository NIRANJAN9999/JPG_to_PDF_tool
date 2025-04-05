import streamlit as st
from PIL import Image
from fpdf import FPDF
import io
import tempfile

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
    # Write the PDF content to the buffer
    pdf.output(pdf_buffer, dest='S')
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



