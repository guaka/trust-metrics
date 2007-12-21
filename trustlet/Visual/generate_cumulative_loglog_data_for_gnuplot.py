
import Advogato

A = Advogato.Advogato()

deghistI = [len(A.in_edges(x)) for x in A.nodes_iter()]
deghistO = [len(A.out_edges(x)) for x in A.nodes_iter()]

thingI = map(lambda n: (n, deghistI.count(n)),range(0, 1000))
thingO = map(lambda n: (n, deghistO.count(n)),range(0, 1000))

cumsumI = [(i, sum(map(lambda x: x[1], thingI[i:]))) for i, dummy in thingI]
cumsumO = [(i, sum(map(lambda x: x[1], thingO[i:]))) for i, dummy in thingO]

f_out = open("deg_out.data", 'w')
f_in = open("deg_in.data", 'w')
for a,b in cumsumI:
    f_in.write("%i %i\n" % (a+1, b))
for a,b in cumsumO:
    f_out.write("%i %i\n" % (a+1, b))
f_out.close()
f_in.close()

