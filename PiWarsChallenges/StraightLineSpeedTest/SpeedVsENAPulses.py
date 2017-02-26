import matplotlib.pyplot as plt
import csv
import plotly.plotly as py
import plotly.graph_objs as go

# MatPlotlib
from matplotlib import pylab

# Scientific libraries
from numpy import arange,array,ones
from scipy import stats



x = arange(195, 265, 10)
average = []
m1 = []
m3 = []


with open('Encoders1_3.txt', 'r') as csvfile:
	plots = csv.reader(csvfile, delimiter=',')
	
	for row in plots:
		average.append(float(row[1]))	
		m1.append(float(row[2]))
		m3.append(float(row[3]))
		#print row
#print x

A = array([ x, ones(7)])


slope, intercept, r_value, p_value, std_err = stats.linregress(x,average)
lineAvg = slope*x+intercept
plt.plot(x,average,'o', x, lineAvg)

slopem1, interceptm1, r_valuem1, p_valuem1, std_errm1 = stats.linregress(x,m1)
linem1 = slopem1*x+interceptm1
plt.plot(x,m1,'o', x, linem1)

slopem3, interceptm3, r_valuem3, p_valuem3, std_errm3 = stats.linregress(x,m3)
linem3 = slopem3*x+interceptm3
plt.plot(x,m3,'o', x, linem3)

pylab.title('Linear Fit with Matplotlib')
ax = plt.gca()
ax.set_axis_bgcolor((0.898, 0.898, 0.898))
fig = plt.gcf()

plt.plot(x,average, 'ro')
plt.xlabel('speed')
plt.ylabel('# of ENA pulses')

my_legend = "average = "+ str(intercept)+ " + "+ str(slope)+ "*x, " +" std_err = "+str(std_err)
#plt.legend(my_legend)
plt.title(my_legend)
plt.show()
#y.plot_mpl(fig, filename='linear-Fit-with-matplotlib')

print "intercept avg", intercept, " slopeavg ", slope
print "intercept m1", interceptm1, " slopem1 ", slopem1
print "intercept m3", interceptm3, " slopem3 ", slopem3
  
