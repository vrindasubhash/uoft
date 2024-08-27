#include <stdio.h>
#include <unistd.h>

int main()
{
    int c = 0; 
    for (int i = 0; i < 3; i++) { 
        if (fork() == 0) { 
            printf("%d ", i);
//            printf("%d ", c + i); 
            fflush(stdout); 
        } 
        else { 
            c = c + i + 3; 
        } 
    } 

    return 0; 
}
