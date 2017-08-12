#!/usr/bin/env python
import logging
import argparse
import sys
import mmap
import os

def name(g):
    return g[0]
def price (g):
    return g[1]

gifts=( 
         ("bar",125)
        ,("moo",125)
        ,("foo",250)
        ,("candy bar", 500)
        ,("paperback book", 700)
        ,("detergent",1000)
        ,("headphones",1400)
        ,("earmuffs",2000)
        ,("bluetooth stereo",6000)
    )


'''binary search the file, seeking the price equal or closest to the complement.start from the current position forward (file is sorted by price).
O(n*log(n))
'''
def bsearch(mm,seeking_price):
    save_position=mm.tell()
    print("bsearch: {line}, mm.tell={tell}".format(line=mm.readline().strip(),tell=mm.tell()))

def open_file(filename,total):
    with open(filename, "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        print "filename={filename},size={size} bytes".format(filename=filename,size=mm.size())
        for line in iter(mm.readline,''):
            desc, price1 = line.strip().split(',')
            seeking_price = int(total) - int(price1)
            print("%s|%s|%d-%s=%d, mm.tell()=%d" % (desc, price1, total,price1,complement_seeking,mm.tell()))
            price2=bsearch(mm,seeking_price)
            s=price1+price2
            diff=total-s
            if diff >= 0 and (diff < best_diff or best_diff is None):
                best_diff = diff

def get_num_end(mm,commapos,newlpos):
    commapos = mm.rfind(",", 0, commapos)
    newlpos = mm.rfind("\n", 0, newlpos)
    savedpos=mm.tell()
    mm.seek(commapos,os.SEEK_SET)
    between=mm.readline()
    mm.seek(savedpos)
    print ("get_num_end commapos=%d, newlpos=%d,between=%s" % (commapos,newlpos,between))
    return commapos,newlpos

def  get_l(mm,fromm):
    mm.seek(fromm, os.SEEK_SET)
    line=mm.readline().strip()
    desc, price = line.strip().split(',')
    price=int(price)
    print("get_l():fromm=%d,tell=%d,line=[%s],desc=[%s],price=[%d]" % (fromm, mm.tell(), line,desc,price))  # 0,15
    return mm.tell(),desc,price

def  get_r(mm,fromm):
    #rpos = mm.rfind("\n",0,pointer)
    #logging.debug("\nget_r():rpos=%d,pointer=%d,tell=%d" % (rpos, pointer, mm.tell())) #105,106
    to = mm.rfind("\n",0,fromm-1)
    #logging.debug("get_r():fromm=%d,to=%d,tell=%d" % (fromm,to, mm.tell()))  # 82,106
    mm.seek(to+1, os.SEEK_SET)
    line = mm.readline().strip()
    desc, price = line.strip().split(',')
    price = int(price)
    print("get_r():fromm=%d,to=%d,tell=%d,line=[%s],desc=[%s],price=[%d]" % (fromm,to, mm.tell(),line,desc,price))  # 82,106
    return to,desc,price

def open_file2(filename,target):
    with open(filename, "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        print "filename={filename},size={size} bytes".format(filename=filename,size=mm.size())

        #int minDiff = INT_MAX;
        #int end = nums.size() - 1;
        #sort(nums.begin(), nums.end() );
        start = 0
        end=mm.size()

        '''
        start = get_l(mm, start)
        start = get_l(mm, start)
        start = get_l(mm, start)
        start = get_l(mm, start)

        end=get_r(mm,end)
        end=get_r(mm,end)
        end = get_r(mm, end)
        end = get_r(mm, end)
        return
        '''
        best_diff=sys.maxint
        diff=sys.maxint
        best_combo=()
        while (start < end):
            logging.debug("if {start}<{end}:".format(start=start,end=end))
            nextstart,desc1,price1=get_l(mm, start)
            nextend,desc2,price2=get_r(mm, end)
            sum=price1+price2
            #diff = min(diff, abs(sum - target))
            diff=target-sum

            if diff >= 0 and diff < best_diff:
                best_diff=diff
                best_combo=((desc1,price1),(desc2,price2))

            if (sum > target):
                end=nextend     #=end--
            else:
                start=nextstart #=start++

        #logging.debug("price1=%d,price2=%d,sum=%d,target=%d,best_diff=%d".format(best_combo))
        logging.debug("best_combo={}".format(best_combo))
        return best_combo

        commapos=mm.rfind(",")
        rpos = mm.rfind("\n")
        print("rpos=%d,tell=%d" % (rpos,  mm.tell()))

        while commapos !=-1:
            mm.seek(commapos+1, os.SEEK_SET)
            price2 = int(mm.readline().strip())
            print("commapos=%d, price2=[%d], tell=%d" % (commapos, price2,mm.tell()))
            commapos = mm.rfind(",", 0, commapos)

            #commapos, newlpos=get_num_end(mm,commapos,newlpos)
            #print("commapos=%d, newlpos=%d" % (commapos,newlpos))
            #commapos=mm.rfind(",", 0,commapos)
            #newlpos = mm.rfind("\n", 0, newlpos)

        #print ("mm.rfind(,)=%d" % (mm.rfind("\n",mm.size()-10)))
        #mm.seek(end, os.SEEK_SET)
        print("mm.tell()=%d" % (mm.tell()))

        '''
        while (start < end) {
            int sum = nums[end] + nums[start];
            minDiff = min(minDiff, abs(sum - target) );
            if (sum > target) {
                end--;
            } else {
                start++;
            }
        }
        return minDiff;
        '''
''' 
    for each item, iterate over all other items, sum up 2 prices, and find the smallest diff from total.
    TODO - since the list (or file) is sorted by price, we can do binary search for the second item, by price 
'''
def find_pair(total):

    best_diff=None
    iters=0
    logging.debug("--------find_pair(%d)",total)
    #for i, item in enumerate(gifts):
    for i in range (0,len(gifts)):
        logging.debug("%d - %s",i,gifts[i])
        if (price(gifts[i]) >=total): #then no second item is possible and we can break here.
            logging.debug("optimization1: breaking off because %d>=total(%d)", price(gifts[i]),total )
            break

        complement2find=total-price(gifts[i])
        #bsearch
        for j in range (i+1,len(gifts)):
            s=price(gifts[i]) + price(gifts [j])
            diff=total-s
            if diff>=0 and (diff < best_diff or best_diff is None):
                best_diff=diff
                item1=i
                item2=j
                if diff==0:
                    logging.debug( "optimization2:breaking off because diff=0:perfect match, no need to look further")
                    break
            elif diff<0:
                    logging.debug("optimization3:(%s(%d) + %s(%d)=%d > %d). breaking off. since data is sorted,no need to look further",name(gifts[i]),price(gifts[i]),name(gifts[j]),price(gifts[j]),s,total)
                    break
            #elif diff>best_diff:
            #        logging.debug("optimization4:(%s(%d) + %s(%d)=%d  diff=%d,best_diff=%d,total=%d). breaking off. ",name(gifts[i]),price(gifts[i]),name(gifts[j]),price(gifts[j]),s,diff,best_diff,total)
            #        break
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
#parser.add_argument("-f", "--filename", type=file, help="filename to parse")
parser.add_argument("-t", "--total", dest='total',type=int, help="card balance")
parser.add_argument("-f", "--filename",  help="filename to parse")

args = parser.parse_args()
loglevel=logging.INFO
if args.verbose:
    loglevel=logging.DEBUG

#logging.basicConfig(format='%(levelname)s:%(message)s',level=loglevel)
logging.basicConfig(format='%(message)s',level=loglevel)

open_file2(filename=args.filename,target=args.total)
exit (0)
assert(find_pair (400)  ==[('bar', 125),      ('foo', 250)])
assert(find_pair (2500) ==[("candy bar", 500),("earmuffs",2000)])
assert(find_pair (2300) ==[('foo', 250),      ('earmuffs', 2000)])
assert(find_pair (10000)==[("earmuffs",2000), ("bluetooth stereo",6000)])
assert(find_pair (1100) ==[("foo",250),       ("paperback book", 700)])
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

2) + optimization1
$ ./try1.py|grep "Best combination"
find_pair( 400 )-Best combination= ('bar', 125, 125) , ('foo', 250, 250) sum= 375  best_diff= 25  nItems= 9  Iterations= 21
find_pair( 2500 )-Best combination= ('candy bar', 500, 500) , ('earmuffs', 2000, 2000) sum= 2500  best_diff= 0  nItems= 9  Iterations= 36
find_pair( 2300 )-Best combination= ('foo', 250, 250) , ('earmuffs', 2000, 2000) sum= 2250  best_diff= 50  nItems= 9  Iterations= 36
find_pair( 10000 )-Best combination= ('earmuffs', 2000, 2000) , ('bluetooth stereo', 6000, 6000) sum= 8000  best_diff= 2000  nItems= 9  Iterations= 36
find_pair( 1100 )-Best combination= ('foo', 250, 250) , ('paperback book', 700, 700) sum= 950  best_diff= 150  nItems= 9  Iterations= 33
find_pair( 125 )-Best combination Not possible  nItems= 9  Iterations= 0

3) + optimization3:
find_pair( 400 )-Best combination= ('bar', 125) , ('foo', 250) sum= 375  best_diff= 25  nItems= 9  Iterations= 3
find_pair( 2500 )-Best combination= ('candy bar', 500) , ('earmuffs', 2000) sum= 2500  best_diff= 0  nItems= 9  Iterations= 24
find_pair( 2300 )-Best combination= ('foo', 250) , ('earmuffs', 2000) sum= 2250  best_diff= 50  nItems= 9  Iterations= 23
find_pair( 10000 )-Best combination= ('earmuffs', 2000) , ('bluetooth stereo', 6000) sum= 8000  best_diff= 2000  nItems= 9  Iterations= 36
find_pair( 1100 )-Best combination= ('foo', 250) , ('paperback book', 700) sum= 950  best_diff= 150  nItems= 9  Iterations= 9
find_pair( 125 )-Best combination Not possible  nItems= 9  Iterations= 0
All tests passed, exiting

'''

