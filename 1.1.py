from pygooglenews import GoogleNews
import pandas as pd
from datetime import datetime


# Function to get titles
def get_titles(search, country_code):
    gn = GoogleNews(lang='en', country=country_code)
    stories = []
    try:
        search_result = gn.search(search)
        newsitem = search_result['entries']
        for item in newsitem:
            published = item.get('published', 'Unknown Date')
            publisher = item.get('source', {}).get('title', 'Unknown Publisher')
            story = {
                'title': item.title,
                'link': item.link,
                'publisher': publisher,
                'published': published,
                'keyword': search
            }
            stories.append(story)
    except Exception as e:
        print(f"An error occurred while fetching stories for {search}: {e}")
    return stories


# Function to convert the 'published' string into a 'Month Year' format
def convert_to_month_year(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        return date_obj.strftime('%B %Y')
    except ValueError:
        return 'Unknown Date'


# Keywords list


# Dictionary of countries with their codes and file names
countries = {
    'US': 'United States',
    'IN': 'India',
    'ID': 'Indonesia',
    'CA': 'Canada',
    'AU': 'Australia',
    'UK': 'United Kingdom',
    'MY': 'Malaysia',
    'SG': 'Singapore',
    'PH': 'Philippines',
    'NZ': 'New Zealand'

}

for country_code, country_name in countries.items():
    all_stories = []  # Initialize an empty list to hold all stories from all searches

    # Collect stories for each keyword
    for keyword in keywords:
        print(f"Fetching stories for keyword: {keyword} in {country_name}")
        stories = get_titles(keyword, country_code)
        all_stories.extend(stories)  # Extend the list with the new stories

    # Convert the list of all stories to a DataFrame
    df_all_stories = pd.DataFrame(all_stories)

    # Debug: print number of stories and DataFrame columns
    print(f"Number of stories fetched for {country_name}: {len(all_stories)}")
    print("DataFrame columns:", df_all_stories.columns)

    # Check if the DataFrame is empty before proceeding
    if not df_all_stories.empty and 'published' in df_all_stories.columns:
        # Apply the conversion function to the 'published' column
        df_all_stories['published'] = df_all_stories['published'].apply(convert_to_month_year)
    else:
        print(f"No 'published' column found for {country_name} or the DataFrame is empty.")

    # Save the DataFrame to an Excel file if it's not empty
    if not df_all_stories.empty:
        excel_path = f'combined_esg_logistics_news_{country_code}.xlsx'
        df_all_stories.to_excel(excel_path, index=False)
        print(f"All stories for {country_name} saved to {excel_path}")
    else:
        print(f"No data to save for {country_name}")
