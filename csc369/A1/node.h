/*
 * node.h
 *
 * Definition of your node structure. 
 *
 * You should update this file to complete the assignment.
 *
 */
 
#ifndef _NODE_H_
#define _NODE_H_


// forward declaration of queue structure
struct _fifo_queue; 
 
typedef struct _node_item {
    
    /*
     * must have for each item. do not remove.
     */
    int id;
    
    /*
     * Pointer to the next node
     */
     struct _node_item* next;

    /*
     * Flag to check if a node is already in the queue
     */
     int in_queue; // 1 if yes, 0 if no 

    
} node_item_t;


#endif /* _NODE_H_ */
