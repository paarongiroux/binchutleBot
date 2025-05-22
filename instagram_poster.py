import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time



def make_instagram_post(username, password, imagePath, caption):
    options = uc.ChromeOptions()
    options.add_argument("--disable-notifications")

    driver = uc.Chrome(options=options)

    driver.get("https://www.instagram.com/")
    time.sleep(5)

    try:
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)

        driver.get("https://www.instagram.com/")
        time.sleep(5)
    except Exception as e:
        print("Failed to log into instagram:", e)

    
    try:
        create_span = driver.find_element(By.XPATH, '//span[text()="Create"]')
        create_span.click()
        time.sleep(2)
    except Exception as e:
        print("Failed to find or click the Create button:", e)

    try:
        post_span = driver.find_element(By.XPATH, '//span[text()="Post"]')
        post_span.click()

        time.sleep(2)
    except Exception as e:
        print("Failed to find or click the Post button:", e)
        
    try:
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys(imagePath)
        time.sleep(2)

        next_div = driver.find_element(By.XPATH, '//div[text()="Next"]')
        next_div.click()
        time.sleep(2)

        next_div = driver.find_element(By.XPATH, '//div[text()="Next"]')
        next_div.click()
        time.sleep(2)
    except Exception as e:
        print("Failed to upload image:", e)

    try:
        caption_box = driver.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]')

        print("trying caption")
        actions = ActionChains(driver)
        actions.click(caption_box)
        actions.pause(1)
        actions.send_keys(caption)
        actions.perform()
        time.sleep(2)
    except Exception as e:
        print("Failed to input caption:", e)
        
    try:
        share_div = driver.find_element(By.XPATH, '//div[text()="Share"]')
        share_div.click()
        time.sleep(2)
    except Exception as e:
        print("Failed to publish the post:", e)
