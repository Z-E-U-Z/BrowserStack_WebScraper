# El País Article Scraper

A web scraping tool that extracts articles from El País Spanish news website, translates them to English, and performs text analysis. Built with Selenium for local testing and validation.

## Core Features

- Scrapes articles from El País Opinion section
- Extracts title, content, and cover images  
- Translates Spanish headlines to English
- Analyzes repeated words across articles
- Local testing for development and validation

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver (automatically managed by Selenium)

## Installation

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

Simply run the scraper:
```bash
python main.py
```

The script will:
1. Navigate to El País website
2. Go to Opinion section
3. Scrape first 5 articles
4. Extract titles, content, and images
5. Translate titles to English
6. Analyze repeated words

## Output

- **Console**: Article titles in Spanish and English, repeated words analysis
- **images/folder**: Downloaded cover images from articles
