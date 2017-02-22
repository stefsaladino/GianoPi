import matplotlib.pyplot as plt
import csv
import plotly.plotly as py
import plotly.graph_objs as go

# MatPlotlib
from matplotlib import pylab

# Scientific libraries
from numpy import arange,array,ones
from scipy import stats



x = arange(100, 255, 20)
y = []

with open('EncodersA.txt', 'r') as csvfile:
	plots = csv.reader(csvfile, delimiter=',')
	for row in plots:
		y.append(float(row[1]))


A = array([ x, ones(8)])
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
line = slope*x+intercept

plt.plot(x,y,'o', x, line)
pylab.title('Linear Fit with Matplotlib')
ax = plt.gca()
ax.set_axis_bgcolor((0.898, 0.898, 0.898))
fig = plt.gcf()
plt.plot(x,y, 'ro')
plt.xlabel('speed')
plt.ylabel('# of ENA pulses')

my_legend = "y = "+ str(intercept)+ " + "+ str(slope)+ "*x, " +" std_err = "+str(std_err)
#plt.legend(my_legend)
plt.title(my_legend)
plt.show()
py.plot_mpl(fig, filename='linear-Fit-with-matplotlib')

print "intercept ", intercept, " slope ", slope
 

		#plt.show()
