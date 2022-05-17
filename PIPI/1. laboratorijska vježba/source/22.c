#include <stdio.h>

int main(void)
{
	float x,y;
	scanf("%f",&x);
	if(x<0) y=3*x;
	if(x>=1) y=x*x+3;
	if(x>=0 && x<1) y=(3./4)*x+1;
	printf("x = %.3f y = %.3f",x,y);
	return 0;
}
