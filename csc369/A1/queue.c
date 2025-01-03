/*
 * queue.c
 *
 * Definition of the queue structure and implemenation of its API functions.
 *
 */

#include "queue.h"
#include <stdlib.h>
#include <assert.h>

struct _fifo_queue {
    /*
     * Pointer to the head of the queue (first node)
     */
   node_item_t *head;

    /*
     * Pointer to the tail of the queue (last node)
     */
   node_item_t *tail;

    /*
     * Number of nodes
     */
   int count;

    /*
     * Max number of nodes in the queue
     */
   int capacity;

};

bool node_in_queue(node_item_t * node)
{
    assert(node != NULL);
    return node->in_queue == 1;
}

fifo_queue_t * queue_create(unsigned capacity)
{
    if (capacity <= 0) {
        return NULL;
    }
    
    fifo_queue_t *queue = (fifo_queue_t *)malloc(sizeof(fifo_queue_t));  

    // Allocation failed
    if (queue == NULL) {
       return NULL;
    }
    
    queue->head = NULL;
    queue->tail = NULL;
    queue->count = 0;
    queue->capacity = capacity;
    
    return queue;
}

void queue_destroy(fifo_queue_t * queue)
{
    assert(queue->head == NULL && queue->tail == NULL);
   
    free(queue);
}

node_item_t * queue_pop(fifo_queue_t * queue)
{
    assert(queue != NULL);

    if (queue->head == NULL) {
       return NULL;
    }
    
    node_item_t *head = queue->head;
    queue->head = queue->head->next;
  
    // If queue becomes empty, update tail to be NULL
    if (queue->head == NULL){
       queue->tail = NULL;
    }

    queue->count -= 1;
    head->in_queue = 0; // mark node as no longer in a queue
    return head;
}

node_item_t * queue_top(fifo_queue_t * queue)
{
    assert(queue != NULL);

    if (queue->head == NULL) {
       return NULL;
    } 
 
    return queue->head;
}

int queue_push(fifo_queue_t * queue, node_item_t * node)
{
    assert(queue != NULL);
    assert(node != NULL);
    // check if the node isnt already in another queue
    assert(node->in_queue == 0);

    // check if the queue is already at capacity
    if (queue->count == queue->capacity) {
       return -1;
    } 

    // if queue is empty, head and tail should both be the new node    
    if (queue->count == 0) {
       queue->head = node;
       queue->tail = node;
    } else {
       queue->tail->next = node;
       queue->tail = node;
    }
   
    queue->tail->next = NULL;
    queue->count += 1; 
    node->in_queue = 1;

    return 0;
}

node_item_t * queue_remove(fifo_queue_t * queue, int id)
{
    assert(queue != NULL);

    node_item_t *found = NULL;

    // if the queue is empty
    if (queue->head == NULL) {
       return NULL;
    }

    // if there is only one item in the queue
    if (queue->count == 1) {
        if (queue->head->id == id) {
           found = queue->head;
           queue->head = NULL;
           queue->tail = NULL;
           queue->count -= 1;
           found->in_queue = 0; //mark node as no longer in a queue.
           return found;
        } 
        return NULL;
    }

    // more than one node 
    node_item_t *curr = queue->head;
    node_item_t *prev = NULL;

    // find node with matching id if it exists
    while (curr != NULL) {
        if (curr->id == id) {
           found = curr;
           break;
        }
        prev = curr;
        curr = curr->next;
    }

    // node does not exist
    if (found == NULL) {
       return NULL;
    }
   
    // remove node 
    // found node is tail
    if (found == queue->tail) {
       queue->tail = prev;
       if (prev != NULL) {
          prev->next = NULL;
       }
    // found node is head
    } else if (found == queue->head) {
       queue->head = found->next;
    } else {
       prev->next = found->next;
    } 

    queue->count -= 1;
    found->in_queue = 0; // mark node as no longer in a queue.
    
    return found; 
}
