# this should use selenium or something similar to: 
    # open up chrome 
    # log into instagram
    # make post (supply image path and caption)
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time



def makeInstagramPost(username, password, imagePath, caption):

    # Create an undetected Chrome browser instance
    options = uc.ChromeOptions()
    # options.add_argument("--headless")  # Optional
    options.add_argument("--disable-notifications")

    driver = uc.Chrome(options=options)

    driver.get("https://www.instagram.com/")
    # Now proceed with login, upload, etc.

    time.sleep(5)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)

    driver.get("https://www.instagram.com/")
    time.sleep(5)

    # Find the "Create" span by visible text and click its parent button
    try:
        # Locate the span with "Create"
        create_span = driver.find_element(By.XPATH, '//span[text()="Create"]')

        # Click the parent element (usually a button or div)
        create_span.click()
        print("Clicked the Create button.")
        time.sleep(1)

        post_span = driver.find_element(By.XPATH, '//span[text()="Post"]')
        post_span.click()

        time.sleep(2)
        # Find the input element (this is usually inside a <form> or <div> with display: none)
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')

        # Upload the image
        file_input.send_keys(imagePath)
        time.sleep(2)

        next_div = driver.find_element(By.XPATH, '//div[text()="Next"]')
        next_div.click()

        time.sleep(2)

        next_div = driver.find_element(By.XPATH, '//div[text()="Next"]')
        next_div.click()
        print("clicked again??")
        time.sleep(2)

        caption_box = driver.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]')
        # caption_box.click()
        # time.sleep(2)
        # print("typing caption")
        # caption_box.send_keys(caption)
        # time.sleep(2)

        print("trying caption")
        actions = ActionChains(driver)
        actions.click(caption_box)
        actions.pause(1)
        actions.send_keys(caption)
        actions.perform()

        time.sleep(2)

        share_div = driver.find_element(By.XPATH, '//div[text()="Share"]')
        share_div.click()
        time.sleep(2)

    except Exception as e:
        print("Could not find or click the Create button:", e)

    time.sleep(3)
