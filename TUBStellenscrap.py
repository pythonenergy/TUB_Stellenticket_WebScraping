import requests
from bs4 import BeautifulSoup
import csv
import re


def url_soup(url):
    page = requests.get(url).content
    soup_page = BeautifulSoup(page, 'lxml')

    return soup_page


def job_extractor(soup_page, researchjobs= False):

    if researchjobs:
        job_type = 'jobs_science'
    else:
        job_type = 'jobs_companies'

    jobs_companies = soup_page.find('table', id=job_type).tbody
    jobs_companies_list = jobs_companies.find_all('tr', class_='offer_list_tr')

    for job in jobs_companies_list:
        try:
            company = job.find('td', class_=re.compile("cleared name_td small-none*")).text
            jobtitle = job.find('td', class_=re.compile("column_heading offer_list_td*")).text
            dateposted = job.find('div', class_="offer_still_searching_box").text
            company = str(company).replace('­', '')
            jobtitle = str(jobtitle).replace('­', '')
            print('Company: ', company)
            print('Job:', jobtitle)
            print('Post Date :', dateposted)
            # print(company, title)
        except:
            print('Error skipped')

    next_pages = soup_page.find_all('a', class_="weiter pagechange")

    if researchjobs:
        next_page = next_pages[1]['href']
    else:
        next_page = next_pages[0]['href']

    return next_page


# URL for full time jobs in Berlin
# url = 'https://tub.stellenticket.de/de/offers/results/workplacecity/Berlin/worktype/118%2C119%2C121%2C120%2C122%2C117%2C216%2C218/'

url = 'https://tub.stellenticket.de/de/offers/'

for i in range(10):
    print('Extract round :', i)
    soup_page= url_soup(url)
    nexturl = job_extractor(soup_page,researchjobs= True)
    if url == nexturl:
        print("Exhausted the search results")
        break
    else:
        url = nexturl
