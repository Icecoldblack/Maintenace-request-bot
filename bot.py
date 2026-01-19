import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION: EDIT THIS SECTION ---
URL = "https://georgiastate.webtma.com/?tkn=DNB9KTKAgMy8J17B-fF_PD1ZF5hBKsNY8w44e7eHPwZCBx9SEU6fuYTm_2q90bRPDSPtMCXVpA9s3KONRjNdwrPOM8EluoOLA86MDBY9cfgzuMTFiYpvgh3um10KQ6zghYvKLqjvSbDR3EniI8Tb6QPrtho_zCcK4HPs3BWip3pvGjipYmOCYEkYEqBbpjHAdD35aw5m4V30t5YVv4Ot6JLTqXq9QUQgdT74-PuVK7V6N_0bnJv0ClbkZR1WyXJGeRiosl_BY1kPu2iNAdOMtTb-SwrE5chY-iXnVKl00x8"

# DATA TO ENTER
USER_DATA = {
    "name": "Uyiosa Nehikhuere",
    "email": "unehikhuere1@students.gsu.edu",
    "phone": "", #this is not needed dont have too put it
    "facility": "Patton Hall",
    "building": "Patton Hall",
    "floor": "",  # Leave empty if not needed
    "room": "327",
    "request_type": "Maintenance Request",  # Leave empty to skip, or enter exact text like "Maintenance"
    "action_requested": "my room is freezing please can you fix it too about 73 degrees"
}

# XPATH SELECTORS (using aria-label attributes since IDs are not available)
SELECTORS = {
    "name_input": "//input[@aria-label='Name']",
    "email_input": "//input[@aria-label='Email Address']",
    "phone_input": "//input[@aria-label='Phone #']",
    "facility_input": "//input[@aria-label='Facility Name']",
    "building_input": "//input[@aria-label='Building Name']",
    "floor_input": "//input[@aria-label='Floor Name']",
    "room_input": "//input[@aria-label='Room # / Area # (Start typing your room)']",
    "request_type_input": "//input[@aria-label='Request Type']",
    "action_input": "//textarea[@aria-label='Action Requested']",
    "save_button": "//input[@value='Save']"
}
# ----------------------------------------


def fill_kendo_dropdown(driver, xpath, value, wait_time=2):
    """
    Helper to handle WebTMA's Kendo UI searchable dropdowns.
    Types the value, waits for filtering, then confirms with TAB or ENTER.
    """
    if not value:  # Skip if value is empty
        print(f"Skipping field (no value provided)")
        return
    
    try:
        wait = WebDriverWait(driver, 10)
        field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        
        # Click to focus the field
        field.click()
        time.sleep(0.5)
        
        # Clear existing content and type new value
        field.send_keys(Keys.CONTROL + "a")  # Select all
        field.send_keys(Keys.DELETE)  # Delete selected
        field.send_keys(value)
        
        time.sleep(wait_time)  # Wait for dropdown to filter results
        
        # Try to select the first matching option
        field.send_keys(Keys.ARROW_DOWN)  # Navigate to first option
        time.sleep(0.3)
        field.send_keys(Keys.ENTER)  # Select it
        
        print(f"Filled dropdown with '{value}'")
    except Exception as e:
        print(f"Could not fill dropdown: {e}")


def fill_text_field(driver, xpath, value):
    """
    Helper to fill standard text input fields.
    """
    if not value:  # Skip if value is empty
        print(f"Skipping field (no value provided)")
        return
    
    try:
        wait = WebDriverWait(driver, 10)
        field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        field.click()
        field.clear()
        field.send_keys(value)
        print(f"Filled text field with '{value}'")
    except Exception as e:
        print(f"Could not fill text field: {e}")


def run_single_submission():
    """Run a single form submission."""
    driver = webdriver.Chrome()
    
    try:
        print("Opening WebTMA form...")
        driver.get(URL)
        driver.maximize_window()
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, SELECTORS["name_input"])))
        print("Page loaded successfully!")
        time.sleep(2)  # Extra wait for Kendo UI to initialize

        # 1. Name Field (Kendo Dropdown)
        print("\n Filling Name")
        fill_kendo_dropdown(driver, SELECTORS["name_input"], USER_DATA["name"])

        # 2. Email (Standard Text Input)
        print("\n Filling Email")
        fill_text_field(driver, SELECTORS["email_input"], USER_DATA["email"])

        # 3. Phone (Standard Text Input)
        print("\n Filling Phone")
        fill_text_field(driver, SELECTORS["phone_input"], USER_DATA["phone"])

        # 4. Facility (Kendo Dropdown)
        print("\n Filling Facility")
        fill_kendo_dropdown(driver, SELECTORS["facility_input"], USER_DATA["facility"])
        time.sleep(2)  # Wait for building list to potentially update

        # 5. Building (Kendo Dropdown)
        print("\n Filling Building")
        fill_kendo_dropdown(driver, SELECTORS["building_input"], USER_DATA["building"])
        time.sleep(2)

        # 6. Floor (Kendo Dropdown) - Optional
        if USER_DATA["floor"]:
            print("\n Filling Floor")
            fill_kendo_dropdown(driver, SELECTORS["floor_input"], USER_DATA["floor"])
            time.sleep(1)

        # 7. Room (Kendo Dropdown)
        print("\n Filling Room")
        fill_kendo_dropdown(driver, SELECTORS["room_input"], USER_DATA["room"])

        # 8. Request Type (Kendo Dropdown) - Optional
        if USER_DATA["request_type"]:
            print("\n Filling Request Type")
            fill_kendo_dropdown(driver, SELECTORS["request_type_input"], USER_DATA["request_type"])

        # 9. Action Requested (Text Area)
        print("\n Filling Action Requested")
        fill_text_field(driver, SELECTORS["action_input"], USER_DATA["action_requested"])

        # 10. Scroll down to make the Save button visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # 11. Auto-click the Save button
        print("\n Clicking Save button...")
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, SELECTORS["save_button"])))
        save_button.click()
        
        print("\n" + "="*50)
        print("Form submitted!")
        print("="*50)
        
        # Wait a moment to let the submission process
        time.sleep(3)
        
        return True

    except Exception as e:
        print(f"\n An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        driver.quit()
        print("Browser closed.")


def main():
    """Main loop - runs continuously until stopped with Ctrl+C."""
    submission_count = 0
    delay_between_submissions = 10  # seconds
    
    print("="*50)
    print("AUTO-SUBMIT BOT STARTED")
    print("Press Ctrl+C to stop")
    print("="*50)
    
    try:
        while True:
            submission_count += 1
            print(f"\n{'='*50}")
            print(f"SUBMISSION #{submission_count}")
            print(f"{'='*50}")
            
            success = run_single_submission()
            
            if success:
                print(f"\n Submission #{submission_count} completed!")
            else:
                print(f"\n Submission #{submission_count} failed, retrying...")
            
            print(f"\n Waiting {delay_between_submissions} seconds before next submission...")
            time.sleep(delay_between_submissions)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*50)
        print(f"BOT HAS STOPPED")
        print(f"Total submissions attempted: {submission_count}")
        print("="*50)


if __name__ == "__main__":
    main()