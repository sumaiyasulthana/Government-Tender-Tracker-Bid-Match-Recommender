import requests
from bs4 import BeautifulSoup
import sqlite3

def fetch_cppp_tenders():
    url = 'https://gem.gov.in/cppp'
    response = requests.get(url)
    tenders = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tender_rows = soup.find_all('tr')
        for row in tender_rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                tenders.append({ 'Opening_Date': cells[0].text.strip(),
                    'Closing_Date': cells[1].text.strip(),'e_Published_Date': cells[2].text.strip(), 
                    'title': cells[3].text.strip(),
                    'Organisation': cells[4].text.strip(),
                    'source_portal': 'CPPP'
                })
    return tenders
