#include <iostream>
using namespace std;

int potprogram_c(int a, int b, int c);

extern "C" int potprogram_asm(int,int,int);  


int main(){
	std::cout << "ASM: " << potprogram_asm(3,5,6) <<std::endl;
	std::cout << "C++: " << potprogram_c(3,5,6) <<std::endl;
	return 0;
}
