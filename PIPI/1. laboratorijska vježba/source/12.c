#include <stdio.h>

int main(void)
{
	int x,y,i,rez;
	scanf("%d %d",&x,&y);
	scanf("%d",&i);
	if(i==1) rez=x+y;
	if(i==2) 
		{
			if(x>y) rez=x-y;
			else rez=y-x;
		}
	if(i==1) printf("%d + %d = %d",x,y,rez);
	if(i==2 && rez==x-y) printf("%d - %d = %d",x,y,rez);
	else if(i==2 && rez==y-x) printf("%d - %d = %d",y,x,rez);
	return 0;
}