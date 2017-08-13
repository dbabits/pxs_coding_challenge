#!/bin/bash

#remove blank lines and spaces at the end of the line
removeblanks() {
   sed '/^[[:space:]]*$/d;s/[[:space:]]*$//'
}

removecomments() {
   sed 's/\#.*$//';
}

trimspace() {
   sed 's/[[:space:]]*|[[:space:]]*/|/g'
}

usage() {
   echo "
   Goal:
        Write a program to find the best two items. It takes two inputs:
        1. A filename with a list of sorted prices
        2. The balance of your gift card
        If no two items have a sum that is less than or equal to the balance on the gift card, print 'Not possible'

   Usage: 
        $0 filename giftcard_balance
   
   Sample run:

        $0 prices.txt 2300

        rowid       rowid       combination                  first_price  second_price  summ
        ----------  ----------  ---------------------------  -----------  ------------  ----------
        2           4           Paperback Book + Headphones   700          1400         2100

   The file is expected to be in this format:
        $ cat prices.txt
        Candy Bar, 500
        Paperback Book, 700
        Detergent, 1000
        Headphones, 1400
        Earmuffs, 2000
        Bluetooth Stereo, 6000

   Test cases:
        $0 `dirname $0`/prices.txt 2500
            Candy Bar 500, Earmuffs 2000

        $0 `dirname $0`/prices.txt 2300
            Paperback Book 700, Headphones 1400

        $0 `dirname $0`/prices.txt 10000
            Earmuffs 2000, Bluetooth Stereo 6000

        $0 `dirname $0`/prices.txt 1100
            Not possible


   This program depends on sqlite csv extension, included in the distribution
   It works by cross-joining the same table to itself, filtering by sum of prices and excluding permutations of the same combination (e.g. (a,b) is same as (b,a)
   The file is not loaded into memory nor converted into sqlite's format,but simply mapped. 
   It does not do it optimally because the file is sorted, and it doesn't take advantage of it.
   However, I though it's elegant and deserves to be shown.
   Converting to sqlite format would likely speed it up because an index can be created which will take advantage of sort.

   Big O: O(n^2) if file is mapped (without indexing).
          O(n log n) if index is used (can be clustered which will take advantage of pre-sorted data) 

   Details: 
            https://sqlite.org/howtocompile.html
            https://sqlite.org/csv.html
            https://sqlite.org/loadext.html

            Actual commands used for compilation are in sqlite-amalgamation-3200000/build
   "
   exit 1
}

<<COMMENT
#virtual csv table in memory:
selectid    order       from        detail
----------  ----------  ----------  -----------------------------------------
0           0           0           SCAN TABLE t AS t1 VIRTUAL TABLE INDEX 0:
0           1           1           SCAN TABLE t AS t2 VIRTUAL TABLE INDEX 0:
0           0           0           USE TEMP B-TREE FOR ORDER BY

#perm sqlite table:
No Index:
selectid    order       from        detail
----------  ----------  ----------  ------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SEARCH TABLE t AS
0           0           0           USE TEMP B-TREE FO

CREATE INDEX IF NOT EXISTS idx1 ON t(c1);
and summ<=$giftcard_balance
selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SEARCH TABLE t AS t2 USING INTEGER PRIMARY KEY (rowid>?)
0           0           0           USE TEMP B-TREE FOR ORDER BY

change the query to: and t2.c1<=$giftcard_balance-t1.c1 - DOESNT RETURN CORRECT ROWS for some reason

selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SEARCH TABLE t AS t2 USING INTEGER PRIMARY KEY (rowid>?)
0           0           0           USE TEMP B-TREE FOR ORDER BY

and t2.c1<=($giftcard_balance-t1.c1); t t2 INDEXED BY idx1 - DOESNT RETURN CORRECT ROWS for some reason
selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SEARCH TABLE t AS t2 USING INDEX idx1 (c1<?)
0           0           0           USE TEMP B-TREE FOR ORDER BY

t1.c0<t2.c0 
selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SCAN TABLE t AS t2
0           0           0           USE TEMP B-TREE FOR ORDER BY

CREATE TABLE IF NOT EXISTS t (c0 TEXT PRIMARY KEY,c1) WITHOUT ROWID; (clustered index)
selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SCAN TABLE t AS t2
0           0           0           USE TEMP B-TREE FOR ORDER BY

--ORDER BY summ DESC:
selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SEARCH TABLE t AS t2 USING INTEGER PRIMARY KEY (rowid>?)
0           0           0           USE TEMP B-TREE FOR ORDER BY

-- ORDER BY t2.rowid DESC,t1.rowid DESC - data comes out in the  order of index anyway.
selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           1           SCAN TABLE t AS t2
0           1           0           SEARCH TABLE t AS t1 USING INTEGER PRIMARY KEY (rowid<?)

-- ORDER BY t1.rowid DESC,t2.rowid DESC
selectid    order       from        detail
----------  ----------  ----------  ----------------------------------------------------------------------
0           0           0           SCAN TABLE t AS t1
0           1           1           SEARCH TABLE t AS t2 USING INTEGER PRIMARY KEY (rowid>?)

Memory Used:                         222256 (max 223568) bytes
Number of Outstanding Allocations:   130 (max 134)
Number of Pcache Overflow Bytes:     4096 (max 4096) bytes
Number of Scratch Overflow Bytes:    0 (max 0) bytes
Largest Allocation:                  120000 bytes
Largest Pcache Allocation:           4096 bytes
Largest Scratch Allocation:          0 bytes
Lookaside Slots Used:                34 (max 100)
Successful lookaside attempts:       194
Lookaside failures due to size:      42
Lookaside failures due to OOM:       14
Pager Heap Usage:                    13712 bytes
Page cache hits:                     3
Page cache misses:                   2
Page cache writes:                   0
Schema Heap Usage:                   1672 bytes
Statement Heap/Lookaside Usage:      31200 bytes
Fullscan Steps:                      5
Sort Operations:                     0
Autoindex Inserts:                   0
Virtual Machine Steps:               295

The data for rowid tables is stored as a B-Tree structure containing one entry for each table row, using the rowid value as the key. 
This means that retrieving or sorting records by rowid is fast. 
Searching for a record with a specific rowid, or for all records with rowids within a specified range is around twice as fast as a similar 
search made by specifying any other PRIMARY KEY or indexed value
COMMENT

tempfile=$(mktemp) || exit 42
trap "rm $tempfile" EXIT

filename=$1
giftcard_balance=$2

[ -n "$filename" ] && echo filename=$filename || usage
[ -n "$giftcard_balance" ] && echo giftcard_balance=$giftcard_balance || usage

db="`dirname $0`/prices.sqlite"
sqlite3="`dirname $0`/sqlite-amalgamation-3200000/sqlite3"
$sqlite3 $db <<EOF

DROP TABLE IF  EXISTS t;
CREATE TABLE IF NOT EXISTS t (c0,c1 INTEGER);
CREATE INDEX IF NOT EXISTS idx1 ON t(c1) ;
--CREATE UNIQUE INDEX IF NOT EXISTS idxrowid ON t(rowid); --this does not work:  no such column: rowid
EOF

cat $filename|removecomments|removeblanks|trimspace|$sqlite3 -separator ',' $db ".import /dev/stdin t"

cat <<EOF | $sqlite3 $db -header -column
.width 10 10 10 70
.stats on
.scanstats on
	--EXPLAIN QUERY PLAN
	SELECT t1.rowid,t2.rowid,
		   '2 gifts' as 'Number of Gifts'
		  ,t1.c0 || " + " || t2.c0 as combination
		  ,t1.c1 as first_price
		  ,t2.c1 as second_price
		  ,t1.c1+t2.c1 as summ 
		  ,$giftcard_balance-t1.c1 as '$giftcard_balance-first_price'
	FROM t t1, t t2 
	WHERE t1.rowid < t2.rowid   --we need combinations, not permutations: (a,b) considered same as  (b,a), hence <
	     --and t2.c1<=($giftcard_balance-t1.c1)
	     and  summ<=$giftcard_balance
	     ORDER BY t1.rowid DESC,t2.rowid DESC	--Fullscan Steps:                      1, Sort Operations:                     0
		 --ORDER BY summ DESC	--Fullscan Steps:                      5, Sort Operations:                     1
	LIMIT 1		-- Fullscan Steps:                      1  (5 without it)
         ;
		 
	SELECT --t1.rowid,t2.rowid,t3.rowid,
		 '3 gifts' as 'Number of Gifts'
		 ,t1.c0 || " + " || t2.c0 || " + " || t3.c0 as combination
		 ,t1.c1 as first_price
		 ,t2.c1 as second_price
		 ,t3.c1 as third_price
		 ,t1.c1+t2.c1+t3.c1 as summ 
	FROM t t1, t t2, t t3
	WHERE t1.rowid < t2.rowid and t2.rowid < t3.rowid  --we need combinations, not permutations: (a,b) considered same as  (b,a), hence <
	   and summ<=$giftcard_balance
	--ORDER BY summ DESC
	ORDER BY t1.rowid DESC,t2.rowid DESC,t3.rowid DESC
	LIMIT 1;
		 
EOF

ls -ltr ${db}*
#exit 0

cat <<EOF | $sqlite3 -header -column #| tee >(grep --count summ)
SELECT load_extension('`dirname $0`/sqlite-amalgamation-3200000/csv') as ''; --csv.so, compiled separately is loaded this way. Also can do: .load path/csv

CREATE VIRTUAL TABLE temp.t USING csv(filename='$filename');
.stats on
.scanstats on
.output $tempfile
--SELECT  ' ' as '2 gifts:';
--EXPLAIN QUERY PLAN
SELECT --t1.rowid,t2.rowid,
	   '2 gifts' as 'Number of Gifts'
	  ,t1.c0 || " + " || t2.c0 as combination
	  ,t1.c1 as first_price
	  ,t2.c1 as second_price
	  ,t1.c1+t2.c1 as summ 
FROM t t1, t t2 
WHERE t1.rowid < t2.rowid   --we need combinations, not permutations: (a,b) considered same as  (b,a), hence <
   and summ<=$giftcard_balance
--ORDER BY summ DESC
ORDER BY t1.rowid DESC,t2.rowid DESC
LIMIT 1;

--SELECT  ' ' as '3 gifts:';

SELECT --t1.rowid,t2.rowid,t3.rowid,
	 '3 gifts' as 'Number of Gifts'
	 ,t1.c0 || " + " || t2.c0 || " + " || t3.c0 as combination
	 ,t1.c1 as first_price
	 ,t2.c1 as second_price
	 ,t3.c1 as third_price
	 ,t1.c1+t2.c1+t3.c1 as summ 
FROM t t1, t t2, t t3
WHERE t1.rowid < t2.rowid and t2.rowid < t3.rowid  --we need combinations, not permutations: (a,b) considered same as  (b,a), hence <
   and summ<=$giftcard_balance
--ORDER BY summ DESC
ORDER BY t1.rowid DESC,t2.rowid DESC,t3.rowid DESC
LIMIT 1;

EOF

cat $tempfile
exit 0

grep -B 2 '2 gifts' $tempfile || echo "2 gifts Not possible"
grep -B 2 '3 gifts' $tempfile || echo "3 gifts Not possible"

#grep --quiet summ $tempfile #if there are no rows returned, there won't be no header line with summ
#[ $? -eq 0 ] && cat $tempfile || echo "Not possible"


