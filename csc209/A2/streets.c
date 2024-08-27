#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>
#include <float.h>
#include "streets.h"


#define SAFE_DELETE(p) if (p != NULL) free(p)
#define BUFFER_BLOCK_SIZE 10

struct node {
    double lat;
    double lon;
    int num_ways;
    int *p_way_ids;
};

struct way {
    char *p_name;
    double speed_limit;
    bool is_oneway;
    int num_nodes;
    int *p_node_ids; // node ids are ordered. If oneway, use order of ids to figure out which way.
};

struct ssmap {
    int num_nodes;
    struct node *p_nodes;
    int num_ways;
    struct way *p_ways;
};

struct ssmap *
ssmap_create(int nr_nodes, int nr_ways)
{
    if ((nr_nodes == 0) || (nr_ways == 0))
        return NULL;

    // Nodes and Ways will be an array of structs.
    // Assumption/Observation: ids start at 0 and are contigous.
    struct node *p_nodes = NULL;
    struct way *p_ways = NULL;
    struct ssmap *p_ssmap = NULL;
    p_nodes = malloc(sizeof(struct node) * nr_nodes);
    p_ways = malloc(sizeof(struct way) * nr_ways);
    p_ssmap = malloc(sizeof(struct ssmap));
    if ((p_nodes == NULL) || (p_ways == NULL) || (p_ssmap == NULL)) {
        goto error_exit;
    }
    p_ssmap->num_nodes = nr_nodes;
    p_ssmap->p_nodes = p_nodes;
    p_ssmap->num_ways = nr_ways;
    p_ssmap->p_ways = p_ways;
    memset(p_nodes, 0, (sizeof(struct node) * nr_nodes));
    memset(p_ways, 0, (sizeof(struct way) * nr_ways));
    return p_ssmap;

error_exit:
    SAFE_DELETE(p_nodes);
    SAFE_DELETE(p_ways);
    SAFE_DELETE(p_ssmap);

    return NULL;
}

bool
ssmap_initialize(struct ssmap * m)
{
    return true;
}

void
ssmap_destroy(struct ssmap * m)
{
    if (m != NULL) {
        if (m->p_nodes != NULL) {
            for (int i = 0; i < m->num_nodes; i++) {
                SAFE_DELETE(m->p_nodes[i].p_way_ids);
            }
            free(m->p_nodes);
        }
        if (m->p_ways != NULL) {
            for (int i = 0; i < m->num_ways; i++) {
                SAFE_DELETE(m->p_ways[i].p_name);
                SAFE_DELETE(m->p_ways[i].p_node_ids);
            }
            free(m->p_ways);
        }
        free(m);
    }
}

struct way *
ssmap_add_way(struct ssmap * m, int id, const char * name, float maxspeed, bool oneway,
              int num_nodes, const int node_ids[num_nodes])
{
    struct way *p_way = &(m->p_ways[id]);
    p_way->p_name = malloc(strlen(name) + 1);
    if (p_way->p_name == NULL)
        return NULL;
    strcpy(p_way->p_name, name);
    p_way->speed_limit = maxspeed;
    p_way->is_oneway = oneway;
    p_way->num_nodes = num_nodes;
    p_way->p_node_ids = malloc(sizeof(int) * num_nodes);
    if (p_way->p_node_ids == NULL)
        return NULL;
    memcpy(p_way->p_node_ids, node_ids, (sizeof(int) * num_nodes));

    return p_way;
}


struct node *
ssmap_add_node(struct ssmap * m, int id, double lat, double lon,
               int num_ways, const int way_ids[num_ways])
{
    struct node *p_node = &(m->p_nodes[id]);
    p_node->lat = lat;
    p_node->lon = lon;
    p_node->num_ways = num_ways;
    p_node->p_way_ids = malloc(sizeof(int) * num_ways);
    if (p_node->p_way_ids == NULL)
       return NULL;
    memcpy(p_node->p_way_ids, way_ids, (sizeof(int) * num_ways));

    return p_node;
}

void
ssmap_print_way(const struct ssmap * m, int id)
{
    if ((id < 0) || (id >= m->num_ways))
        printf("error: way %d does not exist.\n", id);
    else
        printf("Way %d: %s\n", id, m->p_ways[id].p_name);
}

