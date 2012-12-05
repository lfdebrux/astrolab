"""
Get RA and Dec for an target from JPL Horizons.
Useage:
get_jpl_position.py target_name time

where time is in ISO format, ie
'YYYY-MM-DD hh:mm:ss'
"""

import signal
import urllib
import sys
import datetime
import pytz

from store_parameters import store_parameters

TEL_LONG_DEG = 1.583
TEL_LAT_DEG = 54.767
TEL_HEIGHT = 75.

URL = 'http://ssd.jpl.nasa.gov/horizons.cgi'

session_id = None

def query(params):
	params = urllib.urlencode(params)
	urllib.urlopen(URL, params).close()

@store_parameters
def set_target(target):
	"""Tell Horizons which object we want ephemeris for"""
	
	# print "Checking target " + target + " exists ... "
	
	params = urllib.urlencode({
		'sstr' : target,
		'find_body' : 'Search',
		'CGISESSID' : session_id
	})

	jpl = urllib.urlopen(URL, params)

	for line in jpl:
		# print line
		if 'Generate Ephemeris' in line:
			break
	else:
		raise ValueError("No matching body found!")

	jpl.close()

	# print "Setting target to " + target + "... "

	params = {
		'body' : target,
		'select_body' : 'Select Indicated Body',
		'CGISESSID' : session_id
	}

	query(params)

	#target = new_target
	
	return target

@store_parameters
def set_observer(observer):
	"""Set observer location"""

	# print "Setting observer location ... "
	
	params = {
		# 'lon' : TEL_LONG_DEG,
		# 'ulon' : 'W',
		'lon' : 360.-TEL_LONG_DEG,  # this is what JPL needs
		'ulon' : 'E',
		'lat' : TEL_LAT_DEG,
		'u_lat' : 'N',
		'alt' : '0.122',
		's_pos' : 'Use Specified Coordinates',
		'CGISESSID' : session_id
	}

	query(params)

	return observer

@store_parameters
def set_time(time):
	"""Set date and time"""

	# print "Setting date and time ..."
	
	end_time = calculate_end_time(time)

	params = {
		'start_time' : time,
		'stop_time' : end_time,
		'step_size' : '1',
#		'selected' : 'm',
		'set_time_span' : 'Use Specified Times',
		'CGISESSID' : session_id
	}

	query(params)

	return time

def calculate_end_time(time):

	year  = int(time[0:4])
	month = int(time[5:7])
	mday  = int(time[8:10])
	hour  = int(time[11:13])
	mins  = int(time[14:16])
	secs  = int(time[17:19])
	msecs = long(time[20:].ljust(6,'0'))
	
	# print time[20:]
	# print msecs

	date = datetime.datetime(year, month, mday, hour, mins, secs, msecs, tzinfo=pytz.UTC)
	date += datetime.timedelta(minutes=1)

	# print str(date)
	
	return str(date.date()) + " " + str(date.time())

def get_ephemeris():
	"""Generate ephemeris"""

	# print "Generating ephemeris ..."

	params = urllib.urlencode({
		'go' : 'Generate Ephemeris',
		'CGISESSID' : session_id
	})

	jpl = urllib.urlopen(URL, params)

	# print "Extracting position ... "

	for line in jpl:
#		print line
		if '$$SOE' in line:
			req_line = jpl.next()
			break

	jpl.close()

#	print req_line.split()
	try:
		test=int(req_line.split()[2])
		(rah,ram,ras,ded,dem,des) = req_line.split()[2:8]
	except:
#		print 'ignoring solar/lunar entry'
		(rah,ram,ras,ded,dem,des) = req_line.split()[3:9]

	ra  = rah+' '+ram+' '+ras
	dec = ded+' '+dem+' '+des

	return ra, dec

def new_session():
	"""Get CGI session ID"""
	
	global session_id

	# print "Getting JPL session ID ... "
	
	jpl = urllib.urlopen(URL+'?')

	check = '<input type=\"hidden\" name=\"CGISESSID\" value=\"'

	for line in jpl:
		if check in line:
			session_id = line[len(check):len(check)+32]

	jpl.close()

	set_observer(True)

	# print session_id
	return session_id


def timeout(signum, frame):
	raise IOError('Failed: Timeout')

def find_jpl_position(target=None, time=None, session_id=None):

#	print "-------------->", target

	signal.signal(signal.SIGALRM, timeout)
	signal.alarm(20)   # 20 second timeout

	try:
		new_session()

		set_target(target)

		set_time(time)

		ra, dec = get_ephemeris()
		
	except:
		signal.alarm(0)
		raise

	signal.alarm(0) # cancel timeout

	return ra, dec

if __name__ == "__main__":

	obj_req = sys.argv[1]
	time  = sys.argv[2].replace('T',' ')

	year  = int(time[0:4])
	month = int(time[5:7])
	mday  = int(time[8:10])
	# hour  = int(time[11:13])
	# mins  = int(time[14:16])
	# secs  = int(time[17:19])

	#print year, month, mday, hour, mins, secs

	# print obj_req
	# print time

	ra, dec =  find_jpl_position(obj_req, time)
	# print type(ret_str), len(ret_str)

	# print ra, dec

	word = ra.split()
	ra_deg = float(word[0])*15. + float(word[1])/4. + float(word[2])/240.
	# print ra_deg
	word = dec.split()
	if "-" in word[0]:
		dec_deg = -1.*(abs(float(word[0])) + float(word[1])/60. + float(word[2])/3600.) 
	else:
		dec_deg = float(word[0]) + float(word[1])/60. + float(word[2])/3600.
	# print dec_deg

	print obj_req, "    ", year, month, mday, "   ", time.replace(' ','T'), \
		ra_deg, dec_deg, "    ", ra, dec
