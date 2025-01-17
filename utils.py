"""
Utilities for various common things we might need to do while working on astrolab data.
Mostly manipulations for RA and Dec
"""

# placeholders for packages we may or may not need
re = None
subprocess = None
math = None

def ra2hr(ra):
	"""Turn an RA tuple into one number in hours"""
	return dec2deg(ra)

def ra2deg(ra):
	"""Turn an RA tuple into one number in degrees of arc"""
	return 15*ra2hr(ra)

def dec2deg(dec):
	"""Turn a Dec tuple into one number in degress of arc"""
	# only import math when we need it
	global math
	if math is None: import math
	
	sign = reduce(lambda x,y: x*y,
		#map(lambda x: math.copysign(1,float(x)),dec)
		[math.copysign(1,float(x)) for x in dec]
		)
	return sign*sum(
		#map(lambda x,y: abs(float(x))/float(y), dec, (1, 60, 3600))
		[abs(float(x))/float(y) for x,y in zip(dec,(1,60,3600))]
		)

def delta_ra(ra1,ra2):
	"""Subtract two RA tuples and return the result as one number in degrees of arc"""
	return ra2deg(ra1)-ra2deg(ra2)

def delta_dec(dec1,dec2):
	"""Subtract two Dec tuples and return the result as one number in degrees of arc"""
	return dec2deg(dec1)-dec2deg(dec2)

def deg2dmstuple(dec):
	"""Take a number in degrees of arc and return a Dec tuple"""
	return tuple(dmsStrFromDeg(dec).split(':'))

def deg2hmstuple(ra):
	"""Take a number in degrees of arc and return an RA tuple"""
	# only import re when we need it
	global re
	if re is None: import re

	ra = re.split('[hms]',deg2hms(ra))
	del ra[-1] # get rid of trailing ''
	return tuple(ra)

def deg2dms(degree):
	"""from jrl_utils.py"""
	out=dmsStrFromDeg(degree)
	out2=out.replace(':','d',1)
	out3=out2.replace(':','m',1)
	return (out3 + 's')
#    sign = '+'
#    if degree < 0.0: sign = '-'
#    degree = abs(degree)
#    ideg=int(degree)
#    mind=abs(ideg-degree)*60
#    mins=int(mind)
#    sec=(mind-mins)*60
#    isec = int(sec)
#    frac = int((sec - float(isec))*10.+0.5)
#    out = "%s%2.2dd%2.2dm%2.2d.%1ds" % (sign,ideg,mins,sec,frac)
	return out
 
def deg2hms(degree):
	"""from jrl_utils.py"""
	hour = degree/15.
	ihour=int(hour)
	mind=abs(hour-ihour)*60
	mins=int(mind)
	sec=(mind-mins)*60
	isec = int(sec)
	frac = int((sec - float(isec))*100.+0.5)
	out = "%2.2dh%2.2dm%2.2d.%2.2ds" % (ihour,mins,sec,frac)
	return out

def dmsStrFromDeg (decDeg, nFields=3, precision=1, omitExtraFields = False):
	"""
	Convert a number to a sexagesimal string with 1-3 fields.

	Inputs:
	- decDeg: value in decimal degrees or hours
	- nFields: number of fields; <=1 for dddd.ddd,
									   2 for dddd:mm.mmm,
									 >=3 for dddd:mm:ss.sss
	- precision: number of digits after the decimal point in thelast field;
		if 0, no decimal point is printed; must be >= 0
	- omitExtraFields: omit fields that are zero, starting from the right

	Error conditions:
	- Raises ValueError if precision < 0

	from jrl_utils.py
	"""
	if nFields <= 1:
		return "%.*f" % (precision, decDeg)
	nFields = min(3, nFields)
		# to allow more than 3 fields, omit this statement

	if decDeg < 0:
		signStr = "-"
		decDeg = abs(decDeg)
	else:
		signStr = "+"

	# compute a list of output fields; all but the last one are integer
	remVal = decDeg
	fieldList = []
	for fieldNum in range(nFields-1):
		(intVal, remVal) = divmod (abs(remVal), 1.0)
		intVal = int(intVal)
		fieldList.append(intVal)
		remVal *= 60.0

	# compute last field as a string, but don't add to the field list
	# until we've handled fields >= 60
	if precision > 0:
		minFloatWidth = precision + 3
	elif precision == 0:
		minFloatWidth = 2
	else:
		raise ValueError("precision=%r; must be >= 0" % (precision,))
	lastFieldStr = "%0*.*f" % (minFloatWidth, precision, remVal)

	# make sure no field is >= 60 (except the first field)
	# and then convert all fields to strings
	if lastFieldStr[0] == "6":
		lastFieldStr = "0" + lastFieldStr[1:]
		incrNextField = True
	else:
		incrNextField = False
	for fieldInd in range(nFields-2, -1, -1):
		if incrNextField:
			fieldList[fieldInd] += 1
		if fieldInd == 0:
			fieldList[fieldInd] = "%s%02d" % (signStr,fieldList[fieldInd])
		else:
			if fieldList[fieldInd] >= 60:
				fieldList[fieldInd] -= 60
				incrNextField = True
			else:
				incrNextField = False
			fieldList[fieldInd] = "%02d" % fieldList[fieldInd]
	fieldList.append(lastFieldStr)

	if omitExtraFields:
		while fieldList and float(fieldList[-1]) == 0.0:
			fieldList.pop(-1)

	return ":".join(fieldList)
