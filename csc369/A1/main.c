/*
 * main.c
 *
 * Testing code for your queue library. This file will not be graded.
 *
 */

#include "queue.h"
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

void node_init(node_item_t * node)
{
    /* TODO: you probably need this function to help you initialize your 
     *       node item for testing.
     */
    memset(node, 0, sizeof(node_item_t));
}

int create_node_and_push(fifo_queue_t * queue)
{
    static int next_id = 1;
    node_item_t * item = malloc(sizeof(node_item_t));
    assert(item);
    node_init(item);
    item->id = next_id++;
    printf("pushing item %d into queue\n", item->id);
    int ret = queue_push(queue, item);
    if (ret < 0)
        free(item);
    return ret;
}

int pop_and_free_node(fifo_queue_t * queue)
{
    node_item_t * item = queue_pop(queue);
    if (!item)
        return -1;
    printf("popped item %d from queue\n", item->id);
    free(item);
    return 0;
}

/* 
 * Write your own test cases here
 */
int main(int argc, const char * argv[])
{
    int ret;

    /* Example test case: ensure we cannot add above queue capacity */
    fifo_queue_t * q1 = queue_create(1);

    // Should succeed the first time
    ret = create_node_and_push(q1);
    assert(ret == 0);

    // Should fail this time
    ret = create_node_and_push(q1);
    assert(ret < 0);

    // Should succeed the first time
    ret = pop_and_free_node(q1);
    assert(ret == 0);

    // Should fail this time
    ret = pop_and_free_node(q1);
    assert(ret < 0);

    return 0;
}
