import json
import os
import threading
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from urllib.parse import urlparse

class ScrapeTimeoutException(Exception):
    """Custom exception for handling timeouts during scraping."""
    pass

def is_video_based_url(url):
    video_domains = ["youtube.com", "vimeo.com", "dailymotion.com"]
    domain = urlparse(url).netloc
    return any(video_domain in domain for video_domain in video_domains)

def is_social_media_url(url):
    social_media_domains = [
        "facebook.com", "twitter.com", "instagram.com", "linkedin.com",
        "pinterest.com", "tiktok.com", "reddit.com", "snapchat.com"
    ]
    domain = urlparse(url).netloc
    return any(social_domain in domain for social_domain in social_media_domains)

def scrape_text_and_images_with_timeout(driver, url, timeout=30):
    def scrape():
        nonlocal page_text, image_urls, exception_raised
        try:
            driver.get(url)
            page_text = driver.find_element(By.TAG_NAME, "body").text
            images = driver.find_elements(By.TAG_NAME, "img")
            image_urls = [img.get_attribute('src') for img in images if img.get_attribute('src')]
        except Exception as e:
            exception_raised = e

    page_text, image_urls, exception_raised = None, [], None
    thread = threading.Thread(target=scrape)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        thread.join(0)  # Ensure thread termination
        raise ScrapeTimeoutException(f"Scraping {url} exceeded the time limit of {timeout} seconds.")
    if exception_raised:
        raise exception_raised
    return page_text, image_urls

def download_images(image_urls, image_folder):
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    downloaded_images = []
    for image_url in image_urls:
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_name = os.path.basename(urlparse(image_url).path)
                image_path = os.path.join(image_folder, image_name)
                with open(image_path, 'wb') as out_file:
                    out_file.write(response.content)
                downloaded_images.append(image_path)
            else:
                print(f"Failed to download image {image_url}")
        except Exception as e:
            print(f"Error downloading image {image_url}: {e}")
    
    return downloaded_images

def append_to_json_file(data, output_filename):
    if os.path.exists(output_filename):
        with open(output_filename, 'r+') as f:
            existing_data = json.load(f)
            existing_data.extend(data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)
    else:
        with open(output_filename, 'w') as f:
            json.dump(data, f, indent=4)

def process_json_file_for_scraping(filename, output_filename, image_folder, timeout=30):
    with open(filename, 'r') as f:
        data = json.load(f)

    driver = webdriver.Chrome()  # Or specify the path to your ChromeDriver
    formatted_data = []
    total_sites = len(data)  # Total number of sites to scrape

    for index, website in enumerate(data):
        url = website["link"]
        print(f"Scraping website {index + 1} out of {total_sites}")  # Progress counter

        if is_video_based_url(url) or is_social_media_url(url):
            print(f"Skipping URL: {url}")
            continue

        try:
            text_content, image_urls = scrape_text_and_images_with_timeout(driver, url, timeout=timeout)
        except ScrapeTimeoutException as e:
            print(f"Timeout: {e}")
            continue
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue

        if text_content or image_urls:
            downloaded_images = download_images(image_urls, image_folder)
            document = {
                "content": text_content,
                "images": downloaded_images,  # Store paths of downloaded images
                "metadata": {
                    "title": website.get("title"),
                    "url": url,
                    "snippet": website.get("snippet"),
                    "source": website.get("source"),
                    "position": website.get("position"),
                }
            }
            formatted_data.append(document)
            append_to_json_file([document], output_filename)

    driver.quit()
    print(f"Scraping completed. Data saved to {output_filename}")

# Example usage
input_filename = "Web Scraper/json processing/final_serp_api.json"  # Update with your actual file path
output_filename = "Web Scraper/scraped data/scrapedtext.json"
image_folder = "Web Scraper/scraped data/images"  # Folder to save downloaded images
process_json_file_for_scraping(input_filename, output_filename, image_folder, timeout=30)