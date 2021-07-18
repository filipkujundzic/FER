#include <stdio.h>

int main(void)
{
	int a,b,c;
	scanf("%d %d %d",&a,&b,&c);
	if(a + b == c) printf("%d + %d = %d",a,b,c);
	if(b + c == a) printf("%d + %d = %d",b,c,a);
	if(a + c == b) printf("%d + %d = %d",a,c,b);
	else printf("Niti jedan broj nije jednak zbroju preostalih brojeva.");
	return 0;
}
	