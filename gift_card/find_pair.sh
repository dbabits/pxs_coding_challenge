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

validate_int() {
     [[ $1 =~ ^-?[0-9]+$ ]] && return 0 || return 1;
}

usage() {
   local message=$1
   cat <<EOF 
   $message
   
   This program tries to spend the most of a giftcard's balance on 2 and on 3 gifts out of a list.
   Usage: 
        $0 -f filename -t giftcard_balance [-d (show debug info,will overwhelm with useful stats)]
 
        The file with a list of items SORTED by price is expected to be in this format:
            Candy Bar, 500
            Paperback Book, 700
         
   Test cases:
        $0 -f `dirname $0`/prices.txt -t 2500
            nGifts   combination                                         first_price  second_price  third_price  summ
            -------  --------------------------------------------------  -----------  ------------  -----------  ----------
            2 gifts  Candy Bar + Earmuffs                                500          2000          NA           2500
            3 gifts  Candy Bar + Paperback Book + Detergent              500          700           1000         2200

        $0 -f `dirname $0`/prices.txt -t 2300
            2 gifts  Paperback Book + Headphones                         700          1400          NA           2100
            3 gifts  Candy Bar + Paperback Book + Detergent              500          700           1000         2200

        $0 -f `dirname $0`/prices.txt -t 10000
            2 gifts  Earmuffs + Bluetooth Stereo                         2000         6000          NA           8000
            3 gifts  Headphones + Earmuffs + Bluetooth Stereo            1400         2000          6000         9400

        $0 -f `dirname $0`/prices.txt -t 2100
            2 gifts  Paperback Book + Headphones                         700          1400          NA           2100
            3 gifts  Not possible
        
        $0 -f `dirname $0`/prices.txt -t 1100
            2 gifts  Not possible
            3 gifts  Not possible

   This program uses sqlite, and there are 2 different ways to use it:
   1) Convert text file into sqlite format, and build index on price.     
      This gives O(n log n) compute complexity, but will take O(2n) space + time for initial load.
   2) Process text file using csv extension,which I compiled, included in the distribution. Binaries and commands used for compilation are included.
      This will be O(n^2) compute, but will not take extra space.

    Details: 
            https://sqlite.org/howtocompile.html
            https://sqlite.org/csv.html
            https://sqlite.org/loadext.html
    
    $message

EOF
   exit 1
}

debug=
while getopts "hdf:t:" opt; do
    case "$opt" in
        f) filename="$OPTARG";;
        t) giftcard_balance="$OPTARG"
           validate_int $giftcard_balance  ||  usage "ERROR: -t arg must be an integer" 
        ;;
        d) debug=1;;
        h|*) usage;;
    esac
done

[ -n "$filename" ]         && echo "filename=$filename" || usage
[ -n "$giftcard_balance" ] && echo "giftcard_balance=$giftcard_balance" || usage
echo

[ -z "$debug" ] && tempfile=$(mktemp) && trap "rm -v $tempfile" EXIT 
[ -n "$debug" ] && tempfile=stdout && stats_on_off="on" || stats_on_off="off"

db="`dirname $0`/prices.sqlite"
sqlite3="`dirname $0`/sqlite-amalgamation-3200000/sqlite3"

read -r -d '' sqls << EOF
--.width 3 3 3 7 50
.width 7 50
.echo      $stats_on_off
.stats     $stats_on_off
.scanstats $stats_on_off
.eqp       $stats_on_off
.output $tempfile

    SELECT 
          '2 gifts'                as 'nGifts'
          ,t1.c0 || " + " || t2.c0 as combination
          ,t1.c1                   as first_price
          ,t2.c1                   as second_price
          ,'NA'                    as third_price
          ,t1.c1+t2.c1             as summ 
    FROM t t1, t t2 
    WHERE t1.rowid < t2.rowid               --we need combinations, not permutations: (a,b) considered same as  (b,a), hence <
         AND  summ<=$giftcard_balance
    ORDER BY summ DESC                      --Fullscan Steps:5, Sort Operations:1
    LIMIT 1;                                --Fullscan Steps:1  (5 without it)

.header off    

    SELECT 
         '3 gifts'                                  as 'nGifts'
         ,t1.c0 || " + " || t2.c0 || " + " || t3.c0 as combination
         ,t1.c1                                     as first_price
         ,t2.c1                                     as second_price
         ,t3.c1                                     as third_price
         ,t1.c1+t2.c1+t3.c1                         as summ 
    FROM t t1, t t2, t t3
    WHERE t1.rowid < t2.rowid AND t2.rowid < t3.rowid   --we need combinations, not permutations: (a,b) considered same as  (b,a), hence <
         AND summ<=$giftcard_balance
    ORDER BY summ DESC                                  -- This makes it do: USE TEMP B-TREE FOR ORDER BY
    LIMIT 1;
EOF


echo "---Approach 1: Load text file into sqlite format to achieve O(n log n) - see help(-h) for details---"; echo
$sqlite3 $db <<EOF
	DROP TABLE IF  EXISTS t;
	CREATE TABLE IF NOT EXISTS t (c0,c1 INTEGER);
	CREATE INDEX IF NOT EXISTS idx1 ON t(c1) ;
EOF

cat $filename|removecomments|removeblanks|trimspace|$sqlite3 -separator ',' $db ".import /dev/stdin t"

cat <<EOF | $sqlite3 $db -header -column
$sqls   
EOF

if [ -z "$debug" ]; then
    grep -B 2 '2 gifts' $tempfile || echo "2 gifts  Not possible"
    grep      '3 gifts' $tempfile || echo "3 gifts  Not possible"
fi

echo
echo "---Approach 2: Use virtual table functionality (direct navigation of csv without copying  into sqlite format): O(n^2) - see help(-h) for details---";echo

cat <<EOF | $sqlite3 -header -column
--SELECT load_extension('`dirname $0`/sqlite-amalgamation-3200000/csv') as ''; --csv.so, compiled separately is loaded this way. Also can do: .load path/csv
.load `dirname $0`/sqlite-amalgamation-3200000/csv
CREATE VIRTUAL TABLE temp.t USING csv(filename='$filename');
$sqls
EOF

if [ -z "$debug" ]; then
    grep -B 2 '2 gifts' $tempfile || echo "2 gifts  Not possible"
    grep      '3 gifts' $tempfile || echo "3 gifts  Not possible"
fi

echo
ls -ltr  ${db}*


<<COMMENT
         --and t2.c1<=($giftcard_balance-t1.c1)  -- this does not work.
         --CREATE UNIQUE INDEX IF NOT EXISTS idxrowid ON t(rowid); --this does not work:  no such column: rowid
         --t1.rowid,t2.rowid,t3.rowid,
          --ORDER BY t1.rowid DESC,t2.rowid DESC    -- This gives incorrect answer! Fullscan Steps:1, Sort Operations:0
            2 gifts          Detergent + Headphones  1000         1400          2400
            2 gifts          Paperback Book + Headp  700          1400          2100
            2 gifts          Paperback Book + Deter  700          1000          1700
            2 gifts          Candy Bar + Earmuffs    500          2000          2500
        --ORDER BY t1.rowid DESC,t2.rowid DESC,t3.rowid DESC
    
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

