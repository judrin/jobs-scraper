import requests
import helper
from datetime import datetime
from constants import JOB_SITE_INDEED_ID, REQUEST_HEADERS
from bs4 import BeautifulSoup

LIMIT = 50
BASE_URL = 'https://ca.indeed.com'
SEARCH_LOCATION = 'Canada'
SEARCH_POSITION = 'developer'


search_url = f'{BASE_URL}/jobs/?q={SEARCH_POSITION}&l={SEARCH_LOCATION}&limit={LIMIT}&sort=date'


def extract_job(html):
    title = html.find('h2', {'class': 'jobTitle'}).find(
        'span', {'title': True})['title']
    company_tag = html.find('span', {'class': 'companyName'})

    if company_tag is None:
        company_tag = html.find('a', {'class': 'companyOverviewLink'})

    company = company_tag.get_text().strip()
    location = html.find(
        'div', {'class': 'companyLocation'}).get_text().strip()
    job_id = html['data-jk']

    return {'job_id': job_id, 'title': title, 'company': company, 'location': location, 'link': f'{BASE_URL}/viewjob?jk={job_id}'}


def extract_jobs(last_index, last_job_id):
    jobs = []
    index = last_index + 1

    response = requests.get(
        search_url, headers=REQUEST_HEADERS, proxies=helper.get_proxies())
    soup = BeautifulSoup(response.text, 'html.parser')
    parsed_pages = soup.find_all('a', {'class': 'tapItem'})

    for page in reversed(parsed_pages):
        job = extract_job(page)

        if job['job_id'] == last_job_id:
            print(f'found duplicated item[{job["job_id"]}]')
            break

        job['site_id'] = JOB_SITE_INDEED_ID
        job['doc_id'] = index
        job['created_at'] = int(round(datetime.now().timestamp()))
        jobs.append(job)
        index += 1

    return jobs


def get_jobs(last_index, last_job_id):
    return extract_jobs(last_index, last_job_id)
