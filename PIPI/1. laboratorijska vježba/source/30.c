#include <stdio.h>

int main(void)
{
	int a,b,c;
	scanf("%d %d %d",&a,&b,&c);
	if(a<b && b<c && b-a == c-b) printf("Brojevi %d , %d, %d su poredani uzlazno (razlika izmedju susjednih brojeva je %d).",a,b,c,c-b);
	if(a<b && b<c && b-a != c-b) printf("Brojevi %d , %d, %d su poredani uzlazno (razlika izmedju susjednih brojeva nije jednaka).",a,b,c);
	if(!(a<b && b<c)) printf("Brojevi %d , %d , %d nisu poredani uzlazno.",a,b,c);
	return 0;
}