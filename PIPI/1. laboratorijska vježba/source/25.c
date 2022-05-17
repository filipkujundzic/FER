#include <stdio.h>
#define PI 3.14159

int main(void)
{
	float x;
	scanf("%f",&x);
	if(x<0) 
		{
			printf("Duljina stranice mora biti pozitivni broj.");
			return 0;
		}
	printf("Povrsina trokuta: %.2f\nPovrsina kruga: %.2f",(x*x)/2,(x*x*PI));
	return 0;
}
	