import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry

# Importing the two datasets in CSV format
cyber_salaries = pd.read_csv('cyber_salaries.csv')
ds_salaries = pd.read_csv('ds_salaries.csv')

"""
# Function to transform country codes into full country names using pycountry library
def country_full_name(country_name):
    try:
        return pycountry.countries.get(alpha_2=country_name).name      # Transform country code (alpha-2) like US into full name United States
    except:
        return country_name     # Otherwise, leave the country code as is

# Apply the function to 'employee_residence' and 'company_location' columns in both datasets
ds_salaries['employee_residence'] = ds_salaries['employee_residence'].apply(country_full_name)
ds_salaries['company_location'] = ds_salaries['company_location'].apply(country_full_name)

cyber_salaries['employee_residence'] = cyber_salaries['employee_residence'].apply(country_full_name)
cyber_salaries['company_location'] = cyber_salaries['company_location'].apply(country_full_name)

"""

# Identifying common locations in both datasets
common_location = set(cyber_salaries['company_location']).intersection(ds_salaries['company_location'])

# Filter datasets to only include rows with matching company locations
cyber_salaries = cyber_salaries[cyber_salaries['company_location'].isin(common_location)]
ds_salaries = ds_salaries[ds_salaries['company_location'].isin(common_location)]

# Descriptive analysis of the two datasets
print(ds_salaries.describe())
print(cyber_salaries.describe())

# Mapping for the 'experience_level' variable
experience_level_mapping = {'EN': 'Entry Level', 'MI': 'Mid Level', 'SE': 'Senior', 'EX': 'Executive'}
cyber_salaries['experience_level'] = cyber_salaries['experience_level'].map(experience_level_mapping)
ds_salaries['experience_level'] = ds_salaries['experience_level'].map(experience_level_mapping)
# Mapping for the 'company_size' variable
company_size_mapping = {'L': 'Large', 'M': 'Medium', 'S': 'Small'}
cyber_salaries['company_size'] = cyber_salaries['company_size'].map(company_size_mapping)
ds_salaries['company_size'] = ds_salaries['company_size'].map(company_size_mapping)

# Correlation Matrix for Data Science Dataset
plt.figure(figsize=(10, 8))
sns.heatmap(ds_salaries.corr(numeric_only=True), annot=True)
plt.show()
# Correlation Matrix for Cyber-Security Dataset
plt.figure(figsize=(10, 8))
sns.heatmap(cyber_salaries.corr(numeric_only=True), annot=True)
plt.show()

def plot_comparison(cyber_salaries, ds_salaries, group_by, title, xlabel, ylabel):

    # Calculate average salaries by experience level for both datasets
    cyber_avg = cyber_salaries.groupby(group_by)["salary_in_usd"].mean()
    ds_avg = ds_salaries.groupby(group_by)["salary_in_usd"].mean()

    # Merge results into a single DataFrame
    combined_df = pd.DataFrame({'Avg_Salary_Cyber': cyber_avg, 'Avg_Salary_DS': ds_avg})

    # Creating the plot
    combined_df.plot(kind='bar', figsize=(10, 6))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

# Calling plot_comparison function for cyber_salaries and ds_salaries dataframes
plot_comparison(cyber_salaries, ds_salaries, 'company_size', 'Average Salary Comparison by Company Size', 'Company Size', 'Average Salary in USD')

plot_comparison(cyber_salaries, ds_salaries, 'experience_level', 'Average Salary Comparison by Experience Level', 'Experience Level', 'Average Salary in USD')

# Cyber Salaries and Data Science Boxplot

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.boxplot(x='experience_level', y='salary_in_usd', data=cyber_salaries, palette='Set3')
plt.title('Cyber Security Salaries by Experience Level')

plt.subplot(1, 2, 2)
sns.boxplot(x='experience_level', y='salary_in_usd', data=ds_salaries, palette='Set3')
plt.title('Data Science Salaries by Experience Level')
plt.show()

# List of European Countries and United States
eu_countries_vs_us = ['United States',
    "Austria", "Belgium", "Bulgaria", "Cyprus", "Croatia", "Denmark",
    "Estonia", "Finland", "France", "Germany", "Greece", "Ireland",
    "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Czech Republic", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden", "Hungary"]
# New datasets for comparing Europe and the United States
ds_salaries_eu_vs_us = ds_salaries[ds_salaries['company_location'].isin(eu_countries_vs_us)]
cyber_salaries_eu_vs_us = cyber_salaries[cyber_salaries['company_location'].isin(eu_countries_vs_us)]

def plot_horizontal_bar(data, group_by, title, xlabel, ylabel, color_palette, top_10=False):

    if top_10:
        # Calculate average salaries and get the top 10 values
        salary_means = data.groupby(group_by)["salary_in_usd"].mean().sort_values(ascending=False).head(10)
    else:
        salary_means = data.groupby(group_by)["salary_in_usd"].mean().sort_values(ascending=False)

    # Set plot style
    sns.set(style="whitegrid", palette=color_palette, font_scale=1.1)

    # Create a horizontal bar plot
    plt.figure(figsize=(14, 8))
    barplot = sns.barplot(
        x=salary_means.values,
        y=salary_means.index,
        errorbar=None,
        palette=color_palette,
        orient='h'
    )

    # Add title and axis labels
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)

    # Add value labels on bars
    for index, value in enumerate(salary_means.values):
        barplot.text(value, index, f' ${value:,.0f}', color='black', va="center")

    # Remove unnecessary borders
    sns.despine(left=True, bottom=True)

    # Show the plot
    plt.tight_layout()

    return plt

