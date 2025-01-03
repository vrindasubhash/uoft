#ifndef _TEST_H_

#include "../ut369.h"
#include "../queue.h"
#include <sys/time.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <malloc.h>
#include <stdio.h>

static inline int
thread_ret_ok(Tid ret)
{
	return (ret >= 0 ? 1 : 0);
}

#endif /* _TEST_H_ */