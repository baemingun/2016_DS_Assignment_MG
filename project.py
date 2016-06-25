import os

INFTY = 1E10

WHITE = 0
GRAY = 1
BLACK = 2
HASHNUM = 1500

class Heap:
    def __init__(self):
        self.nelem = 0
        self.A = []
    def parent(self,n):
        return (n-1)//2
    def left(self,n):
        return 2*n+1
    def right(self,n):
        return 2*n+2
    def compare(self,a,b):
        return a - b > 0
    def exchange(self,i,j):
        A = self.A
        A[i],A[j] = A[j],A[i]
    def heapify(self,i):
        A = self.A
        l = self.left(i)
        r = self.right(i)
        if l < self.nelem and self.compare(A[l], A[i]):
            largest = l
        else:
            largest = i
        if r < self.nelem and self.compare(A[r], A[largest]):
            largest = r
        if largest != i:
            self.exchange(i,largest)
            self.heapify(largest)
            
class PrioNode:
    def __init__(self, key, n):
        self.ndx = 0
        self.n = n
        self.key = key

class MaxQueue(Heap):
    def __init__(self):
        super().__init__()
    def compare(self,a,b):
        return a.key > b.key
    def exchange(self,i,j):
        A = self.A
        A[i].ndx = j
        A[j].ndx = i
        super().exchange(i,j)
    def update_key(self,i):
        parent = lambda x: self.parent(i)
        compare = lambda a,b: self.compare(a,b)
        A = self.A
        while i > 0 and not compare(A[parent(i)], A[i]):
            self.exchange(i,parent(i))
            i = parent(i)
    def increase_key(self,i,key):
        A = self.A
        if key < A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)
    def insert(self,n):
        A = self.A
        while (len(A) < self.nelem):
            A.append(None)
        i = self.nelem
        A.append(None)
        self.nelem = self.nelem + 1
        A[i] = n
        A[i].ndx = i
        self.update_key(i)
    def extract(self):
        elem = self.A[0]
        self.exchange(0,self.nelem-1)
        self.nelem = self.nelem - 1
        self.heapify(0)
        return elem
    def is_empty(self):
        return self.nelem == 0

class MinQueue(MaxQueue):
    def __init__(self):
        super().__init__()
    def compare(self,a,b):
        return a.key < b.key
    def update_key(self,i):
        parent = lambda x: self.parent(i)
        A = self.A
        while i > 0 and not self.compare(A[parent(i)], A[i]):
            self.exchange(i,parent(i))
            i = parent(i)
    def decrease_key(self,i,key):
        A = self.A
        if key > A[i].key:
            print ("Error")
            sys.exit(-1)
        A[i].key = key
        self.update_key(i)

def hash(str):
    m = 0
    i = 1
    for c in str:
        m = m + ord(c)*i
        i = i + 1
    return m % HASHNUM

class Adj:
    def __init__(self, n):
        self.n = n
        self.next = None

class Adjh():
    def __init__(self):
        self.n = []
        self.tn = []
        self.l = 0
        self.pre = None
        self.next = None
        self.content = None

class Weight(Adj):
    def __init__(self, n, w):
        super().__init__(n)
        self.w = w

class Vertex:
    def __init__(self, uid):
        self.parent = -1
        self.n = 0
        self.color = WHITE
        self.uid = uid 
        self.name = None
        self.first = None
        self.numf = 0
        self.numt = 0
        self.t = []
    def add(self, v):
        a = Adj(v.n)
        a.next = self.first
        self.first = a
        self.numf = self.numf + 1
    def copy(self, other):
        self.parent = other.parent
        self.n = other.n
        self.color = other.color
        self.uid = other.uid
        self.name = other.name
        self.first = other.first
        self.numf = other.numf

class DijkVertex(Vertex):
    def __init__(self, uid):
        super().__init__(uid)
        self.d = INFTY
        self.priority = None
    def add(self, v):
        a = Weight(v, v.numf)
        a.next = self.first
        self.first = a
    def set_priority(self,n):
        self.priority = n
    def decrease_key(self, q):
        prio = self.priority
        ndx = prio.ndx
        q.decrease_key(ndx, self.d)

class DFSVertex(Vertex):
    def __init__(self, uid):
        super().__init__(uid)
        self.d = 0
        self.f = 0
        self.scc = 0

