import sheet
import time
from selenium import webdriver


def submit_form():
    driver = webdriver.Chrome()
    driver.get('https://tally.so/r/waDMG2')

    time.sleep(10)

    driver.quit()


if __name__ == "__main__":
    submit_form()
