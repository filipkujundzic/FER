#include <stdio.h>

int main(void)
{
	int m,s;
	scanf("%d %d",&m,&s);
	if(s>59) 
		{
			printf("Neispravan broj sekundi.");
			return;
		}
	printf("sekunde: %d; sati: %.3f",m*60+s,1.0*(m*60+s)/3600);
	return 0;
}
	