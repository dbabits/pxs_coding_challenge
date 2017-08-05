#include <stdio.h>
#include <string.h>

void print(const char* s, int n) {

   for (int i = 0; i != n; i++) {
      printf("%c",  (s[i] == 'X' || s[i] == '0') ? '0' : '1' );
   }
   printf("\n");
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

