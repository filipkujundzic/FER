#include <stdio.h>

int main(void)
{
	int x,y;
	scanf("%d %d",&x,&y);
	if(x%2==0 || y%2==0)
	{
		if(x<y)
		{
			if(x%2==0) printf("Manji parni broj je: %d.",x);
			if(y%2==0) printf("Manji parni broj je: %d.",y);
		}
 		if(y<x)
		{
			if(x%2==0) printf("Manji parni broj je: %d.",x);
			if(y%2==0) printf("Manji parni broj je: %d.",y);
		}
	}
	else printf("Niti jedan broj nije paran."); 
	return 0;
}