from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
#from graficas import *


def csv_find():
    number_plates = []  # Store the number plates
    # Open the CSV file
    with open(csv_file_path, "r") as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        # Iterate over each row in the CSV file
        for row in reader:
            number_plate = row[1]
            if number_plate != "Number":  # Skip the "Number" value
                number_plates.append(number_plate)

    return number_plates


def csv_save_info(info):
    # New CSV file for number plate information
    csv_file_path_info = "number_plate_info.csv"
    # Open the CSV file in append mode
    with open(csv_file_path_info, "a", newline="") as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Autoincrement the ID
        with open(csv_file_path_info, "r") as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                last_id = int(rows[-1][0])
            else:
                last_id = 0
            new_id = last_id + 1

        # Append the information to the CSV file
        for row in info:
            writer.writerow([new_id] + row)
            new_id += 1


csv_file_path = "high_precision_results.csv"
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

driver.get("https://pasarela.atu.gob.pe/#")

os.system('cls')
time.sleep(5)


# driver.maximize_window()

# First click on the slide
slide_trigger = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "aTriggerExpanderMain")))
slide_trigger.click()

# Second click on "Consultar Infracciones y Pagos"
consulta_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'menu-simple-component#Menu2Main a.white-text')))
action = ActionChains(driver)
action.move_to_element(consulta_link).click().perform()

# Third click on the select wrapper to show the menu
select_wrapper = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, '.select-dropdown.dropdown-trigger')))
select_wrapper.click()

# Fourth click on "Por placa" option
por_placa_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Por Placa']")))
por_placa_option.click()

number_plates = csv_find()
# Define the column indices
column_indices = [3, 7, 8, 12, 13]

# Define the column names
column_names = ["Placa", "Falta",
                "Fecha Infracción", "Total a Pagar", "Estado"]

for placa_number in number_plates:
    try:
        # Find the input field
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "PlacaBusquedainputElemento")))

        # Clear the input field
        input_field.clear()

        # Write the license plate number
        input_field.send_keys(placa_number)

        # Find and click the "Buscar" button
        try:
            buscar_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Buscar')]")))
            buscar_button.click()

        except Exception as e:
            print(f"Exception '{e}' for license plate: {placa_number}")
            time.sleep(2)
            continue

        time.sleep(2)

        # Check if the "Aceptar" button is present
        aceptar_button_present = False
        try:
            aceptar_button = driver.find_element(
                By.XPATH, "//button[@class='swal2-confirm swal2-styled swal2-default-outline']")
            aceptar_button_present = True
        except NoSuchElementException:
            pass

        # If the "Aceptar" button is present, click on it
        if aceptar_button_present:
            aceptar_button.click()
            time.sleep(2)
            print(
                f"Clicked 'Aceptar' button for license plate: {placa_number}")

        # Extract the HTML content of the table
        table = driver.find_element(
            By.CSS_SELECTOR, "table.highlight.responsive-table")
        table_html = table.get_attribute("innerHTML")

        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(table_html, "html.parser")

        # Find all the rows in the table body
        rows = soup.find("tbody", {"name": "tbody-table"}).find_all("tr")

        # Check if there are no records
        if len(rows) == 0:
            print(f"No records found for license plate: {placa_number}")
        else:
            # Iterate over the rows and extract the desired information
            extracted_data = []
            for row in rows:
                # Find all the cells in the row
                cells = row.find_all("td")

                # Create a list to store the column values
                data = []

                # Iterate over the column indices and extract the values
                for idx in column_indices:
                    # Check if the index is within the range of available cells
                    if idx < len(cells):
                        cell_value = cells[idx].text.strip()
                        if (idx == 12):
                            cell_value = float(cell_value.replace(',', ''))
                    else:
                        cell_value = ""
                    data.append(cell_value)

                # Print the extracted information
                for column_name, cell_value in zip(column_names, data):
                    print(f"{column_name}: {cell_value}")
                print("--------")

                # Add the extracted information to the list
                extracted_data.append(data)

                # Save the information to CSV if data is present
        if any(cell_value for row_data in extracted_data for cell_value in row_data):
            csv_save_info(extracted_data)
            print(f"Data saved for license plate: {placa_number}")
            print("\n--------------------------\n\n")
            # reporte_visual()

        time.sleep(1)  # Wait for the page to reset

    except TimeoutException:
        print(f"Timeout occurred for license plate: {placa_number}")
        continue
driver.quit()
