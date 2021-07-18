#include <stdio.h>

int main(void)
{
	int x,y;
	scanf("%d %d",&x,&y);
	if(x>y) 
		{ 
			printf("Brojevi nisu dobro zadani");
			return 0;
		}
	else 
		{ 
			int t=x;
		 	x=y;
	         	y=t;
			printf("x = %d  y = %d",x,y);
		}
	return 0;
}