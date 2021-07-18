#include <stdio.h>

int main(void)
{
	int a,b;
	scanf("%d %d",&a,&b);
	if(a%10 + a/10 == b%10 + b/10) 
		printf("Brojevi %d i %d imaju jednaku sumu znamenaka",a,b);
	else 
	{
		if(a%10 + a/10 > b%10 + b/10) printf("Broj %d ima vec sumu znamenaka od broja %d",a,b);
		else printf("Broj %d ima vec sumu znamenaka od broja %d",b,a);
	}
	return 0;
}
