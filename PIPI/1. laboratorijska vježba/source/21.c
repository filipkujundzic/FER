#include <stdio.h>

int main(void)
{
	float x,y;
	scanf("%f",&x);
	if(x<0) y=-x;
	if(x==0) y=x;
	if(x>0) y=((2./3)*x)+3;
	printf("x = %.2f y = %.2f",x,y);
	return 0;
}
	