#include <stdio.h>

int main(void)
{
	float x1,x2,y;
	scanf("%f %f",&x1,&x2);
	if(x1>x2)
		{
			if(x1<0) y=-x1;
			else y=x1;
		}
	if(x2>=x1) 
		{
			if(x1*x1>x2*x2) y=x1*x1;
			else y=x2*x2;
		}
	printf("y = %.2f",y);
	return 0;
}