#include <stdio.h>
#include <string.h>

int func(char *j){
	unsigned int t;
	if(strlen(j) > 10) return 1;

	for(int i=0;i<strlen(j);i++){
		t += ((j[i] * 0x460B) << (i & 7 ));
	}
	printf("%#010x\n", t);
	return 0;
}


int main() {
	char jmbg[11];
	unsigned int *a;

	scanf("Enter username: %s\n", jmbg);
	scanf("Enter password: %u\n", a);

	if (func(jmbg)) printf("Wrong\n");
	else printf("Correct");
	return 0;
}
