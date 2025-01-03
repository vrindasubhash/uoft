/*
 * thread.c
 *
 * Implementation of the threading library.
 */

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include "ut369.h"
#include "queue.h"
#include "thread.h"
#include "schedule.h"
#include "interrupt.h"

// put your global variables here
struct thread thread_array[THREAD_MAX_THREADS];
struct thread * current_thread = NULL; 

volatile int check = 0;

// for debugging
int debug_print = 0;

static void
thread_stub(int (*thread_main)(void *), void *arg);

static void
thread_destroy(struct thread * dead);

/**************************************************************************
 * Cooperative threads: Refer to ut369.h and this file for the detailed 
 *                      descriptions of the functions you need to implement. 
 **************************************************************************/

/* Initialize the thread subsystem */
void
thread_init(void)
{
    for (int i = 0; i < THREAD_MAX_THREADS; i++) {
       struct thread *t = &thread_array[i];
       t->id = i;
       t->state = THREAD_UNUSED;
       t->stack = NULL;
       t->in_queue = 0;
       t->exit_code = 0;
       t->waiting_lock = 0;
       t->next = NULL;
       t->priority = 0;
    }

    // setup the main thread    
    current_thread = &thread_array[0];
    current_thread->state = THREAD_RUNNING; // set the first thread to be running
}

/* Returns the tid of the current running thread. */
Tid
thread_id(void)
{
    if (current_thread == NULL) {
       return THREAD_INVALID;
    }
	return current_thread->id;
}

/* Return the thread structure of the thread with identifier tid, or NULL if 
 * does not exist. Used by thread_yield and thread_wait's placeholder 
 * implementation.
 */
static struct thread * 
thread_get(Tid tid)
{
    // if the tid is valid return the thread structure
    if (tid >= 0 && tid < THREAD_MAX_THREADS) {
       if (thread_array[tid].state == THREAD_UNUSED)
          return NULL; // test expects this
       return &thread_array[tid];
    }
	return NULL;
}

/* Return whether the thread with identifier tid is runnable.
 * Used by thread_yield and thread_wait's placeholder implementation
 */
static bool
thread_runnable(Tid tid)
{
    // get the thread for the given id
    struct thread *t = thread_get(tid);
    // return if that thread stucture is valid and is in the ready state
    return t != NULL && (t->state == THREAD_READY || t->state == THREAD_RUNNING); 
}

static void
set_context_and_switch(struct thread * t)
{
    assert(current_thread != t);
    // update current threads state
    if (thread_runnable(current_thread->id)) {
       current_thread->state = THREAD_READY;
       scheduler->enqueue(current_thread); 
    }

    current_thread = t; 
    check++;

    if (debug_print)
       printf("set_context_and_switch thread id %d, is at state %d\n", t->id, t->state);
    // new thread state can be set to running
    t->state = THREAD_RUNNING;
    setcontext(&t->context); 
}

/* Context switch to the next thread. Used by thread_yield. */
static void
thread_switch(struct thread * next)
{
    int checkval = check;
    if (current_thread && getcontext(&current_thread->context) != 0) { 
       // if the current thread context wasn't saved, don't proceed with next thread
       perror("Failed to get context of the thread");
       return;
    }
    
    // warning dont move this code above getcontext
    // check if we are in a restored thread
    // condition will only happen when you are done calling setcontext()
    if (checkval != check)
       return;
 
    assert(thread_runnable(next->id)); 
   
    set_context_and_switch(next);
}

struct thread * 
dequeue_thread()
{
    struct thread * next_thread = NULL;
    do {
       next_thread = scheduler->dequeue();
       if (next_thread == NULL)
          return NULL;
       if (next_thread->state == THREAD_READY)
          return next_thread;
    } while (next_thread != NULL);

    return next_thread;
}

/* Voluntarily pauses the execution of current thread and invokes scheduler
 * to switch to another thread.
 */
