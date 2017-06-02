from selenium import webdriver
from bs4 import BeautifulSoup
import time

#You need to install ChromeDriver and use Python 3.xx with Selenium and BeautifulSoup

# ------  put your own credentials here ------
userNetname = "xxxx"
userPassword = "xxxx"


gradeList = []
driver = webdriver.Chrome(executable_path="/Users/Palmirouze/Desktop/python_grade_scrapper/chromedriver")
driver.get("https://my.concordia.ca")

netnameBox = driver.find_element_by_xpath('//*[@id="userid"]')
passwordBox = driver.find_element_by_id("pwd")

netnameBox.send_keys(userNetname)
passwordBox.send_keys(userPassword)

driver.find_element_by_class_name("form_button_submit").click()
time.sleep(1)
driver.find_element_by_id("fldra_CU_MY_STUD_CENTRE").click()
time.sleep(1)
driver.find_element_by_partial_link_text("View My Grades").click()
time.sleep(1)

driver.switch_to.frame("ptifrmtgtframe")

#selects a grade from the radio buttons available
#top of the list is semesterNumber = 0, second element is 1 etc.
#number of courses is the number of course per specific semester
def getGradesForSemester(semesterNumber, numberOfCourses):
    driver.find_element_by_id("SSR_DUMMY_RECV1$sels$"+str(semesterNumber)+"$$0").click()
    driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()
    driver.implicitly_wait(3)
    scrapeGrades(numberOfCourses)

    #goes back to semester selection page
    driver.find_element_by_id("DERIVED_SSS_SCT_SSS_TERM_LINK").click()


#gets the data from one semester page
def scrapeGrades(numberOfCourses):
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.implicitly_wait(3)

    i = 0
    while(i < numberOfCourses):
        #get course number
        gradeList.append(soup.find(id="CLS_LINK$" + str(i)).get_text())
        #get own grade
        gradeList.append(soup.find(id="DERIVED_SSS_HST_DESCRSHORT$" + str(i)).get_text())
        i = i+1

    time.sleep(1)
    driver.find_element_by_id("ICTAB_1_52").click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.implicitly_wait(3)

    #get course grade distribution
    for distribution in soup.find_all("span", class_="PSEDITBOX_DISPONLY"):
        gradeList.append(distribution.get_text())



#first parameter is position of semester you want in the list in View My Grades
#second is the number of courses you took during this semester
getGradesForSemester(3, 3)
getGradesForSemester(4, 4)
getGradesForSemester(5, 4)
getGradesForSemester(6, 4)
getGradesForSemester(7, 2)
getGradesForSemester(8, 4)

#print all the data
for grades in gradeList:
    print(grades)

#this data can be plugged in excel to plot
#will eventually add excel export