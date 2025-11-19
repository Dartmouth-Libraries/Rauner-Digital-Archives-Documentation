# Project Overview

## YouTube Data Capture

This project is designed to capture and organize information from YouTube videos and channels using the YouTube Data API. The project extracts channel and video details, gathers comments, retrieves thumbnail images, and generates both CSV files and a PDF report containing all of the retrieved information.

### Key Features
1. **Channel Information Retrieval**: Fetches details like channel title, description, published date, subscriber count, view count, and more.
2. **Video Information Retrieval**: Extracts video-specific information including title, description, view count, like/dislike counts, and comment count.
3. **Comments Extraction**: Captures the top-level comments for the specified video, including the author, comment text, and like count.
4. **Thumbnail Image Capture**: Downloads the high-resolution thumbnail of the video.
5. **PDF Report Generation**: Creates a PDF report with channel and video summaries, embedded thumbnail, and formatted comments.
6. **CSV Data Export**: Outputs the extracted data to CSV files for further analysis.

### How it Works

The project is divided into multiple functions, each responsible for a different aspect of data retrieval and formatting.

#### 1. **get_channel_and_video_id_from_url()**
- **Purpose**: Parses a YouTube video URL to extract the video ID and the corresponding channel ID.
- **Input**: A YouTube video URL.
- **Output**: Returns the `channel_id` and `video_id`.

#### 2. **get_channel_details()**
- **Purpose**: Fetches channel details using the YouTube Data API.
- **Input**: The `channel_id`.
- **Output**: A dictionary containing channel information, such as the title, description, subscriber count, and total views.

#### 3. **get_video_details()**
- **Purpose**: Retrieves specific information about the video, including title, description, view count, like count, and comment count.
- **Input**: The `video_id`.
- **Output**: A dictionary containing video information.

#### 4. **get_video_comments()**
- **Purpose**: Extracts the top-level comments for a given video, with details such as the author name, comment text, like count, and timestamp.
- **Input**: The `video_id`.
- **Output**: A list of dictionaries, each representing a comment.

#### 5. **get_thumbnail_image()**
- **Purpose**: Downloads the high-resolution thumbnail for the video.
- **Input**: The `video_id`.
- **Output**: An image object representing the thumbnail.

#### 6. **generate_pdf()**
- **Purpose**: Generates a PDF report containing channel and video details, along with the thumbnail and comments.
- **Input**: Channel information, video information, comments list, thumbnail image, and output path.
- **Output**: Saves a formatted PDF report to the specified path.

#### 7. **capture_youtube_data()**
- **Purpose**: The main function that ties everything together. It takes the video URL as input, extracts relevant data, and saves the information in CSV and PDF formats.
- **Input**: A YouTube video URL.
- **Output**: Saves channel details, video details, and comments as CSV files, and generates a PDF report.

### Project Dependencies

The project requires the following Python libraries:
- `googleapiclient.discovery` for interacting with the YouTube Data API.
- `pandas` for saving data to CSV.
- `re` for regular expression operations.
- `requests` for HTTP requests.
- `PIL` (from `Pillow`) for working with images.
- `reportlab` for generating the PDF report.

All dependencies are listed in the `requirements.txt` file.

### How to Use
1. **Clone the Repository**: Clone the GitHub repository to your local machine.
2. **Install Dependencies**: Run `pip install -r requirements.txt` to install all required packages.
3. **Obtain YouTube API Key**: Get your YouTube Data API key and replace the placeholder in the script.
4. **Run the Script**: Execute the main script (`main.py`) and provide a YouTube video URL to capture the data.

### Outputs
- **CSV Files**: Channel information, video details, and comments are saved as CSV files for easy analysis.
- **PDF Report**: A detailed report is generated containing the channel and video summary, including an embedded thumbnail and comments.

### Future Enhancements
- **Support for Multiple Videos**: Extend the project to handle multiple video URLs simultaneously.
- **Interactive Dashboard**: Create an interactive dashboard to visualize the data more effectively.
- **Enhanced Error Handling**: Improve error handling to manage network issues or invalid URLs more gracefully.