class hnode(object):
    def __init__(self, key):
        self.key = key
        self.first = None
    def add(self, uid, content):
        e = self.exist_c(content)
        if e == None:
            a = Adjh()
            a.n.append(uid)
            a.l = 1
            a.content = content
            a.next = self.first
            self.first = a
            if a.next != None:
                a.next.pre = a
        else:
            e.n.append(uid)
            e.n.sort()
            e.l = e.l + 1
        
    def exist_c(self,content):
        p = self.first
        while p:
            if p.content == content:
                return p
            p = p.next
        return None

class rbnode(object):
    def __init__(self, key):
        self._key = key
        self._word = None
        self._point = None
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)

class Graph:
    def __init__(self):
        self.vertices = []
    def add_vertex(self,uid):
        n = len(self.vertices)
        v = Vertex(uid)
        v.n = n
        self.vertices.append(v)
        return v
    def get_vertex(self,uid):
        for v in self.vertices:
            if v.uid == uid:
                return v
        return None
    def get_vertex_name(self,name):
        for v in self.vertices:
            if v.name == name:
                return v
        return None
    def delete_vertex(self,uid):
        for v in self.vertices:
            if v.uid == uid:
                del v

class Dijkstra(Graph):
    def __init__(self):
        super().__init__()
        self.q = MinQueue()
    def add_vertex(self,uid):
        n = len(self.vertices)
        v = DijkVertex(uid)
        v.n = n
        self.vertices.append(v)
        return v
    def relax(self, u):
        vset = self.vertices
        q = self.q
        p = u.first
        while p:
            v = p.n;
            d = u.d + p.w
            if d < v.d:
                v.d = d
                v.parent = u.n
                v.decrease_key(q)
            p = p.next

    def shortest_path(self):
        q = self.q
        vset = self.vertices
        for v in vset:
            n = PrioNode(v.d, v.n)
            v.set_priority(n)
            q.insert(n)
        while not q.is_empty():
            u = q.extract()
            self.relax(vset[u.n])

