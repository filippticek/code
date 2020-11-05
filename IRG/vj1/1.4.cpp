#include <stdio.h>
#include <malloc.h>
#include <math.h>

struct vektor{
	double x;
	double y;
	double z;
};

vektor sumaVektora(vektor* a, vektor* b){
	vektor c;
	c.x = a->x + b->x;
	c.y = a->y + b->y;
	c.z = a->z + b->z;
	return c;
}

double skalarniUmnozak(vektor* a, vektor* b){
	vektor c;
	double s;
	c.x = a->x * b->x;
	c.y = a->y * b->y;
	c.z = a->z * b->z;
	s = c.x + c.y + c.z;
	return s;
}

vektor promijeniSmjer(vektor* a){
	vektor c;
	c.x = -a->x;	
	c.y = -a->y;	
	c.z = -a->z;	
	return c;
}

vektor vektorskiUmnozak(vektor* a, vektor* b){
	vektor c;
	c.x = a->y * b->z - a->z * b->y;
	c.y = a->z * b->x - a->x * b->z;
	c.z = a->x * b->y - a->y * b->x;
	return c;
}

double norma(vektor* a){
	return sqrt(a->x * a->x + a->y * a->y + a->z * a->z);
}

vektor normiraniVektor(vektor* a){
	vektor c;
	double norm = norma(a);
	c.x = a->x / norm;
	c.y = a->y / norm;
	c.z = a->z / norm;
	return c;
}

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
				sum += a[i][k]*b[k][j];
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
	vektor a, b, c, v1, v2, v3, v4;
	double prva[3][3] = { {1,2,3}, {2,1,3}, {4,5,1} };
	double druga[3][3] = { {-1,2,-3}, {5,-2,7}, {-4,-1,3} };

	a.x = 1;
	a.y = 2;
	a.z = 3;

	b.x = 2;
	b.y = 2;
	b.z = 4;

	c.x = 2;
	c.y = 2;
	c.z = 4;

	printf("V1####################\n");
	v1 = sumaVektora(&a, &b);
	printf("x: %f, y: %f, z: %f\n", v1.x, v1.y, v1.z);
	

	double s = skalarniUmnozak(&a, &b);
	
	printf("Skalar: %f\n", s);

	printf("V2####################\n");
	v2 = vektorskiUmnozak(&a, &b); 
	printf("x: %f, y: %f, z: %f\n", v2.x, v2.y, v2.z);
	
	printf("V3####################\n");
	v3 = normiraniVektor(&v2);
	printf("x: %f, y: %f, z: %f\n", v3.x, v3.y, v3.z);
	
	printf("V4####################\n");
	v4 = promijeniSmjer(&v2);
	printf("x: %f, y: %f, z: %f\n", v4.x, v4.y, v4.z);

	printf("M1####################\n");
	double** m1 = sumaMatrica(prva, druga);
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			printf("%f ", m1[i][j]);
		}
		printf("\n");
	}

	printf("M2####################\n");
	double** m1T= transponiraj(druga);
	double** m2 = produktMatrica(prva,m1T);
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			printf("%f ", m2[i][j]);
		}
		printf("\n");
	}

	printf("M3####################\n");
	double** m3 = inverz(druga);
	double** m4 = produktMatrica(prva, m3); 
	for (int i=0; i<3; i++){
		for (int j=0; j<3; j++){
			printf("%f ", m4[i][j]);
		}
		printf("\n");
	}

	return 0;
}









