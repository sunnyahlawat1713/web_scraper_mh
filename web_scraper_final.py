'''
Sunny Ahlawat
sunnyahlawat1713@gmail.com
9818610034
'''

# IMPORTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv


# INITIALIZING A CSV FILE FOR STORING THE DATA BY DEFINING THE COLUMN HEADS
csv_file = open('property_records_mh.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Project Name', 'Promoter Name', 'Last Modified Date', 'Project Status',
 'Proposed Date of Completion', 'Revised proposed date of completion', 'Project Type',
  'Number of buildings','Total Number of Apartments', 'Total Number of Booked Apartments'])




# INITIALIZING TWO WEB DRIVERS, ONE FOR THE FIRST 3 FIELDS, AND THE OTHER FOR THE REST
driver = webdriver.Chrome('C:/Users/Sunny Ahlawat/Desktop/chromedriver.exe')
driver_2 = webdriver.Chrome('C:/Users/Sunny Ahlawat/Desktop/chromedriver.exe')



# LOADING THE TARGET WEBSITE WITHIN THE DRIVER
driver.get('https://maharerait.mahaonline.gov.in/')



# CLICKING ON THE 'Search Project Details' button
search = driver.find_element_by_class_name("search-pro-details")
search.click()



element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "Promoter"))
)
element.click()# Clicking on the "Registered Projects" radio button

advsearch = driver.find_element_by_id("btnAdvance")
advsearch.click()# Clicking on "Advanced Search" button
time.sleep(2)

state = driver.find_element_by_id("State")
state.click()# Clicking on "State/UT" dropdown box

statemh = driver.find_element_by_xpath("//select[@id='State']/option[text()='MAHARASHTRA']")
statemh.click() # Selecting the state of Maharashtra
time.sleep(2)

district = driver.find_element_by_id("District")
district.click()# Clicking the "District" dropdown box

districtemh = driver.find_element_by_xpath("//select[@id='District']/option[text()='Mumbai Suburban']")
districtemh.click()# Selecting the "Mumbai Suburban" district
time.sleep(2)

advsearch = driver.find_element_by_id("btnSearch")
advsearch.click() # Clicking on "Search" option
def grab_records():

    page_rows = driver.find_elements_by_xpath('//*[@id="gridview"]/div[1]/div/table/tbody/tr')
  
    for row in page_rows:

        try:
            project_name = row.find_element_by_xpath('./td[@data-name = "Project"]').text
        except:
            project_name = 'NA'
        try:
            promoter_name = row.find_element_by_xpath('./td[@data-name = "Name"]').text
        except:
            promoter_name = 'NA'
        try:
            last_modified_date = row.find_element_by_xpath('./td[@data-name = "lastModifiedDate"]').text 
        except:
            last_modified_date = 'NA'
        try:
            link_to_next_page = row.find_element_by_xpath('./td//a[text() = " View"]').get_attribute('href')
        except:
            break    
        driver_2.get(link_to_next_page)
        try:
            project_status = driver_2.find_element_by_xpath('//*[@id="DivProject"]//div[label[contains(text(), "Project Status")]]/following-sibling::div[1]').text 
        except:
            project_status = "NA"
        try:
            prop_date_of_completion = driver_2.find_element_by_xpath('//*[@id="DivProject"]//div[label[contains(text(), "Proposed Date of Completion")]]/following-sibling::div[1]').text 
        except:
            prop_date_of_completion = "NA"
        try:
            rev_prop_date_of_completion = driver_2.find_element_by_xpath('//*[@id="DivProject"]//div[label[contains(text(), "Revised Proposed Date of Completion")]]/following-sibling::div[1]').text 
        except:
            rev_prop_date_of_completion = "NA"
        try:
            project_type = driver_2.find_element_by_xpath('//*[@id="DivProject"]//div[label[contains(text(), "Project Type")]]/following-sibling::div[1]').text 
        except:
            project_type = "NA"
        try:
            total_buildings = driver_2.find_element_by_xpath('//*[@id="DivProject"]//div[label[contains(text(), "Total Building Count")]]/following-sibling::div[1]').text 
        except:
            total_buildings = 'NA'

    # Initializing apartment variables
        total_apartments = 0
        total_booked_apartments = 0

    #Retrieving header row to find our index of "Number of Apartment" column
        apt_header_row = driver_2.find_elements_by_xpath('//*[@id="DivBuilding"]/div/table//table[contains(@class,"table-responsive")]/tbody/tr/th')
        header_index = 0                                    
        corr_index = 0
        for header_index in range(len(apt_header_row)):
            if apt_header_row[header_index].text == "Number of Apartment":
                corr_index = header_index + 1
                break 
        #print("Corr_index", corr_index)

    # Retrieving list of all numbers of apartments in a project
        total_aptmts_element = driver_2.find_elements_by_xpath(f"//*[@id='DivBuilding']/div/table//table[contains(@class,'table-responsive')]/tbody/tr/td[{corr_index}]")
        j = 0
        num_apt = 0
        for j in total_aptmts_element:
            num_apt = int(j.text)
            total_apartments += num_apt
        b_apt_header_row = driver_2.find_elements_by_xpath('//*[@id="DivBuilding"]/div/table//table[contains(@class,"table-responsive")]/tbody/tr/th')
        print(total_apartments)

    #Retrieving header row to find our index of "Number of Booked Apartment" column
        header_index_b = 0
        corr_index_b = 0
        for header_index_b in range(len(b_apt_header_row)):
            if b_apt_header_row[header_index_b].text == "Number of Booked Apartment":
                corr_index_b = header_index_b + 1
                break
        #print("Correct index B", corr_index_b)
        
    # Retrieving list of all numbers of booked apartments in a project
        total_booked_aptmts_element = driver_2.find_elements_by_xpath(f"//*[@id='DivBuilding']/div/table//table[contains(@class,'table-responsive')]/tbody/tr/td[{corr_index_b}]")
        k = 0
        num_booked_apt = 0
        for k in total_booked_aptmts_element:
            num_booked_apt = int(k.text)
            total_booked_apartments += num_booked_apt
        print(total_booked_apartments)
    
    # Writing retrieved records to the CSV file
        csv_writer.writerow([project_name, promoter_name,last_modified_date, project_status,
            prop_date_of_completion, rev_prop_date_of_completion, project_type,
            total_buildings, total_apartments, total_booked_apartments])
        

while True: # Iterating over all pages
    try:
        grab_records()
        next_pg = driver.find_element_by_xpath('//*[@id="btnNext"]') # Clicking to get the next page
        next_pg.click()
    except:
        break

driver.quit()
driver_2.quit()
csv_file.close()
