# scraper.py
import os
import csv
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from scraper.fbref_resources import OUTPUT_BASE_DIR, RESOURCES

def fetch_page(url):
    """Fetches the HTML content of the page."""
    headers = {'User-Agent': generate_user_agent(device_type="desktop")}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def clean_filename(name):
    """Creates a safe filename by removing special characters."""
    return "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in name)

def parse_table(table):
    """Parses a single table with complex structure."""
    headers = []
    for th in table.select('thead tr:not(.over_header) th'):
        if th.get('data-stat'):
            header_info = {
                'key': th['data-stat'],
                'name': th.get('aria-label') or th.get_text(strip=True),
                'type': 'team' if 'team' in th['data-stat'] else 'data'
            }
            headers.append(header_info)

    rows = []
    for row in table.select('tbody tr'):
        row_data = {}
        for cell in row.find_all(['th', 'td']):
            if cell.get('data-stat'):
                key = cell['data-stat']
                value = cell.get_text(strip=True)
                if key != 'team':
                    value = value.replace(',', '.').replace('−', '-')
                row_data[key] = value
        if row_data:
            rows.append(row_data)
    
    return headers, rows

def save_table(headers, rows, table_name, season, output_base_dir):
    """Saves the table data as a CSV file."""
    save_path = os.path.join(output_base_dir, season)
    os.makedirs(save_path, exist_ok=True)
    
    safe_name = clean_filename(table_name)
    filename = f'{safe_name}.csv'
    file_path = os.path.join(save_path, filename)
    
    if os.path.exists(file_path):
        print(f'File {filename} already exists. Overwriting...')
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[h['key'] for h in headers])
        writer.writerow({h['key']: h['name'] for h in headers})
        writer.writerows(rows)

def save_metadata(season, num_tables, output_base_dir, source_url):
    """Saves metadata about the scraping process."""
    metadata = {
        'scrape_date': datetime.now().isoformat(),
        'source_url': source_url,
        'tables_scraped': num_tables,
        'season': season
    }
    
    save_path = os.path.join(output_base_dir, season)
    os.makedirs(save_path, exist_ok=True)
    
    with open(os.path.join(save_path, '_metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

def process_all_tables(soup, season, output_base_dir):
    """Processes all tables on the page."""
    tables = soup.find_all('table', class_='stats_table')
    num_tables = 0
    
    for i, table in enumerate(tables):
        try:
            table_id = table.get('id') or f'table_{i+1}'
            table_name = table_id
        
            headers, rows = parse_table(table)
            
            if headers and rows:
                save_table(headers, rows, table_name, season, output_base_dir)
                print(f'Saved: {table_name:<40} ({len(headers):<2} cols)({len(rows):<2} rows)')
                num_tables += 1
            else:
                print(f'Skipped: {table_name:<40} (no data)')
                
        except Exception as e:
            print(f'Error processing table {table_id}: {str(e)}')
    
    return num_tables

def main():
    """Main function to scrape and save all tables for each resource."""
    print(f'Starting scraping process...\n')
    
    for resource in RESOURCES:
        season = resource['season']
        url = resource['url']
        
        print(f'Processing season: {season}')
        
        try:
            html = fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            num_tables = process_all_tables(soup, season, OUTPUT_BASE_DIR)
            save_metadata(season, num_tables, OUTPUT_BASE_DIR, url)
            
            print(f'\nScraping completed for season: {season}')
            print(f'Total tables processed: {num_tables}\n')
            
        except Exception as e:
            print(f'Error processing season {season}: {str(e)}')
            continue

if __name__ == "__main__":
    main()