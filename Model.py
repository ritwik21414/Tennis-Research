import math
from tabulate import tabulate
import csv
import matplotlib.pyplot as plt
import pandas as pd

def read_gdp_data(file_path):
    gdp_data = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            country = row[1]
            gdp = float(row[0])
            gdp_data[country] = gdp
    return gdp_data

def calculate_x_and_y(source_country, source_gdp, target_gdp, target_country=None):
    result = {1: [], 2: [], 3: [], 4: []}
    if source_country in source_gdp:
        source_gdp_value = source_gdp[source_country]
        if target_country is None or target_country == '':
            countries = target_gdp.keys()
        else:
            countries = [target_country]
        for country in countries:
            target_gdp_value = target_gdp.get(country, 0)
            if target_gdp_value != 0:
                x = math.ceil(source_gdp_value / target_gdp_value)
                y = target_gdp_value * x
                if target_gdp_value >= 40000:
                    result[1].append([country, x, y])
                elif target_gdp_value >= 20000:
                    result[2].append([country, x, y])
                elif target_gdp_value >= 10000:
                    result[3].append([country, x, y])
                else:
                    result[4].append([country, x, y])
    return result

def calculate_x(source_country, source_gdp, target_gdp, target_country=None):
    x_values = []
    if source_country in source_gdp:
        source_gdp_value = source_gdp[source_country]
        if target_country is None or target_country == '':
            countries = target_gdp.keys()
        else:
            countries = [target_country]
        for country in countries:
            if country in target_gdp:
                target_gdp_value = target_gdp[country]
                if target_gdp_value != 0:
                    x = math.ceil(source_gdp_value / target_gdp_value)
                    x_values.append(x)
            else:
                x_values.append(None)  # Append a default value if target_country is not found
    return x_values

def count_country_occurrences(source_country, target_country, country_list):
    source_count = country_list.tolist().count(source_country) if source_country in country_list else 0
    target_count = country_list.tolist().count(target_country) if target_country in country_list else 0
    return source_count, target_count

def plot_graph(target_gdp, filtered_x_values, source_country, countries_file_path):
    # Read country abbreviations and names from the CSV file
    countries_df = pd.read_csv(countries_file_path)
    country_labels = dict(zip(countries_df['Country'], countries_df['Abbreviation']))
    
    plt.figure(figsize=(12, 8))
    plt.plot(list(target_gdp.values())[:len(filtered_x_values)], filtered_x_values, color='b', label='x values', marker='o')
    plt.xlabel('Salaries')
    plt.ylabel('No. of players')
    plt.title(f'No. of players vs. Salary in {source_country}')
    plt.xticks(range(0, int(max(target_gdp.values())) + 10000, 10000))
    plt.yticks(list(range(0, int(max(filtered_x_values)) + 1, 4)))
    plt.grid(True)
    plt.legend()
    plt.axvline(x=10000, color='r', linestyle='--', label='10k')
    plt.axvline(x=20000, color='r', linestyle='--', label='20k')
    plt.axvline(x=40000, color='r', linestyle='--', label='40k+')
    
    # Add country labels
    for i, country in enumerate(target_gdp.keys()):
        if i < len(filtered_x_values):
            country_abbreviation = country_labels.get(country, 'Unknown')
            plt.text(list(target_gdp.values())[i] + 1000, filtered_x_values[i], country_abbreviation, fontsize=8, ha='left', va='center')
     
    plt.legend()
    plt.show()

# Read source GDP data
source_gdp_file_path = 'source.csv'  
source_gdp = read_gdp_data(source_gdp_file_path)

# Read target GDP data
target_gdp_file_path = 'target.csv'  
target_gdp = read_gdp_data(target_gdp_file_path)

# Load the Excel file into a DataFrame
df = pd.read_excel('ranking.xlsx')

#Till what ranking do we need to consider
RankLimit=1000

# Extract the third row as an array
Country_List = df.iloc[:RankLimit,2].values

# Input source country
source_country = input("Enter the source country: ")
currentIncome= round(source_gdp[source_country])
print()
print(f"Current income is {currentIncome} $")
print()

target_country = input("Enter the target country (press Enter for all): ")
print()

# Calculate x and y values
table_data = calculate_x_and_y(source_country, source_gdp, target_gdp, target_country)

# Calculate x values
x_values = calculate_x(source_country, source_gdp, target_gdp, target_country)

# Filter out None values
filtered_x_values = [x for x in x_values if x is not None]

# Print the results as tables for each grade or plot the graph
if target_country != '' and target_country is not None:
    for i in range(1, 5):
        if len(table_data[i]) > 0:
            print(f"List of target countries for {source_country} with Salary grade {i}:")
            print(tabulate(table_data[i], headers=["Target Country", "Number of players", "Salary (in $)"], tablefmt="grid"))
            print()
    
    source_count, target_count = count_country_occurrences(source_country, target_country, Country_List)
    if target_count == 0:
        print(f"{target_country} does not have any player in ATP top {RankLimit} .")
    else:
        actual_Rank_Ratio = round((source_count)/(target_count), 1)
        print(f"The actual rank ratio for given countries in ATP top {RankLimit} ranking is {actual_Rank_Ratio}")

# No specific target country, displaying all countries
else:
    for i in range(1, 5):
        if len(table_data[i]) > 0:
            print(f"List of target countries for {source_country} with Salary grade {i}:")
            print(tabulate(table_data[i], headers=["Target Country", "Number of players", "Salary (in $)"], tablefmt="grid"))
            print()

    # Plot the graph with filtered x values
    # Update the plot_graph function call to include the file path for country abbreviations
    plot_graph(target_gdp, filtered_x_values, source_country, 'countryCodes.csv')