from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import sqlite3

def main():
	driver = webdriver.PhantomJS()
	driver.get("https://www.inc.com/inc5000/list/2018")
	#allLinks will store the list of all the URLs for the company profiles
	allLinks = []
	#this loop gathers all company profile URLs
	for i in range(1,101):
		page = bs(driver.page_source, 'html.parser')
		links = page.find_all('tr', {'class':'jss45'})
		for link in links:
			try:
				allLinks.append(link.find('a').get('href'))
			except AttributeError:
				continue
		driver.find_element_by_xpath("//*[@id='app']/div/div/div[2]/div/div/div[1]/div/div[1]/button[2]").click()
	print("done with collecting company profile URLs")
	#This portion of the code iterates through all the gathered links and pulls the information we want from each link
	companyInfo = []
	for link in allLinks:

		#Open the Company profile of each company
		driver.get(link)
		companyProfile = bs(driver.page_source, 'html.parser')
		#Rank
		try:
			rank = companyProfile.find("dl", {"class": "rank"}).find("dd").text
		except AttributeError:
			rank = "couldn't find"
		#Company Name
		try:
			name = companyProfile.find("h1").text
		except AttributeError:
			name = "couldn't find"
		#Leadership
		try:
			leader = companyProfile.find("dl", {"class": "leadership"}).find("dd").text
		except AttributeError:
			leader = "couldn't find"
		#2017 Revenue
		try:
			revenue = companyProfile.find("dl", {"class": "revenue"}).find("dd").text
		except AttributeError:
			revenue = "couldn't find"
		#Industry
		try:
			industry = companyProfile.find("dl", {"class": "ifi_industry"}).find("dd").text
		except AttributeError:
			industry = "couldn't find"
		#Founded
		try:
			founded = companyProfile.find("dl", {"class": "ifc_founded"}).find("dd").text
		except AttributeError:
			founded = "couldn't find"
		#3-year growth
		try:
			growth = companyProfile.find("dl", {"class": "growth"}).find("dd").text
		except AttributeError:
			growth = "couldn't find"
		#Location
		try:
			location = companyProfile.find("dl", {"class": "location"}).find("dd").text
		except AttributeError:
			location = "couldn't find"
		#Employees
		try:
			employees = companyProfile.find("dl", {"class": "employees"}).find("dd").text
		except AttributeError:
			try:
				employees = companyProfile.find("dl", {"class": "ifc_company_size"}).find("dd").text
			except AttributeError:
				employees = "couldn't find"
		companyInfo.append([rank, name, leader, revenue, industry, founded, growth, location, employees])

	#convert companyInfo to a DataFrame
	companydf = pd.DataFrame(companyInfo, columns = ["Rank", "CompanyName", "Leadership", "2017Revenue", "Industry", "Founded", "Growth", "Location", "Employees"])
	
	#to convert the companyInfo dataframe to a sqlite3 database	
	conn = sqlite3.connect("inc2018.db")
	companydf.to_sql('company', conn)
	
	
	#to close all connections
	driver.close()
	conn.close()
	
if __name__ == "__main__":
	main()
	
	
	
