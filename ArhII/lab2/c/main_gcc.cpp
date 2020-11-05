#include <iostream>
using namespace std;

extern "C" int p_asm(int);  

int potprogram_c(int n){
        int zbr=0;
        for(int i=0; i<n; i++)          
            zbr+= i;
        
        return zbr;
}

int main(){
        for(int i=0; i<15; i++){
                std::cout << i << std::endl;  
                std::cout << "ASM: " << p_asm(i) <<std::endl;
        
                std::cout << "C++: " << potprogram_c(i) <<std::endl;
        }
        return 0;
}

