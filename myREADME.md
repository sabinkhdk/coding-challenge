Solution of Insight Data Engineering coding challenge
==============================================================

@author: mr.sabinkhadka@gmail.com

Date 07/14/2016

===

# Task

1. Clean and extract information os venmot transaction provided in JSON format
    * Extract timestamp of when transaction occured
    * Extract actor and target

2. Maintain data within 60 seconds
    * We would only be calculating median degree of actor <--> target of transaction within 60 secs window
    * Calculate difference of transaction from the recent 

3. Graph creation from actor, target
    * Python package *networkx* was used to create graph and get degrees of each nodes
    * Calculate degrees of only valid transaction
    * No calculation was done if either of actor, target and datetime field were empty
    
====

## Workflow

1. Read venmo transaction file (in json format)

2. Parse and clean json line (extract actor, target and created timestamp)

3. Remove unvalid json line and store in table

4. Calculate time differene of all transaction from newest transaction.

5. Delete records of transaction beyond 60 seconds.

6. Create graph with edges from actor <--> transasction values in table within 60 seconds period.

7. Calculate median of degrees of each nodes of the Graph and write it in a output file (output.txt)

===

### Python Packages used

1. json
2. time
3. sys
4. sqlite3
5. datetime
6. networkx
7. numpy