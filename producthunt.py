import csv
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from bs4 import BeautifulSoup

# 设置浏览器驱动路径，这里假设使用Chrome
driver = webdriver.Chrome()

# 打开网页
driver.get('https://www.producthunt.com/products/hubspot/reviews')

try:
    # 等待"show more"按钮出现
    show_more_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Show")]'))
    )

    # 循环点击"show more"按钮，直到没有更多按钮出现
    while show_more_button:
        # 使用ActionChains来点击按钮
        actions = ActionChains(driver)
        actions.move_to_element(show_more_button).click().perform()

        time.sleep(2)  # 等待加载评论

        # 继续查找是否还有"show more"按钮
        try:
            show_more_button = driver.find_element(By.XPATH, '//button[contains(text(), "Show")]')
        except:
            show_more_button = None

    # 等待一段时间确保所有内容加载完成
    time.sleep(5)

    # 获取当前页面的HTML源码
    html = driver.page_source

except Exception as e:
    html = driver.page_source
    print(f"Error: {e}")

driver.quit()

soup = BeautifulSoup(html, 'html.parser')

# 找到所有的<script type="application/ld+json">标签
scripts = soup.find_all('script', type='application/ld+json')

# 遍历每个<script type="application/ld+json">标签，找到包含"review"的内容
for script in scripts:
    script_text = script.string.strip() if script.string else ''
    if '"review"' in script_text:
        # 使用正则表达式或其他方法提取review代码块的内容
        pattern = re.compile(r'"review"\s*:\s*(\[.*?\])')
        match = re.search(pattern, script_text)
        if match:
            review_content = match.group(1)
            data = json.loads(review_content)
            #print(review_content)
            #print(type(review_content))
            for re in data:
                #print(re)
                review_text = re.get('reviewBody', None) or None
                review_date = re.get('datePublished', None)
                rating = re.get('reviewRating', {}).get('ratingValue', None)
                print(review_text)
                print(review_date)
                print(rating)
                with open("test.csv", "a", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([review_text,review_date,rating])