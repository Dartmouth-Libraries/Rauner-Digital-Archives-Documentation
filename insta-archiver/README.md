# Instagram Profile Archiver

**Part of the Rauner Digital Archives Project**

Instagram Profile Archiver is a Python-based tool that allows users to download and create an archive of Instagram posts from any public profile. The tool generates a professional PDF report that includes images, captions, likes, and other metadata for each post. The PDF is formatted to be visually appealing, clean, and suitable for presentations or professional portfolios.

## Features
- Download Instagram posts and related images from any public profile.
- Supports input as Instagram usernames or direct links.
- Generate a high-quality PDF archive including post images, captions, likes, and dates.
- Handles profiles with multiple images per post by creating high-resolution collages.
- Provides professional cover page and PDF metadata.
- Includes error handling for invalid usernames and connection issues.

## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Code Structure](#code-structure)
- [Contributing](#contributing)
- [License](#license)

## Getting Started
This guide will help you get a copy of the Instagram Profile Archiver up and running on your local machine for development and testing purposes.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.6+
- [pip](https://pip.pypa.io/en/stable/)
- An Instagram account (for scraping public profile information using Instaloader)

You will also need the following Python packages:
- `instaloader`
- `fpdf2`
- `Pillow`

To install these dependencies, follow the [Installation](#installation) section.

## Installation
1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/your-username/instagram-profile-archiver.git
   cd instagram-profile-archiver
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

   Alternatively, you can install the dependencies manually:
   ```sh
   pip install instaloader fpdf2 Pillow
   ```

3. Make sure you have Python 3.6 or higher installed by running:
   ```sh
   python --version
   ```

## Usage
The Instagram Profile Archiver can be used to download any public profile's posts and generate a PDF archive. Follow these steps to get started:

1. Run the script:
   ```sh
   python src/main.py
   ```

2. Enter the Instagram username or profile URL when prompted:
   ```
   Enter the Instagram username or URL: https://www.instagram.com/username/
   ```

3. The tool will start downloading posts and generate the PDF report.

### Example Output
The PDF output contains:
- **Cover Page**: Includes the profile picture, username, and description of the document.
- **Post Pages**: Each page has:
  - Images from the post (single image or collage).
  - Post date, caption, and likes.
- **Page Numbering**: Each page includes a footer with the page number for easy navigation.

## Error Handling
The script includes error handling to manage common issues:
- **Invalid Username**: Prompts the user to enter a valid username if the provided one doesn't exist.
- **Connection Issues**: Displays a message if there's a problem connecting to Instagram, such as network issues.
- **Unexpected Errors**: Catches any unexpected exceptions and provides an error message to guide the user.

## Code Structure
The project has the following structure:
```
InstArchive Pro/
├── src/
│   ├── main.py        # Main script to run the archiver
├── LICENCE
├── requirements.txt   # Dependencies for the project
└── README.md          # Project documentation
```

### Main Components
- **Instaloader Integration**: The tool uses `instaloader` to download posts and profile pictures from Instagram.
- **FPDF2 for PDF Generation**: The `fpdf2` library is used to create a professional-looking PDF, with headers, footers, and a cover page.
- **Pillow for Image Processing**: The `Pillow` library is used to create collages from posts with multiple images.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions, feel free to contact me:
- GitHub: MuhammadMoiz20(https://github.com/MuhammadMoiz20)
- Email: moizzahidofficial@gmail.com

Thank you for using InstArchive pro!

