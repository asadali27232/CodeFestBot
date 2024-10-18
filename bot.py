import sheet
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def submit_form(driver, name, email):
    driver.get('https://tally.so/r/waDMG2')

    time.sleep(2)

    name_field = driver.find_element(
        By.ID, 'e729bd5e-3362-4712-823c-9b426dcb0610')
    name_field.send_keys(name)

    email_field = driver.find_element(
        By.ID, '9271d54a-c70b-4375-ac4b-7ad4502d321d')
    email_field.send_keys(email)

    time.sleep(2)

    submit_button = driver.find_element(By.CLASS_NAME, 'sc-5b8353b7-1')
    submit_button.click()

    time.sleep(2)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    start_row = int(input('Enter the row number to start from: ')) + 1
    data = sheet.get()

    for i in range(start_row, len(data)):
        row = data[i-1]
        name = row[0]
        email = row[1]

        submit_form(driver, name, email)

        sheet.post(i, 'Done')

    driver.quit()
