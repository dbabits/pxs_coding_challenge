#include <stdio.h>
#include <string.h>
/*
gcc -g -std=c99 binary_combinations.c -o binary_combinations && ./binary_combinations 0X1XX
0X1XX

1: 00100
2: 00101
3: 00110
4: 00111
5: 01100
6: 01101
7: 01110
8: 01111


DEBUG:orig string=0X1XX;strlen(string)=5,nXs=3, total_iterations=8
*/

/*
total_iterations and count_chars() is just for debugging
It works by incrementing either the pointer or the index, depending on whether the current char is what we count,until the NULL-terminator. 
pointer dereferencing is simply to avoid warning: cast from pointer to integer of different size [-Wpointer-to-int-cast]
*/
int total_iterations=0;
int count_chars(const char* s, char c) {
    int i=0;
    for (i=0; s[i]!='\0'; s[i]==c ? i++ : *(s++));
    return i;
}
/*
Task:
  You are given a string composed of only 1s, 0s, and Xs.
  Write a program that will print out every possible combination where you replace the X with both 0 and 1.

The algorithm works by alternating Xs and Ys, effectively doing binary add with carry. X is printed as 0 and Y as 1
It walks the string right-to-left,turning ALL Ys to Xs and (FIRST X to Y and print)
Example: (need -std=c99 for gcc ver 4.8.3 20140911(not reqd for 5.4.0)(var declaration inside for loop)
        gcc -g -std=c99 binary_combinations.c -o binary_combinations && ./binary_combinations 0X1XX
	
First, the string is printed with 0s in place of all Xs:                                      XX -> prints 00
Iteration 1: right X becomes Y, and the string is printed:                                    XY -> prints 01
Iteration 2: all Ys from right become Xs, and the next X becomes Y and the string is printed: YX -> prints 10 
Iteration 3: right X  becomes Y, and the string is printed:                                   YY -> prints 11
Iteration 4: all Ys from right become Xs, we are now at the left end of the string:           XX -> (no more prints)
Nothing is printed anymore and the original string has been restored with Xs  
Number of iterations = 2^number of Xs 

Big O: O(2^m*n), where m is the number of X’s in the string, and n is the length of the string 
*/
void print(const char* s, int n) {
   static int counter=0;
   printf("%d: ",++counter);
   for (int i = 0; i != n; i++) {
      printf("%c",  (s[i] == 'X' || s[i] == '0') ? '0' : '1' );
   }
   printf("\n");
}

int increment(char* s, int n) {
   int i;
   for (i = n-1; i != -1; i--) {
      if (s[i] == 'X') {
         s[i] = 'Y';
         break;
      } else if (s[i] == 'Y') {
         s[i] = 'X';
      }
   }
   total_iterations++;
   return (i != -1); //are we at the left end of the string?
}

int main(int argc, char* argv[]) {
   char d[] = "10X10X0";
   char* s = (argc>1) ? argv[1] : d;
   int n = strlen(s);
   printf("%s\n\n",s);
   print(s,n); //print all 0s in place of Xs first
   
   while (increment(s,n)) {
      print(s,n);
   }
   
   printf("\n\nDEBUG:orig string=%s;strlen(string)=%d,nXs=%d, total_iterations=%d\n\n",s,n,count_chars(s,'X'),total_iterations);
}


