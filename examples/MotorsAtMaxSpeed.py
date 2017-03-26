import matplotlib.pyplot as plt
import csv
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

# MatPlotlib
from matplotlib import pylab

# Scientific libraries
from numpy import arange,array,ones
from scipy import stats


plotly.tools.set_credentials_file(username='sstef', api_key='IkjiDR8UC1YoIY7Bwzg7')

x = arange(1, 20, 1)

average = []
fl = []
fr = []
rl = []
rr = []



with open('HoloEncodersAnalysis.txt', 'r') as csvfile:
	plots = csv.reader(csvfile, delimiter=',')
	
	for row in plots:
		average.append(float(row[0]))	
		fl.append(float(row[1]))
		fr.append(float(row[2]))
		rl.append(float(row[3]))
		rr.append(float(row[4]))
	#print average
	#print fl
	#print fr
	#print rl


trace0 = go.Scatter(
    x = x, 
    y = average,
)
trace1 = go.Scatter(
    x = x, 
    y = fl,
)
trace2 = go.Scatter(
    x = x, 
    y = fr,
)
trace3 = go.Scatter(
    x = x, 
    y = rl,
)
trace4 = go.Scatter(
    x = x, 
    y = rr,
)

fig = tools.make_subplots(rows=2, cols=2, shared_yaxes=True, subplot_titles=('FL M1', 'FR M2','RL M4', 'RR M3'))

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 2, 1)
fig.append_trace(trace4, 2, 2)


fig['layout'].update(height=600, width=600,
                     title='Four Motors at same Max Speed of 255')
plot_url = py.plot(fig, filename='multiple-subplots-shared-yaxes')

