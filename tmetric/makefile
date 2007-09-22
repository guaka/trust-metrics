CFLAGS=-O3 -Wall `glib-config --cflags`
LDLIBS=`glib-config --libs`

all: tmetric

tmetric:	main.o net_flow.o page_rank.o
	$(CC) $(LDLIBS) $^ -o $@

clean:
	rm -f *.o *~ tmetric