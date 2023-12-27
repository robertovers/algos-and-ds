"""
Ukkonen's Algorithm for Fast Suffix Tree Construction

Time: O(n)
"""

from typing import List


class Node():

    def __init__(self, label: int = -1) -> None:
        self.label = label
        self.edges = []
        self.suffixLink = None

    def addEdge(self, v: 'Node', start: List[int], end: List[int]) -> None:
        self.edges.append(MutableEdge(self, v, start, end))

    def __str__(self) -> str:
        edge_strings = [str(e) for e in self.edges]
        return f"Node {self.label}, Edges: {edge_strings}"


class MutableEdge():

    def __init__(self, u: Node, v: Node, start: List[int], end: List[int]) -> None:
        self.u = u  # node from
        self.v = v  # node to
        self.start = start  # start index of substring
        self.end = end  # end index of substring

    def __str__(self) -> str:
        return f"Edge: {self.u.label} to {self.v.label}, Label: ({self.getStart()}, {self.getEnd()})"

    def split(self, at: int) -> Node:
        w = Node()
        e1 = MutableEdge(self.u, w, self.start, [at])
        e2 = MutableEdge(w, self.v, [at+1], self.end)
        self.u.edges.remove(self)
        self.u.edges.append(e1)
        w.edges.append(e2)
        return e1

    def getStart(self) -> int:
        return self.start[0]

    def getEnd(self) -> int:
        return self.end[0]


class SuffixTree():

    def __init__(self, string: str) -> None:
        self.string = string + "$"
        self.root = Node()
        self.root.suffixLink = self.root
        self.rem = (0, -1)
        self.active = self.root
        self.activeEdge = None
        self.activePos = -1
        self.prevInternal = None
        self.lastRule = None
        self.lastJ = -1
        self.globalEnd = [-1]

        self.ukkonenConstruct()

    def search(self, target: str, prev: Node = None, next: int = 0) -> List[int]:
        active = prev if prev else self.root

        for e in active.edges:
            l = next  # iterator for target
            k = e.getStart()  # iterator on edge

            # perform explicit comparisons
            while k <= e.getEnd() and l < len(target) and target[l] == self.string[k]:
                l += 1
                k += 1

            if l == len(target):  # found target
                if e.v.label == -1:
                    return self.labelsBelow(e.v)
                return [e.v.label]

            elif k > e.getEnd():  # traversed length of edge
                return self.search(target, e.v, l)

        return []

    def labelsBelow(self, node: Node) -> List[int]:
        res = []
        for e in node.edges:
            if e.v.label >= 0:
                res += [e.v.label]
            else:
                res += self.labelsBelow(e.v)
        return res

    def ukkonenConstruct(self) -> None:
        for ip1 in range(len(self.string)):  # phase i+1

            self.globalEnd[0] = ip1
            if self.lastJ >= 0:
                self.lastRule = 1

            for j in range(self.lastJ+1, ip1+1):  # extension j

                # traverse down remainder
                self.skipCount(self.rem[0], self.rem[1])

                # extend str[j...i] with str[i+1]
                self.extend(j, ip1)

                # showstopper or move to next extension
                if self.lastRule == 3:
                    break
                self.moveToNext()

            self.prevInternal = None

    def skipCount(self, start: int, end: int) -> None:
        if end < start:  # empty remainder
            self.activeEdge = None
            self.activePos = -1
            return

        for e in self.active.edges:
            remLen = end - start + 1
            edgeLen = e.getEnd() - e.getStart() + 1
            # traversed remainder
            if remLen < edgeLen and self.string[e.getStart()] == self.string[start]:
                self.activeEdge = e
                self.activePos = e.getStart() + remLen - 1
                self.rem = (e.getStart(), self.activePos)
                return
            elif self.string[e.getStart()] == self.string[start]:
                self.active = e.v
                self.rem = (self.rem[0] + (e.getEnd() -
                            e.getStart() + 1), self.rem[1])
                self.skipCount(self.rem[0], self.rem[1])

    def extend(self, j: int, ip1: int) -> None:
        next = self.activeEdge.v if self.activeEdge else self.active

        # rule 2 alternate
        if not self.activeEdge:
            found = False

            # first check outgoing edges for whether str[i+1] already exists
            for e in next.edges:
                if self.string[e.getStart()] == self.string[ip1]:
                    found = True
                    self.lastRule = 3
                    self.rem = (e.getStart(), e.getStart())
                    break

            if not found:  # otherwise, create new leaf
                next.label = -1
                self.lastRule = 4
                self.lastJ = j
                v = Node(j)
                next.addEdge(v, [ip1], self.globalEnd)

            # resolve suffix links
            if self.prevInternal:
                self.prevInternal.suffixLink = self.active
            self.prevInternal = None

        # rule 2 regular
        elif self.string[self.activePos+1] != self.string[ip1]:
            self.lastRule = 2
            self.lastJ = j
            v = Node(j)
            e1 = self.activeEdge.split(self.activePos)
            e1.v.addEdge(v, [ip1], self.globalEnd)

            # resolve suffix links
            if self.prevInternal:
                self.prevInternal.suffixLink = e1.v
            self.prevInternal = e1.v
            self.active = e1.u
            self.activeEdge = e1

        # rule 3
        else:
            self.lastRule = 3
            # resolve suffix links and remainder
            self.rem = (self.rem[0], self.rem[1] + 1)
            if self.prevInternal:
                self.prevInternal.suffixLink = self.active

    def moveToNext(self) -> None:
        if self.active == self.root and self.rem[1] - self.rem[0] >= 0:
            if self.rem[1] - self.rem[0] == 0:  # removing the only char
                self.rem = (self.rem[0], self.rem[1] - 1)
            else:  # remove char from front of remainder
                self.rem = (self.rem[0]+1, self.rem[1])
        elif self.active.suffixLink:
            self.active = self.active.suffixLink
