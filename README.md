All code is here: https://github.com/dbabits/pxs_coding_challenge

Make sure to checkout the entire repository because it includes dependencies and because the scripts assume the directory structure like in the repo. 

# Webservice that hashes a string.
- Deployed at: .....
- Instructions shown when this default url is hit

Scalability and other improvements: 
- The service keeps the database of hashes and strings in-memory, they are not persisted. A database would be best in real-life usage
 - Use a (NoSql) key-value database to store hashes and messages, e.g. Redis, AWS Dynamo, AWS SimpleDB
- Put the service into a container and scale using OpenShift, or AWS Container Service
- Better yet, but may be more expensive: use serverless compute, e.g. AWS Lambda, that will auto-scale

# Gift Card problem
Pick 2 gifts:
- Python’s implementation shows O(n) solution. Since the input file can be big,it’s memory-mapped and walked without loading prices into memory. 

Pick 2/3 gifts:
- Separately, there’s sql/bash implementation that shows two different approaches: O(n log n) and O(n^2) that trades time for space.


# Generate combinations where you replace the Xs in a string with both 0 and 1.
- A compiled Linux binary is included, tested on Red Hat and Ubuntu
- A command to compile is included in the comment in source code 
- The explanation of the algorithm is also inline
- Big O: O(2^m*n), where m is the number of X’s in the string, and n is the length of the string 


