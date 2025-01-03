/*
 * thread.h
 *
 * Definition of the thread structure and internal helper functions.
 * 
 * You may add more declarations/definitions in this file.
 */

#ifndef _THREAD_H_
#define _THREAD_H_

#include "ut369.h"
#include <stdbool.h>
#include <ucontext.h>


// Different states a thread can be
typedef enum {
    THREAD_UNUSED,
    THREAD_READY,
    THREAD_RUNNING,
    THREAD_BLOCKED,
    THREAD_ZOMBIE
} ThreadState;


struct thread {
    Tid id;

    /*
     * Pointer to the next node
     */
    // struct _node_item* next;
    struct thread * next;

    /*
     * Flag to check if a node is already in the queue
     */
    int in_queue; // 1 if yes, 0 if no

    ThreadState state; // State of the thread
    ucontext_t context; // CPU context for the thread
    void *stack; // Pointer to threads stack
    int exit_code; // Exit code for when the thread finishes 
    int waiting_lock; // modify later
    int priority;
    fifo_queue_t *queue; // which queue is this thread in
    fifo_queue_t *wait_queue; // which threads are waiting for me
    int pending_read_exitcode; // number of threads that need to read exit code
};

// functions defined in thread.c
void thread_init(void);
void thread_end(void);

// functions defined in ut369.c
void ut369_exit(int exit_code);

// for debugging
//void thread_debug(void);

#endif /* _THREAD_H_ */
