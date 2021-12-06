
CFLAGS = -I/usr/include/gsl
LDFLAGS = -lgsl -lgslcblas -lm
CC=gcc

%:	%.c
	$(CC) $(CFLAGS) $(LDFLAGS) $< -o $@
