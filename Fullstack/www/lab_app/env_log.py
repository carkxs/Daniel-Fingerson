import sqlite3
import sys
from MultiSPIonline import read, select
def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/home/pi/Desktop/Fullstack/www/lab_app/lab_app.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	# For the time-related code (record timestamps and time-date calculations) to work 
	# correctly, it is important to ensure that your Raspberry Pi is set to UTC.
	# This is done by default!
	# In general, servers are assumed to be in UTC.
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,temp))
	curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()

#humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
# If you don't have a sensor but still wish to run this program, comment out all the 
# sensor related lines, and uncomment the following lines (these will produce random
# numbers for the temperature and humidity variables):
select(1)
voltages=read()
temperature=voltages[0]
humidity=voltages[1]

log_values("1", temperature, humidity)	
