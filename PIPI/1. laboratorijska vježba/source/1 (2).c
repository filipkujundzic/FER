#include <stdio.h>

int main(void)
{
    int n, i, j;
    float m = 0;
    scanf("%d", &n);
    for(i = 0; i < n + 2; i++)
    {
        m = 0;
        for(j = 0; j < i + 1; j++, m += 0.1)
            printf(" %1.1f", m);
        printf("%*d.red", 4 * (n + 2) - 3 * i - i, i);
        printf("\n");
    }
    return 0;
}
