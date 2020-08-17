import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime as dt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator, FuncFormatter)

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

DataFiles = glob.glob('C:/Users/anders.rylander2/PycharmProjects/Stats/venv/Files/*Bandwidth*.csv') #creates a list of all csv files
#DataFiles = glob.glob('Bandwidth_20200309_0100_81.csv') #creates a list of all csv files
#DataFiles = pd.read_csv (r'Bandwidth_20200309_0100_81.csv')

data = []  # pd.concat takes a list of dataframes as an argument
for csv in DataFiles:
    frame = pd.read_csv(csv)
    frame['Date'] = os.path.basename(csv)
    data.append(frame)

df = pd.concat(data, ignore_index=True) #dont want pandas to try an align row indexes

#REGEX to extract Date from Filename
df['Date'] = df['Date'].str.extract('([0-9]{8})', expand=False)

#Join Date and Time
df['DateTimeStamp'] = pd.to_datetime(df['Date'].apply(str)+' '+df['Hour of Day'])


#Index DateTime columns and drop Hour of Day, Date and DateTimeStamp columns
df.index = pd.to_datetime(df["DateTimeStamp"])
df = df.drop(columns=["Hour of Day", "Date", "DateTimeStamp"])

#Date in Filename is for 1 day after so correcting here
df.index = df.index + pd.Timedelta(days=-1)

df['Total Bytes'] = df['Total Bytes']/1024/1024/1024 #Convert to GB
df['Bytes Received'] = df['Bytes Received']/1024/1024/1024 #Convert to GB
df['Bytes Sent'] = df['Bytes Sent']/1024/1024/1024 #Convert to GB
#df['Requests'] = df['Requests']/1000 #Convert to K Requests

#Sort index (date & time) in cronological order)
df = df.sort_index()

#Name index column
df.index.name = 'DateTime'

#Resampling hourly data to daily DataFrame named DX
dx = df.resample('D').sum()

print(df)
print(dx)
print(df.info())

maxDay = round(dx['Total Bytes'].max(), 0)
maxDay = f"{maxDay:,}"
print('Max Day (GB): ' + str(maxDay))
maxHour = round(df['Total Bytes'].max(), 0)
maxHour = f"{maxHour:,}"
print('Max Hour (GB): ' + str(maxHour))
print('Date and Hour with largest Total GB:')
print(df[df['Total Bytes'] == df['Total Bytes'].max()])
print('Date with largest Total GB:')
print(dx[dx['Total Bytes'] == dx['Total Bytes'].max()])


# Create two subplots sharing x axis
xaxis = dx.index
xhaxis = df.index
#xHTTP = HTTP.index
#y1axis = Ratio
y2axis = dx['Bytes Received']
y3axis = dx['Bytes Sent']
y4axis = dx['Requests']
y2haxis = df['Bytes Received']
y3haxis = df['Bytes Sent']


def millions(y4axis, pos):
    #'The two args are the value and tick position'
    return '%1.1f M' % (y4axis * 1e-6)

formatter = FuncFormatter(millions)

fig, (ax4, ax2, ax3) = plt.subplots(3, sharey=False, figsize=(15, 9))
plt.subplots_adjust(hspace=0.5)

ax4.plot(xaxis, y4axis, color='black', linewidth=0.4)
ax4.grid(which='major', axis='y', linestyle='dotted')
ax4.text(dt.date(2020, 3, 23), 35000000, "C-19 Lock Down --->", color='gray', fontsize=6, rotation=270)
ax4.legend(['Total Requests per Day'], loc='upper right', fontsize='x-small')
# Set the locator
locator = mdates.MonthLocator()  # every month
# Specify the format - %b gives us Jan, Feb...
ax4.xaxis.set_major_locator(locator)
myFmt = DateFormatter("%b %Y")
ax4.xaxis.set_major_formatter(myFmt)
ax4.yaxis.set_major_formatter(formatter)
ax4.set(title='Internet Proxy Volume of Traffic - TOTAL REQUESTS PER DAY', ylabel='No. Requests')

'''
ax1.plot(xHTTP, y1axis, color='black', linewidth=0.4)
ax1.grid(which='both', axis='y', linestyle='dotted')
ax1.grid(which='both', axis='x', linestyle='dotted')
ax1.set_ylim([0, 100])
ax1.legend(['% HTTPS'], loc='lower right', fontsize='x-small')
ax1.set(ylabel= '% HTTPS')
ax1.yaxis.set_minor_locator(AutoMinorLocator())
ax1.tick_params(which='both')
ax1.tick_params(which='major')
#ax1.tick_params(which='minor', labelsize=4)
#ax1.yaxis.set_minor_formatter(FormatStrFormatter("%.0f"))
'''

