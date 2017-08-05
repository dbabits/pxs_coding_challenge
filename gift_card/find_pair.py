#!/usr/bin/python
"""
put all items into an array, sorted by price.
foreach item <=sum, do: 
   complement=sum - price
   find nearest c1<=complement
   s=price+c1
   diff=sum-s
   if diff < saved diff=>it's a better combo, save item, c1 combo

e.g.:  Sum=2500
foo,       300                    2500-300=2200, nearest down=2000. 2000+300=2300. diff=2500-2300=200
Candy Bar, 500                    2500-500=2000, nearest down=2000. 2000+500=2500. diff=2500-2500=0 ->better
Paperback Book, 700
Detergent, 1000
Headphones, 1400
Earmuffs, 2000
Bluetooth Stereo, 6000

"""
import sys

filename=sys.argv[1]
summ=sys.argv[2]
print filename, " ",summ
with open(filename, 'r') as f:
  for line in f:
    desc,price=line.split(',')
    complement=summ-price
    print desc,"|",price,"|", complement
    complements = [summ -x for x in range(10)]

exit (0)
for line in sys.stdin:

    numbersl,X= line.split(';') #first split line into numbers and the sum
    X=int(X)

    numbers= map(int,numbersl.split(',')) #split line of numbers into map of ints

    

    #for each number in the map, see if there's second (and bigger one) that would add up to our X. 
    #If so, concat to  the string
    chunks=[]
    for n in numbers:
        if X-n in numbers and n<X-n:
           chunks.append("%s,%s;" % (n,X-n))

    if not chunks:
       print 'NULL'
    else:
        print ''.join(chunks).rstrip(';'),

