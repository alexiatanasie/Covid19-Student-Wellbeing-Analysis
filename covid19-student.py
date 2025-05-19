import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('COVID-19 Survey Student.csv')

# ANALYSIS

# average time spent per day
#list of columns
time_columns = ['Time spent on Online Class', 'Time spent on self study',
                'Time spent on fitness', 'Time spent on sleep', 'Time spent on social media']
print("\nAverage time spent per day in hours:")
#calculate the avg time spent for each activity
means = df[time_columns].mean(numeric_only=True).round(2)
print(means.to_string())

# age grouping
#new column age subject
#cut- split ages into age groups
#bins -defines age ranges
df['Age Group'] = pd.cut(df['Age of Subject'], bins=[10, 15, 18, 22, 30],
                         labels=['Under 16', '16-18', '19-22', '23+'])


#class rating distribution by age group
#value_counts - egives percentages
#unstack- get table format
#fillna-fills 0 where rating doesnt exist
rating_by_age = df.groupby('Age Group', observed=True)['Rating of Online Class experience'].value_counts(normalize=True).unstack().fillna(0)
print("\nClass Rating distribution by Age Group %:")
print((rating_by_age * 100).round(1)) #converts proportions to %,rounded to 1 decimal


# health issues by age group
#value_counts-how many students selected each type of response

health_by_age = df.groupby('Age Group', observed=True)['Health issue during lockdown'].value_counts().unstack().fillna(0)
print("\nHealth Issues during Lockdown by Age Group:")
print(health_by_age)


# correlation between social media usage and class rating

#create a dictionary to convert ratings into numbers
rating_map = {
    'Very poor': 1,
    'Poor': 2,
    'Average': 3,
    'Good': 4,
    'Excellent': 5
}
#add a new col to dataset with numeric equivalrnts to ratings
#map(rating_map) replaces each text value in the column with its associated numeric value

df['Class Rating Num'] = df['Rating of Online Class experience'].map(rating_map)
#pearson correlation coeff between the number of hours spent on social media and the numeric class rating
correlation = df['Time spent on social media'].corr(df['Class Rating Num'])
print(f"\nCorrelation between social media use and online class rating: {correlation:.2f}")

# VISUALIZATION
# boxplot of sleep time by age group
plt.figure(figsize=(8, 5))
sns.boxplot(x='Age Group', y='Time spent on sleep', data=df)
plt.title("Distribution of Sleep Time by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Sleep Time (hours)")
plt.tight_layout()
plt.show()

# stacked bar chart
#how many students in each age group reported specific health issues
health_by_age.plot(kind='bar', stacked=True, colormap='Set2', figsize=(8, 5))
plt.title("Health Issues during Lockdown by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Students")
plt.legend(title="Health Issue")
plt.tight_layout()
plt.show()
