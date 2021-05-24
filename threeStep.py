import re
import networkx as nx
import operator
import tweets
import random
import copy

# ░█████╗░  ██╗░░░██╗  ████████╗  ░░░  ░█████╗░░█████╗░  ░░░██╗  ██████╗░
# ██╔══██╗  ██║░░░██║  ╚══██╔══╝  ░░░  ██╔══██╗██╔══██╗  ░░░██║  ██╔══██╗
# ███████║  ██║░░░██║  ░░░██║░░░  ░░░  ███████║██║░░╚═╝  ░░░██║  ██████╔╝
# ██╔══██║  ██║░░░██║  ░░░██║░░░  ░░░  ██╔══██║██║░░██╗  ░░░██║  ██╔══██╗
# ██║░░██║  ╚██████╔╝  ░░░██║░░░  ██╗  ██║░░██║╚█████╔╝  ██╗██║  ██║░░██║
# ╚═╝░░╚═╝  ░╚═════╝░  ░░░╚═╝░░░  ╚═╝  ╚═╝░░╚═╝░╚════╝░  ╚═╝╚═╝  ╚═╝░░╚═╝
#
#
# ██╗░░██╗  ░█████╗░  ██████╗░  ██╗  ██████╗░  ██╗
# ██║░██╔╝  ██╔══██╗  ██╔══██╗  ██║  ██╔══██╗  ██║
# █████═╝░  ███████║  ██████╦╝  ██║  ██████╔╝  ██║
# ██╔═██╗░  ██╔══██║  ██╔══██╗  ██║  ██╔══██╗  ██║
# ██║░╚██╗  ██║░░██║  ██████╦╝  ██║  ██║░░██║  ██║
# ╚═╝░░╚═╝  ╚═╝░░╚═╝  ╚═════╝░  ╚═╝  ╚═╝░░╚═╝  ╚═╝
#
#
# ░██████╗  ░█████╗░  ██╗░░░░░███████╗  ██╗  ███╗░░░███╗░█████╗░███╗░░██╗  ██╗
# ██╔════╝  ██╔══██╗  ██║░░░░░██╔════╝  ██║  ████╗░████║██╔══██╗████╗░██║  ██║
# ╚█████╗░  ██║░░██║  ██║░░░░░█████╗░░  ██║  ██╔████╔██║███████║██╔██╗██║  ██║
# ░╚═══██╗  ██║░░██║  ██║░░░░░██╔══╝░░  ██║  ██║╚██╔╝██║██╔══██║██║╚████║  ██║
# ██████╔╝  ╚█████╔╝  ███████╗███████╗  ██║  ██║░╚═╝░██║██║░░██║██║░╚███║  ██║
# ╚═════╝░  ░╚════╝░  ╚══════╝╚══════╝  ╚═╝  ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝  ╚═╝

