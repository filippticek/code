#include<stdio.h>
#include<time.h>
#include<malloc.h>

//Ubuntu 17.10 artful
//Processor: Intel Core i5-5200U @ 4x 2.7GHz 
//L1 32KB Instruction + 32KB Data = 64KB
//L2 256KB
//L3 3072KB

#define s1 32768
#define s2 262144
#define s3 3145728
#define b 64

void init(char *spremnik, int size){
    for(int i=0; i<size; i++)
        spremnik[i]=0;
}

int rez(char *spremnik, int size){
    int zbr=0;

    for(int i=0; i<size; i++)
        zbr+= spremnik[i];
    
    return zbr;
}

double A(){
    char *l1 = (char *)malloc(2*s1*sizeof(char));
    double start, stop, time, bandwidth;

    init(l1, 2*s1);
    start= clock();
    
    for(int i=0; i<5000; i++)
        for(int j=0; j<2*s1; j++)
            l1[j]++;

    stop= clock();

    time= (stop - start) / CLOCKS_PER_SEC;
    printf("A: %.5f s\n", time);
    printf("Zbroj: %d\n", rez(l1, 2*s1));
    bandwidth= 5000 * 2 / time;
    
    free(l1);
    return bandwidth;
}

double B(){
    char *l2= (char *)malloc(2*s1*sizeof(char));
    double start, stop, time, bandwidth;

    init(l2, 2*s1);
    start= clock();
    
    for(int i=0; i<20000; i++)
        for(int j=0; j<2*s1; j+=b)
            l2[j]++;

    stop= clock();

    time= (stop - start) / CLOCKS_PER_SEC;
    printf("B: %.5f s\n", time);
    printf("Zbroj: %d\n", rez(l2, 2*s1));
    bandwidth= 20000 * 2 * s1 / time / b / (1<<18);
    
    free(l2);
    return bandwidth;

}

double C(){
    char *ram = (char*)malloc(2*s2*sizeof(char));
    double start, stop, time, bandwidth;

    init(ram, 2*s2);
    start= clock();
    
    for(int i=0; i<1000; i++)
        for(int j=0; j<2*s2; j+=b)
            ram[j]++;

    stop= clock();

    time= (stop - start) / CLOCKS_PER_SEC;
    printf("C: %.5f s\n", time);
    printf("Zbroj: %d\n", rez(ram, 2*s1));
    bandwidth= 2000 * s2 / time / b / (1<<18);
    
    free(ram);
    return bandwidth;
}

int main(){
    double bL1= A();
    double bL2= B();
    double bRAM= C();

    printf("Propusnost L1: %f MB/s\n", bL1);
    printf("Propusnost L2: %f MB/s\n", bL2);
    printf("Propusnost RAM: %f MB/s\n", bRAM);

    printf("RAM/L3: %f\n", bRAM/bL2);
    printf("L3/L2: %f\n", bL2/bL1);

    return 0;
}
