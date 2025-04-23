import pandas as pd

# Step 1: Create age-based fatality rate table (df1)
age_fatality = []
for age in range(0, 101):
    if age <= 17:
        rate = 20 / 1_000_000
    elif age <= 49:
        rate = 500 / 1_000_000
    elif age <= 64:
        rate = 6000 / 1_000_000
    else:
        rate = 90000 / 1_000_000
    age_fatality.append({'Age': age, 'FatalityRate': rate})

df1 = pd.DataFrame(age_fatality)

# Step 2: Load and Pre-processing WorldDemographics.csv (dt2)
df2 = pd.read_csv("WorldDemographics.csv").drop(columns=["Unnamed: 0"])
df2 = df2.rename(columns={'#Alive': 'Population'})

# Step 3: Merge df1 (fatality rate) with df2 (demographics)
merged = pd.merge(df2, df1, on='Age')

# Step 4: Calculate expected deaths per age
merged['ExpectedDeaths'] = merged['Population'] * merged['FatalityRate']

# Step 5: Group by country code and name
df3 = merged.groupby(['country_code', 'PopulationID']).agg(
    TotalPopulation=('Population', 'sum'),
    TotalExpectedDeaths=('ExpectedDeaths', 'sum')
).reset_index()

# Step 6: Calculate percentage of population expected to die
df3['PercentDied'] = (df3['TotalExpectedDeaths'] / df3['TotalPopulation']) * 100

# Step 7: Rename columns for clarity
df3 = df3.rename(columns={
    'country_code': 'CountryCode',
    'PopulationID': 'CountryName'
})

# Step 8: Save to CSV
df3.to_csv("Assignment4.csv", index=False)