void
ssmap_print_node(const struct ssmap * m, int id)
{
    if ((id < 0) || (id >= m->num_nodes))
        printf("error: node %d does not exist.\n", id);
    else
        printf("Node %d: (%.7f, %.7f)\n", id, m->p_nodes[id].lat, m->p_nodes[id].lon);
}

// Return an array with way ids with matching name.
// Also sets num_items so calling function knows size.
// Used realloc to expand memory used as needed.
// Caller needs to free memory.
int*
way_by_name(const struct ssmap * m, const char * name, int * num_items)
{
    int *p_ids = malloc(sizeof(int) * BUFFER_BLOCK_SIZE);
    int size = BUFFER_BLOCK_SIZE; // how much memory is allocated in p_ids
    int count = 0; // how many items there are in p_ids

    for (int i = 0; i < m->num_ways; i++) {
        if (strstr(m->p_ways[i].p_name, name) != NULL) {
            if (count < size) {
                p_ids[count] = i;
            } else {
                size += BUFFER_BLOCK_SIZE;
                p_ids = realloc(p_ids, sizeof(int) * size);
                p_ids[count] = i;
            }
            ++count;
        }

    }
    *num_items = count;
    return p_ids;
}


// Print the ids in the array.
void
print_ids(const int * p, int num_items)
{
    for (int i = 0; i < num_items; i++) {
        printf("%d ", p[i]);
    }
    printf("\n");
}


void
ssmap_find_way_by_name(const struct ssmap * m, const char * name)
{
    int num_items = 0;
    int *way_ids = way_by_name(m, name, &num_items);
    print_ids(way_ids, num_items);
    free(way_ids);
}


// Used by qsort to compare two items.
// Returns negative or positive number based on value of a and b.
int
int_compare(const void * a, const void * b)
{
    return (*(int*)a - *(int*)b);
}


// Remove duplicates in place.
// Sort first and then duplicates will be nearby.
// Returns number of unique values.
int
remove_duplicates(int * ids, int count)
{
    // Easier to remove duplicates after sorting.
    qsort(ids, count, sizeof(int), int_compare);
    int last_written = -1;
    int next_write = 0;
    for (int i = 0; i < count; i++) {
        if (ids[i] != last_written) {
            last_written = ids[i];
            ids[next_write] = last_written;
            ++next_write;
        }
    }
    return next_write;
}

// Given a list of nodes, find nodes that are part of 2 ways that match name1 and name2.
// Assumption is that p_intersection has enough space and p_count has the location
// in p_intersection array where results have to be filled in.
// p_count will be incremented based on how many matches are found.
void
collect_nodes(const struct ssmap * m, const char * name1, const char * name2,
              const int * p_nodes, int n_nodes, int * p_intersection, int * p_count)
{
    for (int i = 0; i < n_nodes; i++) {
         int node_id = p_nodes[i];
         // check if node is part of both ways (name1 , name2)

         bool name1_found = false;
         bool name2_found = false;
         int num_ways = m->p_nodes[node_id].num_ways;
         for (int j = 0; j < num_ways; j++) {
             int way_id =  m->p_nodes[node_id].p_way_ids[j];
             if (!name1_found && strstr(m->p_ways[way_id].p_name, name1) != NULL)
                 name1_found = true;
             else if (!name2_found && strstr(m->p_ways[way_id].p_name, name2) != NULL)
                 name2_found = true;
         }
         if (name1_found && name2_found)
            p_intersection[(*p_count)++] = node_id;
    }
}


// Returns nodes that are part of ways name1 and name2.
// l1 and l2 are the sets of nodes of length s1 and s2.
// Sets p_count to the number of items in the new list.
// Caller is responsible for freeing the memory.
int*
find_intersection(const struct ssmap * m, const char * name1, const char * name2,
                  const int * l1, const int * l2, int s1, int s2, int *p_count)
{
    int s = (s1 + s2); // allocate the longest possible buffer
    int *p_intersection = malloc(sizeof(int) * s);
    int count = 0;

    collect_nodes(m, name1, name2, l1, s1, p_intersection, &count);
    collect_nodes(m, name1, name2, l2, s2, p_intersection, &count);
    // p_intersection could have duplicates at this point. remove them.
    count = remove_duplicates(p_intersection, count);

    *p_count = count;
    return p_intersection;
}

