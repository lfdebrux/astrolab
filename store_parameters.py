def store_parameters(func):
	cache = {}

	def memoizedFunction(param):
		print param,cache
		if 'params' not in cache or cache['params'] is not param:
			print "Calling func..."
			cache['params'] = param
			func(param)
		print param,cache
		return cache
	
	memoizedFunction.cache = cache
	return memoizedFunction