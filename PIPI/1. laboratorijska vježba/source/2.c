#include <stdio.h>

int main(void)
{
	int x,x1;
	scanf("%d",&x);
	if(x<0) x1=-x;
	else x1=x;
	if(x/10!=5) printf("Prva znamenka broja %d je %d",x,x1/10);
	else printf("Zadnja znamenka broja %d je %d",x,x1%10); 
	return 0;
}
