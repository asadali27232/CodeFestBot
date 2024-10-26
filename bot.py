import sheet
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor



def submit_form(driver, name, email):

    name_field = driver.find_element(
        By.ID, 'e729bd5e-3362-4712-823c-9b426dcb0610')
    name_field.clear()
    name_field.send_keys(name) 

    email_field = driver.find_element(
        By.ID, '9271d54a-c70b-4375-ac4b-7ad4502d321d')
    email_field.clear()
    email_field.send_keys(email)

    submit_button = driver.find_element(By.CLASS_NAME, 'sc-5b8353b7-1')
    submit_button.click()

    error_div = None
    try:
        error_div = driver.find_element(
            By.ID, 'error_9271d54a-c70b-4375-ac4b-7ad4502d321d')
    except:
        pass

    driver.refresh()
    return False if error_div else True


def process_range(start_row, end_row, data):
    driver = webdriver.Chrome()
    driver.get('https://tally.so/r/waDMG2')

    for i in range(start_row, end_row):
        row = data[i]

        if len(row) < 2:
            print(f"Row: {i} skipped due missing values!")
            continue

        name = row[0]
        email = row[1]

        if submit_form(driver, name, email):
            sheet.post(i+1, 'Done')
        else:
            print(f"Row: {i} sipped due to invalid values!")

    driver.quit()


if __name__ == "__main__":
    # Row index starts from 0
    row_to_start = int(input('Enter the row number to start from: ')) - 1
    num_threads = int(input("Enter the number of threads: "))

    data = sheet.get()

    remaining_rows = len(data) - row_to_start
    rows_per_thread = remaining_rows // num_threads
    extra_rows = remaining_rows % num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executer:
        futures = []
        current_start_row = row_to_start

        for thread_num in range(num_threads):
            if thread_num + 1 == num_threads:
                current_end_row = current_start_row + rows_per_thread + extra_rows

            else:
                current_end_row = current_start_row + rows_per_thread

            futures.append(executer.submit(
                process_range, current_start_row, current_end_row, data))

            current_start_row = current_end_row

        for future in futures:
            future.result()
