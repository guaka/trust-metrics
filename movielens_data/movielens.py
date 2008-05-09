#!/usr/bin/env python

from trustlet.Dataset.Network import Network
from networkx import write_dot

def main():
    m = Network()

    #read users

    occupation = {
        "0":  "other",
        "1":  "academic/educator",
        "2":  "artist",
        "3":  "clerical/admin",
        "4":  "college/grad student",
        "5":  "customer service",
        "6":  "doctor/health care",
        "7":  "executive/managerial",
        "8":  "farmer",
        "9":  "homemaker",
        "10":  "K-12 student",
        "11":  "lawyer",
        "12":  "programmer",
        "13":  "retired",
        "14":  "sales/marketing",
        "15":  "scientist",
        "16":  "self-employed",
        "17":  "technician/engineer",
        "18":  "tradesman/craftsman",
        "19":  "unemployed",
        "20":  "writer",
        }

    users = {}

    for x in [(int(x[0]),x[0]+' '+x[1]+' '+x[2]+occupation[x[3]]) for x in [x.strip().split('::') for x in file('users.dat').readlines()]]:
        users[x[0]] = x[1]

    #read ratings
    # [(userid, movieid, rating)]

    ratings = [tuple(map(int,x.strip().split('::')[:-1])) for x in file('ratings.dat').readlines()]
    #print ratings

    #build graph
    m = Network()

    for u in users:
        m.add_node(users[u])

    for u in enumerate(users):
        print int(100.0 * (u[0]+1) / len(users)),"%"
        u = u[1]
        for v in users:
            if u<v:
                #this can be slow

                #list -> dict
                # (id,movie,rating) -> [movie] = rating
                
                #user u
                ur = {}
                for t in filter(lambda x: x[0] is u,ratings):
                    ur[t[1]] = t[2]
                #user v
                vr = {}
                for t in filter(lambda x: x[0] is v,ratings):
                    vr[t[1]] = t[2]

                #print u,v,len(ur),len(vr)

                uvm = [] #common movies
                for i in ur:
                    if i in vr:
                        uvm.append(i)
                if uvm:
                    #creation of egde
                    s = 0
                    for movie in uvm:
                        s += abs(ur[movie] - vr[movie])
                    if not s:
                        value = 1.0 #users u and v completly agree
                    else:
                        value = 1.0 * len(uvm) / s # 1 / avg
                        # s==0 and s==1 is the same
                
                    m.add_edge(u,v,value)
                    m.add_edge(v,u,value)
                
    write_dot(m,'graph.dot')

if __name__=="__main__":
    main()
