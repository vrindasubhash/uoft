#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

bool is_langford_pairing(int n, const int lst[]);
bool create_langford(int n, int val, int* pl);
void print_array(const int* pl, int l);

int main(int argc, char **argv) {
  if ((argc == 1) || (strcmp(argv[1], "-h") == 0)) {
    fprintf(stderr,"usage: %s [-h] -c n | num...\n", argv[0]);
    return 0;
  }

  char* endptr = NULL;
  // This is for generating langford pairing if possible.
  if ((argc >= 2) && (strcmp(argv[1], "-c") == 0)) {
    if (argc == 2) {
      fprintf(stderr,"%s: -c option requires an argument.\n", argv[0]);
      return 1;
    }

    if (argc > 3) {
      fprintf(stderr,"%s: -c option received too many arguments.\n", argv[0]);
      return 1;
    }
    int n = strtol(argv[2], &endptr, 10);

    // Check if we got a valid integer.
    if (endptr && endptr[0] != '\0') {
      fprintf(stderr,"error: %s is not an integer.\n", argv[2]);
      return 1;
    }

    printf("Creating a langford pairing with n=%d\n", n);


    int* p_generate = malloc(sizeof(int) * 2 * n);
    if (create_langford(n, n, p_generate)) {
      print_array(p_generate, 2 * n);
    } else {
      printf("No results found.\n");
    }
    free(p_generate);
    return 0;
  }

  // Read the numbers from the command line.
  int* p_check = malloc(sizeof(int) * (argc - 1));
  for (int i = 1; i < argc; i++) {
    int num = strtol(argv[i], &endptr, 10);
    p_check[i-1] = num;
    // check if we got a valid integer
    if (endptr && endptr[0] != '\0') {
      fprintf(stderr,"error: %s is not an integer.\n", argv[i]);
      free(p_check);
      return 1;
    }
  }

  printf("Your sequence: ");
  print_array(p_check, argc - 1);

  int n = argc - 1;

  if (is_langford_pairing(n, p_check)) {
     printf("It is a langford pairing!\n");
  } else {
     printf("It is NOT a langford pairing.\n");
  }

  free(p_check);
  return 0;
}

// Check if the sequence is a langford pairing.
// input_n is the length of array lst.
// lst is the input array of integers.
// Returns TRUE or FALSE
bool is_langford_pairing(int input_n, const int lst[]) {
  // Check for early failing cases.
  if (((input_n % 2) == 1) || (input_n == 0))
     return false;
  int n = input_n / 2;
  // Approach:
  //   There will be exactly 2n items
  //   Check every number is between 1 and n
  //   Make sure every individual number is seen
  //   When you see a number, make sure its langford pair is present
  //
  //   Since there are 2n item and n unique numbers, implementing the above approach should work.

  // seen is a set representing what values have been seen so far
  // using n + 1 to simplify the code below by ignoring index 0
  int* seen = malloc(sizeof(int) * (n + 1));

  // mark all items as not seen
  for (int i = 1; i < n+1; i++) {
    seen[i] = 0; // 0 means not yet seen, 1 means seen
  }

  // go through each index and check for langford property
  for (int i = 0; i < 2*n; i++) {
    // check for too big or negative numbers or 0
    if (lst[i] > n || lst[i] <= 0) {
      free(seen);
      return false;
    }
    // If we have seen a number before, skip over it.
    // This is ok because this could be the compliment of an earlier number.
    // This could also be a number you have seen before but in an invalid position.
    // This is ok as we will check at the end if all numbers 1-n were seen.
    // Since the size of the array is 2n, an invalid number could cause one or more numbers in 1-n to be missing.
    if (seen[lst[i]] == 0) {
      // we have not seen this number before
      seen[lst[i]] = 1;
      int curr = lst[i];
      if (lst[i+curr+1] != curr) {
        // expected number curr, not found
        free(seen);
        return false;
      }
    }
  }

  // Checking to see if any numbers were excluded.
  // This can happen if one or more numbers were repeated in addition to the pair.
  for (int i = 1; i < n+1; i++) {
    if (seen[i] == 0) {
      free(seen);
      return false;
    }
  }

  free(seen);
  return true;
}


// Find a place to put one val (and its pair).
//
// Will recursively try to find a place to put the next values.
//
// n is the number of pairs to generate.
// val is the current pair you are trying to place.
// pl is the array of langford pairs being filled in.
// Returns true if it was successful.
bool create_langford(int n, int val, int* pl) {
  // Basecase to end recursion
  if (val == 0)
    return true;

  // Used the formula to check for early exit if langford pairing is not possible.
  if ((n <= 0) || ((n % 4 != 0) && (n % 4 != 3))) {
    return false;
  }

  int l = n * 2;
  // Find a location to insert val and its pair.
  for (int i = 0; i < l; i++) {
    int pos = i + val + 1;
    if (pos >= l)
      return false; // no point looking further

    if ((pl[i] == 0) && (pl[pos] == 0)) {
      pl[i] = val;
      pl[pos] = val;

      // Found a place for val, now find a place for val - 1.
      if (create_langford(n, val - 1, pl))
        return true;

      // Position i does not work.
      // Undo and try the next index (backtracking).
      pl[i] = 0;
      pl[pos] = 0;
    }
  }
  // No possible indexes
  return false;
}

// Helper function to print an array.
// pl is an array of integers to print.
// l is the number of integers in the array.
void print_array(const int* pl, int l) {
  printf("[");
  for (int i = 0; i < l; i++) {
    printf("%d", pl[i]);
    if (i < (l - 1))
      printf(", ");
  }
  printf("]\n");
}
