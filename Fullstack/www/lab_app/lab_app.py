from flask import Flask, request, render_template
import time
import datetime
import sys
from MultiSPIonline import read, select
import sqlite3
#from dash import Dash

app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging


#begin new code
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen=30) #length of graph before it resizes horizontally
X.append(1)
Y = deque(maxlen=30)
Y.append(1)


app_dash = dash.Dash(__name__,server=app,routes_pathname_prefix='/dash/')
app_dash.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=10000, #updates every 10 seconds (in mS)
            n_intervals = 0
        ),
    ]
)

@app_dash.callback(Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')])


def update_graph_scatter(n):
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}






#end new code, bein old code

@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/input_dashboard")
def input_dashboard():
    return render_template("input_dashboard.html")

#@app.route('/live_data')
#def live_data():
#    return flask.redirect('/dash')

@app.route("/input_dashboard/new_run")
def new_run():
    return render_template("sample1.html")

@app.route("/input_dashboard/repeat_run")
def repeat_run():
    return render_template("sample2.html")

@app.route("/input_dashboard/review_run")
def review_run():
    return render_template("sample3.html")

@app.route("/input_dashboard/compare_runs")
def compare_runs():
    return render_template("sample4.html")

@app.route("/input_dashboard/calibrate_system")
def calibrate_system():
    return render_template("sample5.html")

@app.route("/live_data")
def live_data():
    return render_template("sample5.html")

@app.route("/lab_temp")
def lab_temp():
	select(1)
	voltages=read()
	temperature=voltages[0]
	humidity=voltages[1]
	return render_template("lab_temp.html",temp=temperature,hum=humidity)

@app.route("/lab_env_db", methods=['GET']) 
def lab_env_db():
	temperatures, humidities, from_date_str, to_date_str = get_records()
	return render_template(	"lab_env_db.html", 	temp 			= temperatures,
							hum 			= humidities,
							from_date 		= from_date_str, 
							to_date 		= to_date_str,
							temp_items 		= len(temperatures),
							hum_items 		= len(humidities))

def get_records():
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
	range_h_form	= request.args.get('range_h','');  #This will return a string, if field range_h exists in the request

	range_h_int 	= "nan"  #initialise this variable with not a number

	try: 
		range_h_int	= int(range_h_form)
	except:
		print ("range_h_form not a number")

	if not validate_date(from_date_str):			# Validate date before sending it to the DB
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")		# Validate date before sending it to the DB

	# If range_h is defined, we don't need the from and to times
	if isinstance(range_h_int,int):	
		time_now		= datetime.datetime.now()
		time_from 		= time_now - datetime.timedelta(hours = range_h_int)
		time_to   		= time_now
		from_date_str   = time_from.strftime("%Y-%m-%d %H:%M")
		to_date_str	    = time_to.strftime("%Y-%m-%d %H:%M")

	conn=sqlite3.connect('/home/pi/Desktop/Fullstack/www/lab_app/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	temperatures 	= curs.fetchall()
	curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	humidities 		= curs.fetchall()
	conn.close()
	return [temperatures, humidities, from_date_str, to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False
#after this new code will exist untill if name

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
