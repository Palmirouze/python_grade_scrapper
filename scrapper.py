from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup

#todo
#put own credentials
userNetname = "ENTER YOURS HERE"
userPassword = "SAME THING"

gradeSelectionList = ["SSR_DUMMY_RECV1$sels$0$$0", "SSR_DUMMY_RECV1$sels$1$$0", "SSR_DUMMY_RECV1$sels$2$$0", "SSR_DUMMY_RECV1$sels$3$$0", "SSR_DUMMY_RECV1$sels$4$$0", "SSR_DUMMY_RECV1$sels$5$$0", "SSR_DUMMY_RECV1$sels$6$$0", "SSR_DUMMY_RECV1$sels$7$$0", "SSR_DUMMY_RECV1$sels$8$$0"]



driver = webdriver.Chrome(executable_path="/Users/Palmirouze/Desktop/concordia grade scrapping/chromedriver")

driver.get("https://my.concordia.ca")


netnameBox = driver.find_element_by_xpath('//*[@id="userid"]')
passwordBox = driver.find_element_by_id("pwd")
netnameBox.send_keys(userNetname)
passwordBox.send_keys(userPassword)
driver.find_element_by_class_name("form_button_submit").click()

#todo better time management
time.sleep(1)
driver.find_element_by_id("fldra_CU_MY_STUD_CENTRE").click()
time.sleep(1)
driver.find_element_by_partial_link_text("View My Grades").click()
time.sleep(1)

#selects a grade from the radio buttons available
#top of the list is semesterNumber = 0, second element is 1 etc.
#number of courses is the number of course per specific semester
def getGradesForSemester(semesterNumber, numberOfCourses):
    driver.switch_to.frame("ptifrmtgtframe")
    driver.find_element_by_id(gradeSelectionList[semesterNumber]).click()
    driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()
    driver.implicitly_wait(3)
    scrapeGrades(numberOfCourses)


    #driver.find_element_by_id("DERIVED_SSS_SCT_SSS_TERM_LINK").click()


def scrapeGrades(numberOfCourses):
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.implicitly_wait(3)

    i = 0
    while(i < numberOfCourses):
        print(soup.find(id="CLS_LINK$" + str(i)).get_text())
        print(soup.find(id="DERIVED_SSS_HST_DESCRSHORT$" + str(i)).get_text())
        i = i+1

    time.sleep(1)
    driver.find_element_by_id("ICTAB_1_52").click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.implicitly_wait(3)

    for distribution in soup.find_all("span", class_="PSEDITBOX_DISPONLY"):
        print(distribution.get_text())




#ids to get course name
#CLS_LINK$0


#class to get your grade
#PABOLDTEXT





getGradesForSemester(5, 4)











    #requests and bs4
#import requests

# url to get downloaded
#page = requests.get("http://www.google.ca")

#print(page.content)