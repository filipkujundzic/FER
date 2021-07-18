#include <stdio.h>

int main(void)
{
	int x,y,br1,br2;
	scanf("%d %d",&x,&y);
	if(x%2==0 && y%2==0)
	{
		br1=y*10+x;
		br2=x*10+y;
		printf("Parni brojevi kreirani od znamenaka %d i %d: %d %d",x,y,br1,br2);
	}
	if(x%2!=0 && y%2==0)
	{
		br1=x*10+y;
		printf("Parni brojevi kreirani od znamenaka %d i %d: %d",x,y,br1);
	}
	if(x%2==0 && y%2!=0)
	{
		br1=y*10+x;
		printf("Parni brojevi kreirani od znamenaka %d i %d: %d",x,y,br1);
	}
	if(x%2!=0 && y%2!=0) printf("Parni brojevi kreirani od znamenaka %d i %d: -",x,y);
	return 0;
}