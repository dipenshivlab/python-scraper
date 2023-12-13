import os
import openpyxl
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs
import urllib.request
import ssl
from clutch_company.models import Company,Review

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context
# Automatically install and set up chromedriver
chromedriver_autoinstaller.install()


def get_webdriver(url, wait_count):
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    wait = webdriver.support.ui.WebDriverWait(driver, wait_count)
    return driver


def remove_query_params(url):
    parsed_url = urlparse(url)
    new_parsed_url = parsed_url._replace(query="")
    return urlunparse(new_parsed_url)


def process_review_page_data(url,company_object):
    content = get_webdriver(url, 5)

    temp_data = content.page_source
    soup = BeautifulSoup(temp_data, "html.parser")

    next_page_link = soup.find('button', class_="sg-pagination__link--icon-next")

    parent_tag = soup.find('div', id="reviews-list")
    listings = parent_tag.find_all('article', class_='profile-review')
    for listing in listings: 
        
        client_name = ''
        client_company = ''
        client_position = ''
        client_industry = ''
        employee_size = ''
        client_location = ''
        review_for = ''
        client_review = ''
        review_date = ''
        project_categories = ''
        project_budgets = ''
        project_duration = ''


        client_name_tag = listing.find('div', class_="reviewer_card--name")
        client_name = client_name_tag.get_text(strip=True) if client_name_tag else ''

        # Start getting client company name and position 
        client_position_tag = listing.find('div', class_="reviewer_position")
        if client_position_tag:
            positionValue = client_position_tag.get_text(strip=True)
            split_values = positionValue.split(', ')
            client_company = split_values[1] if split_values and len(split_values) >= 2 else ''
            client_position = split_values[0] if split_values and len(split_values) >= 1 else ''

        # Start getting client information
        review_list_tag = listing.find('ul', class_="reviewer_list")
        if review_list_tag:
            industryTag = review_list_tag.find('li', {'data-tooltip-content':"<i>Industry</i>"})
            locationTag = review_list_tag.find('li', {'data-tooltip-content':"<i>Location</i>"})
            employeeSizeTag = review_list_tag.find('li', {'data-tooltip-content':"<i>Client size</i>"})

            client_industry =  industryTag.get_text(strip=True) if industryTag else ''
            client_location =  locationTag.get_text(strip=True) if locationTag else ''
            employee_size =  employeeSizeTag.get_text(strip=True) if employeeSizeTag else ''

        review_for_tag = listing.find('div', class_="profile-review__header")
        review_for = review_for_tag.find('h4').get_text(strip=True) if review_for_tag else ''

       
        client_review_tag = listing.find('div', class_="profile-review__quote")
        client_review = client_review_tag.get_text(strip=True) if client_review_tag else '' # Update client review data

        review_date_tag = listing.find('div', class_="profile-review__date")
        review_date = review_date_tag.get_text(strip=True) if review_date_tag else '' # Update client review date

       
         # Start getting project details 
        project_tag = listing.find('ul', class_="data--list")
        if project_tag:
            category_tag = project_tag.find('span', class_="data--item__list")
            budget_tag = project_tag.find('li', {'data-tooltip-content': "<i>Project size</i>"})
            duration_tag = project_tag.find('li', {'data-tooltip-content': "<i>Project length</i>"})

            if category_tag:
                child_spans = category_tag.find_all('span')
                child_texts = [span.get_text(strip=True) for span in child_spans]
                project_categories = ', '.join(child_texts) # Update Project Category Data

            project_budgets = budget_tag.get_text(strip=True) if budget_tag else '' # Update Project Budgets Data
            project_duration = duration_tag.get_text(strip=True) if duration_tag else '' # Update Project Duration Data


       
        
        # sheet.append([client_name, client_company, client_position, client_industry, employee_size, client_location, review_for, client_review, review_date, project_categories, project_budgets, project_duration])
        # workbook.save(review_file_name)
        if not Review.objects.filter(company=company_object,client_name=client_name, client_company=client_company, position=client_position, industry=client_industry, employee_size=employee_size,location=client_location, review_for=review_for, review=client_review, review_date=review_date, project_category=project_categories, project_budgets=project_budgets,  project_duration=project_duration):
            Review.objects.create(company=company_object,client_name=client_name, client_company=client_company, position=client_position, industry=client_industry, employee_size=employee_size,location=client_location, review_for=review_for, review=client_review, review_date=review_date, project_category=project_categories, project_budgets=project_budgets,  project_duration=project_duration)

    content.quit()
    if next_page_link:
        next_page_number = next_page_link.get('data-page')
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params['page'] = [next_page_number]
        encoded_query = urlencode(query_params, doseq=True)
        next_page_link = urlunparse(parsed_url._replace(query=encoded_query))
        process_review_page_data(next_page_link, company_object)


def process_company_review(url, company_object, default_folder):
    # new_company_name = company_name.replace(' ', '_').lower()
    
    # folder_path = f"{default_folder}/reviews"
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)

    # workbook = openpyxl.Workbook()
    # sheet = workbook.active
    # sheet["A1"] = "Client Name"
    # sheet["B1"] = "Client Company"
    # sheet["C1"] = "Position"
    # sheet["D1"] = "Industry"
    # sheet["E1"] = "Employee Size"
    # sheet["F1"] = "Location"
    # sheet["G1"] = "Reviewer For"
    # sheet["H1"] = "Review"
    # sheet["I1"] = "Review Date"
    # sheet["J1"] = "Project Category"
    # sheet["K1"] = "Project Budgets"
    # sheet["L1"] = "Project Duration"

    # review_file_name = f"{folder_path}/{new_company_name}_reviews.xlsx"
    process_review_page_data(url, company_object)
    
