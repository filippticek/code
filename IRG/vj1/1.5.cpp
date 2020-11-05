#include <malloc.h>
#include <math.h>

double** sumaMatrica(double a[3][3], double b[3][3]){
	double** c = (double**) malloc(3 * sizeof(double*));
	for(int i=0; i<3; i++)
		c[i] = (double*) malloc(3 * sizeof(double));
	
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			c[i][j] = a[i][j] + b[i][j];
		}
	}
	return c; 
}

double** transponiraj(double a[3][3]){
	double** c = (double**) malloc(3 * sizeof(double*));
	for(int i=0; i<3; i++)
		c[i] = (double*) malloc(3 * sizeof(double));
	
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			c[j][i] = a[i][j];
		}
	}
	return c; 
}

double** produktMatrica(double a[3][3], double** b){
	double sum = 0;
	double** c = (double**) malloc(3 * sizeof(double*));
	for(int i=0; i<3; i++)
		c[i] = (double*) malloc(3 * sizeof(double));
	
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			for (int k=0; k<3; k++){
				sum += a[i][k]*a[k][j];
			}	
			c[i][j] = sum;
			sum = 0;
		}
	}
	return c; 
}
int determinant(double a[3][3]){
	return (a[0][0]*((a[1][1]*a[2][2]) - (a[2][1]*a[1][2])) -a[0][1]*(a[1][0]*a[2][2] - a[2][0]*a[1][2]) + a[0][2]*(a[1][0]*a[2][1] - a[2][0]*a[1][1]));
}

double** inverz(double a[3][3]){
	double b[3][3];
	for(int i=0;i<3;i++){
		for(int j=0;j<3;j++){
			double rez = 0;
			double pol[4];
			int m = 0;
			for(int k=0;k<3;k++){
				if(k==i)continue;
				for(int l=0;l<3;l++){
					if(l==j) continue;
					pol[m] = a[k][l];
					m++;
				}
			}
			b[i][j]= pol[0]*pol[2] - pol[1]*pol[3];
			if (((i+j) % 2) == 1) b[i][j]= -b[i][j];
		}
	}
	double** d = transponiraj(b);
	int det = determinant(a);
	double** c = (double**) malloc(3 * sizeof(double*));
	for(int i=0; i<3; i++)
		c[i] = (double*) malloc(3 * sizeof(double));
	
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			c[i][j] = d[i][j] / (double)det;
		}
	}
	return c; 

	
}

int main(){
	double a[3][3] = {{2,2,2}, {1,2,3},{2,1,0}};
	double b[3] = {2,1.5,1};
/*	int i = 0;

	for(int j=0;j<3;j++){
		for(int k=0;k<3;k++){
			a[j][k]= argv[i];
			i++;
			if (i == 3 || i==7 || i==11) i++;
		}
	}
	b[0] = argv[3];
	b[1] = argv[7];
	b[2] = argv[11];
*/
	double** in = inverz(a);
	double rj[3];
	double sum = 0;
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			for (int k=0; k<3; k++){
				sum += in[i][k]*b[k];
			}	
			rj[i] = sum;
			sum = 0;
		}
	}
	
	printf("[x y z] = [%0.f %0.f %0.f]\n", rj[0], rj[1], rj[2]);	
	return 0;
}
