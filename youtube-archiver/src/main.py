# Import necessary modules
import os
import platform
from googleapiclient.discovery import build  # Google API client to interact with YouTube API
import pandas as pd  # For handling CSV exports
import re  # For regular expressions, extracting video IDs
from reportlab.lib.pagesizes import letter  # For setting PDF page size
from reportlab.pdfgen import canvas  # For generating PDFs
from reportlab.lib.styles import getSampleStyleSheet  # For PDF styling
from reportlab.lib.utils import simpleSplit  # For text wrapping in PDFs
from selenium import webdriver  # For browser automation (used to capture screenshots)
from selenium.webdriver.chrome.service import Service as ChromeService  # Manage Chrome WebDriver service
from selenium.webdriver.chrome.options import Options  # Manage Chrome options
from selenium.common.exceptions import NoSuchElementException  # For exception handling in Selenium
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manage ChromeDriver downloads
from selenium.webdriver.common.by import By  # To locate elements by HTML attributes
import time  # For adding delays during page load
from selenium.webdriver.support.ui import WebDriverWait  # For waiting for elements in Selenium
from selenium.webdriver.support import expected_conditions as EC  # Conditions for Selenium waits
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # Exception handling
import logging  # For logging events during execution

# YouTube API key (you should not hard-code API keys in production environments, consider environment variables)
api_key = 'Insert API Key Here'


# Raise an error if no API key is provided
if not api_key:
    raise ValueError("API key not found. Make sure the YOUTUBE_API_KEY environment variable is set.")

# Initialize YouTube API client using the provided key
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to extract channel and video IDs from a YouTube video URL
def get_channel_and_video_id_from_url(youtube, url):
    if 'youtube.com/watch' in url:
        video_id = re.search(r"v=([^&]+)", url).group(1)  # Extract video ID
        request = youtube.videos().list(part="snippet", id=video_id)  # Fetch video details
        response = request.execute()
        channel_id = response['items'][0]['snippet']['channelId']  # Extract channel ID from the response
        return channel_id, video_id
    else:
        raise ValueError("Invalid YouTube video URL")

# Function to retrieve channel details
def get_channel_details(youtube, channel_id):
    request = youtube.channels().list(part="snippet,contentDetails,statistics", id=channel_id)
    response = request.execute()
    return response

# Function to retrieve video details
def get_video_details(youtube, video_id):
    request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
    response = request.execute()
    return response

# Function to get video comments (up to 100 comments, with pagination support)
def get_video_comments(youtube, video_id):
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100)
    response = request.execute()

    # Loop through all comments until pagination ends
    while request is not None:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'likeCount': comment['likeCount'],
                'publishedAt': comment['publishedAt']
            })
        request = youtube.commentThreads().list_next(request, response)
        if request:
            response = request.execute()
        else:
            break
    return comments

# Initialize logging for event tracking
logging.basicConfig(level=logging.INFO)

# Function to close pop-ups during webpage interaction via Selenium
def close_popup(driver):
    # List of potential CSS selectors for closing pop-ups
    potential_selectors = [
        'button[aria-label="Close"]',  # Example selector for close buttons
        'button[aria-label="Dismiss"]',
        '#dismiss-button',  # Example ID selector
        '.ytp-ad-overlay-close-button',  # YouTube ad close button
        '.ytp-ad-skip-button'  # YouTube ad skip button
    ]

    # Try each selector to find and click close buttons
    for selector in potential_selectors:
        try:
            logging.info(f"Trying to close pop-up with selector: {selector}")
            wait = WebDriverWait(driver, 10)
            close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            close_button.click()
            logging.info("Pop-up closed successfully.")
            return
        except (NoSuchElementException, TimeoutException):
            logging.info(f"No pop-up found or not clickable for selector: {selector}")
            continue

    logging.info("No pop-up was closed.")

