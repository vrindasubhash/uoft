#ifndef _INTERRUPT_H_
#define _INTERRUPT_H_

#include <stdbool.h>

/*
 * placeholder for ppremptive thread assignment
 */

#define interrupt_off() (false)
#define interrupt_on() (false)
#define interrupt_set(enable) (void)(enable)
#define interrupt_enabled() (false)
#define interrupt_init(preemptive) (void)(preemptive)
#define interrupt_end() 

#endif
