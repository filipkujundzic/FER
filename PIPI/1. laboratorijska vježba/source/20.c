#include <stdio.h>

int main(void)
{
	float a,b,c;
	float min,maks;
	scanf("%f %f %f",&a,&b,&c);
	min=a;
	if(b<min) min=b;
	if(c<min) min=c;
	maks=c;
	if(b>maks) maks=b;
	if(c>maks) maks=c;	
	printf("Broj %.1f je najmanji, a %.1f najveci od ucitanih brojeva.",min,maks);
 	return 0;
}
	