// Find all nodes for a given name.
// Returns a list of unique node ids sorted.
// Caller has to free the return list.
// p_count will have the number of unique ids.
int*
find_node_by_name(const struct ssmap * m, const char * name, int * p_count)
{
    int num_way_ids = 0;
    int *p_way_ids = way_by_name(m, name, &num_way_ids);

    int *p_nodes = malloc(sizeof(int) * BUFFER_BLOCK_SIZE);
    int size = BUFFER_BLOCK_SIZE; // how much memory is allocated for p_nodes
    int count = 0;  // how many items there are in p_nodes

    for (int i = 0; i < num_way_ids; i++) {
        int space_remaining = size - count;
        int space_required = m->p_ways[p_way_ids[i]].num_nodes;
        if (space_remaining < space_required) {
            // adding extra space to avoid reallocating all the time
            size = count + space_required + BUFFER_BLOCK_SIZE;
            p_nodes = realloc(p_nodes, size * sizeof(int));
        }
        memcpy(&p_nodes[count], m->p_ways[p_way_ids[i]].p_node_ids, sizeof(int) * space_required);
        count += space_required;
    }
    *p_count = remove_duplicates(p_nodes, count);
    free(p_way_ids);
    return p_nodes;
}


// Checks if the two nodes belong to one and only one way. 
bool
is_same_way(const struct ssmap * m, const char * name1, const char * name2)
{
    int n1 = 0;
    int n2 = 0;
    int *p_w1 = way_by_name(m, name1, &n1);
    int *p_w2 = way_by_name(m, name2, &n2);

    if ((n1 == 1) && (n2 == 1) && (p_w1[0] == p_w2[0])) {
       free(p_w1);
       free(p_w2);
       return true;
    }

    free(p_w1);
    free(p_w2);
    return false;
}

void
ssmap_find_node_by_names(const struct ssmap * m, const char * name1, const char * name2)
{
    int count1 = 0;
    int *p_nodes1 = find_node_by_name(m, name1, &count1);
    if (name2 == NULL) {
        print_ids(p_nodes1, count1);
        free(p_nodes1);
        return;
    }

    if (is_same_way(m, name1, name2)) {
        printf("\n");
        free(p_nodes1);
        return;
    }

    int count2 = 0;
    int *p_nodes2 = find_node_by_name(m, name2, &count2);

    int count = 0;
    int *p_nodes = find_intersection(m, name1, name2, p_nodes1, p_nodes2, count1, count2, &count);

    print_ids(p_nodes, count);

    free(p_nodes1);
    free(p_nodes2);
    free(p_nodes);
}

/**
 * Converts from degree to radian
 *
 * @param deg The angle in degrees.
 * @return the equivalent value in radian
 */
#define d2r(deg) ((deg) * M_PI/180.)

/**
 * Calculates the distance between two nodes using the Haversine formula.
 *
 * @param x The first node.
 * @param y the second node.
 * @return the distance between two nodes, in kilometre.
 */
static double
distance_between_nodes(const struct node * x, const struct node * y) {
    double R = 6371.;
    double lat1 = x->lat;
    double lon1 = x->lon;
    double lat2 = y->lat;
    double lon2 = y->lon;
    double dlat = d2r(lat2-lat1);
    double dlon = d2r(lon2-lon1);
    double a = pow(sin(dlat/2), 2) + cos(d2r(lat1)) * cos(d2r(lat2)) * pow(sin(dlon/2), 2);
    double c = 2 * atan2(sqrt(a), sqrt(1-a));
    return R * c;
}