Tid
thread_yield(Tid want_tid)
{
	struct thread * next_thread = NULL;
  
    if (want_tid == THREAD_ANY) {
       next_thread = dequeue_thread();
       if (next_thread == NULL) {
          if (debug_print)
              printf("[%d] want %d, return NONE\n", thread_id(), want_tid);
          return THREAD_NONE; 
       }
    } else if (want_tid == thread_id()) {
       assert(thread_runnable(want_tid));
       return want_tid;
    } else {
        next_thread = scheduler->remove(want_tid);
        if (next_thread == NULL) {
            if (debug_print)
                printf("[%d] want %d, thread invalid\n", thread_id(), want_tid);
            return THREAD_INVALID;
        } else if (!thread_runnable(want_tid)) {
            if (debug_print)
                printf("[%d] want %d, thread not runnable\n", thread_id(), want_tid);
            return want_tid; // this is what the test is expecting
        }
    }
   
    if (debug_print)
        printf("[%d] yield to %d, wantid:%d\n", thread_id(), next_thread->id, want_tid);

    int id = next_thread->id;
    thread_switch(next_thread);
    return id;

	/* TODO: The provided code only works when a specific tid is provided.
	 *       You need to support the THREAD_ANY argument, which allows the
	 *       scheduler to choose a thread out of its ready queue.
	 */
    /*
    assert(want_tid != THREAD_ANY);

	if (want_tid == thread_id()) {
		assert(thread_runnable(want_tid));
		return want_tid;
	}

    next_thread = scheduler->remove(want_tid);
    if (next_thread != NULL) {
		// if current thread is still runnable, enqueue it.
		if (thread_runnable(thread_id()))
			scheduler->enqueue(thread_get(thread_id()));
        thread_switch(next_thread);
    }
	else {
		// cannot find thread with that tid in the ready queue 
		want_tid = THREAD_INVALID;
	}

    return want_tid;
    */
}

/* Fully clean up a thread structure and make its tid available for reuse.
 * Used by thread_wait's placeholder implementation
 */
static void
thread_destroy(struct thread * dead)
{
    if (dead == NULL)
       return;
    if (dead->stack != NULL) {
       free(dead->stack);
       dead->stack = NULL;
    }
    if (debug_print)
        printf("[%d] destroying thread %d\n", thread_id(), dead->id); 
    scheduler->remove(dead->id); 
    dead->exit_code = 0;
    dead->waiting_lock = 0;
    assert(dead->state != THREAD_READY);
    assert(dead->state != THREAD_RUNNING);
    dead->state = THREAD_UNUSED;
    dead->priority = 0;
}

/* New thread starts by calling thread_stub. The arguments to thread_stub are
 * the thread_main() function, and one argument to the thread_main() function. 
 */
static void
thread_stub(int (*thread_main)(void *), void *arg)
{
	int ret = thread_main(arg); // call thread_main() function with arg
	thread_exit(ret);
}


Tid
thread_create(int (*fn)(void *), void *parg, int priority)
{
    // get context and set regs and offset rsp +8 after malloc
    // set t stuff and then malloc
    // remove the offest in helper 

    struct thread *t = NULL;
    for (int i = 0; i < THREAD_MAX_THREADS; i++) {
        if (thread_array[i].state == THREAD_UNUSED) {
            t = &thread_array[i];
            break;
        }
    }
    
    if (t == NULL)
        return THREAD_NOMORE;

    if (t->stack == NULL) 
       t->stack = malloc(THREAD_MIN_STACK);

    if (t->stack == NULL)
       return THREAD_NOMEMORY;

    t->waiting_lock = 0;
    t->state = THREAD_READY;
    t->priority = priority;

    getcontext(&t->context);
    long long int l = (long long int)((char*)(t->stack) + THREAD_MIN_STACK + 8);;

    t->context.uc_mcontext.gregs[REG_RBP] = 0; // not strictly required, just easier to debug
    t->context.uc_mcontext.gregs[REG_RSP] = l;
    t->context.uc_mcontext.gregs[REG_RIP] = (greg_t)(long long int)thread_stub;
    t->context.uc_mcontext.gregs[REG_RDI] = (greg_t)(long long int)fn;
    t->context.uc_mcontext.gregs[REG_RSI] = (greg_t)(long long int)parg;

    scheduler->enqueue(t);
    if (debug_print)
        printf("[%d] creating: %d\n", thread_id(),t->id);
    return t->id;
}

