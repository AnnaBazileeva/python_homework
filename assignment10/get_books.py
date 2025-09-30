from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

time.sleep(5)


books = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
print(f"Found {len(books)} results")

results = []

for book in books:
    try:
        title = book.find_element(By.CLASS_NAME, "title-content").text

        authors_elements = book.find_elements(By.CLASS_NAME, "author-link")
        authors = "; ".join([a.text for a in authors_elements])

        format_year = book.find_element(By.CLASS_NAME, "display-info-primary").text


        results.append({
            "Title": title,
            "Author": authors,
            "Format-Year": format_year
        })
    except Exception as e:
        print("Error parsing an entry:", e)

driver.quit()

df = pd.DataFrame(results)
print(df)


df.to_csv("csv/get_books.csv", index=False)

with open("get_books.json", "w") as f:
    json.dump(results, f, indent=2)