def common(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return a_set & b_set
    else:
        return {}

def sim(u, v):
    a = [n for n in G[u]]
    b = [n for n in G[v]]
    c = len(common(a, b))
    d = G.degree[u]
    f = G.degree[v]
    similarity = (2*c)/(f+d)
    return similarity

def delta(u, v):
    o = list()
    o.clear()
    p = list()
    p.clear()
    for i in DC:
        for j in DC[i]:
            if j == u:
                o = DC[i]
            if j == v:
                p = DC[i]
            if len(o) != 0 and len(p) != 0:
                if p == o:
                    return 1
                else:
                    return 0

def calcQ():
    q = 0
    sumq = 0
    for i in sd:
        for j in sd:
            u = i[0]
            v = j[0]
            if delta(i, j):
                if nx.has_path(G, u, v):
                    sumq = sumq + (1 - ((G.degree[u] * G.degree[v]) / (2 * m)))
                else:
                    sumq = sumq - ((G.degree[u] * G.degree[v]) / (2 * m))
            else:
                sumq = sumq + 0

    q = (1 / (2 * m)) * (sumq)
    return q

def merge(u, v):
    # u , v are communities which we are going to merge them
    h = DC[u] + DC[v]
    del DC[u]
    del DC[v]
    DC[u] = h

                                                        #  𝙂𝙧𝙖𝙥𝙝 𝘾𝙤𝙣𝙨𝙩𝙧𝙪𝙘𝙩𝙞𝙤𝙣


hashtags = list()
k = 0
for i in tweets.twts:  #peyda kardane hashtag ha tooye tweet ha
    s = re.findall(r"#(\w+)", tweets.twts[k])
    if len(s) >= 1:
        hashtags.append(s)
    k = k+1
print("Array of Hashtags:", hashtags)

h = dict()
for i in hashtags:  # hashtag haro tooye yek Dictionary zakhire mikonim ta betoonim tedade har kodoom az oonharo ham be invane value oon hashtag dashte bashim
    for j in i:
        if j in h:
            h[j] = h[j] + len(i) - 1
        else:
            h[j] = len(i) - 1
print("Hashtags (Nodes/variable h):", h)

G = nx.Graph()
n = 1
for i in h:  #be ezaye har hashtag ye node mizarim
    G.add_node(i)
    n = n+1
print("Number of nodes:", G.number_of_nodes())

for i in hashtags:  #edge haro be graph ezafe konim
    for j in i:     #be ezaye har node ba hame node haye dige baresi mikonim bebinim edge bezarim ya na
        for k in i:
            if (j in i) and (k in i) and not(G.has_edge(j, k)) and (j != k):
                G.add_edge(j, k)
for i in h.keys():
    h[i] = G.degree(i)

print("Hashtags (Nodes):", h)
print("Hashtags Co-occurrence (Edges):", G.edges)


                                                    # 𝙀𝙣𝙙 𝙤𝙛 𝙂𝙧𝙖𝙥𝙝 𝘾𝙤𝙣𝙨𝙩𝙧𝙪𝙘𝙩𝙞𝙤𝙣
                                                    # 𝙁𝙞𝙧𝙨𝙩 𝙨𝙩𝙖𝙜𝙚 𝙤𝙛 𝙖𝙡𝙜𝙤𝙧𝙞𝙩𝙝𝙢: 𝘾𝙚𝙣𝙩𝙧𝙖𝙡 𝙣𝙤𝙙𝙚𝙨 𝙞𝙙𝙚𝙣𝙩𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣


sd = h   # sd=Sorted Degrees // mikhaym node haro bar asase degree sort konim va berizim too sd
sd = sorted(h.items(), key=operator.itemgetter(1), reverse=True) # alan sd hamoon ranking hast, yani tartibe rank ha in sheklie alan: sd[0], sd[1], sd[2]
print("Sorted Degrees:", sd)

# sumpl: sum of path lengths: baraye mohasebe D nyaz darimesh
p = 0
sumpl = 0
distance = list()
for i in G.nodes:
    for j in G.nodes:
        if i != j:
            try:
                p = nx.shortest_path_length(G, source=i, target=j, weight=None, method='dijkstra')
                p = p+1
                sumpl = sumpl + p
                distance.append([i, j, p])
            except nx.NetworkXNoPath:
                zxcv = 1
n = G.number_of_nodes()
D = (1/(n*(n-1)))*sumpl

print("Average path length:", D)

C_0 = list()            # C_0: initial central nodes set
C_0.append(sd[0])       # dar ebteda node ba bishtarin rank ro mizarim too C_0 tebghe algorithm

for i in sd:
    for j in C_0:
        try:
            q = nx.shortest_path_length(G, source=i[0], target=j[0], weight=None, method='dijkstra')
            if (q > D) and (i not in C_0):
                C_0.append(i)
        except nx.NetworkXNoPath:
            j = 0
print("Central nodes:", C_0)


                                            # 𝙀𝙣𝙙 𝙤𝙛 𝙛𝙞𝙧𝙨𝙩 𝙨𝙩𝙖𝙜𝙚
                                            # 𝙏𝙝𝙚 𝙨𝙚𝙘𝙤𝙣𝙙 𝙨𝙩𝙖𝙜𝙚: 𝙇𝙖𝙗𝙚𝙡 𝙥𝙧𝙤𝙥𝙖𝙜𝙖𝙩𝙞𝙤𝙣


#farz mikonim k (ke K tedade central node ha hast) ta community darim pas ye majmooe aghazin baraye community ha dar nazar migirim
C = list()
NL = dict() #neighbor list // mikhaym bebinim az beyne hamsaye haye azaye majmooe C_0 kodoomeshoon sim bishtari ba azaye in majmooe daran.

for i in C_0:
    l = [n for n in G[i[0]]]   #hameye hamsaye haye ozve i az majmooe C_0
    for q in l:
        if (q, G.degree(q)) not in C_0:
            NL[q] = G.degree(q)


#SNL: sorted neighbor list
SNL = sorted(NL.items(), key=operator.itemgetter(1), reverse=True)

maxarray = list()
b = list()
for i in SNL:
    f = 0
    if i not in C_0:    #kesaei ke tooye C_0 nistan ro bayad taklifeshoon ro moshakhas konim ke bayad che rangi beshe (too che community gharar migiran)
        maximum = 0
        lastversion = 0
        # print("az inja baraye i=", i)
        for j in C_0:
            b.clear()
            b = [item for item in maxarray if item[0] == i[0]]
            if len(b) != 0:     # in khat yani age ghablan ye tuple ei too maxarray dashtim ke khoone avalesh i[0] bood
                if sim(i[0], j[0]) > lastversion:
                    lastversion = sim(i[0], j[0])
                    v = (i[0], j[0], lastversion)
                    maxarray[f-1] = v  # baraye har i miaeem ye tuple tooye array maxarray mizarim be hamrah oon kesi ke bishtarin similarity ro bahash dare ta badan berim oon rangish kon
                    b.clear()
                elif sim(i[0], j[0]) == lastversion and len(b) != 0 and lastversion != 0:
                    xc = b[0]
                    r = random.choice([j[0], xc[1]])
                    # print("last version is:", lastversion, "sim", sim(i[0], j[0]))
                    # print("our choices are", j[0], sim(i[0], j[0]), "and", xc[1], sim(i[0], xc[1]), "and we choose", r)
                    v = (i[0], r, lastversion)
                    maxarray[f-1] = v
                    b.clear()
            else:
                lastversion = sim(i[0], j[0])
                v = (i[0], j[0], lastversion)
                if lastversion != 0:
                    maxarray.append(v)
                b.clear()
        f = f+1

print("Maxarray", maxarray)

for i in C_0:                       #C ro be soorate listi az list ha dar miarim ke har kodoom az list haye darooni bayangare yek community (color) hastan
    v = [i]
    C.append(v)
print("Initial Community set/list C", C)

for i in maxarray:
    for j in C:
        if (i[1], G.degree(i[1])) in j:
            v = (i[0], G.degree(i[0]))
            j.append(v)
        break
print("Filled Community set/list C", C)

DC = dict()
g = 1
for i in C:     #Dictionary format of the community set
    DC[g] =i
    g = g+1
print("Dictionary form of C", DC)                                                            # 𝙀𝙣𝙙 𝙤𝙛 𝙨𝙚𝙘𝙤𝙣𝙙 𝙨𝙩𝙖𝙜𝙚


                                                            # 𝙏𝙝𝙚 𝙩𝙝𝙞𝙧𝙙 𝙨𝙩𝙖𝙜𝙚: 𝘾𝙤𝙢𝙢𝙪𝙣𝙞𝙩𝙮 𝙘𝙤𝙢𝙗𝙞𝙣𝙖𝙩𝙞𝙤𝙣


# mohasebe "m"
for i in G.nodes:
    m = 0.5*G.degree[i]

# Mohasebeye Q

Q0 = calcQ()
print(Q0)
backup_DC = dict(DC)
CDC = dict(DC)
ld = len(DC)
deltaQ_matrix = [[0 for x in range(ld)] for y in range(ld)]
for i in CDC:
    # print("this is i in DC", i)
    for j in CDC:
        if i != j:
            merge(i, j)
            # print("new DC", DC)
            Q = calcQ()
            # print("Q", Q)
            deltaQ_matrix[i-1][j-1] = Q - Q0
            DC.clear()
            # print("is backup exploded?", backup_DC)
            DC = dict(backup_DC)
            # print("Backup reloaded")
            # print("DC at the end is now:", DC)
        else:
            deltaQ_matrix[i-1][j-1] = 0

while(Q > Q0):
    for i in CDC:
        for j in CDC:
            if i != j:
                merge(i, j)
                Q = calcQ()

print(deltaQ_matrix)
aaa = list()
maxC = 0
for i in deltaQ_matrix:
    print(i)
    for j in i:
        if j > maxC:
            msxC = j
            if j>0:
                s = i








