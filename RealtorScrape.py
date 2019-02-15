from selenium import webdriver as wd
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random

driver = wd.Firefox()

# Temporary quote page for testing capture of dynamic ID's
quote_page = "https://www.realtor.com/realestateandhomes-search/Minneapolis_MN/price-155000-161999"



driver.get(quote_page)
webURL = []
cityName = []
sqFoot = []
propertyDate = []
propertyEvent = []
propertyPrice = []
propTaxYearList = []
propTaxList = []
propTotalAssessmentList = []
primaryID = 159

# CSV's declared and opened here
tableCity = r'C:\Users\lkinneberg\Desktop\swc-python\TableCity.csv'
tablePropEvents = r'C:\Users\lkinneberg\Desktop\swc-python\TablePropEvents.csv'
tableTaxHistory = r'C:\Users\lkinneberg\Desktop\swc-python\TableTaxHistory.csv'
csv1 = open(tableCity, "w")
csv2 = open(tablePropEvents, "w")
csv3 = open(tableTaxHistory, "w")

# The number of houses are captured to determine the number of loops that need to be done.
houseComp = ''
numHouses = '/html[1]/body[1]/div[5]/div[2]/div[1]/div[1]/div[2]/section[1]/div[2]/div[1]/span[1]'
NumberHouses = driver.find_element_by_xpath(numHouses).text

for i in NumberHouses:
    if i.isdigit():
        houseComp += i
print (houseComp)

# The links are captured for each house below and loaded into a list.
while True:
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "element_id")))
    except TimeoutException:
        print("Timeout Exception")

    elems = driver.find_elements_by_xpath("//a[@href]")

    for elem in elems:
        try:
            if 'realestateandhomes-detail' in elem.get_attribute("href") and elem.get_attribute("href") not in webURL \
                and len(webURL) < int(houseComp):
                webURL.append(elem.get_attribute("href"))
        except StaleElementReferenceException:
            print("href stale element")
    try:
        driver.find_element_by_xpath("//a[@title='Go to next page']//i[@class='ra ra-chevron-right']").click()
        print('Going to next page')
    except NoSuchElementException:
        break

for i in webURL:
    print (i)

