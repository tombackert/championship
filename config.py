import os

OUTPUT_BASE_DIR = os.path.join('datasets', 'fbref')

def generate_season_resources(start_year=1990, end_year=2024):
    """Generates a list of season resources to scrape."""
    resources = []
    for year in range(start_year, end_year + 1):
        next_year = year + 1
        season_str = f"{year}-{next_year}"
        url = f"https://fbref.com/en/comps/9/{season_str}/{season_str}-Premier-League-Stats"
        resources.append({
            'season': season_str,
            'url': url
        })
    return resources

### Set the resources to scrape 

# RESOURCES = generate_season_resources()
# RESOURCES = [{'season': '2024-2025', 'url': 'https://fbref.com/en/comps/9/Premier-League-Stats'}]
