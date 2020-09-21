# -*- coding: utf-8 -*-
"""CV2_EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NFh9_mWU9ZhSdR1ZBh9RdHN_gYIEB5v2
"""

from google.colab import files
uploaded = files.upload()

import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(io.BytesIO(uploaded['2Mcare_PartD_Spending_2018.csv']))

### Here are the purposes for the data set...
### 1) Potential DV/IV
### 2) Missing Data
### 3) Transformations 
### 4) central tendency and distribution of responses
### 5) value counts
### 6) quartile ranges (.25, .50, .75),
### 7) create at least separate 3 visualizations that help the reader understand your dataset

### I will insert comments throughout the code to make reference to the corresponding concepts

# Lets take a look at the initial data set
df

### Potential Independent variables : Brand name, number of manufacturers
### Potential Dependent Variables: Total beneficiaries, Total Spending, Average Spending Per Dosage Unit
### We also see that we will need to clean up this data!!
### Lets figure out what type of data this is...

df.dtypes

### So here, we see the majority of types are not integers.
### We will need to do multiple transformations!
### Remove the '$' from total spending.
### Remove the ',' commas from all numbers
### Clean up the name of the features and remove '\n'

### Clean up Total Spending name and convert to float
df['Total Spending'] = df['Total Spending'].str.replace('$', '')
df['Total Spending'] = df['Total Spending'].str.replace(',', '').astype(float)

### Force pandas to stop using scientific notation, and only use 2 decimals
pd.set_option('display.float_format', lambda x: '%.2f' % x)

### Clean up Average Spending per unit and convert to float
df['Average Spending Per Dosage Unit (Weighted)'] = df['Average Spending Per Dosage Unit (Weighted)'].str.replace('$', '')
df['Average Spending Per Dosage Unit (Weighted)'] = df['Average Spending Per Dosage Unit (Weighted)'].str.replace(',', '').astype(float)

### Clean up column names
df.rename(columns = {'Total \nBeneficiaries' : 'Total Beneficiaries'}, inplace = True)
df.rename(columns = {'Average \nSpending Per Claim' : 'Average Spending Per Claim'}, inplace = True)
df.rename(columns = {'Average \nSpending Per Beneficiary' : 'Average Spending Per Beneficiary'}, inplace = True)
df.rename(columns = {'Average Spending Per Dosage Unit (Weighted)' : 'Average Price Per Dose'}, inplace = True)
df.rename(columns = {'Outlier \nFlag' : 'Outlier Flag'}, inplace = True)

### Confirm that our changes to the features worked
df.dtypes

### Beautiful!! Now lets look for the features we will be using...
### Check for any null values

df_temp = pd.DataFrame(df['Total Beneficiaries'])
df_temp_missing = df_temp.apply(lambda x: x.str.strip()).replace('', np.nan)
pd.isnull(df_temp_missing['Total Beneficiaries'])
df_temp_missing.isnull().values.sum()

### We have 153 values that are null but we will not be using Total Beneficiaries
### Lets check Total Spending because we are using this for a plot later
df_check = pd.DataFrame(df['Total Spending'])
df_check.isnull().values.sum()

### Excellent, there are no null values

### Just having fun - wanted to sort by decending order
### Interesting, what are the 10 most popular drugs that Medicare spends money on?

df_desc = df.sort_values('Total Spending', ascending=False)
df_desc.head(10)

# This is an interesting relationship between Number of Manufacturers and Total Spending or Average Spending Per Dosage Unit

df.sample(5)

### Lets do a value count
df['Number of Manufacturers'].value_counts()

### Look at central tendency, distribution of responses, and quartile ranges
df_group = df.groupby(['Number of Manufacturers'])
df_group.describe()

### Try representing this data as a box plot instead of just numbers
df_man1 = pd.DataFrame(df['Number of Manufacturers'])
df_man1.dtypes

import seaborn as sns
sns.boxplot(x=df_man1['Number of Manufacturers'])

### Does medicare spending go to drugs with only one manufacturer?
### Does increasing number of manufacturers decrease price? DV/IV numb.manufacturer/avg spending per unit
### Lets visalize this data differently

import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

ax = sns.lineplot(x="Number of Manufacturers", y="Total Spending", data=df)
ax.set(ylim = (0,600000000))

### Looks like Total spending varies but what about Price Per Dose?
ax = sns.lineplot(x="Number of Manufacturers", y="Average Price Per Dose", data=df)
ax.set(ylim = (0,350))
ax.set(xlim = (1, 5))

### Wow this is a great visualization that show as the Number of Manufacturers for a drug increases, 
### the Average Price Per dose decreases.