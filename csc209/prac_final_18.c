#include <stdio.h>
#include <stdlib.h>
#include <string.h> 


int * str_to_int_array(const char * st, int * size_pt) {
 
  int count = 0;
  for (const char * sp = st; *sp != '\0'; sp++) {
    if (*sp == ' ')
      count++;
  }

  count++;

  int * arr = malloc(sizeof(int) * count);
  const char * start = st;

  for (int i = 0; i < count; i++) {
    int value = 0;

    while (*start && *start != ' ') {
      value = value * 10 + (*start - '0');
      start++;
    }
 
    arr[i] = value;
    start++;

  }

  *size_pt = count;
  return arr;
}
 

int main() {
  int size;
  int * array = str_to_int_array("1 2 3 10 18 20", &size);
  for (int i = 0; i < size; i++) {
      printf("%d ", array[i]);
  }
  printf("\n");
  free(array);
  return 0;
}