// Returns if there is a path from a to b.
// Assumption is that a and b are on way_id.
bool
can_go_from_a_to_b(const struct ssmap * m, int way_id, int node_a, int node_b)
{
    int a_id = -1;
  
    for (int i = 0; i < m->p_ways[way_id].num_nodes; i++) {
        if (m->p_ways[way_id].p_node_ids[i] == node_a)
            a_id = i;
    }

    if (a_id == -1)
        return false;

    if ((a_id + 1 < m->p_ways[way_id].num_nodes) && 
        (m->p_ways[way_id].p_node_ids[a_id + 1] == node_b))
        return true;

    if (m->p_ways[way_id].is_oneway)
        return false;

    return ((a_id > 0) && (m->p_ways[way_id].p_node_ids[a_id - 1] == node_b));
}


// Returns the max speed between two nodes in km/hr.
double
max_speed(const struct ssmap * m, int a, int b)
{
    bool reverse_dectected = false;
    bool way_ids_matched = false;
    double max_speed = -1.0;
    int *a_ways = m->p_nodes[a].p_way_ids;
    int *b_ways = m->p_nodes[b].p_way_ids;
    int a_count = m->p_nodes[a].num_ways;
    int b_count = m->p_nodes[b].num_ways;
    for (int a_i = 0; a_i < a_count; a_i++) {
        int way_id = a_ways[a_i];
        for (int b_i = 0; b_i < b_count; b_i++) {
            int b_id = b_ways[b_i];
            if (way_id == b_id) {
               way_ids_matched = true;
               if (!can_go_from_a_to_b(m, way_id, a, b)) {
                   reverse_dectected = true;
                   continue;
               }
               if (m->p_ways[way_id].speed_limit > max_speed)
                    max_speed = m->p_ways[way_id].speed_limit;
           }
        }
    }
    if (!way_ids_matched)
       return -2.0;
    if (max_speed == -1.0 && reverse_dectected)
       return -3.0;
    return max_speed;
}

// Returns id of first duplicate, -1 otherwise.
int
find_first_duplicate(int size, const int id[size])
{
  if (size == 1)
     return -1;

  int max = -1;
  int min = INT_MAX;
  for (int i = 0; i < size; i++) {
      if (id[i] > max)
         max = id[i];
      if (id[i] < min)
         min = id[i];
  }
  // Create a set representation of all possible numbers in range(min, max).
  char *p_set = malloc(sizeof(char) * (max - min + 1));
  memset(p_set, 0, max - min + 1);
  for (int i = 0; i < size; i++) {
      if (p_set[id[i] - min] == 1) {
          free(p_set);
          return id[i];
      }
      p_set[id[i] - min] = 1;
  }
  free(p_set);
  return -1;
}

double
ssmap_path_travel_time(const struct ssmap * m, int size, int node_ids[size])
{
    if (node_ids[0] >= m->num_nodes || node_ids[0] < 0) {
        printf("error: node %d does not exist.\n", node_ids[0]);
        return -1.0;
    }
    int duplicate = find_first_duplicate(size, node_ids);
    if (duplicate != -1) {
         printf("error: node %d appeared more than once.\n", duplicate);
         return -1;
    }
    double current = 0.0; // in hours
    for (int i = 0; i < size - 1; i++) {
        // distance is in kilometers
        if (node_ids[i+1] >= m->num_nodes || node_ids[i+1] < 0) {
            printf("error: node %d does not exist.\n", node_ids[i+1]);
            return -1.0;
        }
        double distance = distance_between_nodes(&(m->p_nodes[node_ids[i]]), &(m->p_nodes[node_ids[i+1]]));
        double speed = max_speed(m, node_ids[i], node_ids[i+1]);
        if (speed == -1.0) {
           printf("error: cannot go directly from node %d to node %d.\n", node_ids[i], node_ids[i+1]);
           return -1.0;
        }
        if (speed == -2.0) {
           printf("error: there are no roads between node %d and node %d.\n", node_ids[i], node_ids[i+1]);
           return -1.0;
        }
        if (speed == -3.0) {
           printf("error: cannot go in reverse from node %d to node %d.\n", node_ids[i], node_ids[i+1]);
           return -1.0;
        }
        current += (distance / speed);
    }
    return current * 60; // to convert to the right units (hours to minutes).
}


// struct to hold information about the nodes
typedef struct{
    int from; // the best path so far
    double cost; // cost of the best path from start_id
    bool in_queue; // if the node is queued
} record;


