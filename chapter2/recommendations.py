from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def euclidian_distance(person1, person2):
	# A dictionary to hold common items
	common_items = {}

	# If item is present in both persons' records,
	# then store them
	for item in critics[person1]:
		if item in critics[person2]:
			common_items[item] = 1

	# If no common items, then they are dissimilar
	if len(common_items) == 0:
		return 0

	# Calculate the Euclidean distance for the common items
	distance = sum([pow(critics[person1][item] - critics[person2][item], 2) for \
			item in common_items])

	addition = 0.0
	for item in common_items:
		addition += pow(critics[person1][item] - critics[person2][item], 2)

	#print str(distance)+" "+str(addition)		

	# This ensures that denomitor is never 0
	return 1.0/(1 + sqrt(distance))


def pearson_correlation_coefficient(person1, person2):
	# A dictionary to hold the common items
	common_items = {}

	# Find the common items
	for item in critics[person1]:
		if item in critics[person2]:
			common_items[item] = 1

	N = len(common_items)
	if N == 0:
		return 0

	# Pearson's correlation coefficient is calculated as
	# p(X,Y) = Cov(X,Y)/(sig(X)*sig(Y))

	# step 1: Find Xmean and Ymean
	sumPerson1 = sum([critics[person1][item] for item in common_items])
	sumPerson2 = sum([critics[person1][item] for item in common_items])
	person1Mean = sumPerson1 * 1.0 / N
	person2Mean = sumPerson2 * 1.0 / N


	# step 2: Find Cov(X,Y)
	product_summation = sum([(critics[person1][item] - person1Mean) * (critics[person2][item] - person2Mean)
			for item in common_items])

	cov = product_summation * 1.0 / (N - 1)

	# step 3: Find standard deviation of X and Y (sig(X) and sig(y))
	
	sum_of_sqrs_person1 = sum([pow(critics[person1][item] - person1Mean, 2) for item in common_items])
	sum_of_sqrs_person2 = sum([pow(critics[person2][item] - person2Mean, 2) for item in common_items])

	sig_x = sqrt(sum_of_sqrs_person1 / (N - 1))
	sig_y = sqrt(sum_of_sqrs_person2 / (N - 1))

	# step 4: Find the Person's correlation coefficient
	p_x_y = 1.0 * cov/sig_x/sig_y

	return p_x_y

# Ranking the critics
def top_matches(person, n=5, distance_function=pearson_correlation_coefficient):
	scores = [(distance_function(person, other), other) for other in critics if other != person]
	scores.sort()
	scores.reverse()
	return scores

# Recommendation using weighted means
def getRecommendations(person, distance_function=pearson_correlation_coefficient):
	totals = {}
	sim_sum = {}

	# Work on every other person
	for other in critics:
		if other == person:
			continue

		similarity = distance_function(person, other)

		# Ignore if score is <= 0
		if similarity <= 0:
			continue

		for item in critics[other]:

			# Work on items which the person hasn't reviewed
			if item not in critics[person] or critics[person][item] != 0:
				# Give more weight to critics of other persons whose
				# interests match with those of the person's
				# #HorribleEnglish

				# setdefault() works only if the item is not present 
				# in the dictionary
				totals.setdefault(item, 0)
				totals[item] += critics[other][item] * similarity
				
				# Get the similarity sum
				sim_sum.setdefault(item, 0)
				sim_sum[item] += similarity
				
	recommendations = [(1.0 * total / sim_sum[item], item) for item, total in \
				totals.items()]

	recommendations.sort()
	recommendations.reverse()
	return recommendations


print euclidian_distance('Lisa Rose', 'Gene Seymour')
print pearson_correlation_coefficient('Lisa Rose', 'Gene Seymour')
print top_matches('Toby')
r = getRecommendations('Toby')
for i in r:
	print i
