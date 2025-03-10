from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd



def setup_driver():
    driver = webdriver.Chrome()
    driver.get("https://mate.academy/en")
    wait = WebDriverWait(driver, 5)
    actions = ActionChains(driver)
    return driver, wait, actions


def initialize_dataframe():
    return pd.DataFrame(columns=['name', 'link', 'description', 'format', 'num_modules', 'num_topics', 'duration'])


def get_course_list():
    # Click on the secondary button to access course list
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Button_secondary__pFIlL"))).click()
    
    # Get all course items
    course_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'DropdownProfessionsItem_link__4NmVV')))
    
    # Extract name and link for each course
    return [[item.text, item.get_attribute("href")] for item in course_list if item.text != '']


def fill_table(i, attempts):
    for attempt in range(attempts):
        try:
            # redicrect to course page
            driver.get(courses['link'][i])
            
            # get description
            courses['description'][i] = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "typography_landingTextMain__Rc8BD"))).text
            
            # get available formates
            formats = [item.text for item in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ButtonBody_buttonText__FMZEg")))]
            
            courses['format'] = courses['format'].fillna(value='')
            
            courses['format'][i] = ', '.join(filter(None, [
                "Full-time" if "I want to study full-time" in formats else None,
                "Flexible" if "I want to study flexibly" in formats else None
            ])) or 'No group openings'
            courses['format'][i] = courses['format'][i].lstrip(', ')
            
            # get number of modules
            button = driver.find_element(By.CLASS_NAME, "Button_neutral__ueX17")
            if button:
                actions.move_to_element(button).perform()
                button.send_keys(Keys.ENTER)
            modules = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "CourseModulesList_moduleListItem__HKJqw")))
            courses['num_modules'][i] = len(modules)
            
            # get number of topics
            topics = [item.text for item in wait.until(EC.presence_of_all_elements_located((By.XPATH, "//p[contains(@class, 'FactBlock_factDescription__Dy2k7') and contains(text(), 'Topics')]/preceding-sibling::p"))) if item.text != ''][0]
            courses['num_topics'][i] = topics
            
            # get duration of course   
            duration = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(text(), 'month')]")))
            duration = [item.text.split()[0] for item in duration if item.text != '']
            courses['duration'][i] = f"{duration[0]}-{duration[1]} months" if 'Full-time' in courses['format'][i] else f"{duration[1]} months"
            return
        except Exception as e:
            print(f"Page: {courses['name'][i]};\nAttempt: {attempt};\nError: {e}")


def process_all_courses(courses, max_attempts=3):
    for i in range(len(courses.index)):
        fill_table(i, max_attempts)
        
    
def main():
    global driver, wait, actions, courses
    
    driver, wait, actions = setup_driver()
    courses = initialize_dataframe()
    
    try:
        course_data = get_course_list()
        courses[['name', 'link']] = course_data
        
        process_all_courses(courses)
        
        print(courses)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()