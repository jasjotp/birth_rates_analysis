'''
Data and System Analyst Technical Exercise 

Goal: Show the chance of being born in Canada in a particular year, using avaialbe public data 

eda-01.py: retrieves birth rate data and population data from the World Bank API at https://www.google.com/url?q=https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information&sa=D&source=editors&ust=1753043891168981&usg=AOvVaw2drl_hYHzDTyk2Alvjdphf
to find the birth rate (per 1,000 people) per country per year and the total population per country per year 
'''
import pandas as pd 
import json 
import sqlite3
import requests 
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np 
import plotly.express as px

def fetch_world_bank_data(url: str, per_page: int = 20000) -> pd.DataFrame: # birth rate URL to retrieve results in JSON - used per_page = 20,000 as a safe upper bound to return all countries data on one page to avoid having to go page by page
    '''
    Fetches and returns normalized World Bank indicator data as a DataFrame 
    '''
    params = {
    'format': 'json',
    'per_page': per_page # to get all countries data in one page
    }

# check if the response was successful 
    try: 
        response = requests.get(url, params = params)
        response.raise_for_status() # raise status if there are any non-200 codes
        data = response.json()

        # the World Bank API returns the JSON response in a list of 2 elements: in the format of data = [metadata, actual data] so data[1] grabs the 1st index/ the actual data
        if len(data) < 2 or not data[1]: # if the JSON response of the birth rate data is empty, easie an error 
            raise ValueError('No Birth Rate data found in response...')
        
        df = pd.json_normalize(data[1])

        # confirm that date is an integer 
        df['date'] = df['date'].astype(int)

        return df 

    except requests.exceptions.RequestException as e: 
        print(f'Request failed: {e}')
    except ValueError as e: 
        print(f'Data error: {e}')
    except Exception as e: 
        print(f'Other error: {e}')


# set the birth rate and population URL to retrieve results in JSON - used per_page = 20,000 as a safe upper bound to return all countries data on one page to avoid having to go page by page
birth_rate_url = "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.CBRT.IN"
population_url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"

# call the above helper to read in the birth date and population data for each country 
birth_rate_df = fetch_world_bank_data(birth_rate_url)
population_df = fetch_world_bank_data(population_url)

# confirm birth rate data and population data got passed in 
print(birth_rate_df.head())
print(population_df.head())

### we are comparing the number of births in Canada for a given year vs the number of births globally in that same year 
# number of births can be found by for each country by doing (birth rate / 1000) * population (we divide by 1000 to get birth rate per person, as population is per person)

# rename columns we want to output to perform the calculation for clarity 
birth_rate_df = birth_rate_df.rename(columns = {
    'countryiso3code': 'country_code',
    'date': 'year',
    'value': 'birth_rate'
})

population_df = population_df.rename(columns = {
    'countryiso3code': 'country_code',
    'date': 'year',
    'value': 'population'
})

# join birth rate df with population df on countryiso3code and year to get each country's birth rate with each country's population per year 
combined_df = pd.merge(birth_rate_df[['country_code', 'year', 'birth_rate']],
                       population_df[['country_code', 'year', 'population']],
                       on = ['country_code', 'year'], 
                       how = 'inner' # default behaviour of merge for the how param is already inner but this is just for clarity 
                       )

# values that are missing are not comparable and it is not possible to calculate number of births, so drop missing values (imputing would cause bias)
combined_df = combined_df.dropna(subset = ['birth_rate', 'population'])

# calculate number of births (we divide by 1000 to get birth rate per person, as population is per person)
combined_df['number_of_births'] = (combined_df['birth_rate'] / 1000) * combined_df['population']

print(combined_df.head())

# Summary statistics
print("=== SUMMARY STATISTICS ===")
print(f"\nGlobal Data Summary:")
print(f"Years covered: {combined_df['year'].min()} - {combined_df['year'].max()}")
print(f"Number of countries: {combined_df['country_code'].nunique()}")
print(f"Average global birth rate: {combined_df['birth_rate'].mean():.2f} per 1,000 people")

### basic EDA for last 10 years only - DO NOT SAVE AS I GET AN OUT OF BOUNDS ERROR 

# plot average birth rates for each country each year and birth rates per year for Canada 
current_year = combined_df['year'].max()
start_year = current_year - 9 # last 10 years including the current year

# calculate avg birth rate by year for all countries 
avg_birth_rates = combined_df[combined_df['year'] >= start_year].groupby('year')['birth_rate'].mean().reset_index()

# create the plot for the average birth rate over time as a line chart to show birth rate trend globally over time
plt.figure(figsize = (16, 8))
ax1 = sns.lineplot(data = avg_birth_rates, x = 'year', y = 'birth_rate', marker = 'o', linewidth = 2.5, markersize = 4)
plt.title(f'Global Average Birth Rate Over Time ({start_year}-{current_year})', fontsize = 14, fontweight = 'bold')
plt.xlabel('Year', fontsize = 12)
plt.ylabel('Birth Rate (per 1,000 people)', fontsize = 12)
plt.grid(True, alpha = 0.3) # add grid to make values easier to read

