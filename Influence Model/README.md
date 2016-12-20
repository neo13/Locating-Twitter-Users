# Tweefind
Tweefind is a tool to locate Twitter users via their tweets. 
## Introduction
This implementation, is of an algorithm introduced in "http://dl.acm.org/citation.cfm?id=2339692", with minor modifications. 

## How to use
1. Clone this repository. 
2. Create your virtual environment: 

        virtualenv venv
    
3. Activate the virtual env using this command:

        source venv/activate
    
4. Install the requirements of this project:

        pip install requirements
    
5. Run "db/load_redis.py". This will load all location names into a redis server in memory for fast querying.
6. Run "db/load_mongo.py". This will read all the data files and store information on a mongodb server.
7. Run "learner.py" to learn influence values for all location names in the database. 
8. Use "predicy.py" to predict the location of a tweet/user.
