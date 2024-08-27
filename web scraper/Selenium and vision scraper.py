import json
import os
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from google.cloud import vision
from urllib.parse import urlparse

class ScrapeTimeoutException(Exception):
    """Custom exception for handling timeouts during scraping."""
    pass

def is_video_based_url(url):
    # Check if a URL is likely video-based by checking common video platforms
    video_domains = ["youtube.com", "vimeo.com", "dailymotion.com"]
    domain = urlparse(url).netloc
    return any(video_domain in domain for video_domain in video_domains)

def scrape_text_and_images_with_timeout(driver, url, timeout=10):
    def scrape():
        nonlocal page_text, image_urls, exception_raised
        try:
            driver.get(url)
            # Extract all the visible text from the page
            page_text = driver.find_element(By.TAG_NAME, "body").text
            # Extract all image URLs from the page
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

def analyze_image_with_vision_api(image_url):
    # Initialize Google Cloud Vision API client
    client = vision.ImageAnnotatorClient()

    # Prepare the image from URL
    image = vision.Image()
    image.source.image_uri = image_url
    
    # Perform text detection on the image
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        print(f"Error processing image {image_url}: {response.error.message}")
        return None
    
    # Return detected text or None if no text was detected
    return texts[0].description if texts else None

def append_to_json_file(data, output_filename):
    # Load existing data if the file exists
    if os.path.exists(output_filename):
        with open(output_filename, 'r+') as f:
            existing_data = json.load(f)
            existing_data.extend(data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)
    else:
        # If the file doesn't exist, create it and dump data
        with open(output_filename, 'w') as f:
            json.dump(data, f, indent=4)

def process_json_file_for_llamaindex_with_vision(filename, output_filename, timeout=10):
    # Load the JSON data
    with open(filename, 'r') as f:
        data = json.load(f)

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()  # Or specify the path to your ChromeDriver
    formatted_data = []

    for entry in data:
        if "organic_results" in entry:
            for website in entry["organic_results"]:
                url = website["link"]

                if is_video_based_url(url):
                    print(f"Skipping video-based URL: {url}")
                    continue
                
                try:
                    print(f"Scraping text and images from: {url}")
                    text_content, image_urls = scrape_text_and_images_with_timeout(driver, url, timeout=timeout)
                except ScrapeTimeoutException as e:
                    print(f"Timeout: {e}")
                    continue  # Skip this URL and move to the next one
                except Exception as e:
                    print(f"Error scraping {url}: {e}")
                    continue  # Skip this URL and move to the next one
                
                analyzed_images = []
                for image_url in image_urls:
                    print(f"Analyzing image: {image_url}")
                    image_text = analyze_image_with_vision_api(image_url)
                    analyzed_images.append({"url": image_url, "text": image_text})
                
                if text_content or analyzed_images:
                    # Format data for LlamaIndex
                    document = {
                        "content": text_content,
                        "images": analyzed_images,
                        "metadata": {
                            "title": website.get("title"),
                            "url": url,
                            "snippet": website.get("snippet"),
                            "source": website.get("source"),
                            "position": website.get("position"),
                        }
                    }
                    formatted_data.append(document)

                    # Save the formatted data for LlamaIndex to the output file
                    append_to_json_file([document], output_filename)
    
    driver.quit()

    print(f"Scraping completed. Data saved to {output_filename}")

# Example usage
input_filename = "Jeff_Wilson_Professor_Dumpster_google_results.json"
output_filename = "formatted_for_llamaindex_with_vision.json"
process_json_file_for_llamaindex_with_vision(input_filename, output_filename, timeout=10)