#!/usr/bin/env python
import logging
import argparse

def name(g):
    return g[0]
def price (g):
    return g[1]

gifts=( 
         ("bar",125,125)
        ,("moo",125,125)
        ,("foo",250,250)
        ,("candy bar", 500,500)
        ,("paperback book", 700,700)
        ,("detergent",1000,1000)
        ,("headphones",1400,1400)
        ,("earmuffs",2000,2000)
        ,("bluetooth stereo",6000,6000)
    )

'''
for each item, iterate over all other items, starting from the next (e.g.: do not iterate both a,b and b,a - only one combo. Data assumed to be sorted
'''
def find_pair(total):

    best_diff=None
    iters=0
    logging.debug("--------find_pair(%d)",total)
    #for i, item in enumerate(gifts):
    for i in range (0,len(gifts)):
        logging.debug("%d - %s",i,gifts[i])
        if (price(gifts[i]) >=total): #then no second item is possible and we can break here. It's just an optimization.
            logging.debug("optimization1: breaking off because %d>=total(%d)", price(gifts[i]),total )
            break

        for j in range (i+1,len(gifts)):
            s=gifts[i][1] + gifts [j][1]
            diff=total-s
            if diff>=0 and (diff < best_diff or best_diff is None):
                best_diff=diff
                item1=i
                item2=j
                if diff==0:
                    logging.debug( "optimization2:breaking off because diff=0:perfect match, no need to look further")
                    break
            elif diff<0:
                    #print "optimization3:breaking off because diff(",diff,")<0(sum>total):since data is sorted,no need to look further"
                    #break
                    pass
            elif diff>=best_diff:
                    #print "optimization4:breaking off because diff(",diff,")>=best_diff(",best_diff,"):since data is sorted,no need to look further"
                    #break
                    pass
            logging.debug(" and %d-- %s total=%d --sum=%d --diff=%d --best diff=%d",j,gifts[j],total,s,total-s,best_diff)
            iters+=1

    if best_diff is None:
        print "find_pair(",total,")-Best combination Not possible"," nItems=",len(gifts)," Iterations=",iters
        return []
    else:
        print "find_pair(",total,")-Best combination=",gifts[item1],",", gifts[item2], "sum=",gifts[item1][1]+gifts[item2][1]," best_diff=",best_diff," nItems=",len(gifts)," Iterations=",iters
        return [gifts[item1],gifts[item2]]


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="make it verbose",action="store_true")

args = parser.parse_args()
loglevel=logging.INFO
if args.verbose:
    loglevel=logging.DEBUG

#logging.basicConfig(format='%(levelname)s:%(message)s',level=loglevel)
logging.basicConfig(format='%(message)s',level=loglevel)

assert(find_pair (400)  ==[('bar', 125, 125) , ('foo', 250, 250)])
assert(find_pair (2500) ==[("candy bar", 500,500),("earmuffs",2000,2000)])
assert(find_pair (2300) ==[('foo', 250, 250) , ('earmuffs', 2000, 2000)])
assert(find_pair (10000)==[("earmuffs",2000,2000),("bluetooth stereo",6000,6000)])
assert(find_pair (1100) ==[("foo",250,250),("paperback book", 700,700)])
assert(find_pair (125)  ==[])
print "All tests passed, exiting"
exit(0)

'''
1) Original:
dima@LAPTOP-MA6OEPO9:~/development/paxos_coding_challenge/gift_card$ ./try1.py|grep "Best combination"
find_pair( 400 )-Best combination= ('bar', 125, 125) , ('foo', 250, 250) sum= 375  best_diff= 25  nItems= 9  Iterations= 36
find_pair( 2500 )-Best combination= ('candy bar', 500, 500) , ('earmuffs', 2000, 2000) sum= 2500  best_diff= 0  nItems= 9  Iterations= 36
find_pair( 2300 )-Best combination= ('foo', 250, 250) , ('earmuffs', 2000, 2000) sum= 2250  best_diff= 50  nItems= 9  Iterations= 36
find_pair( 10000 )-Best combination= ('earmuffs', 2000, 2000) , ('bluetooth stereo', 6000, 6000) sum= 8000  best_diff= 2000  nItems= 9  Iterations= 36
find_pair( 1100 )-Best combination= ('foo', 250, 250) , ('paperback book', 700, 700) sum= 950  best_diff= 150  nItems= 9  Iterations= 36
find_pair( 125 )-Best combination Not possible  nItems= 9  Iterations= 36

2) optimization with price(gifts[i]),">=total(",total,")" -> break
$ ./try1.py|grep "Best combination"
find_pair( 400 )-Best combination= ('bar', 125, 125) , ('foo', 250, 250) sum= 375  best_diff= 25  nItems= 9  Iterations= 21
find_pair( 2500 )-Best combination= ('candy bar', 500, 500) , ('earmuffs', 2000, 2000) sum= 2500  best_diff= 0  nItems= 9  Iterations= 36
find_pair( 2300 )-Best combination= ('foo', 250, 250) , ('earmuffs', 2000, 2000) sum= 2250  best_diff= 50  nItems= 9  Iterations= 36
find_pair( 10000 )-Best combination= ('earmuffs', 2000, 2000) , ('bluetooth stereo', 6000, 6000) sum= 8000  best_diff= 2000  nItems= 9  Iterations= 36
find_pair( 1100 )-Best combination= ('foo', 250, 250) , ('paperback book', 700, 700) sum= 950  best_diff= 150  nItems= 9  Iterations= 33
find_pair( 125 )-Best combination Not possible  nItems= 9  Iterations= 0
'''

