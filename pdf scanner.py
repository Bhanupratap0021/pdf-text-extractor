import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n\n"
    
    return text

def save_to_file(text, output_path):
    """Save extracted text to a .txt file."""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    print("=== PDF Text Extractor ===")
    pdf_path = input("Enter PDF file path: ").strip('"')
    
    if not os.path.exists(pdf_path):
        print("Error: File not found!")
        return
    
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = f"{base_name}_extracted.txt"
    
    print("Extracting text...")
    text = extract_text_from_pdf(pdf_path)
    
    if text.strip():
        save_to_file(text, output_path)
        print(f"Success! Saved to: {output_path}")
        print(f"Characters extracted: {len(text)}")
    else:
        print("Warning: No text could be extracted (might be scanned/Images)")

if __name__ == "__main__":
    main()