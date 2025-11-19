"""
Instagram Profile Archiver

This script allows users to download and archive posts from any public Instagram profile. 
The archive is saved as a professionally formatted PDF, including images, captions, likes, and other metadata.

Features:
- Supports both Instagram usernames and profile URLs.
- Generates a cover page and detailed information about each post.
- Creates image collages for posts with multiple images.

Dependencies:
- Instaloader: For downloading posts and profile data.
- FPDF2: For generating PDF reports.
- Pillow: For image processing and collage creation.

Usage:
- Run the script and provide the username or URL when prompted.
- Handles invalid usernames, network issues, and other errors gracefully.

Author: Muhammad Moiz
GitHub: https://github.com/MuhammadMoiz20/InstarchivePro/blob/main/src/main.py
License: MIT
"""


import instaloader
from fpdf import FPDF
import os
import re
from PIL import Image

# Initialize instaloader instance
L = instaloader.Instaloader()

# Function to extract the username from an Instagram URL
def extract_username(url_or_username):
    # Regular expression to match Instagram URLs
    url_regex = r'(?:https?://)?(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)'
    match = re.match(url_regex, url_or_username)
    
    if match:
        # Return the username from the URL
        return match.group(1)
    else:
        # Assume it's a plain username
        return url_or_username

# Input Instagram username or URL
while True:
    url_or_username = input("Enter the Instagram username or URL: ").strip()
    username = extract_username(url_or_username)

    # Validate and load the profile
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print(f"Successfully retrieved profile for @{username}")
        break  # Exit the loop if successful
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: The username '{username}' does not exist. Please try again.")
    except instaloader.exceptions.ConnectionException:
        print("Error: Unable to connect to Instagram. Please check your internet connection and try again.")
    except instaloader.exceptions.BadResponseException:
        print(f"Error: Instagram returned a bad response for '{username}'. Try again later.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}. Please try again.")

# Create a directory to store images
image_dir = f"{username}_images"
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Custom PDF class to include header and footer
class PDF(FPDF):
    def header(self):
        # Add a logo (profile picture) if available
        if hasattr(self, 'profile_picture_path') and os.path.exists(self.profile_picture_path):
            self.image(self.profile_picture_path, 10, 8, 15)
            self.set_font('helvetica', 'B', 15)
            self.cell(30)
        else:
            self.set_font('helvetica', 'B', 15)
            self.cell(10)
        # Title
        self.cell(0, 10, f'Instagram Archive: @{username}', ln=True, align='L')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

# Initialize PDF
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_title(f'Instagram Archive: {username}')
pdf.set_author(username)

# Download profile picture
profile_pic_filename = f"{username}_profile_pic.jpg"
L.download_profilepic(profile)
pdf.profile_picture_path = os.path.join(image_dir, profile_pic_filename)  # Set the path manually

# Add a cover page
def add_cover_page(pdf, profile):
    pdf.add_page()
    # Add profile picture
    if os.path.exists(profile_pic_filename):
        pdf.image(profile_pic_filename, x=80, y=40, w=50)
    pdf.set_font('helvetica', 'B', 24)
    pdf.ln(100)
    pdf.cell(0, 10, 'Instagram Archive', ln=True, align='C')
    pdf.set_font('helvetica', '', 18)
    pdf.cell(0, 10, f'@{username}', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(0, 10, f'This document contains an archive of Instagram posts from @{username}.', align='C')

add_cover_page(pdf, profile)

# Helper function to create a high-resolution collage for multiple images
def create_collage(images, output_path, grid_size=(2, 2), thumb_size=(500, 500)):
    width, height = thumb_size
    collage_width = width * grid_size[0]
    collage_height = height * grid_size[1]
    collage_img = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))

    for index, image_path in enumerate(images):
        img = Image.open(image_path)
        img.thumbnail(thumb_size)  # High-quality resize
        x_offset = (index % grid_size[0]) * width
        y_offset = (index // grid_size[0]) * height
        collage_img.paste(img, (x_offset, y_offset))

    collage_img.save(output_path, quality=95)  # Save with high quality

# Function to process a single post
def process_post(pdf, post, index):
    # Download post images
    L.download_post(post, target=image_dir)

    # Add a new page
    pdf.add_page()

    # Initialize the y-position
    y_position = pdf.get_y()

    # Find images matching the post
    post_datetime = post.date.strftime('%Y-%m-%d_%H-%M-%S_UTC')
    post_images = [
        os.path.join(image_dir, file)
        for file in os.listdir(image_dir)
        if file.startswith(post_datetime) and file.endswith(('.jpg', '.png'))
    ]

    # Sort images to maintain order
    post_images.sort()

    # Handle multiple images
    if len(post_images) > 1:
        collage_output_path = os.path.join(image_dir, f"collage_{post_datetime}.jpg")
        create_collage(post_images[:4], collage_output_path, grid_size=(2, 2), thumb_size=(500, 500))
        # Open the collage image to get dimensions
        collage_img = Image.open(collage_output_path)
        aspect_ratio = collage_img.height / collage_img.width
        img_width = 190
        img_height = img_width * aspect_ratio
        pdf.image(collage_output_path, x=10, y=y_position, w=img_width)
        y_position += img_height + 10
    elif len(post_images) == 1:
        img = Image.open(post_images[0])
        aspect_ratio = img.height / img.width
        img_width = 190
        img_height = img_width * aspect_ratio
        pdf.image(post_images[0], x=10, y=y_position, w=img_width)
        y_position += img_height + 10

    pdf.set_y(y_position)

    # Add post date
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, f"Post Date: {post.date.strftime('%Y-%m-%d %H:%M')}", ln=True)

    # Add post caption
    caption = post.caption or ""
    caption_ascii = caption.encode('ascii', 'ignore').decode()
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(0, 10, f"Caption: {caption_ascii}")

    # Add likes
    pdf.set_font('helvetica', 'I', 12)
    pdf.cell(0, 10, f"Likes: {post.likes}", ln=True)

# Process each post
post_index = 0
print(f"Downloading posts from {username}")
for post in profile.get_posts():
    post_index += 1
    process_post(pdf, post, post_index)

    # Save the PDF every 10 posts
    if post_index % 10 == 0:
        pdf.output(f"{username}_archive_partial_{post_index}.pdf")

# Save the final PDF
pdf.output(f"{username}_archive_final.pdf")
print(f"All posts from {username} downloaded and added to PDF.")
