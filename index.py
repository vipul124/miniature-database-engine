################################
# Non Editable Region Starting #
################################
def my_index( tuples ):
################################
#  Non Editable Region Ending  #
################################
	# Each tuple has 3 values -- the id, name and year
	
	# A. Creating a Disk - we are going to use two different arrays for disk mapping,
		# one by sorting in order of names 
		# and another one by sorting in order of years
	n = len(tuples)
	tuple_idx = [[t, i] for i, t in enumerate(tuples)]
	
	## Sort by year and name and create an array to make internal mapping between them inside the disk
	sorted_by_year = sorted(tuple_idx, key=lambda x: (x[0][2], x[0][1]))
	idx_year = [None] * n
	for i, t in enumerate(sorted_by_year):
		idx_year[t[1]] = i

	sorted_by_name = sorted(tuple_idx, key=lambda x: (x[0][1], x[0][2]))
	idx_name = [None] * n
	for i, t in enumerate(sorted_by_name):
		idx_name[t[1]] = i

	## Create the disk - first n are ids sorted by year and next n are ids sorted by name
	disk = [t[0][0] for t in sorted_by_year] + [t[0][0] for t in sorted_by_name]


	# B. Creating internal disk mapping index 
		# this is an index of size 2n each element of which stores the other index of the same id in the disk
		# example: if id 5 is at index 3 in disk due to sorting by year, and on index 18 in disk due to sorting by name then disk_idx[5] = 18 and disk_idx[18] = 5
	disk_idx = [None] * 2 * n
	for i in range(n):
		disk_idx[idx_year[i]] = idx_name[i] + n
		disk_idx[n + idx_name[i]] = idx_year[i]


	# C. Creating some useful stats	
	stats = [
		min(t[2] for t in tuples),		# a. min year 
		max(t[2] for t in tuples), 		# b. max year
		0,								# c. start index of year in disk
		n-1								# d. end index of year in disk
	]
	

	# D. Creating the index for years 
		# sorted list - kind of hashmap only each storing the starting and ending index of that year in the disk
	year_idx = [None] * (2100 - 1900 + 1)		# index 0 => 1900 and index 200 => 2100
	i = 0
	for y in range(1900, 2101):
		year_idx[y - 1900] = [None] * 2
		year_idx[y - 1900][0] = i				# start index
		while i < n and sorted_by_year[i][0][2] == y:
			i += 1
		year_idx[y - 1900][1] = i - 1			# end index


	# E. Creating the index for names
		# trie - each trie node has 26 children and 3 parameters
		# children: list of 26 children, each pointing to another trie node
		# params: [start_index in disk, no of entries that match, no of entries that are greater]
	def createTrieNode():
		children = [None] * 26
		params = [None, 0, 0]	  	# [start_index in disk, no of entries that match, no of entries that are greater]
		return [children, params]
		
	name_idx = createTrieNode()
	for i, tup in enumerate(sorted_by_name):
		name = tup[0][1]
		node = name_idx
		for c in name:
			idx = ord(c) - ord('a')
			if node[0][idx] is None:
				node[0][idx] = createTrieNode()
			if node[1][0] is None:
				node[1][0] = i + n
			node[1][2] += 1				# storing this entry in greater count
			node = node[0][idx]

		if node[1][0] is None:
			node[1][0] = i + n
		node[1][1] += 1					# storing this entry in match count
		node[1][2] += 1					# storing this entry in greater count as well cuz LIKE includes equality also


	# FINAL INDEX OBJECT
	idx_stat = [
		disk_idx,			# a. disk mapping index
		year_idx, 			# b. year index
		name_idx,			# c. name index 
		stats				# d. stats
	]

	# THE METHOD SHOULD RETURN A DISK MAP AND A VARIABLE PACKAGING INDICES AND STATS
	return disk, idx_stat