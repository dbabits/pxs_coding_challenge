Make sure to checkout the entire repository because it includes dependencies and some scripts assume this directory structure.

# Webservice that hashes a string.
- Deployed at: (communicated separately)
- Instructions shown when the default url is hit

Scalability and other improvements: 
- The service keeps the database of hashes and strings in-memory, they are not persisted. A database would be best in real-life usage
 - Use a (NoSql) key-value database to store hashes and messages, e.g. Redis, AWS Dynamo, AWS SimpleDB
- Put the service into a container and scale using OpenShift, or AWS Container Service
- Better yet, but may be more expensive: use serverless compute, e.g. AWS Lambda, that will auto-scale

# Gift Card problem
Pick 2 gifts:
- Python’s implementation shows O(n) solution. Since the input file can be big,it’s memory-mapped and walked without loading into memory. 
```sh
$ ./find_pair.py -f ./prices.txt  -t 2300 # -h for more details
best_combo=(('Paperback Book', 700), ('Headphones', 1400))
```
Pick 2/3 gifts:
- *Unofficial*, experimental sql/bash implementation that tries two different approaches: I believe one achieves O(n log n) and the other is O(n^2) that trades time for space.**Note** that Python implementation is better and is the one that should be considered.
```sh
$ ./find_pair.sh -f ./prices.txt -t 2500 # -h for more details

---Approach 1: Load text file into sqlite format to utilize index for O(n log n) - see help(-h) for details and scanstats(-d)---

nGifts   combination                                         first_price  second_price  third_price  summ
-------  --------------------------------------------------  -----------  ------------  -----------  ----------
2 gifts  Candy Bar + Earmuffs                                500          2000          NA           2500
3 gifts  Candy Bar + Paperback Book + Detergent              500          700           1000         2200

---Approach 2: Use virtual table functionality (direct navigation of csv without copying  into sqlite format): O(n^2) - see help(-h) for details and scanstats(-d)---

nGifts   combination                                         first_price  second_price  third_price  summ
-------  --------------------------------------------------  -----------  ------------  -----------  ----------
2 gifts  Candy Bar + Earmuffs                                 500          2000         NA           2500
3 gifts  Candy Bar + Paperback Book + Detergent               500          700           1000        2200

```

# Generate combinations where you replace the Xs in a string with both 0 and 1.
- A compiled Linux binary is included, tested on Red Hat and Ubuntu
- A command to compile is included in the comment in source code 
- The explanation of the algorithm is also inline
- Big O: O(2^m*n), where m is the number of X’s in the string, and n is the length of the string 
```sh
$ ./binary_combinations 10X10X0

10X10X0

1: 1001000
2: 1001010
3: 1011000
4: 1011010

```


