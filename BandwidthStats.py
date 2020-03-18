import pandas as pd
df = pd.read_csv (r'Bandwidth_20200309_0100_81.csv')
#print(df)

#Simple Stats
mean1 = round(df['Requests'].mean(), 0)
mean1 = f"{mean1:,}"
sum1 = round(df['Requests'].sum(), 0)
sum1 = f"{sum1:,}"
max1 = round(df['Requests'].max(), 0)
max1 = f"{max1:,}"
min1 = round(df['Requests'].min(), 0)
min1 = f"{min1:,}"
count1 = round(df['Requests'].count(), 0)
median1 = round(df['Requests'].median(), 0)
median1 = f"{median1:,}"

maxValues = df[['Hour of Day', 'Bytes Sent']].max()
#maxValues = f"{maxValues:,}"

#groupby_sum1 = df.groupby(['HourofDay']).sum()

# print Simple Stats
print('Mean No Requests: ' + str(mean1))
print('Sum of Requests: ' + str(sum1))
print('Max Requests: ' + str(max1))
print('Min Requests: ' + str(min1))
print('Count of Hours: ' + str(count1))
print('Median No Requests: ' + str(median1))

print('Maximum value in each column : ')
print(maxValues)

#print('Sum of Request, grouped by the Hour of Day: ' + str(groupby_sum1))