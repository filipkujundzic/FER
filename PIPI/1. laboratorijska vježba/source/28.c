#include <stdio.h>

int main(void)
{
	int x1,x2,y1,y2;
	scanf("%d %d %d %d",&x1,&y1,&x2,&y2);
	if(y1==y2) printf("Pravac koji prolazi tockama (%d,%d) i (%d,%d) je paralelan s x osi.",x1,y1,x2,y2);
	if(x1==x2) printf("Pravac koji prolazi tockama (%d,%d) i (%d,%d) je paralelan s y osi.",x1,y1,x2,y2);
	if(y1!=y2 && x1!=x2) printf("Pravac koji prolazi tockama (%d,%d) i (%d,%d) nije paralelan ni s jednom osi.",x1,y1,x2,y2);
	return 0;
}
	