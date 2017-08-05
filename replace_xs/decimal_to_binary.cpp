#include <stdio.h>
#include <stdlib.h>     /* atoi */
#include <vector>
#include <cmath>

//compile with g++ decimal_to_binary.cpp
int main (int argc, char* argv[] ){

   int input=(argc>1) ? atoi(argv[1]) : std::pow(2,3);

   std::vector<int> bits;
   if (input==0) {
	  bits.push_back(0);
   }
   else {
      for (int i=input;i>0;i/=2){
		bits.push_back(i % 2);
	  }
   }
   
   printf("input=%d, in binary=", input);
   for (std::vector<int>::reverse_iterator rit = bits.rbegin();rit!=bits.rend(); ++rit){
      printf("%d",*rit);
   }
   printf("\n");

   return 0;
}
