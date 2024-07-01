from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

app = Flask(__name__)
@app.route("/scrape-amenities", methods=["GET"])

def scrape_amenities():

    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 40

    driver = webdriver.Chrome()

    try:
    
        driver.get(url)

        show_amenities_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@data-plugin-in-point-id="AMENITIES_DEFAULT"]/section/div[3]/button[contains(text(), "Show all 41 amenities")]'))
            )
        
        show_amenities_button.click()

        amenities_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="modal-container"]'))
        ) 


        amenities = driver.find_elements(By.CSS_SELECTOR , '._11jhslp')

        result = []

        for a in amenities:
            name = a.find_element(By.CSS_SELECTOR, 'h3').text.strip() if a.find_elements(By.CSS_SELECTOR, 'h3') else None

            subheadings = [subheading.text.strip() for subheading in a.find_elements(By.CSS_SELECTOR, 'ul > li')]  

            result.append({'heading': name, 'subheadings': subheadings})

        
        return jsonify({"status": "success", "result" : result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
            

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)