import os
import csv
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

BASE_URL = 'https://fbref.com/en/comps/9/Premier-League-Stats'
OUTPUT_DIR = 'datasets/fbref'

def fetch_page(url):
    headers = {'User-Agent': generate_user_agent(device_type="desktop")}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_advanced_table(table):
    # Extract headers with data-stat attributes
    headers = []
    for th in table.select('thead tr:not(.over_header) th'):
        if th.get('data-stat'):
            header_name = th.get('aria-label') or th.get_text(strip=True)
            headers.append({
                'key': th['data-stat'],
                'name': header_name.replace('/', '_')
            })

    rows = []
    for row in table.select('tbody tr'):
        row_data = {}
        for cell in row.find_all(['th', 'td']):
            if cell.name == 'th':
                # Extract team name from link
                if cell.find('a'):
                    row_data[cell['data-stat']] = cell.get_text(strip=True)
                else:
                    row_data[cell['data-stat']] = cell.get_text(strip=True)
            else:
                value = cell.get_text(strip=True).replace(',', '.')
                row_data[cell['data-stat']] = value
        rows.append(row_data)
    
    return headers, rows

def save_table_data(headers, rows, table_name, season):
    save_path = f'{OUTPUT_DIR}/{season}'
    os.makedirs(save_path, exist_ok=True)
    
    filename = f'{table_name}.csv'
    with open(f'{save_path}/{filename}', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[h['key'] for h in headers])
        writer.writerow({h['key']: h['name'] for h in headers})
        writer.writerows(rows)

def main():
    html = fetch_page(BASE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    
    season = soup.find('h1').get_text(strip=True).split(' ')[-1]
    table = soup.find('table', {'id': 'stats_squads_standard_for'})
    
    if table:
        headers, rows = parse_advanced_table(table)
        save_table_data(headers, rows, 'team_statistics', season)
        print(f'Successfully saved: {len(rows)} rows with {len(headers)} columns')
    else:
        print('Table not found')

if __name__ == "__main__":
    main()