Tid
thread_kill(Tid tid)
{
    // check if the thread id is valid 
    if (tid < 0 || tid >= THREAD_MAX_THREADS || tid == thread_id()) {
       if (debug_print)
           printf("ignoring thread kill: %d\n", tid);
       return THREAD_INVALID;
    }

    struct thread *target_thread = &thread_array[tid];

    if (debug_print)
        printf("[%d] killing thread %d in state: %d\n", thread_id(), tid, target_thread->state);

    // check if thread is already in an unusable state
    if (target_thread->state == THREAD_UNUSED)
       return THREAD_INVALID;

    // force it to run thread exit next time it is scheduled
    target_thread->context.uc_mcontext.gregs[REG_RIP] = (greg_t)(long long int)thread_exit;
    target_thread->context.uc_mcontext.gregs[REG_RDI] = (greg_t)(long long int)0;

    // the target_thread is running, so let it run until it yields or exits
	return tid;
}

void
thread_exit(int exit_code)
{
    // set state to zombie
    current_thread->state = THREAD_ZOMBIE;
    current_thread->exit_code = exit_code;

    // get the next thread
    struct thread *next = dequeue_thread();
    // clean up all the threads if there aren't anymore threads
    if (!next) {
       thread_end();
       ut369_exit(exit_code); // exit the threading system
    } 
   
    set_context_and_switch(next);
}

/* Clean-up logic to unload the threading system. Used by ut369.c. You may 
 * assume all threads are either freed or in the zombie state when this is 
 * called.
 */
void
thread_end(void)
{
    // go through all of the threads 
    for (int i = 0; i < THREAD_MAX_THREADS; i++) {
       struct thread *t = &thread_array[i];

       // free its stack if it exists
       if (t->stack != NULL) {
          free(t->stack);
          t->stack = NULL;
       }
       // set thread state to unused 
       t->state = THREAD_UNUSED;
    }
}

/**************************************************************************
 * Preemptive threads: Refer to ut369.h for the detailed descriptions of 
 *                     the functions you need to implement. 
 **************************************************************************/

Tid
thread_wait(Tid tid, int *exit_code)
{
	// This is a placeholder implementation for cooperative threads.
	// It will not work once you start preemptive threads. Do not change
	// this for A2, but definitely change it for A3.
	
	if (tid == thread_id()) {
		return THREAD_INVALID;
	}

	// If thread does not exist, return error
	struct thread * target = thread_get(tid);
	if (target == NULL) {
		return THREAD_INVALID;
	}

	// Continue to yield to the thread until its no longer runnable
	while (thread_runnable(tid)) {
		int ret = thread_yield(tid);
		assert(ret == tid);
	}

	// Clean up all resources used by this thread, and make its tid available
	thread_destroy(target);

	// Unused for now
	(void)exit_code;
	return 0;
}

Tid
thread_sleep(fifo_queue_t *queue)
{
	/* TBD */
	(void)queue;
	return THREAD_TODO;
}

/* When the 'all' parameter is 1, wake up all threads waiting in the queue.
 * returns whether a thread was woken up on not. 
 */
int
thread_wakeup(fifo_queue_t *queue, int all)
{
	/* TBD */
	(void)queue;
	(void)all;
	return THREAD_TODO;
}

struct lock {
	/* ... fill this in ... */
};

struct lock *
lock_create()
{
	struct lock *lock = malloc(sizeof(struct lock));
	/* TBD */
	return lock;
}

void
lock_destroy(struct lock *lock)
{
	assert(lock != NULL);
	/* TBD */
	free(lock);
}

void
lock_acquire(struct lock *lock)
{
	assert(lock != NULL);
	/* TBD */
}

void
lock_release(struct lock *lock)
{
	assert(lock != NULL);
	/* TBD */
}


/*
void
thread_debug(void)
{
   int ready_count = 0;
   int running_count = 0;
   int zombie_count = 0;
   int unused_count = 0;
   int unknown_state = 0;
   int in_queue = 0;
   for (int i = 0; i < THREAD_MAX_THREADS; i++) {
       struct thread *t = &thread_array[i];
       if (t->in_queue == 1) in_queue++;
       if (t->state == THREAD_READY) ready_count++;
       else if (t->state == THREAD_RUNNING) running_count++;
       else if (t->state == THREAD_ZOMBIE) zombie_count++;
       else if (t->state == THREAD_UNUSED) unused_count++;
       else unknown_state++;
   }
   printf("ready:%d, running:%d, zombie:%d, unused:%d, unknown:%d, inqueue:%d\n", 
         ready_count, running_count, zombie_count, unused_count, unknown_state, in_queue);
   
}
*/
