from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

class GroupManager:
    def __init__(self, driver: webdriver, contact_list: list, group_name: str):
        self._contact_list = contact_list
        self._group_name   = group_name
        self._driver       = driver

    def check_if_group_exists(self) -> bool:
        self._open_whatsapp_web()

        self._search_group_name()

        try:
            group_title = self._driver.find_element(By.CSS_SELECTOR, 'span[title="{}"]'.format(self._group_name)).text      # Get the group title from the search results

            if group_title == self._group_name:     # Check if the group title matches the group name
                
                # Entry to group
                self._driver.find_element(By.XPATH, f'//span[@title="{self._group_name}"]').click()
                time.sleep(1)
                
                # Click on group element
                self._driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div/span').click()
                time.sleep(1)
                
                # Click on add member in existed group
                self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/div/section/div[7]/div[2]/div[1]/div[2]/div/div').click()
                time.sleep(1)

                self._add_contacts_to_existed_group()

                print("Group has been created")
                return True

        except NoSuchElementException:
            return False

    def create_group(self):
        self._click_on_new_chat()

        # click on create group
        self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div[1]/div[2]/div').click()
        time.sleep(1)

        self._add_contacts_to_new_group()

        print("Group has been created")

    def _add_contacts_to_existed_group(self):
        for contact in self._contact_list:
            # Search for the contact
            try:
                search_box = self._driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p')
                search_box.send_keys(contact)
                time.sleep(2)  # Wait for search results to appear

                # Click on the "Add" button next to the contact
                self._driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/span').click()
                time.sleep(2)  # Wait for the contact to be added

                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)

            except NoSuchElementException:
                print("Cannot find contact member")
                # Click on the "Add" button next to the contact
                self._driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/span').click()
                time.sleep(2) 

                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)

        add_members = self._driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/span[2]/div/div/div/span')
        add_members.click()
        time.sleep(2)

        conform = self._driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button[2]/div/div')
        conform.click()
        time.sleep(2)

    def _open_whatsapp_web(self):
        self._driver.get("https://web.whatsapp.com/")

        # In this case, we're waiting for the New Chat button to be present before proceeding
        WebDriverWait(self._driver, 120).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))) 
        # No need for a sleep here as WebDriverWait will wait for the condition to be met

    def _search_group_name(self):
        search_box = self._driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.send_keys(self._group_name)
        time.sleep(2)  # Wait for search results to appear

    def _click_on_new_chat(self):
        chat = self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[4]')
        try:
            chat.click()
        except Exception:
            print ('Could not find matching contact name')
            exit(0)

        time.sleep(2)

    def _add_contacts_to_new_group(self):
        for contact in self._contact_list:
            # Search for the contact
            try:
                search_box = self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/span/div/div/div[1]/div/div/div[2]/input')
                search_box.send_keys(contact)
                time.sleep(2)  # Wait for search results to appear

                # Click on the "Add" button next to the contact
                self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/span/div/div/div[2]/div/div/div/div/div/div/div[2]').click()
                time.sleep(2)  # Wait for the contact to be added

                # Clear the search box
                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)

            except NoSuchElementException:
                print("Cannot find contact member")
                # Click on the "Add" button next to the contact
                self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/span/div/div/div[2]/div[2]/div[2]/div[1]/div/span').click()
                time.sleep(2) 

                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)

        # Enter the group name
        forward = self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/span/div/div/span/div/span')
        forward.click()
        time.sleep(2)

        group_name_input = self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/span/div/div/div[1]/div[2]/div/div[2]/div[3]/div/div[1]/p')
        group_name_input.send_keys(self._group_name)
        time.sleep(2)

        # Click on the "Create" button
        self._driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/span/div/div/span/div/div/span').click()