# Function to capture a screenshot of a YouTube video webpage
def capture_screenshot(video_url, output_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,720")  # Set window size for capturing screenshot

    # Set up Chrome WebDriver with WebDriver Manager
    chrome_service = ChromeService(ChromeDriverManager().install())

    # Launch Chrome WebDriver
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get(video_url)  # Navigate to the video URL
    time.sleep(5)  # Wait for the page to fully load

    # Close any potential pop-ups
    close_popup(driver)

    # Save the screenshot
    driver.save_screenshot(output_path)
    driver.quit()

# Function to generate a PDF report containing YouTube video details, comments, and screenshots
def generate_pdf(channel_info, video_info, comments, screenshot_path, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin = 72
    y_position = height - margin

    # Helper function to handle wrapped text drawing in the PDF
    def draw_wrapped_text(canvas, text, x, y, width, leading=14):
        lines = simpleSplit(text, 'Helvetica', 12, width)
        for line in lines:
            if y < margin:
                canvas.showPage()
                y = height - margin
            canvas.drawString(x, y, line)
            y -= leading
        return y

    # Add channel info to PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y_position, "YouTube Channel Information")
    c.setFont("Helvetica", 12)
    y_position -= 28

    # Loop through channel details and add to PDF
    for key, value in channel_info.items():
        y_position = draw_wrapped_text(c, f"{key.capitalize()}: {value}", margin, y_position, width - 2 * margin)
        y_position -= 10 
        if y_position < margin:
            c.showPage()
            y_position = height - margin

    # Add video information to PDF
    c.setFont("Helvetica-Bold", 16)
    y_position -= 20
    c.drawString(margin, y_position, "Video Information")
    c.setFont("Helvetica", 12)
    y_position -= 28

    # Insert the screenshot into the PDF
    if y_position - 290 < margin:
        c.showPage()
        y_position = height - margin
    c.drawImage(screenshot_path, margin, y_position - 270, width=480, height=270)
    y_position -= 290  

    # Add video details
    for key, value in video_info.items():
        y_position = draw_wrapped_text(c, f"{key.capitalize()}: {value}", margin, y_position, width - 2 * margin)
        y_position -= 10  
        if y_position < margin:
            c.showPage()
            y_position = height - margin

    # Add comments to PDF
    c.setFont("Helvetica-Bold", 16)
    y_position -= 20
    c.drawString(margin, y_position, "Comments")
    c.setFont("Helvetica", 12)
    y_position -= 28

    # Loop through comments and add to PDF
    for comment in comments:
        for key, value in comment.items():
            y_position = draw_wrapped_text(c, f"{key.capitalize()}: {value}", margin, y_position, width - 2 * margin)
            y_position -= 10  
            if y_position < margin:
                c.showPage()
                y_position = height - margin
        y_position -= 20
        if y_position < margin:
            c.showPage()
            y_position = height - margin

    c.save()  # Save the PDF file

# Main function to handle the overall data capture process
def capture_youtube_data(video_url):
    # Extract channel and video IDs from the URL
    channel_id, video_id = get_channel_and_video_id_from_url(youtube, video_url)
    
    # Retrieve channel and video details
    channel_details = get_channel_details(youtube, channel_id)
    video_details = get_video_details(youtube, video_id)
    
    # Extract channel information
    channel_info = {
        'channelId': channel_details['items'][0]['id'],
        'title': channel_details['items'][0]['snippet']['title'],
        'description': channel_details['items'][0]['snippet']['description'],
        'published At': channel_details['items'][0]['snippet']['publishedAt'],
        'subscriber Count': channel_details['items'][0]['statistics']['subscriberCount'],
        'video Count': channel_details['items'][0]['statistics']['videoCount'],
        'view Count': channel_details['items'][0]['statistics']['viewCount']
    }

    # Extract video information
    video_info = {
        'videoId': video_details['items'][0]['id'],
        'title': video_details['items'][0]['snippet']['title'],
        'description': video_details['items'][0]['snippet']['description'],
        'published At': video_details['items'][0]['snippet']['publishedAt'],
        'view Count': video_details['items'][0]['statistics'].get('viewCount', 0),
        'like Count': video_details['items'][0]['statistics'].get('likeCount', 0),
        'dislike Count': video_details['items'][0]['statistics'].get('dislikeCount', 0),
        'comment Count': video_details['items'][0]['statistics'].get('commentCount', 0)
    }

    # Retrieve video comments
    comments = get_video_comments(youtube, video_id)

    # Determine the path for saving the data
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_directory = os.path.join(desktop_path, f"Youtube/{channel_info['title']}/{video_info['title']}")
    os.makedirs(output_directory, exist_ok=True)

    # Uncomment these lines if you want to save CSV files
    pd.DataFrame([channel_info]).to_csv(os.path.join(output_directory, 'channel_info.csv'), index=False)
    pd.DataFrame([video_info]).to_csv(os.path.join(output_directory, 'video_info.csv'), index=False)
    pd.DataFrame(comments).to_csv(os.path.join(output_directory, 'comments.csv'), index=False)

    # Capture a screenshot of the video
    screenshot_path = os.path.join(output_directory, 'video_screenshot.png')
    capture_screenshot(video_url, screenshot_path)

    # Generate a PDF report
    pdf_path = os.path.join(output_directory, f"{video_info['title']}.pdf")
    generate_pdf(channel_info, video_info, comments, screenshot_path, pdf_path)

    # Optionally remove the screenshot after PDF generation
    os.remove(screenshot_path)

    # Print the final success message
    print(f"Channel information, video details, comments, and PDF report have been saved to {output_directory}")

# Entry point for the script, prompts user for YouTube video URL
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    capture_youtube_data(video_url)