def company_info(url):
    content = get_webdriver(url, 10)
    temp_data = content.page_source
    soup = BeautifulSoup(temp_data, "html.parser")
    
    linked_in_link = ''
    facebook_link = ''
    twitter_link = ''
    instagram_link = ''

    if soup:
        profile_social_tag = soup.find('div', class_="profile-social")
        if profile_social_tag:
                linked_in_tag = profile_social_tag.find('a',{'data-type':'linkedin'})
                facebook_tag = profile_social_tag.find('a',{'data-type':'facebook'})
                twitter_tag = profile_social_tag.find('a',{'data-type':'twitter'})
                instagram_tag = profile_social_tag.find('a',{'data-type':'instagram'})

                if linked_in_tag:
                    linked_in_link = linked_in_tag['href']
                
                if facebook_tag:
                    facebook_link = facebook_tag['href']
                
                if twitter_tag:
                    twitter_link = twitter_tag['href']
                
                if instagram_tag:
                    instagram_link = instagram_tag['href']

    content.quit()
    return {
        'linked_in_link': linked_in_link,
        'facebook_link': facebook_link,
        'twitter_link': twitter_link,
        'instagram_link': instagram_link,
    }

def process_page_data(url, file_name, page_file_name,init_page_count, final_page):
    content = get_webdriver(url, 10)

    temp_data = content.page_source
    soup = BeautifulSoup(temp_data, "html.parser")
    listings = soup.find_all('li', class_='provider provider-row')

    for listing in listings:
        company_name = ''
        company_website = ''
        company_location = ''
        company_review = ''
        company_min_budget = ''
        company_hourly_rate = ''
        company_employee_size = ''


        profile_url = ''
        company_data = []

        company_name_tag = listing.find('h3', class_="company_info")
        company_website_tag = listing.find('li', class_="website-link website-link-a")
        company_location_tag = listing.find('span', class_="locality")
        company_review_tag = listing.find('a', class_="reviews-link sg-rating__reviews directory_profile")
        company_min_budget_tag = listing.find('div',{'data-content':'<i>Min. project size</i>'})
        company_hourly_rate_tag = listing.find('div',{'data-content':'<i>Avg. hourly rate</i>'})
        company_employee_size_tag = listing.find('div',{'data-content':'<i>Employees</i>'})
    

        # Company name 
        if company_name_tag:
            company_name = company_name_tag.get_text(strip=True)
            profile_url = company_name_tag.find('a', class_="directory_profile")['href']
           
        # Company Website
        if company_website_tag:
            website_anchor = company_website_tag.find('a', class_="website-link__item")
            if website_anchor:
                parsed_url = urlparse(website_anchor['href'])
                company_website = remove_query_params(website_anchor['href'])
                
  
        # Company location
        if company_location_tag:
            company_location = company_location_tag.get_text(strip=True)

        if company_review_tag:
            company_review = company_review_tag.get_text(strip=True)
        
        if company_min_budget_tag:
            company_min_budget = company_min_budget_tag.get_text(strip=True)

        if company_hourly_rate_tag:
            company_hourly_rate = company_hourly_rate_tag.get_text(strip=True)

        if company_employee_size_tag:
            company_employee_size = company_employee_size_tag.get_text(strip=True)

        if company_name and profile_url:
                companyData = company_info(f"https://clutch.co{profile_url}")

        linked_in_link = companyData["linked_in_link"]

        print('- ',f"{company_name} - {company_review}")

        
        company_object,created=Company.objects.get_or_create(company_name=company_name, website=company_website, location=company_location, min_project_size=company_min_budget, hourly_rate=company_hourly_rate, employee_size=company_employee_size, linkedin_url=linked_in_link,position=file_name)
        # sheet.append([company_name, company_website, company_location, company_min_budget, company_hourly_rate, company_employee_size, linked_in_link])
        # workbook.save(f"{file_name}/{file_name}_{page_file_name}.xlsx")

        
        if company_name and profile_url and company_review:
            process_company_review(f"https://clutch.co{profile_url}", company_object, file_name)
        

    next_page_li = soup.find('li', class_='page-item next')
    content.quit()
    if next_page_li:
        next_link = "https://clutch.co" + next_page_li.find("a")['href']
        new_page = 0
        new_query_def = parse_qs(urlparse(next_link).query)

        if new_query_def:
            if 'page' in new_query_def:
                new_page = new_query_def['page'][0]

        if (int(final_page) - 1) == int(new_page):
            pass
            # new_file(next_link, init_page_count, file_name)
        else:
            # new_page_count = int(new_page) + int(init_page_count)
            new_page_count = final_page
            process_page_data(next_link,file_name, page_file_name,init_page_count, new_page_count)

# New Page function
def newFile(url, initPageCount, fileName):
    # workbook = openpyxl.Workbook()
    # sheet = workbook.active
    # sheet["A1"] = "Company Name"
    # sheet["B1"] = "Website"
    # sheet["C1"] = "Location"
    # sheet["D1"] = "Min. Project Size"
    # sheet["E1"] = "Hourly Rate"
    # sheet["F1"] = "Employee Size"
    # sheet["G1"] = "Linked In"
    if int(initPageCount) == 0:
        initPageCount = 1
    page = 0
    queryDef = parse_qs(urlparse(url).query)
    if queryDef:
        if 'page' in queryDef:
            page = queryDef['page'][0]
    page = int(page) + int(1)
    finalPage = int(page) + int(initPageCount)
   
    pageFileName = f"{int(page)}_to_{int(finalPage) - 1 }"
    process_page_data(url,fileName, pageFileName,initPageCount, finalPage)