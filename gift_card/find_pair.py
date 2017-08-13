#!/usr/bin/env python
import logging
import argparse
import sys
import mmap
import os
import subprocess

def make_regression_test_file():
    file=os.path.dirname(os.path.realpath(__file__))+"/regression_test.txt"
    script='''
cat <<EOF > {file}
Candy Bar, 500
Paperback Book, 700
Detergent, 1000
Headphones, 1400
Earmuffs, 2000
Bluetooth Stereo, 6000
EOF
ls -l {file}*
'''.format(file=file)
    subprocess.check_call(script, shell=True)
    return file

def  walk_l(mm,fromm):
    mm.seek(fromm, os.SEEK_SET)           #set the file pointer at the beginning of the line
    line=mm.readline().strip()            #read the line (this moves the pointer forward)
    to=mm.tell()                          #next time, start from the current position
    desc, price = line.strip().split(',') #parse the line
    price=int(price)                      #convert to int
    logging.debug("walk_l():from=%d,to=%d,line=[%s],desc=[%s],price=[%d]" % (fromm, to, line,desc,price))
    return to,desc,price                  #Since we're moving L->R here, the next From will be the current To

def  walk_r(mm,to):
    fromm = mm.rfind("\n",0,to-1)         #To points to EOL. Backtrack from given position to find the beginning of this line
    mm.seek(fromm+1, os.SEEK_SET)         #set the file pointer
    line = mm.readline().strip()          #read the line (this moves the pointer forward)
    desc, price = line.strip().split(',') #parse the line
    price = int(price)                    #convert to int
    logging.debug("walk_r():from=%d,to=%d,tell=%d,line=[%s],desc=[%s],price=[%d]" % (fromm,to, mm.tell(),line,desc,price))
    return fromm,desc,price               #Since we're moving R->L here, the next To will be the current From

'''Walk the file from two ends at a time: O(n)'''
def walk_file(filename,target):
    with open(filename, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)     # memory-map the file, size 0 means whole file
        logging.debug("filename={filename},size={size} bytes".format(filename=filename,size=mm.size()))

        best_diff=diff=sys.maxint
        best_combo=()
        start = 0
        end=mm.size()
        while (start < end): #We break when left and right overlap
            logging.debug("if {start}<{end}:".format(start=start,end=end))
            nextstart,desc1,price1=walk_l(mm, start)
            nextend,  desc2,price2=walk_r(mm, end)
            sum=price1+price2
            diff=target-sum

            if diff >= 0 and diff < best_diff and desc1!=desc2: #The condition is not to pick same item twice
                best_diff=diff
                best_combo=((desc1,price1),(desc2,price2))

            if  (sum > target):
                end=nextend     #=end--
            elif(sum < target):
                start=nextstart #=start++
            else:
                logging.debug( "optimization2:breaking off because sum=target:perfect match, no need to look further")
                break

        logging.debug("best_combo={}".format(best_combo))
        return best_combo

def main():
    parser = argparse.ArgumentParser(description='Find the best combination of 2 items to spend max gift card balance')
    parser.add_argument("-v", "--verbose", help="make it verbose",action="store_true")
    parser.add_argument("-f", "--filename",  help="filename to parse",required=True)
    parser.add_argument("-t", "--target", dest='target',type=int, help="card balance",required=True)
    parser.add_argument("-x", "--runtests", help="run built-in tests",action="store_true")

    args = parser.parse_args()

    loglevel=logging.DEBUG if args.verbose else logging.INFO

    logging.basicConfig(format='%(levelname)s:%(message)s',level=loglevel)

    if args.runtests:
      file=make_regression_test_file()
      assert(walk_file (filename=file,target=2500) ==(('Candy Bar', 500), ('Earmuffs', 2000)) )
      assert(walk_file (filename=file,target=2300) ==(('Paperback Book', 700), ('Headphones', 1400)) )
      assert(walk_file (filename=file,target=10000)==(('Earmuffs', 2000), ('Bluetooth Stereo', 6000)) )
      assert(walk_file (filename=file,target=1100) ==() )
      print "All tests passed, exiting"
    else:
      best_combo = walk_file(filename=args.filename, target=args.target)
      if len(best_combo) == 0:
          print "Not possible"
      else:
          print("best_combo={}".format(best_combo))

    exit (0)

if __name__ == "__main__":
    main() # execute only if run as a script


