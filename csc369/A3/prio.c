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
#include <limits.h> 
#include <stdio.h>

fifo_queue_t *queue = NULL;
extern struct thread *current_thread;
extern int debug_print;

int 
prio_init(void)
{
    queue = queue_create(THREAD_MAX_THREADS);
    assert(queue != NULL);
    return 0;
}

int
prio_enqueue(struct thread * thread)
{
    if (thread->in_queue == 0)
       return queue_push(queue, thread);
    return 0;  
}

struct thread *
prio_dequeue(void)
{
   // iterate thru queue and find smallest priority - track tid
   // remove it from queue
   // return thread you just removed
   int min_priority = INT_MAX;
   Tid tid_min = -1;

   node_item_t *tmp = queue_top(queue);
   while (tmp) {
      if (tmp->priority <= min_priority) {
         min_priority = tmp->priority;
         tid_min = tmp->id;
      }
      tmp = tmp->next;
   }
  
   if (debug_print) 
      printf("[%s:%d:%d] priority:%d, tid:%d\n", 
          __func__, current_thread->id, current_thread->priority, min_priority, tid_min); 

   // if current_thread has higher priority, continue running current_thread
   if (current_thread->priority < min_priority && current_thread->state == THREAD_READY)
      return current_thread;
   
   return prio_remove(tid_min); // if tid_min is -1, it will return NULL
}

struct thread *
prio_remove(Tid tid)
{
    return queue_remove(queue, tid);
}

void
prio_destroy(void)
{
   if (queue != NULL)
      queue_destroy(queue);
   queue = NULL;
}
