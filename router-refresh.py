from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
#from webdriver_manager.chrome import ChromeDriverManager  <-- Uncomment To make it work on mac or linux

# --- 1. CONFIGURATION ---

ROUTER_URL = "http://192.168.8.1" 
PASSWORD = "IsThisMyPa$$WORD?"  # <-- REPLACE WITH YOUR PASSWORD
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# --- XPATHS ---
XPATH_PASSWORD_FIELD    = '//*[@id="login_password"]'
XPATH_LOGIN_BUTTON      = '//*[@id="login_btn"]'
XPATH_OPTIMIZE_LOCATION = '//*[@id="home_location_btn"]'
XPATH_START_TEST        = '//*[@id="test_location_btn"]'
XPATH_CANCEL_BUTTON     = '//*[@id="location_result_btn_cancel"]' 
XPATH_GO_HOME_BUTTON    = '//*[@id="goHomeBtn"]'

# --- 2. SCRIPT EXECUTION ---
driver = None
try:
    print("Starting router automation script...")
    
   # Initialize the Driver
   # service = ChromeService(ChromeDriverManager().install())

    chrome_options = Options()
    chrome_options.add_argument("--headless")         # Run the browser without a visible GUI
    chrome_options.add_argument("--no-sandbox")       # Bypass OS security model (essential for root/server execution)
    chrome_options.add_argument("--disable-dev-shm-usage") # Overcomes resource constraints in some environments

    service = ChromeService(CHROMEDRIVER_PATH)
    #driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(ROUTER_URL)
    
    # ----------------------------------------------------
    # PART A: LOGIN (PASSWORD ONLY LOGIN SCREEN)
    # ----------------------------------------------------
    print("\n--- A. Logging In ---")
    
    # Wait for the password field to be ready

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, XPATH_PASSWORD_FIELD))
    )
    
    # Enter the password
    driver.find_element(By.XPATH, XPATH_PASSWORD_FIELD).send_keys(PASSWORD)
    
    # Click the Login button
    driver.find_element(By.XPATH, XPATH_LOGIN_BUTTON).click()
    print(" Password entered and Login button clicked. Waiting for dashboard...")
    
    # Simple pause to allow the dashboard to load after login
    time.sleep(5) 
    
    # ----------------------------------------------------
    # PART B: FIRST CLICK: Optimize location Button
    # ----------------------------------------------------

    print("\n--- B. Starting Optimization Process ---")
    
    # Wait for the first button to become clickable
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_OPTIMIZE_LOCATION))
    ).click()
    
    print(" Clicked 'Optimize location'.")
    
    # Short pause for the new elements to appear
    time.sleep(5) 
    
    # ----------------------------------------------------
    # PART C: SECOND CLICK: Start Test Button
    # ----------------------------------------------------

    print("\n--- C. Starting Signal Test ---")
    
    # Wait for the SECOND button to become clickable
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_START_TEST))
    ).click()
    
    print(" Successfully started the signal strength test.")
    
    # Longer pause to let the test run
    print("Waiting 5 seconds for the test to complete before closing the browser...")
    time.sleep(5) 
    
   # print("\n--- D. Script Finished ---") 

    print("\n--- D. Test Run and Exit ---")

    TEST_DURATION = 20 # The test duration in seconds, as you specified
    print(f"Waiting {TEST_DURATION} seconds for the signal strength test to run...")
    time.sleep(TEST_DURATION) 
    print("Test duration complete.")

    # 1. Click the CANCEL button
    print("Attempting to click the CANCEL button...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_CANCEL_BUTTON))
    ).click()
    print(" Clicked CANCEL.")

    # Short pause for the page to transition
    time.sleep(2) 

    # 2. Click the GO TO HOME button
    print("Attempting to click the GO TO HOME button...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_GO_HOME_BUTTON))
    ).click()
    print(" Clicked GO TO HOME. Automation successfully completed all steps.")

except Exception as e:
    # This catch block specifically handles errors in the final exit steps
    print(f" Failed during the CANCEL or GO TO HOME steps.")
    print(f"Details: {e}")

finally:
    if driver:
        # Closes the browser window regardless of success/failure
        time.sleep(2) # Final visual pause
        driver.quit() 
        print("Browser session closed.")
