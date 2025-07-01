import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from locators import Locators
import os


def setup_driver():
    """Initialize Chrome driver with basic options"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def check_spanish_content(driver):
    """Verify the website is displaying Spanish content"""
    page_source = driver.page_source.lower()
    spanish_words = ['españa', 'opinión', 'política']
    
    for word in spanish_words:
        if word in page_source:
            print(f"Spanish content verified - found '{word}' on page")
            return True
    
    print("Could not verify Spanish content")
    return False


def handle_cookies(driver):
    """Accept cookie consent if banner is present"""
    time.sleep(2)  # wait for banner to load / we can use wait_till_element_displayed() as well, not implemented yet
    
    cookie_button = Locators.COOKIE_ACCEPT_BUTTON.get_element(driver)
    if cookie_button:
        print("Accepting cookies...")
        driver.execute_script("arguments[0].click();", cookie_button)
        time.sleep(1)
    else:
        print("No cookie banner found")


def download_image(url, filename):
    """Download and save article image"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists("images"):
                os.makedirs("images")
            
            filepath = f"images/{filename}"
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download image: {url}")
    except Exception as e:
        print(f"Error downloading image: {e}")


def scrape_articles(driver):
    """Main scraping function for El Pais opinion articles"""
    print("Navigating to El Pais...")
    driver.get("https://elpais.com/")
    time.sleep(3)

    # Verify Spanish content
    check_spanish_content(driver)
    
    # Handle cookie consent
    handle_cookies(driver)
    
    # Navigate to Opinion section
    print("Going to Opinion section...")
    opinion_link = Locators.OPINION_LINK.get_element(driver)
    if not opinion_link:
        print("Could not find Opinion link")
        return []
    
    Locators.OPINION_LINK.click_js(driver)
    time.sleep(3)

    # Find article links
    print("Finding articles...")
    article_elements = Locators.ARTICLE_LINKS.find_elements(driver)
    
    article_urls = []
    for link in article_elements:
        href = link.get_attribute("href")
        if href and '/opinion/' in href and href not in article_urls:
            article_urls.append(href)
        if len(article_urls) >= 5:
            break

    if not article_urls:
        print("No articles found")
        return []

    print(f"Found {len(article_urls)} articles to scrape")

    # Scrape each article
    articles = []
    for i, url in enumerate(article_urls, 1):
        print(f"Scraping article {i}...")
        driver.get(url)
        time.sleep(2)

        # Get title and content
        title = Locators.TITLE.text(driver)
        paragraphs = Locators.CONTENT_PARAGRAPHS.find_elements(driver)
        content = " ".join([p.text for p in paragraphs[:3]])

        # Get image if available
        image_element = Locators.IMAGE.get_element(driver)
        image_url = None
        if image_element:
            image_url = image_element.get_attribute("src")
            if image_url:
                download_image(image_url, f"article_{i}.jpg")

        articles.append({
            "title": title,
            "content": content,
            "image_url": image_url
        })

    return articles


def translate_text(text):
    """Translate Spanish text to English using Google Translate"""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': 'es',
        'tl': 'en', 
        'dt': 't',
        'q': text
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.json()
            if result and result[0] and result[0][0]:
                return result[0][0][0]
    except Exception as e:
        print(f"Translation error: {e}")
    
    return text


def analyze_word_frequency(titles):
    """Find words repeated more than twice across titles"""
    word_count = {}
    
    for title in titles:
        words = title.lower().split()
        for word in words:
            clean_word = word.strip(".,!?\"()[]")
            if len(clean_word) > 2:
                word_count[clean_word] = word_count.get(clean_word, 0) + 1
    
    return {word: count for word, count in word_count.items() if count > 2}


def main():
    
    print("El Pais Article Scraper")
    print("-" * 30)
    
    driver = setup_driver()
    
    try:
        # Scrape articles
        articles = scrape_articles(driver)
        
        if not articles:
            print("No articles scraped. Exiting.")
            return

        print(f"\nSuccessfully scraped {len(articles)} articles")
        print("-" * 50)

        # Display articles in Spanish
        print("\nARTICLES IN SPANISH:")
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"Content: {article['content'][:200]}...")
            if article['image_url']:
                print(f"Image: Downloaded as article_{i}.jpg")

        # Translate titles
        print(f"\nTRANSLATED TITLES:")
        translated_titles = []
        for i, article in enumerate(articles, 1):
            translated = translate_text(article['title'])
            translated_titles.append(translated)
            print(f"{i}. Spanish: {article['title']}")
            print(f"   English: {translated}")

        # Analyze word frequency
        print(f"\nWORD FREQUENCY ANALYSIS:")
        repeated_words = analyze_word_frequency(translated_titles)
        
        if repeated_words:
            print("Words appearing more than twice:")
            for word, count in repeated_words.items():
                print(f"  '{word}': {count} times")
        else:
            print("No words repeated more than twice")

        print(f"\nScraping completed successfully!")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
