/*
 * This code is provided solely for the personal and private use of students
 * taking the CSC369H course at the University of Toronto. Copying for purposes
 * other than this use is expressly prohibited. All forms of distribution of
 * this code, including but not limited to public repositories on GitHub,
 * GitLab, Bitbucket, or any other online platform, whether as given or with
 * any changes, are expressly prohibited.
 *
 * Authors: Andrew Peterson, Karen Reid, Alexey Khrabrov, Angela Brown, Kuei Sun
 *
 * All of the files in this directory and all subdirectories are:
 * Copyright (c) 2019, 2021 Karen Reid
 * Copyright (c) 2023, Angela Brown, Kuei Sun
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "malloc369.h"
#include "sim.h"
#include "coremap.h"
#include "swap.h"
#include "pagetable.h"
#include "khash.h"

#define INVALID_FRAME (memsize + 1)

KHASH_MAP_INIT_INT64(pt_hash, pt_entry_t*)
khash_t(pt_hash) *pt = NULL;


// Counters for various events.
// Your code must increment these when the related events occur.
size_t hit_count = 0;
size_t miss_count = 0;
size_t ref_count = 0;
size_t evict_clean_count = 0;
size_t evict_dirty_count = 0;

// Accessor functions for page table entries, to allow replacement
// algorithms to obtain information from a PTE, without depending
// on the internal implementation of the structure.

/* Returns true if the pte is marked valid, otherwise false */
bool is_valid(pt_entry_t *pte)
{
    return pte->valid;
}

/* Returns true if the pte is marked dirty, otherwise false */
bool is_dirty(pt_entry_t *pte)
{
	return pte->dirty;
}

/* Returns true if the pte is marked referenced, otherwise false */
bool get_referenced(pt_entry_t *pte)
{
	return pte->referenced;
}

/* Sets the 'referenced' status of the pte to the given val */
void set_referenced(pt_entry_t *pte, bool val)
{
	pte->referenced = val;
}

/*
 * Initializes your page table.
 * This function is called once at the start of the simulation.
 * For the simulation, there is a single "process" whose reference trace is
 * being simulated, so there is just one overall page table.
 *
 * In a real OS, each process would have its own page table, which would
 * need to be allocated and initialized as part of process creation.
 * 
 * The format of the page table, and thus what you need to do to get ready
 * to start translating virtual addresses, is up to you. 
 */
void init_pagetable(void)
{
    // create a hash table to store page table entries
    // key is the page number
    // value is the page table entry
    pt = kh_init(pt_hash);
}


/*
 * Write virtual page represented by pte to swap, if needed, and update 
 * page table entry.
 *
 * Called from allocate_frame() in coremap.c after a victim page frame has
 * been selected. 
 *
 * Counters for evictions should be updated appropriately in this function.
 */
void handle_evict(pt_entry_t * pte)
{
    if (is_dirty(pte)) {
       pte->swap_offset = swap_pageout(pte->frame_number, pte->swap_offset);
       evict_dirty_count++;
    } else {
       evict_clean_count++;
    }
    pte->dirty = false;
    pte->frame_number = INVALID_FRAME;
    pte->valid = false;
}

/*
 * Locate the physical frame number for the given vaddr using the page table.
 *
 * If the page table entry is invalid and not on swap, then this is the first 
 * reference to the page and a (simulated) physical frame should be allocated 
 * and initialized to all zeros (using init_frame from coremap.c).
 * If the page table entry is invalid and on swap, then a (simulated) physical 
 * frame should be allocated and filled by reading the page data from swap.
 *
 * Make sure to update page table entry status information:
 *  - the page table entry should be marked valid
 *  - if the type of access is a write ('S'tore or 'M'odify),
 *    the page table entry should be marked dirty
 *  - a page should be marked dirty on the first reference to the page,
 *    even if the type of access is a read ('L'oad or 'I'nstruction type).
 *  - DO NOT UPDATE the page table entry 'referenced' information. That
 *    should be done by the replacement algorithm functions.
 *
 * When you have a valid page table entry, return the page frame number
 * that holds the requested virtual page.
 *
 * Counters for hit, miss and reference events should be incremented in
 * this function.
 */
int find_frame_number(vaddr_t vaddr, char type)
{
    pt_entry_t *pte = NULL;

    // use khash to get the pte
    vaddr_t pt_page_number = vaddr / SIMPAGESIZE;  

    khiter_t k = kh_get(pt_hash, pt, pt_page_number);
    if (k != kh_end(pt)) {
       pte = kh_value(pt, k);
    }	

    // handle case when pagetable does not exist 
    if (!pte) {
       pte = malloc369(sizeof(pt_entry_t));
       pte->frame_number = INVALID_FRAME;
       pte->swap_offset = INVALID_SWAP;
       pte->valid = false;                   
       pte->dirty = true;                   
       pte->referenced = false;                   
       int ret = 0;
       khiter_t k = kh_put(pt_hash, pt, pt_page_number, &ret);
       assert(ret != 0); // key should not be there already
       kh_value(pt, k) = pte; 
    }
  
    if (type == 'S' || type == 'M')
       pte->dirty = true;
    
    ref_count++; 

    if (is_valid(pte)) {
       hit_count++;
       return pte->frame_number;
    }
  
    miss_count++;

    int frame = allocate_frame(pte); 
    assert(frame >= 0);
    pte->frame_number = (unsigned int)frame;
 
    if (pte->swap_offset == INVALID_SWAP) {
       // first reference to the page
       init_frame(frame);
    } else { 
       // page is on disk, load from disk to memory
       swap_pagein(pte->frame_number, pte->swap_offset);
       if (type == 'L' || type == 'I') {
           assert(pte->dirty == false); // when swapping out, we set it to false
       }
    } 

    pte->valid = true;
    return frame;
}

void print_pagetable(void)
{
    for (khiter_t k = kh_begin(pt); k != kh_end(pt); ++k) {
        if (kh_exist(pt, k)) {
           pt_entry_t * pte = kh_value(pt, k);
           printf("Frame Number: %d\n", pte->frame_number);
        }
    }
}


void free_pagetable(void)
{
    // Clean up
    for (khiter_t k = kh_begin(pt); k != kh_end(pt); ++k) {
        if (kh_exist(pt, k))
           free369(kh_value(pt, k));
    }
    kh_destroy(pt_hash, pt);
}
