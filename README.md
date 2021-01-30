## Solution description ##
This solution uses Pandas - Python Data Analysis Library for aggregating data from provided CSV files and processing the required queries. 
Python Flask is used to serve the queries with REST API.
Sessionizing is done by grouping the data to chunks which are specific to a site and a visitor for example here is the chunk, representing all visits of `visitor_1` to `www.s_1.com`:
![site visitor visits](./imgs/site_visito_visits.png)

Now we can look at visits timestams and find the time difference between each visit. If the difference less than 30 min we will mark those visits with the same session_id. We will change session_id (increase by 1) if the visits time stamps differ more than in 30 min.

While doing this we can also calculate a session duration.

Instead of updating existing data table (DataFrame) it's faster to create new one (`sessisons_df`) which has the follwoing fields:
![sessionized](./imgs/sessionizing.png)
On the picture, `visitor_1002` visits separated to 2 different sessions (marked with session_id 4 and 5) starting at the index 16 as a result of the difference between visits times (1347888253 - 1347869050 = 19203 sec) which is greater than 30 min. Session duration was 2770 sec for session_id 4 and 469 sec for session_id 5.

This is all we need in order to be able to efficiently answer required queries.

Supported queries examples are listed below with responses:
```
GET /num_sessions?site_url=www.s_5.com
> Num sessions for site www.s_5.com = 3623
```

```
GET /median_session_length?site_url=www.s_3.com
> Median session length for site www.s_3.com = 1392.5
```

```
GET num_unique_visited_sites?visitor_id=visitor_1
> Num of unique sites for visitor_1 = 3
```

---


## Running server from docker ##
```
docker pull aliowka/sessionizer
docker run -p 5000:5000 aliowka/sessionizer
```
Navigate in browser to the link http://localhost:5000

---

## Running server from sourcecode ##
```
git clone http://github.com/aliowka/sessionizer`
cd sessionizer
```

### Create the environment ###
```
python3 -m venv venv
```

### Activate the environment ###
```
source venv/bin/activate
```

### Install project dependencies ###
```
pip install -r requirements.txt
```

### Run web-server ###
```
flask run
```

---

## Running tests ##
```
export PYTHONPATH=$(pwd)
export FLASK_APP src/app.py
pytest tests -v
```

The server will start on http://localhost:5000/ 

---

## Space and time complexity ##
In order to build the table `sessions_df` which described above we accomplish following steps:
 1. Merge provided CSV files. `O(n)` time and `O(n)` space
 2. Sort the resulting file by timestamp. `O(nlog(n))` time and `O(n)` space
 3. Filter by site and group by visitor. `O(n)` and `O(n)`
 4. Iterate through such groups and creat global sessions table. Overall `O(n)` and `O(n)`
 5. Each incoming request will end up iterating this sessions table maximum 1 time. `O(n)` and `O(1)`

Finally we have a time complexity `O(4n+nlogn)` which bound by `O(nlogn)` and space complexity `O(n)`.


---

## Thoughs about scaling ##
>Scale in terms of increasing ammount of data.

Althought the complexity of the algorithm seems to be near lenear `O(4n+nlogn)`. Already with 150K (145964 to be precise) input entries it becomes very slow - about 30 seconds to compute all sessions. 
The algorithm currently makes 4 iterations (separate steps for the sake of simplicity) over the data table and one sorting. With 150K input entries it gives us `4*150K+150K*log(150K)=1.35M` iterations! 
Of cause this might be improved. Below are the steps that I would consider:
1. Instead of 4 separate iterations we can rewrite the algorithm to compute sessions in a one single pass. 
This will reduce the ammount of iterations from `1.35M` to `900K` which is `66%`, so expected execution time will become `30 seconds * 0.66 = 19 seconds`, which is still a lot when it comes to a human waiting in front of his browser.
2. Preprocessing and caching for commonly used results. For example in this project I'm using `memoization.cached` decorator on `create_sessions_from_input_data` function to not recompute it for the same site multiple times. And I'm running a javascript on main page load even which sends the requests to __warm__ the cache. It's done once, at the first time the main page is visited and lets the other queries to execute in less then a second.
3. There is a project called [modin](https://github.com/modin-project/modin) which claims a lenear runtime improvement by scaling pandas process to multiple cores on the same machine (I didn't manage to get it work on mine).
4. Consider distributed processing frameworks like Spark, Hadoop, Discoproject etc.. For this purpose we might want to formulate our task in terms of map-reduce to compute the results, and any supported query language on a given frameworks to query the results. We also will need REST API access in order to run those queries, wait for results are ready (optionally), get the results.

> Scale in terms of increasing ammount of outside clients.

In order to support the increasing ammount of clients which will access our system with REST API I would consider the following steps:
1. Serve the client as fast as possible to not handle additional opened connection. For this purpose the paragraphs mentioned above take place.
2. Provide API for client to be able to wait for a result. For example return the response with specified unfinished task id and ammount of time when to come next time to check. This is required to release the client as fast as possible as mentioned before.
3. Provide reliable auotoscaling mechanism for REST API servers - Load Balancer + Metric Based autoscaling. Metrics may be chosen according to expected bottlenecks such as number of opened connections per machine, machine CPU and/or Memory usage etc... whichever better indicates the current state of the load.

---
## Code Testing ##
In addition to the tests, checking the expected results, provided in the assignment, I created [jupyter notebook](https://github.com/aliowka/sessionizer/blob/master/playground.ipynb) which allowed me to slice and dice the input data and test different possible solutions.

I have to admit that one test-case (out of 30) is falling for me.
For `www.s_5.com` I'm getting median of session lenth equals to `1374.0` instead of `1375.0`. Same algorithm gives me correct answers for all other sites. I'm not sure what's the problem there. It may be related to different floating point implementations on different hardware/softaware systems as described [here](https://stackoverflow.com/a/53144736) In order to investigate this issue further, I would test both systems face-to-face, which is out of the scope of this task.

