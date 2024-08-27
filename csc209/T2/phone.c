#include <stdio.h>
#include <stdlib.h>

/*
 * $ gcc -Wall -std=gnu99 -g -o phone phone.c
 */
int main(int argc, char **argv) {
    char phone[11];
    int num;

    scanf("%10s %d", phone, &num);
    if (num == -1) {
       printf("%s\n", phone);
       return 0;
    }
    if (num > 9 || num < -1) {
       printf("ERROR\n"); 
       return 1;
    }
    printf("%c\n", phone[num]);
    return 0;
}
