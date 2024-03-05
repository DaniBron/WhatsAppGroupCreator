from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

from group_creator import GroupManager

def initialize_webdriver():
    return webdriver.Chrome()

def load_excel_sheet(excel_file):
    return pd.read_excel(excel_file)

def load_excel_sheet() -> pd.DataFrame:
    while True:
        excel_file = input("Enter the name of your Excel file (e.g., 'Tests.xlsx'): ")

        try:
            df = pd.read_excel(excel_file)
            return df  # Break out of the loop if the file is found and read successfully

        except FileNotFoundError:
            print(f"File '{excel_file}' not found. Please enter a valid file name.")


def main():

    df          = load_excel_sheet()
    group_name  = input("Enter the name of the group you want to create: ")  # Change this to your group name

    driver  = initialize_webdriver()
    

    contact_list = df['Phone Number'].tolist()

    group_creator = GroupManager(driver, contact_list, group_name)

    try:
        if not group_creator.check_if_group_exists():
            print(f"Group '{group_name}' not exists. Creating a new group")
            group_creator.create_group()
        
    except Exception as e:
        print(f"Error: {e}")

    input()
    #driver.quit()

if __name__ == "__main__":
    main()
