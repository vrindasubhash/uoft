#include <stdio.h>
#include "malloc369.h"

#include "sim.h"
#include "coremap.h"


int idx = 0; // will circle between 0 and memsize (wrap around)
             // current value is where you want to check next

bool *b = NULL;


/* Page to evict is chosen using the CLOCK algorithm.
 * Returns the page frame number (which is also the index in the coremap)
 * for the page that is to be evicted.
 */
int clock_evict(void)
{
    // go through slots till you find a slot with false and evict the slot number
    while (b[idx] != true) {
        b[idx] = true;
        idx++;
        idx = idx % memsize;
    }
   
    int page_to_evict = idx; 

    // update the index to the next slot so you start from there
    idx++;
    idx = idx % memsize;
    
    return page_to_evict;
}

/* This function is called on each access to a page to update any information
 * needed by the CLOCK algorithm.
 * Input: The page table entry and full virtual address (not just VPN)
 * for the page that is being accessed.
 */
void clock_ref(int frame, vaddr_t vaddr)
{
	(void)vaddr;

    // make sure the frame number is valid 
    assert(frame >= 0 && (long unsigned int)frame < memsize);
  
    // mark the boolean flag for the frame as false 
    b[frame] = false;
}

/* Initialize any data structures needed for this replacement algorithm. */
void clock_init(void)
{
    // need memsize of boolean flags
    b = malloc369(sizeof(bool) * memsize);
    if (b == NULL) 
       perror("Failed to allocate boolean flags");

    // need a boolean flag to know if ref is true or false (can be evicted or not)
    // true means 0 (can evict)
    // false means 1 (cannot evict)
    for (long unsigned int i = 0; i < memsize; i++) {
       b[i] = true;
    }
}

/* Cleanup any data structures created in clock_init(). */
void clock_cleanup(void)
{
    if (b != NULL) 
       free369(b);
}
