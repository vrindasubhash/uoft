# 
# Makefile for user-level threading library
#
# Author: Kuei Sun, Angela Demke Brown, Ashvin Goel
# E-mail: kuei.sun@mail.utoronto.ca
#
# University of Toronto, 2023
#

# debug or release
CONF := debug
CFLAGS := -Wall -Wextra -Werror -D_GNU_SOURCE

ifeq ($(CONF),debug)
CFLAGS   += -g -O0 -ggdb
else ifeq ($(CONF),release)
CFLAGS   += -O3
else
$(error CONF must be either debug or release)
endif

TARFILE := $(notdir $(shell pwd)).tar
TESTSRC := $(wildcard test/*.c)
SOURCES := $(wildcard *.c)
OBJECTS := $(SOURCES:.c=.o)
TARGET := main
DEPEND := .depend

# Make sure that 'all' is the first target
all: $(DEPEND) $(TARGET)

zip: realclean
	tar cvf $(TARFILE) *.c *.h Makefile

clean:
	rm -rf *.stackdump *.o *.d $(TARGET) $(DEPEND) *.exe

realclean: clean
	rm -rf *~ *.log *.out *.tar

$(DEPEND):
	$(CC) -MM *.c > $(DEPEND)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

main.o: CFLAGS:=$(CFLAGS) -Wno-cast-function-type -Wno-deprecated-declarations

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^

ifeq ($(DEPEND),$(wildcard $(DEPEND)))
include $(DEPEND)
endif
