# app.py
import streamlit as st
from docx import Document
from pptx import Presentation
import PyPDF2
import io

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def create_cv(text):
    buffer = io.BytesIO()
    doc = Document()
    doc.add_heading('Curriculum Vitae', 0)
    for section in text.split('\n\n'):
        doc.add_paragraph(section.strip())
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def create_presentation(text):
    buffer = io.BytesIO()
    prs = Presentation()
    bullet_slide_layout = prs.slide_layouts[1]
    for idx, section in enumerate(text.split('\n\n')):
        slide = prs.slides.add_slide(bullet_slide_layout)
        slide.shapes.title.text = f"Section {idx+1}"
        body = slide.placeholders[1]
        body.text = ''
        for line in section.split('\n'):
            if line.strip():
                body.text += f"{line.strip()}\n"
    prs.save(buffer)
    buffer.seek(0)
    return buffer

st.title("AutoDoc: Extract & Format Generator")
uploaded_file = st.file_uploader("Upload a DOCX or PDF", type=["docx", "pdf"])
output_choice = st.radio("Choose output format", ("Curriculum Vitae (DOCX)", "Presentation (PPTX)"))

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "docx":
        text = extract_text_from_docx(uploaded_file)
    elif file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file type.")
        text = None

    if text:
        st.subheader("Extracted Text Preview:")
        st.text_area("Extracted Text", text, height=300)

        if output_choice == "Curriculum Vitae (DOCX)":
            buffer = create_cv(text)
            st.download_button("Download CV", data=buffer, file_name="generated_cv.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        
        elif output_choice == "Presentation (PPTX)":
            buffer = create_presentation(text)
            st.download_button("Download Presentation", data=buffer, file_name="generated_presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
