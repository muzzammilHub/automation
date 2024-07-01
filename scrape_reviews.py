from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

app = Flask(__name__)

@app.route('/scrape_airbnb_reviews', methods=['GET'])
def scrape_airbnb_reviews():
    # url = "https://www.airbnb.com/rooms/858697692672545141?category_tag=Tag%3A8678&enable_m3_private_room=true&photo_id=1728488302&search_mode=regular_search&check_in=2024-06-28&check_out=2024-06-29&source_impression_id=p3_1719410416_P3fACuyveajy0eSk&previous_page_section_name=1000&federated_search_id=49a88c11-aa1c-43f2-9125-e1e8745a3d3b"
    url = request.args.get('url')
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        show_reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="pdp-show-all-reviews-button"]'))
        )
        show_reviews_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="pdp-reviews-modal-scrollable-panel"]'))
        )

        # Extract reviews
        review_elements = driver.find_elements(By.CSS_SELECTOR, '[data-review-id]')
        reviews = []
        for el in review_elements:
            name = el.find_element(By.CSS_SELECTOR, 'h2').text.strip() if el.find_elements(By.CSS_SELECTOR, 'h2') else None
            content_element = el.find_element(By.CSS_SELECTOR, 'div.r1bctolv span span')
            content = content_element.text.strip() if content_element else None
            reviews.append({'name': name, 'content': content})

        response = json.dumps(reviews, indent=4)
        return jsonify({"status": "success", "reviews": reviews})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
