#include <stdio.h>
#define PI 3.14159

int main(void)
{
	float x,y;
	scanf("%f %f",&x,&y);
	printf("Polumjer kruga = %.3f\nStranica kvadrata = %.3f",x/(2*PI),y/4);
	if(x/PI>y/4) printf("\nKrug nije moguce smjestiti unutar kvadrata.");
	else printf("\nKrug je moguce smjestiti unutar kvadrata,");
	return 0;
}
	