class DepthFirstSearch:
    def __init__(self):
        self.time = 0;
        self.vertices = None
        self.sccs = []
    def set_vertices(self,vertices):
        self.vertices = vertices
        for i in range(len(self.vertices)):
            self.vertices[i].n = i
    def dfs(self):
        for u in self.vertices:
            u.color = WHITE
            u.parent = -1
        self.time = 0
        for u in self.vertices:
            if u.color == WHITE:
                self.dfs_visit(u)
    def dfs_visit(self, u):
        self.time = self.time + 1
        u.d = self.time
        u.color = GRAY
        v = u.first
        while v:
            if self.vertices[v.n].color == WHITE:
                self.vertices[v.n].parent = u.n
                self.dfs_visit(self.vertices[v.n])
            v = v.next;
        u.color = BLACK
        self.time = self.time + 1
        u.f = self.time

    def set_scc(self, u,n):
        c = self.sccs[n]
        c.add(u)
        c.scc = c.scc + 1
        vset = self.vertices
        while u.parent >= 0:
            u = vset[u.parent]
            c.add(u)
            c.scc = c.scc + 1
        
    def scc_find(self, u):
        u.color = GRAY
        v = u.first
        found = False
        while v:
            if self.vertices[v.n].color == WHITE:
                found = True
                self.vertices[v.n].parent = u.n
                self.scc_find(self.vertices[v.n])
            v = v.next;
        if not found:
            a = DFSVertex(u.uid)
            n = len(self.sccs)
            self.sccs.append(a)
            self.set_scc(u,n)
        u.color = BLACK
        
    def transpose(self):
        verticest = []
        for u in self.vertices:
            verticest.append(DFSVertex(u.uid))
        for u in self.vertices:
            v = u.first
            while v:
                verticest[v.n].add(u)
                v = v.next
        for u in self.vertices:
            self.vertices[u.n].first = verticest[u.n].first

    def left(self,n):
        return 2*n+1

    def right(self,n):
        return 2*n+2

    def heapify(self,A,i,heapsize):
        vset = self.vertices
        l = self.left(i)
        r = self.right(i)
        if l < heapsize and vset[A[l]].f < vset[A[i]].f:
            largest = l
        else:
            largest = i
        if r < heapsize and vset[A[r]].f < vset[A[largest]].f:
            largest = r
        if largest != i:
            A[i],A[largest] = A[largest],A[i]
            self.heapify(A,largest,heapsize)

    def buildheap(self,A):
        for i in range(len(A)//2 + 1,0,-1):
            self.heapify(A,i-1,len(A))

    def heapsort(self,A):
        self.buildheap(A)
        for i in range(len(A),1,-1):
            A[i-1],A[0] = A[0],A[i-1]
            self.heapify(A,0,i - 1)
        
    def sort_by_f(self):
        vset = self.vertices
        sorted_indices = list(range(len(vset)))
        self.heapsort(sorted_indices)
        return sorted_indices
    
    def scc(self):
        self.dfs()
        self.transpose()
        asort = self.sort_by_f()
        vset = self.vertices
        for v in vset:
            v.color = WHITE
            v.parent = -1
        for n in asort:
            if self.vertices[n].color == WHITE:
                self.scc_find(vset[n])

class rbtree(object):
    def __init__(self, create_node=rbnode):
        self._nil = create_node(key=None)
        self._root = self.nil
        self._create_node = create_node

    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")

    def search_point(self, key, content, x=None):
        if None == x:
            x = self.root
        while x != self.nil and (content != x._word or key != x.key):
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                if content < x._word:
                    x = x.left
                else:
                    x = x.right
        return x

    def minimum(self, x=None):
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x


    def maximum(self, x=None):
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def insert_key(self, key, point):
        z = self._create_node(key=key)
        self.insert_node(z, point)
        return z

    def insert_node(self, z, point):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            elif z.key > x.key:
                x = x.right
            else:
                if point.content < x._word:
                    x = x.left
                else:
                    x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        elif z.key > y.key:
            y._right = z
        else:
            if point.content < y._word:
                y._left = z
            else:
                y._right = z
        
        z._left = self.nil
        z._right = self.nil
        z._red = True
        z._point = point
        z._word = point.content
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False


    def _left_rotate(self, x):
        y = x._right
        x._right = y.left
        if y._left != self.nil:
            y._left._p = x
        y._p = x._p
        if x._p == self.nil:
            self._root = y
        elif x == x._p._left:
            x._p._left = y
        else:
            x._p._right = y
        y._left = x
        x._p = y


    def _right_rotate(self, y):
        x = y._left
        y._left = x._right
        if x._right != self.nil:
            x._right._p = y
        x._p = y._p
        if y._p == self.nil:
            self._root = x
        elif y == y._p._right:
            y._p._right = x
        else:
            y._p._left = x
        x._right = y
        y._p = x

    def transplant(self, u, v):
        if u._p == self.nil:
            self._root = v
        elif u == u._p._left:
            u._p._left = v
        else:
            u._p._right  = v
        v._p = u._p

    def _delete_fixup(self,x):
        while x != self.root and x._red == False:
            if x == x._p._left:
                w = x._p._right
                if w:
                    if w._red == True:
                        w._red = False
                        x._p._red = True
                        self._left_rotate(x._p)
                        w = x._p._right
                    if w._left._red == False and w._right._red == False:
                        w._red = True
                        x = x._p
                    else:
                        if w._right._red == False:
                            w._left._red = False
                            w._red = True
                            self._right_rotate(w)
                            w = x._p._right
                        w._red = x._p._red
                        x._p._red = False
                        w._right._red = False
                        self._left_rotate(x._p)
                        x = self.root
                else:
                    x = self.root
            else:
                w = x._p._left
                if w:
                    if w._red == True:
                        w._red = False
                        x._p._red = True
                        self._right_rotate(x._p)
                        w = x._p._left
                    if w._right._red == False and w._left._red == False:
                        w._red = True
                        x = x._p
                    else:
                        if w._left._red == False:
                            w._right._red = False
                            w._red = True
                            self._left_rotate(w)
                            w = x._p._left
                        w._red = x._p._red
                        x._p._red = False
                        w._left._red = False
                        self._right_rotate(x._p)
                        x = self.root
                else:
                    x = self.root
        x._red = False

    def delete_node(self, z):
        y = z
        yred = y._red
        x = None
        if z._left == self.nil:
            x = z._right
            self.transplant(z, z._right)
        elif z._right == self.nil:
            x = z._left
            self.transplant(z, z._left)
        else:
            y = self.minimum(z._right)
            yred = y._red
            x = y._right
            if y._p == z:
                x._p = y
            else:
                self.transplant(y, y._right)
                y._right = z._right
                y._right._p = y
            self.transplant(z, y)
            y._left = z._left
            y._left._p = y
            y._red = z.red
        if yred == False:
            self._delete_fixup(x)


    def top5(self, x, k, f = True):
        if f and x._right and k < 5:
            k = self.top5(x._right, k, True)
        if x != self.nil and k < 5:
            print("Rank",k+1,end=': ')
            print(x._word,end=' ')
            print(x.key, end=' times\n')
            k = k + 1
        if x._left and k < 5:
            k = self.top5(x._left,k, True)
        if x._p and k < 5:
            k = self.top5(x._p,k, False)
        return k

class hash_table:
    def __init__(self):
        self.sccs = []
    def insert_hash(self,n):
        for i in range(n):
            self.sccs.append(hnode(i))

def menu():
    print("0. Read data files")
    print("1. display statistics")
    print("2. Top 5 most tweeted words")
    print("3. Top 5 most tweeted users")
    print("4. Find users who tweeted a word (e.g., ’연세대’)")
    print("5. Find all people who are friends of the above users")
    print("6. Delete all mentions of a word")
    print("7. Delete all users who mentioned a word")
    print("8. Find strongly connected components")
    print("9. Find shortest path from a given user")
    print("99. Quit")
    return input("Select Menu: ")

def main():
    info = Graph()
    t = rbtree()
    d = hash_table()
    d.insert_hash(HASHNUM)

    usernum = 0
    friendnum = 0
    tweetnum = 0
    tweetuser = None # 5 uses it

    try:
        fuser = open('user.txt', 'r+')
        ffriend = open('friend.txt', 'r+')
        fword = open('word.txt', 'r+')
    except:
        print("There's no proper files!")
        exit(0)
    while True:
        num = fuser.readline()
        fuser.readline()
        name = fuser.readline()
        num = num.strip()
        name = name.strip()
        if not num or not name:
            break
        else:
            if not info.get_vertex(int(num)):
                a = info.add_vertex(int(num))
                a.name = name
                usernum = usernum + 1
            fuser.readline()
    while True:
        b = ffriend.readline()
        a = ffriend.readline()
        a = a.strip()
        b = b.strip()
        if not a or not b:
            break
        else:
            p = info.get_vertex(int(a)).first
            flag = True
            while p:
                if int(b) == info.vertices[p.n].uid:
                    flag = False
                    break
                else:
                    flag = True
                p = p.next
            if flag:
                info.get_vertex(int(a)).add(info.get_vertex(int(b)))
                friendnum = friendnum + 1
            ffriend.readline()
    while True:
        num = fword.readline()
        fword.readline()
        word = fword.readline()
        num = num.strip()
        word = word.strip()
        if not num or not word:
            break
        else:
            h = hash(word)
            s = d.sccs[h].add(int(num), word)
            it = info.get_vertex(int(num))
            it.numt = it.numt + 1
            tweetnum = tweetnum + 1
            fword.readline()
    for i in range(HASHNUM):
        p = d.sccs[i].first
        while p:
            z = t.insert_key(p.l, p)
            p.tn.append(z)
            p = p.next
    fuser.close()
    ffriend.close()
    fword.close()
    
    while True:
        os.system("cls")
        num = menu()
        if not num.isdigit():
            print("\nWrong input!\n")
            os.system("pause")
            continue
        else:
            num = int(num)
        print()
        if(num == 0):
            print("Total users:",usernum)
            print("Total friendship records:",friendnum)
            print("Total tweets:",tweetnum)

        elif(num == 1):
            avgf = 0
            minf = INFTY
            maxf = 0
            avgt = 0
            mint = INFTY
            maxt = 0
            for i in range(len(info.vertices)):
                nowf = info.vertices[i].numf
                nowt = info.vertices[i].numt
                avgf = avgf + nowf
                avgt = avgt + nowt
                if nowf > maxf:
                    maxf = nowf
                if nowf < minf:
                    minf = nowf
                if nowt > maxt:
                    maxt = nowt
                if nowt < mint:
                    mint = nowt
            avgf = avgf / usernum
            avgt = avgt / usernum
            print("Average number of friends:", avgf)
            print("Minimum friends:",minf)
            print("Maximum number of friends:",maxf)
            print()
            print("Average tweets per user:",avgt)
            print("Minimum tweets per user:",mint)
            print("Maximum tweets per user:",maxt)

        elif(num == 2):
            t.top5(t.root, 0)

        elif(num == 3):
            muser = list(info.vertices)
            def t_num(n):
                return n.numt
            muser = sorted(muser, reverse = True, key = t_num)
            for i in range(5):
                print("Rank",i+1,end=": ")
                print(muser[i].name,end=" ")
                print(muser[i].numt,end=" times\n")

        elif(num == 4):
            userin = input("tweeted a word: ")
            key = hash(userin)
            tweetuser = d.sccs[key].exist_c(userin)
            print("users who tweeted a word:",end=' ')
            if tweetuser:
                for i in range(len(tweetuser.n)):
                    s = info.get_vertex(tweetuser.n[i])
                    if s and (i == 0 or tweetuser.n[i-1] != tweetuser.n[i]):
                        print(s.name, end=' ')
            print()

        elif(num == 5):
            if tweetuser == None:
                print("user is empty!")
            else:
                for i in range(len(tweetuser.n)):
                    s = info.get_vertex(tweetuser.n[i])
                    p = s.first
                    if i == 0 or tweetuser.n[i-1] != tweetuser.n[i]:
                        print(s.name,end='')
                        print("'s friends:",end=' ')
                        while p:
                            print(info.vertices[p.n].name, end=' ')
                            p = p.next
                        print('\n')

        elif(num == 6):
            userin = input("tweeted a word: ")
            key = hash(userin)
            tword = d.sccs[key].exist_c(userin)
            if not tword:
                print("This word doesn't exist!")
            else:
                if tword.pre:
                    tword.pre.next = tword.next
                if tword.next:
                    tword.next.pre = tword.pre
                for i in range(len(tword.n)):
                    a = info.get_vertex(tword.n[i])
                    a.numt = a.numt - 1
                t.delete_node(t.search_point(tword.l, userin))
                del tword
                print("Complete!")

        elif(num == 7):
            userin = input("tweeted a word: ")
            key = hash(userin)
            userm = d.sccs[key].exist_c(userin)
            if userm:
                for i in range(len(userm.n)):
                    s = info.get_vertex(userm.n[i])
                    if s:
                        del s
            # not yet complete......

        elif(num == 8):
            DFS = DepthFirstSearch()
            vertices8 = []
            for i in range(len(info.vertices)):
                c = info.vertices[i]
                a = DFSVertex(c.uid)
                a.copy(c)
                a.first = None
                vertices8.append(a)
            DFS.set_vertices(vertices8)
            for i in range(len(info.vertices)):
                p = info.vertices[i].first
                temp = DFS.vertices[i]
                while p:
                    temp.add(DFS.vertices[p.n])
                    p = p.next
            DFS.scc()
            def scc_num(n):
                return n.scc
            DFS.sccs = sorted(DFS.sccs, reverse = True, key = scc_num)
            for i in range(5):
                v = DFS.sccs[i]
                v1 = info.get_vertex(DFS.sccs[i].uid)
                print("Rank",i+1, end='(The number of people - ')
                print(v.scc,end='): ')
                print(v1.name,end=' ')
                p = v.first
                while p:
                    print('→ ',info.vertices[p.n].name,end=' ')
                    p = p.next
                print('\n')

        elif(num == 9):
            userin = input("Start user: ")
            sc = Dijkstra()
            for i in range(len(info.vertices)):
                c = info.vertices[i]
                a = sc.add_vertex(c.uid)
                a.copy(c)
                a.first = None
            for i in range(len(info.vertices)):
                p = info.vertices[i].first
                temp = sc.vertices[i]
                while p:
                    temp.add(sc.vertices[p.n])
                    p = p.next
            v = sc.get_vertex_name(userin)
            if v:
                v.d = 0
                sc.vertices[0],sc.vertices[v.n] = sc.vertices[v.n],sc.vertices[0]
                sc.vertices[v.n].n = sc.vertices[0].n
                sc.vertices[0].n = 0
                sc.shortest_path()
                def d_num(n):
                    return n.d
                svertices = list(sorted(sc.vertices, key = d_num))
                print()
                for i in range(len(sc.vertices)-1):
                    vs = svertices[i+1]
                    if v.d < INFTY:
                        print("Rank",i+1, end=': ')
                        print(vs.name,end=' ')
                        print("Cost:",vs.d)
                        if i < 5:
                            print("Path:", vs.name,end=' ')
                            p = vs.parent
                            while p:
                                print("← ", sc.vertices[p].name,end=' ')
                                p = sc.vertices[p].parent
                            print("← ",sc.vertices[p].name)
                            print()
                    else:
                        print("After, there's no shortest path.")
                        break
            else:
                print("There's no user!")

        elif(num == 99):
            break
        else:
            print("Wrong input!")
        print()
        os.system("pause")

main()