# Annotate
#style = dict(size=10, color='gray')
#ax1.text('2020-1-1', 50, "New Year's Day", **style)
#x_line_annotation = HTTP.Date(2020, 03, 03)
#x_text_annotation = df.index(2020, 03, 04)
#ax1.axvline(x=x_line_annotation, linestyle='dashed', alpha=0.5)
#ax1.text(x=x_text_annotation, y=90, s='Holiday in US', alpha=0.7, color='#334f8d')

# Compute the max value (plt.hist returns the x and y positions of the bars)
ymax = y2axis.max()
idx = np.where(y2axis == ymax)[0][0]
xval = xaxis[idx]
#Convert displayed value to Integer
ymax = int(ymax)
print(ymax)

# Annotate the highest value
ax2.text(xval, ymax, ymax, ha='left', va='center', color='red', fontsize=7)


def tbyte(y2axis, pos):
    #'The two args are the value and tick position'
    return '%1.0f TB/day' % (y2axis/1024)

formatter = FuncFormatter(tbyte)

#plt.title('f model: T= {}'.format(maxHour))
p1 = ax2.bar(xaxis, y2axis, width=0.7, color='red')
p2 = ax2.bar(xaxis, y3axis, width=0.7, color='green')
ax2.grid(which='major', axis='y', linestyle='dotted')
ax2.text(dt.date(2020, 3, 23), 1000, "C-19 Lock Down --->", color='gray', fontsize=6, rotation=270)
ax2.legend((p1[0], p2[0]), ('Inbound (Downloaded) TB per Day', 'Outbound (Uploaded) TB per Day'), loc='upper right', fontsize='x-small')
# Set the locator
locator = mdates.MonthLocator()  # every month
# Specify the format - %b gives us Jan, Feb...
ax2.xaxis.set_major_locator(locator)
myFmt = DateFormatter("%b %Y")
ax2.xaxis.set_major_formatter(myFmt)
ax2.yaxis.set_major_formatter(formatter)
ax2.set(title='Internet Proxy Volume of Traffic - INBOUND & OUTBOUND (TB per Day)', ylabel='In/Outbound Data')


####GRAPH 3 PER HOUR #########
# Compute the max value (plt.hist returns the x and y positions of the bars)
yhmax = y2haxis.max()
idxh = np.where(y2haxis == yhmax)[0][0]
xvalh = xhaxis[idxh]
#Convert displayed value to Integer
yhmax = int(yhmax)
print(yhmax)

# Annotate the highest value
ax3.text(xvalh, yhmax, yhmax, ha='left', va='center', color='red', fontsize=7)

def gbyte(y2haxis, pos):
    #'The two args are the value and tick position'
    return '%1.0f GB/Hour' % (y2haxis)

formatter = FuncFormatter(gbyte)

p1 = ax3.bar(xhaxis, y2haxis, width=0.3, color='red')
p2 = ax3.bar(xhaxis, y3haxis, width=0.3, color='green')
ax3.grid(which='major', axis='y', linestyle='dotted')
ax3.text(dt.date(2020, 3, 23), 135, "C-19 Lock Down --->", color='gray', fontsize=6, rotation=270)
ax3.legend((p1[0], p2[0]), ('Inbound (Downloaded) GB per Hour', 'Outbound (Uploaded) GB per Hour'), loc='upper right', fontsize='x-small')
# Set the locator
locator = mdates.MonthLocator()  # every month
# Specify the format - %b gives us Jan, Feb...
ax3.xaxis.set_major_locator(locator)
myFmt = DateFormatter("%b %Y")
ax3.xaxis.set_major_formatter(myFmt)
ax3.yaxis.set_major_formatter(formatter)
ax3.set(title='Internet Proxy Volume of Traffic - INBOUND & OUTBOUND (GB per Hour)', ylabel='In/Outbound Data')

#df.plot(kind='bar', y='Total Bytes', figsize=(10, 3), use_index=True)
#plt.savefig('ProxyTotalandInbound.pdf', bbox_inches='tight', pad_inches=2)
plt.savefig('ProxyIn&Outbound.png', bbox_inches='tight', pad_inches=0.5)
#df.groupby(['Bytes Received', 'Bytes Sent']).size().unstack().plot(kind='bar', stacked=True)
#plt.plot_date([d.astype(datetime.datetime) for d in df[0]], df['Total Bytes'])
plt.show()

"""
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

TotBytes = round(df['Total Bytes'].sum(), 0)
TotBytes = f"{TotBytes:,}"

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

print('Maximum value in each column : ')
print(TotBytes)
print(TotValues)

#print('Sum of Request, grouped by the Hour of Day: ' + str(groupby_sum1))
"""