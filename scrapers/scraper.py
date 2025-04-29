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
# df = pd.DataFrame(tenders)
# Step 2: Save scraped data into SQLite
def save_to_sqlite(tenders):
    conn = sqlite3.connect('tender_tracker.db')
    cursor = conn.cursor()


    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenders (
        id INTEGER PRIMARY KEY AUTOINCREMENT, Opening_Date DateTime, Closing_Date DateTime, e_Published_Date DateTime,
        title TEXT, Organisation Text ,source_portal Text,
        created_at DateTime
    )
    ''')

    # Insert data
    cursor.execute('''
    INSERT INTO tenders (ID, Opening_Date, Closing_Date, e_Published_Date,
        title, Organisation,source_portal,created_at)  VALUES (?,?,?,?,?,?,?,?)
    ''',tenders)

    conn.commit()
    conn.close()
    print(f"✅ Saved {len(tenders)} tenders to SQLite.")

# Step 3: Run the script
def main():
    tenders = fetch_cppp_tenders()
    if tenders:
        save_to_sqlite(tenders)
    else:
        print("No tenders found to save.")

if __name__ == "__main__":
    main()
