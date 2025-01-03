/*
 * fcfs.c
 *
 * Implementation of a first-come first-served scheduler.
 * Becomes round-robin once preemption is enabled.
 */

#include "ut369.h"
#include "queue.h"
#include "thread.h"
#include "schedule.h"
#include <stdlib.h>
#include <assert.h>


static struct thread **ready_queue = NULL;
static int count = 0;
static int capacity = THREAD_MAX_THREADS;

int 
fcfs_init(void)
{
    ready_queue = malloc(sizeof(struct thread *) * capacity);
    if (ready_queue == NULL) {
       return THREAD_NOMEMORY;
    }
    count = 0;
    return 0;
}

int
fcfs_enqueue(struct thread * thread)
{
    if (count >= capacity) {
        //printf("fcfs capacity reached. count:%d, capacity:%d\n", count, capacity); 
        return THREAD_NOMORE; // No more space
    }
    ready_queue[count++] = thread; // Add to the end and increment count
    //printf("fcfs enqueue.thread id:%d,  count:%d, capacity:%d\n", thread->id, count, capacity); 
    return 0;
}

struct thread *
fcfs_dequeue(void)
{
    if (count == 0) {
        return NULL; // No thread to dequeue
    }

    struct thread *first_thread = ready_queue[0];
    // Move all elements one position to the left
    for (int i = 1; i < count; i++) {
        ready_queue[i - 1] = ready_queue[i];
    }
    count--;
    //printf("fcfs dequeue. thread id:%d, count:%d, capacity:%d\n", first_thread->id, count, capacity); 
    return first_thread;
}

struct thread *
fcfs_remove(Tid tid)
{
    struct thread *thread = NULL;
    for (int i = 0; i < count; i++) {
        if (ready_queue[i]->id == tid) {
            thread = ready_queue[i];
            // Move all elements one position to the left from this point
            for (int j = i; j < count - 1; j++) {
                ready_queue[j] = ready_queue[j + 1];
            }
            count--;
            break;
        }
    }
    return thread;
}

void
fcfs_destroy(void)
{
    free(ready_queue);
    ready_queue = NULL;
    count = 0;
}
