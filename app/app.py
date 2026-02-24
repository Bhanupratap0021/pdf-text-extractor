import streamlit as st
import PyPDF2
import pdfplumber
import io

# Page Config
st.set_page_config(
    page_title="PDF Text Extractor",
    page_icon="📄",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📄 PDF Text Extractor")
st.markdown("Upload a PDF and extract text instantly!")

# File Upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Options
col1, col2 = st.columns(2)
with col1:
    method = st.radio("Extraction Method", ["pdfplumber (Recommended)", "PyPDF2"])
with col2:
    page_range = st.text_input("Page Range (e.g., 1-3)", placeholder="All pages")

def extract_with_pypdf2(pdf_file, page_range=None):
    """Extract text using PyPDF2"""
    text_parts = []
    reader = PyPDF2.PdfReader(pdf_file)
    total_pages = len(reader.pages)
    
    # Determine which pages to extract
    pages_to_extract = parse_page_range(page_range, total_pages)
    
    for page_num in pages_to_extract:
        if page_num <= len(reader.pages):
            page = reader.pages[page_num - 1]  # 0-indexed
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    
    return "".join(text_parts)

def extract_with_pdfplumber(pdf_file, page_range=None):
    """Extract text using pdfplumber"""
    text_parts = []
    
    # Reset file pointer
    pdf_file.seek(0)
    
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        pages_to_extract = parse_page_range(page_range, total_pages)
        
        for page_num in pages_to_extract:
            if page_num <= total_pages:
                page = pdf.pages[page_num - 1]  # 0-indexed
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    
    return "".join(text_parts)

def parse_page_range(page_range, total_pages):
    """Parse page range string like '1-3' or '1,3,5'"""
    if not page_range:
        return list(range(1, total_pages + 1))
    
    pages = set()
    try:
        # Handle comma-separated and range formats
        parts = page_range.replace(',', ' ').split()
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
    except ValueError:
        return list(range(1, total_pages + 1))
    
    # Filter valid pages
    return [p for p in sorted(pages) if 1 <= p <= total_pages]

# Process
if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    
    if st.button("Extract Text"):
        with st.spinner("Extracting..."):
            try:
                # Choose method
                if "pdfplumber" in method:
                    text = extract_with_pdfplumber(uploaded_file, page_range)
                else:
                    text = extract_with_pypdf2(uploaded_file, page_range)
                
                if text.strip():
                    # Show preview
                    st.markdown("### 📝 Extracted Text")
                    st.text_area("Text Content", text, height=300)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download as TXT",
                        data=text,
                        file_name=f"{uploaded_file.name}_extracted.txt",
                        mime="text/plain"
                    )
                    
                    # Stats
                    st.markdown("### 📊 Stats")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Characters", len(text))
                    col2.metric("Words", len(text.split()))
                    col3.metric("Pages", len(text.split("\n\n")))
                    
                else:
                    st.error("No text found! This might be a scanned PDF. Try OCR version.")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ using Python & Streamlit*")