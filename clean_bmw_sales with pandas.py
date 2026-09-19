import pandas as pd

# Load the data
df = pd.read_csv('BMW_Sales_Data.csv')
print('Rows before cleaning:', len(df))

# 1. Drop rows that are completely empty
df = df.dropna(how='all')

# 2. Drop exact duplicate rows
df = df.drop_duplicates()

# 3. Drop any remaining rows missing a key field
df = df.dropna(subset=['Date', 'Model', 'Revenue',
                        'Quantity Sold', 'Region', 'Country', 'Channel'])

# 4. Fix data types
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Year'] = df['Date'].dt.year
df['Revenue'] = df['Revenue'].astype(float)
df['Quantity Sold'] = df['Quantity Sold'].astype(int)

# 5. Strip stray whitespace from text columns
for col in ['Model', 'Region', 'Country', 'Channel']:
    df[col] = df[col].str.strip()

# 6. Sort by date and reset the index
df = df.sort_values('Date').reset_index(drop=True)

print('Rows after cleaning:', len(df))
print('Missing values left:', df.isna().sum().sum())
print('Duplicates left:', df.duplicated().sum())

# Save the cleaned file
df.to_csv('BMW_Sales_Data_Cleaned.csv', index=False)
