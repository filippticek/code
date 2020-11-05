#include <iostream>
using namespace std;

void sum_c(float const* A, float const* B, int count, float *R){
        for(int i=0; i<count; i++)
            *(R+i) = *(A+i) + *(B+i);
}

extern "C" int pot_x87(float* ,float* ,int, float*);  


int main(){
        __attribute__ ((aligned(32))) float a[3] = {0.5, 1.5, 2.5};
        __attribute__ ((aligned(32))) float b[3] = {3.25, 4.25, 5.25};
        __attribute__ ((aligned(32))) float r[3];
        
        sum_c(a, b, 3, r);
        for(int i=0; i<3; i++)
            std::cout << "C++: " << *(r+i) << std::endl;
        
        
        pot_x87(a,b,3,r);
        for(int i=0; i<3; i++)
            std::cout << "X87: " << *(r+i) << std::endl;

        return 0;
}
