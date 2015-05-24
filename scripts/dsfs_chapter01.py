# 'Data Science from Scratch' Chapter 1 exampl

# Create list of users
userNames = ["Hero", "Dunn", "Sue", "Chi", "Thor", "Clive", "Hicks", "Devin", "Kate", "Klein"]
users = []
for ind, name in enumerate( userNames ):
    users.append( {"id": ind, "name": name})
    
# Helper function to get id
get_id = lambda userlist: map( lambda user: user["id"], userlist)
    
# Friendship 
friendships = [(0,1), (0,2), (1,2), (1,3), (2,3), (3,4), (4,5), (5,6), (5,7), (6,8), (7,8), (8,9)]
# Store as directed graph
g = friendships
g.extend(map(lambda(i,j): (j,i), friendships))

# Add the list of friends to each user
for user in users:
    user["friends"] = []
    
for i,j in g: 
    users[i]["friends"].append(users[j])
    
# Number of friends each user has
number_of_friends = lambda (user): len(user["friends"])
# Total numnber of connections
number_of_connections = reduce(lambda acc, el: acc + number_of_friends(el), users, 0)

# Sort by popularity
map(lambda user:(user["name"], number_of_friends(user)), 
  sorted(users, key=lambda user:number_of_friends(user), reverse=True))
  
# Friend of a friend
# A friend of a friend is someone who is not your friend 
# but is the friend of one of your friends

# Want to keep track of how many ways we are foaf with each person
from collections import Counter

def foaf(user): 
    all_id = get_id(reduce( lambda acc, user: acc + user["friends"], user["friends"], []))
    # Remove user id and user friends id
    ignore_id = get_id(user["friends"]) + [user["id"]]
    foaf_id = filter( lambda id: id not in ignore_id, all_id)
    return Counter(foaf_id)
    
# Mutual interests
# Store interests as a lookup from user id to list of interests
interests_dict = {0: ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"], 
  1: ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres", "Python", "scikit-learn", "scipy"],
  2: ["numpy", "statsmodels", "pandas"],
  3: ["R", "Python", "statistics", "regression", "probability"],
  4: ["machine learning", "regression", "decision trees", "libsvm"],
  5: ["Python", "R", "Java", "C++"], 
  6: ["statistics", "theory", "probability", "mathematics"],
  7: ["machine learning", "scikit-learn", "Mahout", "neural networks"],
  8: ["neural networks", "deep learning", "Big Data", "artificical intelligence"], 
  9: ["Hadoop", "java", "MapReduce", "Big Data"]}

# Invert to look up from interest to list of user ids
from collections import defaultdict
users_dict = defaultdict(list)   
for k in interests_dict.keys():
  map(lambda v: users_dict[v].append(k), interests_dict[k])
  
def most_common_interests_with(user):
    user_interests = interests_dict[user["id"]]
    id_list = map( lambda interest: users_dict[interest], user_interests)
    all_ids = filter(lambda x: x!= user["id"], reduce( lambda acc, ids: acc+ids, id_list, []))
    return Counter(all_ids)
    
# Find topics of interest
topic_count = map( lambda k: (k.lower(), len(users_dict[k])), users_dict.keys())
topic_dict = defaultdict(int)
for topic, count in topic_count: 
    topic_dict[topic] += count
Counter(topic_dict)
