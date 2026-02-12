# Dartmouth Vietnam Project - Oral History Transcript Summarizer

This tool automatically generates summaries of oral history interview transcripts using AI language models. It's designed for the Dartmouth Vietnam Project but can be adapted for similar oral history collections.

## Table of Contents

- [What This Tool Does](#what-this-tool-does)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Getting API Access](#getting-api-access)
- [Configuration](#configuration)
- [Preparing Your Data](#preparing-your-data)
- [Running the Script](#running-the-script)
- [Understanding the Output](#understanding-the-output)
- [Troubleshooting](#troubleshooting)

---

## What This Tool Does

This script reads oral history interview transcripts and creates concise summaries (approximately 250 words each) using AI. The summaries:

- Focus on the interviewee's Vietnam War era experiences
- Use indirect speech (e.g., "He describes..." rather than direct biography)
- Can optionally incorporate existing bullet points/abstracts for better structure

The results are saved to a CSV file for easy review and importing into archival systems.

---

## Prerequisites

Before you begin, make sure you have:

1. **A computer** with Windows, macOS, or Linux
2. **Internet connection** for accessing the AI API
3. **API access** - You'll need either:
   - A Dartmouth Chat API key (recommended for Dartmouth affiliates), OR
   - An OpenAI API key (paid account required)

### What is Python?

Python is a programming language that this script is written in. You'll need to install it on your computer if you don't have it already.

---

## Installation Guide

Follow these steps in order:

### Step 1: Check if Python is Installed

Open your terminal or command prompt:

- **Windows**: Press `Windows + R`, type `cmd`, and press Enter
- **macOS**: Press `Cmd + Space`, type `Terminal`, and press Enter
- **Linux**: Press `Ctrl + Alt + T`

Type the following and press Enter:

```
python --version
```

or

```
python3 --version
```

If you see a version number (like `Python 3.10.0`), you're good to go!

If you see an error like "command not found," you need to install Python:

**Download Python from:** https://www.python.org/downloads/

- Download the latest version for your operating system
- Run the installer
- **Important:** On Windows, check the box that says "Add Python to PATH" during installation

### Step 2: Clone or Download This Project

**Option A: Using Git (Recommended)**

If you have git installed, open your terminal and run:

```
git clone https://github.com/YOUR_USERNAME/Rauner-Test-Script.git
cd Rauner-Test-Script
```

**Option B: Download as ZIP (No Git Required)**

1. Go to the project page on GitHub
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the downloaded folder to a location of your choice
5. Open your terminal/command prompt and navigate to that folder:
   - **Windows**: `cd path\to\Rauner-Test-Script`
   - **macOS/Linux**: `cd path/to/Rauner-Test-Script`

### Step 3: Install Required Python Packages

Once you're in the project folder, install the required packages by running:

```
pip install -r requirements.txt
```

If that doesn't work, try:

```
pip3 install -r requirements.txt
```

or

```
python -m pip install -r requirements.txt
```

This will install the necessary libraries: OpenAI SDK, LangChain, pandas, and other dependencies.

---

## Getting API Access

You need an API key to run this script. Choose one option below:

### Option 1: Dartmouth Chat API (Recommended for Dartmouth Affiliates)

1. Go to https://chat.dartmouth.edu/
2. Sign in with your Dartmouth credentials
3. Navigate to your account settings or API section
4. Generate or copy your API key

### Option 2: OpenAI API

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (you won't be able to see it again!)

---

## Configuration

### Step 1: Create Your Secrets File

The project includes a template file called `secrets.env.example`. You need to create your own version:

1. Copy `secrets.env.example` and rename it to `secrets.env`
2. Open `secrets.env` in a text editor (Notepad, TextEdit, VS Code, etc.)

**On Windows Command Prompt:**
```
copy secrets.env.example secrets.env
```

**On macOS/Linux Terminal:**
```
cp secrets.env.example secrets.env
```

### Step 2: Add Your API Key

Edit `secrets.env` and replace the placeholder text with your actual API key:

**If using Dartmouth Chat API:**
```
DARTMOUTH_CHAT_API_KEY=your_actual_api_key_here
```

**If using OpenAI API:**
```
OPENAI_API_KEY=your_actual_api_key_here
```

**Important:** Keep your `secrets.env` file private! Don't share it or commit it to GitHub.

---

## Preparing Your Data

The script expects your data to be organized in specific folders:

### Required Folder Structure

```
Rauner-Test-Script/
├── dvp_summarizer.py
├── secrets.env
├── requirements.txt
├── ConvertedTranscripts/        # REQUIRED: Put your interview transcripts here
│   ├── interview1_lastname_firstname.txt
│   ├── interview2_lastname_firstname.txt
│   └── ...
└── ConvertedAbstractsBulletPoints/  # OPTIONAL: Put bullet points/abstracts here
    ├── lastname_firstname.txt
    └── ...
```

### About the Files

- **ConvertedTranscripts**: Put your interview transcript text files here. The script will process all files in this folder.
- **ConvertedAbstractsBulletPoints** (Optional): If you have bullet points or abstracts for each interview, put them here. They should be named to match their corresponding transcripts (e.g., `lastname_firstname.txt`).

---

## Running the Script

Once everything is set up:

### Step 1: Open Your Terminal

Navigate to the project folder if you haven't already:

```
cd path/to/Rauner-Test-Script
```

### Step 2: Run the Script

```
python dvp_summarizer.py
```

or

```
python3 dvp_summarizer.py
```

### What You'll See

The script will:

1. Test your API connection
2. Load all transcripts from the `ConvertedTranscripts` folder
3. Load any bullet points from `ConvertedAbstractsBulletPoints` (if available)
4. Process each transcript and generate a summary
5. Save all results to `dvp_summaries.csv`

### Processing Time

- Each transcript typically takes 10-30 seconds to process
- If you have many transcripts, the total time will vary
- The script shows progress as it works

---

## Understanding the Output

The script creates a file called `dvp_summaries.csv` with the following columns:

| Column | Description |
|--------|-------------|
| `source` | The filename of the original transcript |
| `summary` | The AI-generated summary (~250 words) |
| `prompt` | The system prompt used (for reference) |
| `Bullet Used` | Whether bullet points were used in generating the summary |
| `LLM Model` | Which AI model was used |
| `Date` | When the summary was created |
| `Time` | The exact time of creation |

### Opening the Results

You can open `dvp_summaries.csv` in:
- Microsoft Excel
- Google Sheets
- Any spreadsheet software
- A text editor (though it will be harder to read)

---

## Troubleshooting

### Problem: "No module named 'dotenv'" (or similar errors)

**Solution:** The required packages aren't installed. Run:
```
pip install -r requirements.txt
```

### Problem: "No API key configured"

**Solution:**
1. Make sure you created a `secrets.env` file
2. Check that your API key is correctly pasted
3. Ensure there are no extra spaces or quotes around the key

### Problem: API connection fails or times out

**Solution:**
1. Check your internet connection
2. Verify your API key is valid and hasn't expired
3. Try a different model by adding a line to `secrets.env`:
   ```
   DARTMOUTH_MODEL=anthropic.claude-3-5-haiku-20241022
   ```

### Problem: Empty responses from the API

**Solution:** Some models may not work properly. Try switching to a different model in your `secrets.env`:
```
DARTMOUTH_MODEL=anthropic.claude-3-5-haiku-20241022
```

### Problem: "ConvertedTranscripts folder not found"

**Solution:** Create the folder and add your transcript files:
```
mkdir ConvertedTranscripts
```
Then copy your `.txt` files into that folder.

---

## Advanced Configuration

### Processing Only One Interviewee

To test with a single transcript, you can modify the script. Open `dvp_summarizer.py` in a text editor and look for these lines near the bottom:

```python
TARGET_INTERVIEWEE = None  # Set to e.g., "cox_robert" to process only that interviewee
```

Change `None` to the interview identifier (usually `lastname_firstname`):

```python
TARGET_INTERVIEWEE = "smith_john"  # Only processes files containing "smith_john"
```

### Disabling Bullet Points

If you don't want to use the bullet points/abstracts, change:

```python
USE_ABSTRACTS = False
```

### Changing the Output Filename

To save results to a different file:

```python
OUTPUT_FILE = "my_summaries.csv"
```

---

## Support

If you encounter issues not covered here:

1. Check the console output for specific error messages
2. Verify all files are in the correct folders
3. Ensure your API key is valid and has available credits
4. Try running with just one transcript first for testing

---

## License

This project is part of the Dartmouth Vietnam Project at Rauner Special Collections Library.
