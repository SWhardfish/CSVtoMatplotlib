from pandas import read_csv
from matplotlib import pyplot
series = read_csv('bandwidth_20200309_0100_81.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
#print(series.head())
series.plot()
#pyplot.show()
pyplot.savefig('Bandwidth.png')
