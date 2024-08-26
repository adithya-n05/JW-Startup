from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

def scrape_data(urls):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless if necessary
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(), options=chrome_options)  # Initialize WebDriver with options
    data = {}  # Dictionary to store scraped data

    for url in urls:
        try:
            driver.get(url)
            time.sleep(5)  # Increase wait time for the page to load
            title = driver.title
            data[url] = {'title': title}
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            data[url] = {'error': str(e)}

    driver.quit()  
    with open('jeff_wilson_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return data

urls = [
    'https://www.linkedin.com/in/jeffwilsonphd/',
    'https://capbase.com/jeff-wilson-minimalistic-design-affordable-housing/',
    'https://theorg.com/org/jupe/org-chart/jeff-wilson-1',
    'https://joinhampton.com/blog/jupe-scaled-to-12-million-in-3-years-with-an-innovative-glamping-tent-and-business-model',
    'https://x.com/ProfDumpster',
    'https://www.youtube.com/watch?v=xN_og8z5yQw',
    'https://www.instagram.com/profdumpster/?hl=am-et',
    'https://www.youtube.com/watch?v=bhuUdCseF3k',
    'https://blog.initialized.com/2022/10/video-interview-with-jeff-wilson-ceo-of-jupe/',
    'https://miamiadschool.com/event/jeff-wilson-jupe/',
    'https://www.capitalletter.com/p/jupe'
]

scraped_data = scrape_data(urls)
