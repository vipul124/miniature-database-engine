# function to compare seeks of both the methods in order to return the best one
def getTime(arr):
	seeks = 0
	for i in range(1, len(arr)):
		seeks += abs(arr[i] - arr[i - 1] - 1)
	return seeks

# function defined to evaluate the year clauses and return the list of points on disk that satisfy the clause
def evaluateYearClause(clause, yearIdx, stats):
	if (clause[1] == "<=" or clause[1] == "=") and int(clause[2]) < stats[0]:
			return []
	if (clause[1] == ">=" or clause[1] == "=") and int(clause[2]) > stats[1]:
			return []
		
	if (clause[1] == "="):
		return list(range(yearIdx[int(clause[2]) - 1900][0], yearIdx[int(clause[2]) - 1900][1] + 1))
	if (clause[1] == "<="):
		return list(range(stats[2], yearIdx[int(clause[2]) - 1900][1] + 1))
	if (clause[1] == ">="):
		return list(range(yearIdx[int(clause[2]) - 1900][0], stats[3] + 1))
	
# function defined to evaluate the name clauses and return the list of points on disk that satisfy the clause
def evaluateNameClause(clause, nameIdx):
	def getTrieNode(trieRoot, chars):
		node = trieRoot
		for c in chars:
			idx = ord(c) - ord('a')
			if node[0][idx] is None: 
				return None
			node = node[0][idx]
		return node
	
	if (clause[1] == "="):
		node = getTrieNode(nameIdx, clause[2][1:-1])
		if node is None:
			return []
		return list(range(node[1][0], node[1][0] + node[1][1]))
	
	if (clause[1] == "LIKE"):
		node = getTrieNode(nameIdx, clause[2][1:-2])
		if node is None:
			return []
		return list(range(node[1][0], node[1][0] + node[1][2]))

# function defined to transform the disk pointers to the corresponding year / name pointers
def transformDiskPtrs(diskPtrs, diskIdx):
	return sorted([diskIdx[i] for i in diskPtrs])


################################
# Non Editable Region Starting #
################################
def my_execute( clause, idx ):
################################
#  Non Editable Region Ending  #
################################
	diskIdx = idx[0]
	yearIdx = idx[1]
	nameIdx = idx[2]
	stats = idx[3]

	# CASE 1: clause has only one predicate
	if len(clause) == 1:
		## A. If the predicate is on year
		if clause[0][0] == "year":
			return evaluateYearClause(clause[0], yearIdx, stats)
		
		## B. If the predicate is on name
		if clause[0][0] == "name":
			return evaluateNameClause(clause[0], nameIdx)
		
			
	# CASE 2: clause has two predicates - conjunctive query
		# APPROACH -
		# 1. evaluate the name and year clauses separately
		# 2. shift the name / year disk points to the corresponding year / name disk points using disk index
		# 3. find the sorted intersection of the two sets
	if len(clause) == 2:
		yearClause = clause[0] if clause[0][0] == "year" else clause[1]
		nameClause = clause[0] if clause[0][0] == "name" else clause[1]

		yearArr = set(evaluateYearClause(yearClause, yearIdx, stats))
		nameArr = set(diskIdx[i] for i in evaluateNameClause(nameClause, nameIdx))       # name disk points transformed to year disk points

		## In case any array is empty, return nothing
		if not yearArr or not nameArr:
			return []

		## Finding the sorted intersection of the two sets
			# yearDiskPtrs - disk points in order of years and then names
			# nameDiskPtrs - disk points in order of names and then years
		yearDiskPtrs = sorted(list(yearArr & nameArr))
		nameDiskPtrs = transformDiskPtrs(yearDiskPtrs, diskIdx)
		
		# returning the ans with best possible seeks
		return nameDiskPtrs if (getTime(nameDiskPtrs) < getTime(yearDiskPtrs)) else yearDiskPtrs
	
	return []