// Returns the id of the record which still needs to be considered with the smallest cost.
// Note: this is order(n) where n is the number of nodes which is slow.
int
get_smallest_in_queue(const record * p_table, int size)
{
    double smallest = DBL_MAX;
    int id = -1;
    for (int i = 0; i < size; i++) {
        if (p_table[i].in_queue && (p_table[i].cost < smallest)) {
            smallest = p_table[i].cost;
            id = i;
        }
    }
    return id;
}


// struct to hold the information about a way
typedef struct {
    int id;
    double speed;
} idwithspeed;


// Returns all the neighboring nodes from the given node.
// Caller must free.
idwithspeed*
get_neighbors(const struct ssmap * m, int node_id, int *p_count)
{
    int *p_ways = m->p_nodes[node_id].p_way_ids;
    int num_ways = m->p_nodes[node_id].num_ways;

    // you will have at most num_ways * 2 neighbors
    idwithspeed *p_neighbors = malloc(sizeof(idwithspeed) * (num_ways * 2));
    int count = 0;
    for (int i = 0; i < num_ways; i++) {
        int way_id = p_ways[i];
        int * p_nodes = m->p_ways[way_id].p_node_ids;
        int num_nodes = m->p_ways[way_id].num_nodes;
        for (int j = 0; j < num_nodes; j++) {
            if (p_nodes[j] == node_id) {
               if (j + 1 < num_nodes) {
                   p_neighbors[count].id = p_nodes[j+1];
                   p_neighbors[count].speed = m->p_ways[way_id].speed_limit;
                   count++;
               }
               if ((j - 1 >= 0) && (!m->p_ways[way_id].is_oneway)) {
                   p_neighbors[count].id = p_nodes[j-1];
                   p_neighbors[count].speed = m->p_ways[way_id].speed_limit;
                   count++;
               }
               break;
            }
        }
    }
    *p_count = count;
    return p_neighbors;
}


#define CHECK_ID(id) if (id >= m->num_nodes) \
{ \
    printf("error: node %d does not exist.\n", id); \
    return; \
}

void
ssmap_path_create(const struct ssmap * m, int start_id, int end_id)
{
    CHECK_ID(start_id);
    CHECK_ID(end_id);

    if (start_id == end_id) {
        printf("%d\n", start_id);
        return;
    }

    int count = m->num_nodes;
    record *p_table = malloc(sizeof(record) * count);
    for (int i = 0; i < count; i++) {
        p_table[i].from = -1;
        p_table[i].cost = DBL_MAX;
        p_table[i].in_queue = false;
    }

    // Add the starting node to the table.
    p_table[start_id].cost = 0;
    p_table[start_id].in_queue = true;

    while (true) {
        // find the smallest cost item in the queue.
        int id = get_smallest_in_queue(p_table, count);
        if (id == -1) {
            break;
        }
        if (id == end_id)
            break; // working solution, however may not be optimal.
        double cost = p_table[id].cost;
        int count = 0;
        idwithspeed *p_neighbors = get_neighbors(m, id, &count);
        p_table[id].in_queue = false;
        for (int i = 0; i < count; i++) {
            int n_id = p_neighbors[i].id;
            double distance = distance_between_nodes(&m->p_nodes[id], &m->p_nodes[n_id]);
            double additional_cost = distance/p_neighbors[i].speed;
            // update the table if this cost is better.
            if (p_table[n_id].cost > cost + additional_cost) {
                p_table[n_id].cost = cost + additional_cost;
                p_table[n_id].in_queue = true;
                p_table[n_id].from = id;
            }
        }
        free(p_neighbors);
    }

    // Getting the path from end to start and then reversing it to print.
    int next_id = end_id;
    int c_id = 0;
    while (true) {
        c_id++;
        next_id = p_table[next_id].from;
        if (next_id == start_id) {
           c_id++;
           break;
        }
    }

    int *p_ids = malloc(sizeof(int) * c_id);
    next_id = end_id;
    for (int i = c_id - 1; i >= 0; i--) {
        p_ids[i] = next_id;
        next_id = p_table[next_id].from;
    }

    print_ids(p_ids, c_id);

    free(p_ids);
    free(p_table);

}
