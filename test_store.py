import time
import find_jpl_position as jpl

target = 'niobe'
t = time.strftime('%Y-%m-%dT%H:%M:%S') # current time in ISO format

jpl.new_session()

jpl.set_target(target)
jpl.set_time(t)


t = time.strftime('%Y-%m-%dT%H:%M:%S')
jpl.set_target(target)
jpl.set_time(t)