# Using plot_horizontal_bar function to create the following plots based on different groupings for the four datasets

plt_cyber_geo_salary = plot_horizontal_bar(
    cyber_salaries,
    'company_location',
    'Top 10 Cyber Security Salaries by Geography',
    'Average Salary in USD',
    'Company Location',
    'coolwarm',
    top_10=True
)
plt_cyber_geo_salary.show()

plt_ds_geo_salary = plot_horizontal_bar(
    ds_salaries,
    'company_location',
    'Top 10 Data Science Salaries by Geography',
    'Average Salary in USD',
    'Company Location',
    'viridis',
    top_10=True
)
plt_ds_geo_salary.show()

plt_ds_job_title_salary = plot_horizontal_bar(
    ds_salaries,
    'job_title',
    'Top 10 Data Science Salaries by Job Title',
    'Average Salary in USD',
    'Job Title',
    'RdPu',
    top_10=True
)
plt_ds_job_title_salary.show()

plt_cyber_job_title_salary = plot_horizontal_bar(
    cyber_salaries,
    'job_title',
    'Top 10 Cyber Security Salaries by Job Title',
    'Average Salary in USD',
    'Job Title',
    'GnBu',
    top_10=True
)
plt_cyber_job_title_salary.show()

plt_cyber_geo_salary = plot_horizontal_bar(
    ds_salaries_eu_vs_us,
    'company_location',
    'Data Science Salary Europe Vs United States',
    'Average Salary in USD',
    'Company Location',
    'cool'
)
plt_cyber_geo_salary.show()

plt_cyber_geo_salary = plot_horizontal_bar(
    cyber_salaries_eu_vs_us,
    'company_location',
    'Cyber Security Salary Europe Vs United States',
    'Average Salary in USD',
    'Company Location',
    'plasma'
)
plt_cyber_geo_salary.show()


# Calculation of average salaries based on remote work ratio
cyber_remote_salary = cyber_salaries.groupby('remote_ratio')['salary_in_usd'].mean().reset_index()
ds_remote_salary = ds_salaries.groupby('remote_ratio')['salary_in_usd'].mean().reset_index()

fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharey='all')

# Cyber-Security graphic
ax[0].bar(cyber_remote_salary['remote_ratio'], cyber_remote_salary['salary_in_usd'], color='skyblue')
ax[0].set_title('Cyber Security Salaries by Remote Ratio')
ax[0].set_xlabel('Remote Ratio')
ax[0].set_ylabel('Average Salary in USD')
ax[0].set_xticks(cyber_remote_salary['remote_ratio'])
ax[0].set_xticklabels(['No Remote', 'Partial', 'Full Remote'])

# Data Scientist graphic
ax[1].bar(ds_remote_salary['remote_ratio'], ds_remote_salary['salary_in_usd'], color='orange')
ax[1].set_title('Data Science Salaries by Remote Ratio')
ax[1].set_xlabel('Remote Ratio')
ax[1].set_xticks(ds_remote_salary['remote_ratio'])
ax[1].set_xticklabels(['No Remote', 'Partial', 'Full Remote'])

plt.tight_layout()
plt.show()


# Geopandas Geographic Map

# Geopandas only recognizes "United States of America" and not "United-States"
cyber_salaries['employee_residence'].replace({'United States': 'United States of America'}, inplace=True)
ds_salaries['employee_residence'].replace({'United States': 'United States of America'}, inplace=True)

# Calculating the number of employees per country for the two datasets
cyber_employees_for_country = cyber_salaries['employee_residence'].value_counts().rename_axis('country').reset_index(name='Cyber Security Employees')
ds_employees_for_country = ds_salaries['employee_residence'].value_counts().rename_axis('country').reset_index(name='Data Science Employees')

# Loading the world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merging data for both datasets
world = world.merge(cyber_employees_for_country, left_on='name', right_on='country', how='left')
world = world.merge(ds_employees_for_country, left_on='name', right_on='country', how='left')

# Replacing NaNs with zeros
world['Cyber Security Employees'] = world['Cyber Security Employees'].fillna(0)
world['Data Science Employees'] = world['Data Science Employees'].fillna(0)


# Creating maps for the two Datasets

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.plot(column='Cyber Security Employees', ax=ax, legend=True,
           cmap='YlOrRd', vmax=300, edgecolor='black',
           missing_kwds={'color': 'lightgrey'})
ax.set_title('Cyber Security Employees Worldwide')
ax.set_axis_off()

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.plot(column='Data Science Employees', ax=ax, legend=True,
           cmap='YlOrRd', vmax=300, edgecolor='black',
           missing_kwds={'color': 'lightgrey'})
ax.set_title('Data Science Employees Worldwide')
ax.set_axis_off()

plt.show()
