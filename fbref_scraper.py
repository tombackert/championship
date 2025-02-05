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

def parse_table(table):
    """Extrahiert Daten aus einer HTML-Tabelle mit komplexen Headern"""
    headers = []
    rows = []
    
    # Header-Verarbeitung
    header_rows = table.find_all('thead')
    for hr in header_rows:
        cols = hr.find_all(['th', 'td'])
        headers = [col.get('aria-label') or col.text.strip() for col in cols]
    
    # Datenzeilen
    body = table.find('tbody')
    for row in body.find_all('tr'):
        cells = row.find_all(['th', 'td'])
        row_data = [cell.text.strip() for cell in cells]
        rows.append(row_data)
    
    return headers, rows

def save_data(season, table_name, headers, rows):
    save_path = f'{OUTPUT_DIR}/{season}'
    os.makedirs(save_path, exist_ok=True)
    
    filename = f'{table_name.lower().replace(" ", "_")}.csv'
    with open(f'{save_path}/{filename}', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    html = fetch_page(BASE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Saisoninformation extrahieren
    season = soup.select_one('h1 span').text.split('-')[0].strip()
    
    # Alle relevanten Tabellen finden
    tables = soup.select('table.stats_table')
    
    for i, table in enumerate(tables):
        table_name = table.get('id') or f'table_{i+1}'
        headers, rows = parse_table(table)
        
        if headers and rows:
            save_data(season, table_name, headers, rows)
            
    print(f'Successfully scraped {len(tables)} tables for season {season}')

if __name__ == "__main__":
    main()