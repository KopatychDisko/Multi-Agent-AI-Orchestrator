import matplotlib.pyplot as plt
import pandas as pd

# Sample GDP data for Russia (in billion USD)
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
gdp = [1524, 2047, 2210, 2297, 2059, 1363, 1283, 1574, 1657, 1699, 1483, 1778]

# Create a DataFrame
data = pd.DataFrame({'Year': years, 'GDP (Billion USD)': gdp})

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data['Year'], data['GDP (Billion USD)'], marker='o', linestyle='-', color='b')
plt.title('Russian GDP Over the Years (2010-2021)')
plt.xlabel('Year')
plt.ylabel('GDP (Billion USD)')
plt.grid(True)
plt.show()