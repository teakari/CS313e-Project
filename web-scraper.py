from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-gpu")
options.add_argument("enable-automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")

url = "https://www.ratemyprofessors.com/search/professors/1255?q=*&did=?"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.get(url)

timeout = 20


# closes cookies and ads that first appear when going into the website
try:
    cookies_exit = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/button')))
    cookies_exit.click()
except TimeoutException:
    print("No cookies")

try:
    close_ad2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="IL_SR_X4"]/svg/g/path[2]')))
    close_ad2.click()
except TimeoutException:
    print("Timed Out")

try:
    close_ad = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bx-close-inside-1177612"]')))
    close_ad.click()
except TimeoutException:
    print("Unable to close--Timed out")


action = ActionChains(driver)
button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[4]/button')

# clicks the show more button until it is no longer visible
try:
    show_more = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[4]/button')))
    while show_more:
        action.move_to_element(button).click().perform()
        try:
            show_more = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[4]/button')))
        except StaleElementReferenceException:
            print("Hit a stalemate")
            break
        except TimeoutException:
            break

except TimeoutException:
    print("Timed Out Waiting for Page to Load")



in_department = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[1]/div/h1')
total = in_department[0].text.split()
total_professors = int(total[0])
print(total_professors)


num_ratings = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a/div/div[1]/div/div[2]')
reviews = []


for i in range(1, total_professors + 1):
    try:
        # finds prof name
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[1]')))
        name = driver.find_elements(By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[1]')

        # finds prof rating
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[1]/div/div[2]')))
        rating = driver.find_elements(By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[1]/div/div[2]')

        # finds prof department
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[2]/div[1]')))
        department = driver.find_elements(By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[2]/div[1]')

        # finds total number of ratings
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[1]/div/div[3]')))
        num_ratings = driver.find_elements(By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[1]/div/div[3]')

        # finds the percentage of students who would repeat the course
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[3]/div[1]/div')))
        would_repeat = driver.find_elements(By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[3]/div[1]/div')

        # finds the difficulty of the course rated out of 5
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[3]/div[3]/div')))
        difficulty = driver.find_elements(By.XPATH,
                '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div[3]/a[' + str(i) + ']/div/div[2]/div[3]/div[3]/div')

        professor_review = {'name': name[0].text,
                            'department': department[0].text,
                            'rating': rating[0].text,
                            'total_ratings': num_ratings[0].text,
                            'would take again': would_repeat[0].text,
                            'difficulty': difficulty[0].text}
        reviews.append(professor_review)

    except TimeoutException:
        break


df = pd.DataFrame(reviews)
# print(df)
df.to_csv('professors.csv')
