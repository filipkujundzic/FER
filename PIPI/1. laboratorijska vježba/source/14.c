#include <stdio.h>

int main(void)
{
	int m,n;
	scanf("%d %d",&m,&n);
	if(n%10==0)
	{ 
		printf("Dijeljenje nije moguce.");
		return 0;
	}
	printf("%d / %d = %3.2f",m,n%10,1.0*m/(n%10));
	return 0;
}