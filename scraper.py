from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

BASE_URL = "https://www.newegg.com/All-Laptop/SubCategory/ID-32/Page-{}"
TARGET_COUNT = 100
OUTPUT_FILE = "newegg_laptops.csv"

def start_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_newegg(driver):
    data = []
    page = 1

    while len(data) < TARGET_COUNT:
        print(f"Fetching page {page}...")
        driver.get(BASE_URL.format(page))
        time.sleep(2)  # allow page to load

        # WAIT for ".item-container" to appear
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".item-container"))
            )
        except:
            print("No product containers found on page", page)
            break

        cards = driver.find_elements(By.CSS_SELECTOR, ".item-container")
        if not cards:
            print("No products found on page", page)
            break

        for card in cards:
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, ".item-title")
                title = title_elem.text.strip()
                url = title_elem.get_attribute("href")
            except:
                title, url = None, None

            try:
                price_elem = card.find_element(By.CSS_SELECTOR, ".price-current")
                price = price_elem.text.strip()
            except:
                price = None

            try:
                rating_elem = card.find_element(By.CSS_SELECTOR, ".item-rating")
                rating = rating_elem.get_attribute("title")
            except:
                rating = None

            try:
                reviews_elem = card.find_element(By.CSS_SELECTOR, ".item-rating-num")
                reviews = reviews_elem.text.strip("()")
            except:
                reviews = None

            try:
                img_elem = card.find_element(By.CSS_SELECTOR, "a.item-img img")
                img_url = img_elem.get_attribute("src")
            except:
                img_url = None

            try:
                brand_elem = card.find_element(By.CSS_SELECTOR, ".item-brand img")
                brand = brand_elem.get_attribute("title")
            except:
                brand = None

            data.append([title, price, rating, reviews, url, img_url, brand])
            if len(data) >= TARGET_COUNT:
                break

        page += 1
        time.sleep(1)  # polite delay between page loads

    return data

try:
    print("Running headless mode first...")
    driver = start_driver(headless=True)
    products = scrape_newegg(driver)

    if len(products) < 10:
        print("Headless mode captured too few products — retrying in visible mode...")
        driver.quit()
        driver = start_driver(headless=False)
        products = scrape_newegg(driver)
finally:
    driver.quit()

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product Name", "Price", "Rating", "Reviews", "Product URL", "Image URL", "Brand"])
    writer.writerows(products)

print(f"✅ Scraped {len(products)} products. Saved to {OUTPUT_FILE}")

   