for urlAdd in webURL:
    # Web page is loaded here. Random iterations for page load to prevent website detections.
    randint = random.randint(15, 52)
    try:
        element = WebDriverWait(driver, randint).until(EC.presence_of_element_located((By.ID, "element_id")))
    except TimeoutException:
        print("Timeout Exception")

    print (urlAdd)
    newPage = urlAdd
    driver.get(newPage)
    primaryID += 1
    """ Name City Done Here"""
    row = str(primaryID) + ','
    # Squarefootage and City name are captured and loaded into a CSV in first loop
    try:
        city = '/html/body/div[5]/div[4]/div[2]/div[2]/div/section[1]/div[1]/div[2]/div[2]/div/div[2]' \
                   '/div/h1/span[2]'
        cityName.append(driver.find_element_by_xpath(city).text)
        row += driver.find_element_by_xpath(city).text + ','
    except NoSuchElementException:
        print ("No such element city name not found")
        continue

    try:
        sqFt = "/html/body/div[5]/div[4]/div[2]/div[2]/div/section[1]/div[1]/div[2]/div[2]/div/div[1]/ul/li[3]/span"
        sqFoot.append(driver.find_element_by_xpath(sqFt).text)
        row += driver.find_element_by_xpath(sqFt).text + ','
    except NoSuchElementException:
        print ("No such element sq foot not found")

    row += urlAdd + '\n'
    print(row)
    csv1.write(row)
    """ Property History """
    """ Property Date (Multiple possible items)"""
    increment = 0  # Default value was 1 where increment was

    while True:
        # This nested loop captures the Listing History for the property. Because there are multiple listing's per
        # property the loop will capture all data requred and load to a CSV by primary ID.
        increment += 1
        print ("Grabbing prop values")
        row = str(primaryID) + ','

        try:
            propPrice = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[6]/div[1]/div/div/table/" \
                        "tbody/tr[" + str(increment) + "]/td[3]"
            propertyPrice.append(driver.find_element_by_xpath(propPrice).text)
            var1 = driver.find_element_by_xpath(propPrice).text
            varTrans = ''
            for i in var1:
                if i.isdigit():
                    varTrans += i
            row += str(varTrans) + ','
        except NoSuchElementException:
            try:
                propPrice = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[7]/div[1]/div/div/table/" \
                            "tbody/tr[" + str(increment) + "]/td[3]"
                propertyPrice.append(driver.find_element_by_xpath(propPrice).text)
                var1 = driver.find_element_by_xpath(propPrice).text
                varTrans = ''
                for i in var1:
                    if i.isdigit():
                        varTrans += i
                row += str(varTrans) + ','
            except NoSuchElementException:
                break


        try:
            propDate = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[6]/div[1]/div/div/" \
                       "table/tbody/tr[" + str(increment) + "]/td[1]"
            propertyDate.append(driver.find_element_by_xpath(propDate).text)
            row += driver.find_element_by_xpath(propDate).text + ','
        except NoSuchElementException:
            try:
                propDate = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[7]/div[1]/div/div/" \
                           "table/tbody//tr[" + str(increment) + "]/td[1]"
                propertyDate.append(driver.find_element_by_xpath(propDate).text)
                row += driver.find_element_by_xpath(propDate).text + ','
            except NoSuchElementException:
                print("no prop date found")

        try:
            propEvent = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[6]/div[1]/div/div/table/" \
                        "tbody/tr[" + str(increment) + "]/td[2]"
            propertyEvent.append(driver.find_element_by_xpath(propEvent).text)
            row += driver.find_element_by_xpath(propEvent).text
        except NoSuchElementException:
            try:
                propEvent = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[7]/div[1]/div/div/table/tbody" \
                            "/tr[" + str(increment) + "]/td[2]"
                propertyEvent.append(driver.find_element_by_xpath(propEvent).text)
                row += driver.find_element_by_xpath(propEvent).text
            except NoSuchElementException:
                print("No propEvent found")

        row += '\n'
        print(row)
        csv2.write(row)

    increment = 0
    print ("entering next loop")
    while True:
        # The final nested loop is similar to above, except it captures the tax history for the property.
        increment += 1
        row = str(primaryID) + ','
        try:
            propTaxYear = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[6]/div[2]/div/div/table/" \
                          "tbody/tr[" + str(increment) + "]/td[1]"
            propTaxYearList.append(driver.find_element_by_xpath(propTaxYear).text)
            row += driver.find_element_by_xpath(propTaxYear).text + ','
        except NoSuchElementException:
            try:
                propTaxYear = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[7]/div[2]/div/div/" \
                              "table/tbody/tr[" + str(increment) + "]/td[1]"
                propTaxYearList.append(driver.find_element_by_xpath(propTaxYear).text)
                row += driver.find_element_by_xpath(propTaxYear).text + ','
            except NoSuchElementException:
                print("No such element Property tax year not found")
                break

        try:
            propTaxes = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[6]/div[2]/div/div/table/" \
                        "tbody/tr[" + str(increment) + "]/td[2]"
            propTaxList.append(driver.find_element_by_xpath(propTaxes).text)
            var1 = driver.find_element_by_xpath(propTaxes).text
            varTrans = ''
            for i in var1:
                if i.isdigit():
                    varTrans += i
            row += str(varTrans) + ','
        except NoSuchElementException:
            try:
                propTaxes = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[7]/div[2]/div/div/" \
                              "table/tbody/tr[" + str(increment) + "]/td[2]"
                propTaxList.append(driver.find_element_by_xpath(propTaxes).text)
                var1 = driver.find_element_by_xpath(propTaxes).text
                varTrans = ''
                for i in var1:
                    if i.isdigit():
                        varTrans += i
                row += str(varTrans) + ','
            except NoSuchElementException:
                print("No such element Property Taxes not found")

        try:
            propTotalAssessment = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[6]/div[2]/div/div/table/" \
                                  "tbody/tr[" + str(increment) + "]/td[7]"
            propTotalAssessmentList.append(driver.find_element_by_xpath(propTotalAssessment).text)
            var1 = driver.find_element_by_xpath(propTotalAssessment).text
            varTrans = ''
            for i in var1:
                if i.isdigit():
                    varTrans += i
            row += str(varTrans) + ','
        except NoSuchElementException:
            try:
                propTotalAssessment = "/html/body/div[5]/div[4]/div[2]/div[2]/div/div[7]/div[2]/div/div/" \
                              "table/tbody/tr[" + str(increment) + "]/td[7]"
                propTotalAssessmentList.append(driver.find_element_by_xpath(propTotalAssessment).text)
                var1 = driver.find_element_by_xpath(propTotalAssessment).text
                varTrans = ''
                for i in var1:
                    if i.isdigit():
                        varTrans += i
                row += str(varTrans)
            except NoSuchElementException:
                print("No such Property total assessment not found")

        row += '\n'
        print(row)
        csv3.write(row)

print ('Code finished executing')

csv1.close()
csv2.close()
csv3.close()
