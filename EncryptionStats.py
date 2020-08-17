import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

DataFiles = glob.glob('C:/Users/anders.rylander2/PycharmProjects/Stats/venv/Files/*Protocol*.csv') #creates a list of all csv files
#DataFiles = glob.glob('*Protocol*.csv') #creates a list of all csv files

data = []  # pd.concat takes a list of dataframes as an argument
for csv in DataFiles:
    frame = pd.read_csv(csv)
    frame['Date'] = os.path.basename(csv)
    data.append(frame)

df = pd.concat(data, ignore_index=True) #dont want pandas to try an align row indexes

#REGEX to extract Date from Filename
df['Date'] = df['Date'].str.extract('([0-9]{8})', expand=False)

#Index Date Column and Create DateTime column
df.index = pd.to_datetime(df["Date"])

#Drop Date column
df = df.drop(columns=["Date"])

#Date in Filename is for 1 day after so correcting here
df.index = df.index + pd.Timedelta(days=-1)

df['Total Bytes'] = df['Total Bytes']/1024/1024/1024 #Convert to GB
df['Bytes Received'] = df['Bytes Received']/1024/1024/1024 #Convert to GB
df['Bytes Sent'] = df['Bytes Sent']/1024/1024/1024 #Convert to GB
df['Requests'] = df['Requests']/1000 #Convert to K Request

#ratio = df['Bytes Received'] / df['Bytes Sent']
#print(ratio)
#df['RatioII'] = df['Bytes Received'] / df['Bytes Sent']
#print(df)


#Sort index (date) in cronological order)
df = df.sort_index()

#Name index column
df.index.name = 'DateTime'

HTTP = df.loc[df['Protocol'] == 'http']
#print(HTTP)
HTTPS = df.loc[df['Protocol'] == 'https']
#print(HTTPS)
#print(df)

HTTP['HTTPSReceived'] = HTTPS['Bytes Received'] #add the HTTPS column to the HTTP DF
Ratio = (HTTP['HTTPSReceived'] / (HTTP['Bytes Received'] + HTTP['HTTPSReceived'])) * 100
HTTP['Ratio'] = Ratio #add Ratio to the HTTP DF
HTTP = HTTP.drop(columns=["Page Views", "Bytes Sent", "Total Bytes", "Protocol"])
print(HTTP)



#Stats = df['Requests'].describe()
#print(Stats)

#df.insert(7, "HTTP", [HTTP], True)
#HTTPS = [df.loc[df['Protocol'] == 'https']]
#df['HTTPS'] = HTTPS

#print(df)
#Find largest value in column
##print(df['Total Bytes'].max())
#Print row with largest hour 'Total Bytes'
print('------------------------------------------------------------------------------')
print('Date and Hour with largest Total Thousand Requests:')
print(df[df['Requests'] == df['Requests'].max()])
print('------------------------------------------------------------------------------')
print('Date and Hour with largest Total GB:')
print(df[df['Total Bytes'] == df['Total Bytes'].max()])
print('------------------------------------------------------------------------------')
print('Date and Hour with largest Total Received GB:')
print(df[df['Bytes Received'] == df['Bytes Received'].max()])
print('------------------------------------------------------------------------------')
print('Date and Hour with largest Total Sent GB:')
print(df[df['Bytes Sent'] == df['Bytes Sent'].max()])
print('------------------------------------------------------------------------------')
#print(df.index)
#print(type(df.index))
##### P L O T #####
#df.plot(kind='bar', x='DateTime', y='Bytes Received', color='lightblue')
#df.plot(kind='bar', x='DateTime', y='Bytes Sent', color='lightblue')

#fig, ax = plt.subplots(figsize=(13, 3))
#xaxis = df.index
#yaxis = df['Total Bytes']
#ax.plot(xaxis, yaxis)
#xfmt = mdates.DateFormatter('%d %b')
#ax.xaxis.set_major_formatter(xfmt)
#plt.title('Amount of Data Uploaded Data during Peak Hour per Day')
#plt.ylabel('Uploaded Data (GB)')

##TEST SUBPLOT1##
#xaxis = df.index
#y1axis = df['Total Bytes']
#y2axis = df['Bytes Sent']
#y3axis = df['Bytes Received']

#plt.subplot(3, 1, 1)
#plt.plot(xaxis, y1axis)
#plt.title('3 subplots')
#plt.ylabel('Total Bytes (GB)')

#plt.subplot(3, 1, 2)
#plt.plot(xaxis, y2axis)
#plt.ylabel('Bytes Sent (GB)')

#plt.subplot(3, 1, 3)
#plt.plot(xaxis, y3axis)
#plt.ylabel('Bytes Received (GB)')
################

#######TEST SUBPLOT2#####
# Create two subplots sharing x axis
#xaxis = df.index
xHTTP = HTTP.index
y1axis = HTTP['Ratio']
y2axis = HTTP['HTTPSReceived']
y3axis = HTTP['Bytes Received']
y4axis = HTTP['Requests']


fig, (ax4, ax1, ax2) = plt.subplots(3, sharey=False, figsize=(15, 6))
plt.subplots_adjust(hspace=0.5)

ax4.plot(xHTTP, y4axis, color='black', linewidth=0.4)
ax4.grid(which='major', axis='y', linestyle='dotted')
ax4.legend(['Total Requests (x1000) per Day'], loc='upper right', fontsize='x-small')
ax4.set(title='Internet Proxy Volume of HTTPS Traffic - INBOUND', ylabel='No. Requests')

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

# Annotate
#style = dict(size=10, color='gray')
#ax1.text('2020-1-1', 50, "New Year's Day", **style)
#x_line_annotation = HTTP.Date(2020, 03, 03)
#x_text_annotation = df.index(2020, 03, 04)
#ax1.axvline(x=x_line_annotation, linestyle='dashed', alpha=0.5)
#ax1.text(x=x_text_annotation, y=90, s='Holiday in US', alpha=0.7, color='#334f8d')

p1 = ax2.bar(xHTTP, y2axis, width=0.7, color='red')
p2 = ax2.bar(xHTTP, y3axis, width=0.7, color='green')
ax2.grid(which='major', axis='y', linestyle='dotted')
#ax2.legend((y2axis, y3axis), ('HTTPS Received GB per Day', 'HTTP Received GB per Day'))
ax2.legend((p1[0], p2[0]), ('HTTPS Received GB per Day', 'HTTP Received GB per Day'), loc='upper right', fontsize='x-small')
ax2.set(ylabel='HTTP/S Data')

###ax3.bar(xHTTP, y3axis, width=0.7, color='green')
###ax3.grid(which='major', axis='y', linestyle='dotted')
###ax3.legend(['HTTP Received GB per Day'], loc='upper right', fontsize='x-small')
###ax3.set(ylabel='HTTP Data')

#df.plot(kind='bar', y='Total Bytes', figsize=(10, 3), use_index=True)
plt.savefig('ProxyEncrypted.pdf', bbox_inches='tight', pad_inches=2)
plt.savefig('ProxyEncrypted.png', bbox_inches='tight', pad_inches=0.5)
#df.groupby(['Bytes Received', 'Bytes Sent']).size().unstack().plot(kind='bar', stacked=True)
#plt.plot_date([d.astype(datetime.datetime) for d in df[0]], df['Total Bytes'])
plt.show()
#print(df)




