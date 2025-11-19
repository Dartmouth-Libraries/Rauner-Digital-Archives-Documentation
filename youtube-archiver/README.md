# YouTube Data Capture

**Part of the Rauner Digital Archives Project**

## Overview
YouTube Data Capture is a Python-based software tool designed to capture and organize information from YouTube videos and channels using the YouTube Data API. This tool can extract channel and video details, gather comments, retrieve thumbnail images, and generate CSV files and a PDF report containing all the retrieved information.

Additionally, this software can be used to close any ads or ad pop-ups on YouTube videos to ensure a clean screenshot, making it especially useful for data analysis and presentations.

## Key Features
- **Channel Information Retrieval**: Fetch details like channel title, description, published date, subscriber count, view count, and more.
- **Video Information Retrieval**: Extract video-specific information, including title, description, view count, like/dislike counts, and comment count.
- **Comments Extraction**: Capture the top-level comments for the specified video, including author, text, like count, and timestamp.
- **Thumbnail Image Capture**: Download the high-resolution thumbnail of the video.
- **PDF Report Generation**: Create a PDF report containing channel and video summaries, embedded thumbnails, and formatted comments.
- **CSV Data Export**: Output the extracted data to CSV files for further analysis.
- **Ad Removal for Screenshot Capture**: Close ads or pop-ups before capturing screenshots of videos to ensure a clean view.

## Project Structure
```
/YouTubeDataCapture
│
├── /src
│   └── main.py               # Main script
├── /data
│   ├── example_channel_info.csv
│   ├── example_video_info.csv
│   └── example_comments.csv
├── /docs
│   ├── project_overview.md    # Project documentation
│   └── API_setup.md           # API setup guide
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

## Installation
1. **Clone the Repository**
   ```
   git clone https://github.com/username/YouTubeDataCapture.git
   cd YouTubeDataCapture
   ```

2. **Install the Required Libraries**
   ```
   pip install -r requirements.txt
   ```

3. **Obtain a YouTube API Key**
   - Follow the instructions in [API_setup.md](docs/API_setup.md) to generate a YouTube API key.

## Usage
Run the script with:
```bash
python src/main.py
```
After running the script, you will be prompted to enter a YouTube video URL. The tool will then extract data from the specified video, outputting the results to CSV files and a PDF report.

### Example Output
- **CSV Files**: Channel information, video details, and comments.
- **PDF Report**: A detailed report is generated containing the channel and video summary, including an embedded thumbnail and comments.

## Requirements
- Python 3.7+
- Libraries listed in `requirements.txt`
  - `googleapiclient.discovery`
  - `pandas`
  - `requests`
  - `Pillow`
  - `reportlab`

## API Setup
Refer to the [API Setup Guide](docs/API_setup.md) for detailed steps on how to set up your YouTube Data API key.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## Future Enhancements
- **Support for Multiple Videos**: Extend the project to handle multiple video URLs simultaneously.
- **Interactive Dashboard**: Create an interactive dashboard to visualize the data more effectively.
- **Enhanced Error Handling**: Improve error handling to manage network issues or invalid URLs more gracefully.

## Contribution
Contributions are welcome! Please open an issue or submit a pull request to suggest improvements.

## Acknowledgements
- **Google** for providing the YouTube Data API v3.
- **ReportLab** for PDF generation tools.

## Contact
For any questions or suggestions, please contact Moiz at [moiz@example.com](mailto:moiz@example.com).

By using YouTube Data Capture, you can easily gather and analyze information from YouTube without the clutter of ads, making it an efficient tool for research and data analysis.
