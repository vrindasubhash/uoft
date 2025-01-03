/*
 * thread.c
 *
 * Implementation of the threading library.
 */

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
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
       t->priority = INT_MAX;
       t->wait_queue = NULL;
       t->pending_read_exitcode = 0;
    }

    // setup the main thread
    current_thread = &thread_array[0];
    current_thread->state = THREAD_RUNNING; // set the first thread to be running
    current_thread->wait_queue = queue_create(THREAD_MAX_THREADS);
    current_thread->priority = 0;
}

/* Returns the tid of the current running thread. */
Tid
thread_id(void)
{
    int enabled = interrupt_off();
    Tid tid = THREAD_INVALID;

    if (current_thread != NULL) {
	   tid = current_thread->id;
    }

    interrupt_set(enabled);
    return tid;
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

char *
state_str(ThreadState s)
{
  if (s == THREAD_UNUSED)
     return "THREAD_UNUSED";
  if (s == THREAD_READY)
     return "THREAD_READY";
  if (s == THREAD_RUNNING)
     return "THREAD_RUNNING";
  if (s == THREAD_BLOCKED)
     return "THREAD_BLOCKED";
  if (s == THREAD_ZOMBIE)
     return "THREAD_ZOMBIE";
  return "Unknown state";
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
       printf("[%d] set_context_and_switch thread id %d, is at state %s\n",
         thread_id(), t->id, state_str(t->state));
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
    int enabled = interrupt_off();

	struct thread * next_thread = NULL;

    if (want_tid == THREAD_ANY) {
       next_thread = dequeue_thread();
       if (next_thread == NULL) {
          if (debug_print)
              printf("[%s:%d] want %d, return NONE\n", __func__, thread_id(), want_tid);
          interrupt_set(enabled);
          return THREAD_NONE;
       }
       if (next_thread->id == thread_id()) {
          assert(thread_runnable(next_thread->id));
          interrupt_set(enabled);
          return next_thread->id;
       }
    } else if (want_tid == thread_id()) {
       assert(thread_runnable(want_tid));
       interrupt_set(enabled);
       return want_tid;
    } else {
        next_thread = scheduler->remove(want_tid);
        if (next_thread == NULL) {
            if (debug_print)
                printf("[%d] want %d, thread invalid\n", thread_id(), want_tid);
            interrupt_set(enabled);
            return THREAD_INVALID;
        } else if (!thread_runnable(want_tid)) {
            if (debug_print)
                printf("[%d] want %d, thread not runnable\n", thread_id(), want_tid);
            interrupt_set(enabled);
            return want_tid; // this is what the test is expecting
        }
    }
 
    if (debug_print)
        printf("[%d] yield to %d, wantid:%d\n", thread_id(), next_thread->id, want_tid);

    int id = next_thread->id;
    thread_switch(next_thread);
    interrupt_set(enabled);
    return id;
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

    if (dead->wait_queue != NULL) {
       queue_destroy(dead->wait_queue);
       dead->wait_queue = NULL;
    }

    if (debug_print)
        printf("[%d] destroying thread %d\n", thread_id(), dead->id);
    scheduler->remove(dead->id);
    dead->exit_code = 0;
    dead->waiting_lock = 0;
    assert(dead->state != THREAD_READY);
    assert(dead->state != THREAD_RUNNING);
    dead->state = THREAD_UNUSED;
    dead->priority = INT_MAX;
    assert(dead->pending_read_exitcode == 0);
}

/* New thread starts by calling thread_stub. The arguments to thread_stub are
 * the thread_main() function, and one argument to the thread_main() function.
 */
static void
thread_stub(int (*thread_main)(void *), void *arg)
{
    // turned off interrupts before getcontext so not clear if we need to turn off or on after this
    interrupt_on();
	int ret = thread_main(arg); // call thread_main() function with arg
	thread_exit(ret);
}

int next_slot = 1;

Tid
thread_create(int (*fn)(void *), void *parg, int priority)
{
    int enabled = interrupt_off();
    // get context and set regs and offset rsp +8 after malloc
    // set t stuff and then malloc
    // remove the offest in helper

    struct thread *t = NULL;

    // search from next_slot to THREAD_MAX_THREADS - 1 
    // then wrap from 0 to next_slot - 1
    for (int i = next_slot; i < THREAD_MAX_THREADS; i++) {
        if (thread_array[i].state == THREAD_UNUSED) {
            t = &thread_array[i];
            next_slot = i + 1;
            break;
        }
    }
    
    if (t == NULL) {
       for (int i = 0; i < next_slot; i++) {
           if (thread_array[i].state == THREAD_UNUSED) {
               t = &thread_array[i];
               next_slot = i + 1;
               break;
           }
       }
    }
   
    if (next_slot == THREAD_MAX_THREADS)
       next_slot = 0;
 
    if (t == NULL) {
        interrupt_set(enabled);
        return THREAD_NOMORE;
    }

    if (t->stack == NULL)
       t->stack = malloc(THREAD_MIN_STACK);

    if (t->stack == NULL) {
       interrupt_set(enabled);
       return THREAD_NOMEMORY;
    }

    if (t->wait_queue == NULL)
       t->wait_queue = queue_create(THREAD_MAX_THREADS);
 
    if (t->wait_queue == NULL) {
       interrupt_set(enabled);
       return THREAD_NOMEMORY;
    }

    t->waiting_lock = 0;
    t->state = THREAD_READY;
    t->priority = priority;
    t->pending_read_exitcode = 0;

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

    if (scheduler->realtime)
       thread_yield(THREAD_ANY);
  
    interrupt_set(enabled);
    return t->id;
}

Tid
thread_kill(Tid tid)
{
    int enabled = interrupt_off();
    // check if the thread id is valid
    if (tid < 0 || tid >= THREAD_MAX_THREADS || tid == thread_id()) {
       if (debug_print)
           printf("ignoring thread kill: %d\n", tid);
       interrupt_set(enabled);
       return THREAD_INVALID;
    }

    struct thread *target_thread = &thread_array[tid];

    if (debug_print)
        printf("[%d] killing thread %d in state: %s\n", thread_id(), tid, state_str(target_thread->state));

    // check if thread is already in an unusable state
    if (target_thread->state == THREAD_UNUSED) {
       interrupt_set(enabled);
       return THREAD_INVALID;
    }

    // assuming the thread is not currently running on a different processor
    // force it to run thread exit next time it is scheduled
    target_thread->context.uc_mcontext.gregs[REG_RIP] = (greg_t)(long long int)thread_exit;
    target_thread->context.uc_mcontext.gregs[REG_RDI] = (greg_t)(long long int)THREAD_KILLED;

    target_thread->state = THREAD_READY;
    scheduler->enqueue(target_thread);
    
    if (scheduler->realtime)
       thread_yield(THREAD_ANY);

    // the target_thread is running, so let it run until it yields or exits
    interrupt_set(enabled);
	return tid;
}

void
thread_exit(int exit_code)
{
    // dont know state of interrupt when thread_exit is called from the stub
    int enabled = interrupt_off();
    if (debug_print)
        printf("[%d] thread exit(%d), in state: %s\n", thread_id(), exit_code, state_str(current_thread->state));

    // set state to zombie
    current_thread->state = THREAD_ZOMBIE;
    current_thread->exit_code = exit_code;

    // put all waiting threads into the scheduler if needed
    while (queue_count(current_thread->wait_queue) > 0) {
        struct thread *t = queue_pop(current_thread->wait_queue);
        if (t->state == THREAD_BLOCKED) {
           t->state = THREAD_READY;
           scheduler->enqueue(t);
        }
    }

    // get the next thread
    struct thread *next = dequeue_thread();
    // clean up all the threads if there aren't anymore threads
    if (!next) {
       thread_end();
       ut369_exit(exit_code); // exit the threading system
    }

    interrupt_set(enabled);
    set_context_and_switch(next);
}

/* Clean-up logic to unload the threading system. Used by ut369.c. You may
 * assume all threads are either freed or in the zombie state when this is
 * called.
 */
void
thread_end(void)
{
    int curr_tid = thread_id();

    // go through all of the threads
    for (int i = 0; i < THREAD_MAX_THREADS; i++) {
       struct thread *t = &thread_array[i];

       // free its stack if it exists
       // do not free the stack of the current running thread
       if (t->stack != NULL && t->id != curr_tid) {
          free(t->stack);
          t->stack = NULL;
       }

       if (t->wait_queue != NULL) {
           while (queue_count(t->wait_queue) > 0)
              queue_pop(t->wait_queue);
           queue_destroy(t->wait_queue);
           t->wait_queue = NULL;
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
    int ret = THREAD_INVALID;

	if (tid == thread_id()) {
		return ret;
	}

    int enabled = interrupt_off();

	// If thread does not exist, return error
	struct thread * target = thread_get(tid);
	if (target == NULL) {
        interrupt_set(enabled);
		return ret;
	}
 
    if (debug_print)
        printf("[%s:%d] waiting on %d:%s\n", __func__, thread_id(), tid, state_str(target->state));

    if (target->state == THREAD_UNUSED) {
        interrupt_set(enabled);
		return ret;
    }

    if (target->state == THREAD_ZOMBIE) {
        if (exit_code != NULL)
           *exit_code = target->exit_code;
        if (target->pending_read_exitcode == 0) {
           thread_destroy(target);
           ret = 0;
        }
        interrupt_set(enabled);
        return ret;
    }

    ret = 0;

    // add yourself to the wait queue for tid
    int push_success = queue_push(target->wait_queue, current_thread);
    assert(push_success == 0); // we should always have enough capacity
    target->pending_read_exitcode++;

    // set yourself as waiting
    current_thread->state = THREAD_BLOCKED;
    thread_yield(THREAD_ANY);
    target->pending_read_exitcode--;

    // check if the target is good before setting
    if (exit_code != NULL)
       *exit_code = target->exit_code;

	// Clean up all resources used by this thread, and make its tid available
    if (target->pending_read_exitcode == 0)
	   thread_destroy(target);

    if (debug_print)
        printf("[%s:%d] thread wait done, pending:%d on %d:%s\n",
           __func__, thread_id(), target->pending_read_exitcode, tid, state_str(target->state));

    interrupt_set(enabled);
	return ret;
}

Tid
thread_sleep(fifo_queue_t *queue)
{
    /* The standard advice I give here is to call thread_yield(THREAD_ANY). If that returns THREAD_NONE, then you have to undo your changes by setting current thread’s state back to running, and then removing current thread from the wait queue.
    */

    if (queue == NULL) {
       return THREAD_INVALID;
    }
    int enabled = interrupt_off();
    Tid tid = thread_id();

    if (tid != THREAD_INVALID) {
       int old_state = thread_array[tid].state;
       thread_array[tid].state = THREAD_BLOCKED;
       if (queue_push(queue, &thread_array[tid]) != 0)
          assert(0); // assert since push failed
       Tid thread_next = thread_yield(THREAD_ANY);
       if (thread_next == THREAD_NONE) {
          thread_array[tid].state = old_state;
          queue_remove(queue, tid);
       }
       tid = thread_next; // could be THREAD_NONE or valid tid of next thread
    }

    interrupt_set(enabled);
	return tid;
}

/* When the 'all' parameter is 1, wake up all threads waiting in the queue.
 * returns whether a thread was woken up on not.
 */
int
thread_wakeup(fifo_queue_t *queue, int all)
{
    if (queue == NULL) {
       return 0;
    }
    int enabled = interrupt_off();
    int count = 0;
    while (queue_count(queue) > 0) {
       struct thread * t = queue_pop(queue);
       t->state = THREAD_READY;
       scheduler->enqueue(t);
       count++;
       if (all == 0)
          break;
    }
    interrupt_set(enabled);
	return count;
}


#define LOCK_AVAILABLE -1

struct lock {
    Tid tid; // tid of holding thread (LOCK_AVAILABLE if no one holds it)
    fifo_queue_t *lock_queue; // which threads are waiting for this lock
};

struct lock *
lock_create()
{
	struct lock *lock = malloc(sizeof(struct lock));
    lock->tid = LOCK_AVAILABLE;
    lock->lock_queue = queue_create(THREAD_MAX_THREADS);
	return lock;
}

void
lock_destroy(struct lock *lock)
{
	assert(lock != NULL);
    assert(lock->tid == LOCK_AVAILABLE);
    queue_destroy(lock->lock_queue);
	free(lock);
}

void
lock_acquire(struct lock *lock)
{
	assert(lock != NULL);
    int enabled = interrupt_off();

    while (lock->tid != LOCK_AVAILABLE) {
      thread_sleep(lock->lock_queue);
    }

    lock->tid = thread_id();

    interrupt_set(enabled);
}

void
lock_release(struct lock *lock)
{
	assert(lock != NULL);
    int enabled = interrupt_off();
    assert(lock->tid == thread_id());
    lock->tid = LOCK_AVAILABLE;

    // wakeup one thread from lock queue
    thread_wakeup(lock->lock_queue, 0);

    if (scheduler->realtime)
       thread_yield(THREAD_ANY);

    interrupt_set(enabled);
}

void
set_priority(int priority)
{
    int enabled = interrupt_off();
    current_thread->priority = priority; // may need to yield since priority could be lower now
    if (scheduler->realtime)
       thread_yield(THREAD_ANY);
    interrupt_set(enabled);
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
