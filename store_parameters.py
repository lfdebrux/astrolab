def store_parameters(func):
	cache = {}

	def memoizedFunction(param):
		# print param,cache
		if 'params' not in cache or cache['params'] is not param:
			# print "Calling func " + func.func_name +"..."
			cache['params'] = param
			func(param)
		# else:
			# print "Skipping func " + func.func_name + "..."
		# print param,cache
		return cache
	
	memoizedFunction.cache = cache
	return memoizedFunction