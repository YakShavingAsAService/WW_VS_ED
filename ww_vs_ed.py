import IPython
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# downloaded wastewater data csv from https://doh.wa.gov/data-and-statistical-reports/diseases-and-chronic-conditions/communicable-disease-surveillance-data/respiratory-illness-data-dashboard#WasteWater
WW_DATAF = "./data/Downloadable_Wastewater_04182024.csv"

# downloaded disease activity data csv froWhttps://doh.wa.gov/data-and-statistical-reports/diseases-and-chronic-conditions/communicable-disease-surveillance-data/respiratory-illness-data-dashboard#DiseaseActivity 
DA_DATAF = "./data/Respiratory_Disease_RHINO_COVID_Hosp_Emergency_Care_Downloadable_04182024.csv"

# Read the wastewater CSV file
wwdf = pd.read_csv(WW_DATAF)

# just look at rows after 2023-10-1 (the start of the 2023-2024 respiratory season)
wwdf.loc[:,'Sample Collection Date'] = pd.to_datetime(wwdf['Sample Collection Date'])
wwdf = wwdf[wwdf['Sample Collection Date'] > pd.to_datetime('2023-10-01')]

# this dataset has a few 0.0 concentration entries and I don't believe them
wwdf = wwdf[wwdf['Normalized Pathogen Concentration (gene copies/person/day)'] > 0.0]

# Filter the data for the "Brightwater Treatment Plant" site, and "sars-cov-2" PCR Pathogen Target
brightwater_data = wwdf[(wwdf['Site Name'] == 'Brightwater Treatment Plant') & (wwdf['PCR Pathogen Target'] == 'sars-cov-2')]

# Filter the data for the "West Point Wastewater Treatment Plant Influent" site, and "sars-cov-2" PCR Pathogen Target
westpoint_data = wwdf[(wwdf['Site Name'] == 'West Point Wastewater Treatment Plant Influent') & (wwdf['PCR Pathogen Target'] == 'sars-cov-2')]

# Filter the data for the "King County South Wastewater Treatment Plant" site, and "sars-cov-2" PCR Pathogen Target
kingcountysouth_data = wwdf[(wwdf['Site Name'] == 'King County South Wastewater Treatment Plant') & (wwdf['PCR Pathogen Target'] == 'sars-cov-2')]

# Extract the relevant columns for Brightwater Treatment Plant
brightwater_x = brightwater_data['Sample Collection Date']
brightwater_y = brightwater_data['Normalized Pathogen Concentration (gene copies/person/day)']

# Extract the relevant columns for West Point Wastewater Treatment Plant Influent
westpoint_x = westpoint_data['Sample Collection Date']
westpoint_y = westpoint_data['Normalized Pathogen Concentration (gene copies/person/day)']

# Extract the relevant columns for King County South Wastewater Treatment Plant
kingcountysouth_x = kingcountysouth_data['Sample Collection Date']
kingcountysouth_y = kingcountysouth_data['Normalized Pathogen Concentration (gene copies/person/day)']

# Create the plot
plt.figure(figsize=(12, 6))
ax = plt.subplot()
ax.scatter(westpoint_x, westpoint_y, color='#1f77b4', label='West Point Treatment Plant')
ax.scatter(brightwater_x, brightwater_y, color='#ff7f0e', label='Brightwater Treatment Plant')
ax.scatter(kingcountysouth_x, kingcountysouth_y, color='#2ca02c', label='King County South Treatment Plant')
ax.legend()

# Add labels for this collection of series
#plt.xlabel('2023-2024 Respiratory Infection Season')
plt.ylabel('Normalized Pathogen Concentration (gene copies/person/day)')

# Read the hospital emergency care CSV file
hecdf = pd.read_csv(DA_DATAF)

# Filter the data for the "Healthier Here" location (King County ACH region), and "Emergency Visits" care type and in the 2023-2024 season
kingcounty_2023_2024_emergency_care_data = hecdf[(hecdf['Location'] == 'Healthier Here') & (hecdf['Care Type'] == 'Emergency Visits') & (hecdf['Season'] == '2023-2024')]
kingcounty_2023_2024_emergency_care_data.loc[:,'Week Start'] = pd.to_datetime(kingcounty_2023_2024_emergency_care_data['Week Start'])
kingcounty_2023_2024_emergency_care_data.loc[:,'Week End'] = pd.to_datetime(kingcounty_2023_2024_emergency_care_data['Week End'])

# Extract the relevant columns for King County emergency visits
kingcounty_2023_2024_emergency_care_y = kingcounty_2023_2024_emergency_care_data['1-Week Percent COVID-19']
kingcounty_2023_2024_emergency_care_timedelta = pd.to_timedelta(kingcounty_2023_2024_emergency_care_data['Week End'] - kingcounty_2023_2024_emergency_care_data['Week Start'])
kingcounty_2023_2024_emergency_care_x_width = kingcounty_2023_2024_emergency_care_timedelta.dt.days

# Create a new y-axis for a new series
ax2 = ax.twinx()

# Plot the new data series on the new y-axis
ax2.bar(kingcounty_2023_2024_emergency_care_data['Week Start'], kingcounty_2023_2024_emergency_care_y, width=kingcounty_2023_2024_emergency_care_x_width, label='% emergency room visits',hatch='///',edgecolor='black', facecolor='none')

# Customize the new y-axis
ax2.set_ylabel('Percent of COVID-19 Emergency Room Visits')
ax2.tick_params(axis='y', colors='black')

# Format the x-axis to show dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=90)

# Add title and data source info and show the plot
plt.title('Sars-CoV-2 Wastewater Concentration vs Percent COVID-19 Emergency Room Visits\nKing County, WA, Oct 2023 - March 2024')
plt.figtext(0.99, 0.01, 'data source: https://doh.wa.gov/data-and-statistical-reports/diseases-and-chronic-conditions/communicable-disease-surveillance-data/respiratory-illness-data-dashboard', horizontalalignment='right')
plt.show()


