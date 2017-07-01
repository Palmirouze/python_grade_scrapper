# DEPENDENCIES
# - ChromeDriver
# - Selenium
# - BeautifulSoup
# - Python 3.x

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

# USER CREDENTIALS
USER_NAME = "X_XXXXX"
USER_PASSWORD = "XXXXXXXXXX"
CHROME_DRIVER_PATH = "XXXXXXXXXX"


#gets all the grades for a specific semester and number of courses taken this semester
def getGradesForSemester(semesterNumber, numberOfCourses):
    driver.find_element_by_id("SSR_DUMMY_RECV1$sels$"+str(semesterNumber)+"$$0").click()
    driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()
    driver.implicitly_wait(3)

    #scrapes all the grades
    scrapeGrades(numberOfCourses)

    #goes back to semester selection page
    driver.find_element_by_id("DERIVED_SSS_SCT_SSS_TERM_LINK").click()


#gets the data from one semester page
def scrapeGrades(numberOfCourses):
    time.sleep(SLEEP_TIME)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.implicitly_wait(3)

    i = 0
    while(i < numberOfCourses):
        #get course number
        gradeList.append(soup.find(id="CLS_LINK$" + str(i)).get_text())
        #get own grade
        gradeList.append(soup.find(id="DERIVED_SSS_HST_DESCRSHORT$" + str(i)).get_text())
        i = i+1

    time.sleep(SLEEP_TIME)
    driver.find_element_by_id("ICTAB_1_52").click()
    time.sleep(SLEEP_TIME)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.implicitly_wait(3)

    #get course grade distribution
    count = 0
    for distribution in soup.find_all("span", class_="PSEDITBOX_DISPONLY"):

        if(count == 0):
            tempGradeList = []

        tempGradeList.append(distribution.get_text())
        count = count + 1

        if(count == 17):
            distributionList.append(tempGradeList)
            count = 0


def mergeLists():
    i = 0
    for elements in distributionList:
        elements.insert(0, gradeList[i])
        i = i + 1
        elements.insert(2, gradeList[i])
        i = i + 1

def outputToCSV():
    with open("output.csv", "w") as f:
        writer = csv.writer(f)

        writer.writerow(gradeLegend)

        for lists in distributionList:
            writer.writerow(lists)


#MAIN

#Increase sleep time if connexion is slow
SLEEP_TIME = 0.3

gradeList = []
distributionList = []
gradeLegend = ["COURSE NUMBER", "COURSE NAME", "GRADE", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+",
               "D", "D-", "F", "FNS", "R", "NR"]

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get("https://my.concordia.ca")

# login
netnameBox = driver.find_element_by_xpath('//*[@id="userid"]')
passwordBox = driver.find_element_by_id("pwd")
netnameBox.send_keys(USER_NAME)
passwordBox.send_keys(USER_PASSWORD)

# navigate to grade screen
driver.find_element_by_class_name("form_button_submit").click()
time.sleep(SLEEP_TIME)
driver.find_element_by_id("fldra_CU_MY_STUD_CENTRE").click()
time.sleep(SLEEP_TIME)
driver.find_element_by_partial_link_text("View My Grades").click()
time.sleep(SLEEP_TIME)
driver.switch_to.frame("ptifrmtgtframe")

#first parameter is position of semester you want in the list in View My Grades (Starts at 0)
#second is the number of courses you took during this semester
#example:
getGradesForSemester(0, 4) # winter 2018 - 4 courses
getGradesForSemester(1, 5) # fall 2017 - 5 courses
getGradesForSemester(2, 2) # summer 2017 - 2 courses
getGradesForSemester(3, 3) # winter 2017 - 3 courses
getGradesForSemester(4, 4)
getGradesForSemester(5, 4)
getGradesForSemester(6, 4)
getGradesForSemester(7, 2)
getGradesForSemester(8, 4)


mergeLists()

for grades in distributionList:
    print(grades)

outputToCSV()
