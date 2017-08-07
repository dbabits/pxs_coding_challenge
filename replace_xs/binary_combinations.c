#include <stdio.h>
#include <string.h>

int total_iterations=0;
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
   print(s,n); 
   

}
/*

*/

