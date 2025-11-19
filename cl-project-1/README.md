# DOCX to TXT Converter

**Part of the Rauner Digital Archives Project**

A simple utility script to batch convert Microsoft Word documents (`.docx`) to plain text (`.txt`) format.

## Usage

1.  Ensure you have Python installed.
2.  Install the required dependency:
    ```bash
    pip install python-docx
    ```
3.  Edit the `docx_to_txt.py` script to update the input and output folder paths:
    ```python
    # Specify the folder containing your DOCX files
    docx_folder = "/path/to/your/docx/files"

    # Specify the folder where you want to save the TXT files
    txt_folder = "/path/to/output/txt/files"
    ```
4.  Run the script:
    ```bash
    python docx_to_txt.py
    ```

## Requirements

*   Python 3.x
*   `python-docx` library