# add data labels for each point every 2 years (to avoid overlapping of labels)
years_to_label = avg_birth_rates[avg_birth_rates['year'] % 2 == 0]['year'].tolist()
for year in years_to_label:
    rate = avg_birth_rates[avg_birth_rates['year'] == year]['birth_rate'].iloc[0] # grab birth rate for year
    plt.annotate(f'{rate:.1f}', (year, rate), xytext = (0,10), ha = 'center', fontsize = 8)

plt.xticks(rotation = 45)

# save figure 
plt.savefig('global_average_birth_rate.png', bbox_inches = 'tight')
plt.close()
print("Figure saved as 'global_average_birth_rate.png'")

# plot birth rates per year for Canada 

canada_data = combined_df[(combined_df['country_code'] == 'CAN') & (combined_df['year'] >= start_year)].copy()

# if the canada data is not empty, create the line plot 
if not canada_data.empty:
    plt.figure(figsize = (16, 8))
    ax2 = sns.lineplot(data = canada_data, x = 'year', y = 'birth_rate', marker = 'o', linewidth = 2.5, markersize = 4)
    plt.title(f'Canada Birth Rate Over Time ({start_year}-{current_year})', fontsize = 14, fontweight = 'bold')
    plt.xlabel('Year', fontsize = 12)
    plt.ylabel('Birth Rate (per 1,000 people)', fontsize = 12)
    plt.grid(True, alpha = 0.3) # add grid to make values easier to read

    # add data labels for each point every 2 years (to avoid overlapping of labels)
    years_to_label_canada = canada_data[canada_data['year'] % 2 == 0]['year'].tolist()
    for year in years_to_label_canada:
        rate = canada_data[canada_data['year'] == year]['birth_rate'].iloc[0] # grab birth rate for year
        plt.annotate(f'{rate:.1f}', (year, rate), xytext = (0,10), ha = 'center', fontsize = 8)

plt.xticks(rotation = 45)

# save the plot 
plt.savefig('canada_birth_rate.png', bbox_inches = 'tight')
plt.close()
print("Figure saved as 'canada_birth_rate.png'")

# plot to show the population of Canada year over year 

if not canada_data.empty:
    plt.figure(figsize = (16, 8))
    ax3 = sns.lineplot(data = canada_data, x = 'year', y = 'population', marker = 'o', linewidth = 2.5, markersize = 4)
    plt.title(f'Canada Population Over Time ({start_year}-{current_year})', fontsize = 14, fontweight = 'bold')
    plt.xlabel('Year', fontsize = 12)
    plt.ylabel('Population', fontsize = 12)
    plt.grid(True, alpha = 0.3) # add grid to make values easier to read

    # Format y-axis to show population in millions
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

    # add data labels for each point every 5 years (to avoid overlapping of labels)
    for year in years_to_label_canada:
        if year in canada_data['year'].values:
            pop = canada_data[canada_data['year'] == year]['population'].iloc[0]
            plt.annotate(f'{pop/1e6:.1f}M', (year, pop), xytext = (0,10), ha = 'center', fontsize = 8)

plt.xticks(rotation = 45)

# save the figure 
plt.savefig('canada_population.png', bbox_inches = 'tight')
plt.close()
print("Figure saved as 'canada_birth_population_analysis.png'")

# create a SQlite database connection
conn = sqlite3.connect('birth_stats.db')

# save the df to SQLite 
combined_df.to_sql('birth_data', conn, if_exists = 'replace', index = False)
print("Data loaded into SQLite successfully.")

# run the SQL query to get the chances of being born in Canada for each year (for each year, compute number of births in Canada divided by number of births of all countries)
query = """
SELECT 
    year, 
    ROUND(SUM(CASE WHEN country_code = 'CAN' THEN number_of_births ELSE 0 END), 0) AS canada_births, 
    ROUND(SUM(number_of_births), 0) AS total_births, 
    ROUND(
    100.0 * SUM(CASE WHEN country_code = 'CAN' THEN number_of_births ELSE 0 END) / SUM(number_of_births),
    3
    ) AS chance_percent
FROM birth_data
GROUP BY year
ORDER BY year DESC
"""

result_df = pd.read_sql_query(query, conn)

# make sure all rows and columns are shown 
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(result_df)

# plot the year and chance of being born in Canada using plotly 

fig = px.line(
    result_df,
    x = 'year',
    y = 'chance_percent',
    title = 'Chance of Being Born in Canada by Year',
    labels = {
        'year': 'Year',
        'chance_percent': 'Chance (%)'
    },
    markers = True
)

fig.update_traces(line = dict(width=2))
fig.update_layout(
    yaxis_tickformat = '.3f',
    hovermode = 'x unified',
    template = 'plotly_white'
)

fig.write_html("chance_of_being_born_in_canada.html")