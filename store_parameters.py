def store_parameters(func):
	cache = {}

	def memoizedFunction(*param):
		if 'param' not in cache or cache['param'] is not param:
			print "Calling func..."
			cache['param'] = param
			func(*param)
		print param,cache
		return cache
	
	memoizedFunction.cache = cache
	return memoizedFunction