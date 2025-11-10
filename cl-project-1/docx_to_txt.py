import os
from docx import Document

def convert_docx_to_txt(docx_path, txt_path):
    doc = Document(docx_path)
    text = ""
    
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)

# Specify the folder containing your DOCX files
docx_folder = "/Users/moiz/Downloads/test"


# Specify the folder where you want to save the TXT files
txt_folder = "/Users/moiz/Downloads/test"

# Create the output folder if it doesn't exist
os.makedirs(txt_folder, exist_ok=True)

# Loop through each DOCX file in the folder
for docx_file in os.listdir(docx_folder):
    if docx_file.endswith(".docx"):
        # Create the full paths for input and output
        docx_path = os.path.join(docx_folder, docx_file)
        txt_file = os.path.splitext(docx_file)[0] + ".txt"
        txt_path = os.path.join(txt_folder, txt_file)
        
        # Convert DOCX to TXT
        convert_docx_to_txt(docx_path, txt_path)

print("Conversion complete.")