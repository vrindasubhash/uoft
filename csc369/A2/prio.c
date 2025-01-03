/*
 * prio.c
 *
 * Implementation of a priority scheduler (A3)
 */

#include "ut369.h"
#include "queue.h"
#include "thread.h"
#include "schedule.h"
#include <stdlib.h>
#include <assert.h>

int 
prio_init(void)
{
    return THREAD_TODO;
}

int
prio_enqueue(struct thread * thread)
{
    (void)thread;
    return THREAD_TODO;
}

struct thread *
prio_dequeue(void)
{
    return NULL;
}

struct thread *
prio_remove(Tid tid)
{
    (void)tid;
    return NULL;
}

void
prio_destroy(void)
{
    /* TODO: complete me */
}