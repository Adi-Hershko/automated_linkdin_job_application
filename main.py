import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# ! pip install selenium

# This is the jobs search result page, you can change the search parameters to your needs
# Be aware that in order for it to work, you must turn on the "Easy Apply" option in the search parameters
search_result = "Some linkdin job search result page"

# Opening up our page using chrome
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(search_result)
driver.maximize_window()
time.sleep(3)

def auto_login(username, password):
    try:
        # Automatically clicking on the "Sign in" button
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Sign in")))
        element.click()
    except:
        print("Couldn't find the element")
        return False
    try:
        # Filling in the login form
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys(username)
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)
        return True

    except:
        print("Can't login - check your credentials")
        return False

def find_additional_questions():
    try:
        # Checking if there are additional questions        
        h3 = driver.find_elements(By.TAG_NAME, "h3")
        for h in h3:
            text = h.text
            print("*****************" + text + "*****************")
            if text == "Additional Questions":
                print("Text found, trying to close the window")
                exit_current_window()
                return True
        return False
    except:
        print("Couldn't find text")
        return False

def exit_current_window():
    # Exiting current window
    try:
        # Pressing "Esc" button
        try:
            # Simulate pressing the Esc key
            actions = ActionChains(driver)            
            actions.send_keys(Keys.ESCAPE)
            actions.perform()            
            print("Esc button pressed")
            time.sleep(2)
        except:
            print("Couldn't press the Esc button")
            return False
        
        # Pressing the "Discard" button
        try:
            driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[3]/button[1]/span").click()
            time.sleep(2)
            print("Discard button pressed")
        except:
            print("Couldn't find the discard button")
            return False
        
        print("Window closed")
        return True
    except:
        print("Couldn't close the window - random error")
        return False

def short_form(to_follow = False):
    choose_resume_button = driver.find_element(By.LINK_TEXT, "Choose")
    submit_application_button = driver.find_element(By.LINK_TEXT, "Submit application")
    if choose_resume_button != None and submit_application_button != None:
        if not to_follow:
            follow_tick = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/div/footer/div[1]/label")
            if follow_tick != None:
                follow_tick.click()
                time.sleep(2)
                print("Follow tick disabled")
            else:
                time.sleep(2)
                print("Couldn't find the follow button")
        choose_resume_button.click()
        time.sleep(2)
        print("Resume selected")
        submit_application_button.click()
        time.sleep(2)
        print("Application submitted")
        return True
    else:
        print("Couldn't find the choose resume button or the submit application button")
        return False

def apply_to_job(to_follow = False):
        # Looping through all the jobs
        for i in range(1,25):

            job = driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[" + str(i) + "]/div/div[1]")
            if job == None:
                print("Couldn't find job")
                break
            # Clicking on the job - selecting it
            job.click()
            time.sleep(2)                        

            try:
                # Clicking on the "Easy Apply" button
                driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/div/div/div/button/span").click()
                time.sleep(2)
            except:
                print("Couldn't find the easy apply button")
                time.sleep(2)
                continue

            print("Checking if the job is a short form")
            # Checking if the job is a short form
            if short_form():
                print("************* Short form *************")
                continue
            
            # Clciking on the "Next" button
            
            # If there are additional questions, the "Next" button won't appear
            if find_additional_questions():
                print("There are additional questions")            
                time.sleep(2)
                continue

            # There are no additional questions
            next_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button/span")
            if next_button != None:
                next_button.click()
                time.sleep(2)            

            else:
                print("Couldn't find the next button")
                time.sleep(2)


            # If there are additional questions, the "Choose Resume" button won't appear
            if find_additional_questions():
                print("There are additional questions")
                time.sleep(2)
                continue
            
            # Clicking on the "Choose resume" button
            resume_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/div/div[1]/div/div/div/div[2]/button[1]/span")
            if resume_button != None:
                resume_button.click()
                time.sleep(2)
            else:
                print("Couldn't find the 'Choose resume' button")
                time.sleep(2)                
                        
            # If there are additional questions, the "Review" button won't appear
            if find_additional_questions():
                print("There are additional questions")
                time.sleep(2)
                continue

            # Clicking on the "Review" button - if there are additional questions, the "Review" button won't apepar
            review_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]/span")
            if review_button != None:
                review_button.click()
                time.sleep(2)
            else:
                print("Couldn't find the review button")
                time.sleep(2)
            
            # Disable the check sign on the "Follow" button
            if not to_follow:
                    if find_additional_questions():
                        print("There are additional questions")
                        time.sleep(2)
                        continue

                    follow_tick = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/div/footer/div[1]/label")
                    if follow_tick != None:
                        follow_tick.click()
                        time.sleep(2)
                        print("Follow tick disabled")
                    else:
                        time.sleep(2)
                        print("Couldn't find the follow button")
                                
            if find_additional_questions():
                print("There are additional questions")
                time.sleep(2)
                continue

            submit_button = driver.find_element(By.LINK_TEXT, "Submit")
            submit_application_button = driver.find_element(By.LINK_TEXT, "Submit application")

            if submit_button != None:
                submit_button.click()
                time.sleep(2)
                print("Submit button pressed")
            elif submit_application_button != None:
                submit_application_button.click()
                time.sleep(2)
                print("Submit application button pressed")
            else:
                print("Couldn't find the submit button")
                exit_current_window()
                time.sleep(2)
                continue
            

            # Pressing "Esc" button
            try:
                # Simulate pressing the Esc key
                time.sleep(2)
                actions = ActionChains(driver)            
                actions.send_keys(Keys.ESCAPE)
                actions.perform()            
                print("Esc button pressed")
                time.sleep(2)
            except:
                print("Couldn't press the Esc button")
                return False


success = auto_login("YOUR_EMAIL", "YOUR_PASSWORD")

if success:
    sucess = apply_to_job()

driver.quit()