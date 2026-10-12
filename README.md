# Graph Theory

## Why graphs, here?

A protein-protein interaction network, a gene regulatory network, and genome assembly 
are all the same kind of object: a set of things (vertices) connected by relationships (edges).

Structure of the session:
1. **Representation and degree** (theory) → **Task 1**
2. **Walks, trails, paths and cycles** (theory) → **Task 2** (paper only)
3. **Connectivity and finding your way around a graph** (theory) → **Task 3**
4. **Does an Eulerian path exist?** (theory) → **Task 4**
5. **Hamiltonian paths, and why they are hard** (theory) → **Task 5** (paper only)

The paper parts of Tasks 1–5 (drawing, hand traces, classifying graphs, and the
questions that go with them) are on the printed handout. This README has the code.

Write your own code from scratch in a single file, `graphs_exercise.py`. Fork this
repository to your own GitHub account, clone your fork, and commit and push your work to
it as you go (e.g. one commit per finished task).

Reading: Compeau & Pevzner, *Bioinformatics Algorithms: An Active Learning Approach*,
2nd ed., Vol. I, Chapter 3 ("How Do We Assemble Genomes?"), sections 3.1–3.2 cover
graphs, Eulerian paths and Hamiltonian paths at the depth used here.

---

## Task 1: Representation and degree

A tiny protein-protein interaction (PPI) network: five proteins, five interactions.

```
V = {P1, P2, P3, P4, P5}
E = {{P1, P2}, {P1, P3}, {P2, P3}, {P3, P4}, {P4, P5}}
```

First do the paper part of Task 1 on the handout (degrees and the adjacency matrix of
this graph).

### Code

In code, represent a graph as an **adjacency list**:
a `dict` mapping each vertex to the list of its neighbours. Write the following three
functions.

#### `build_adjacency_list(edges, directed=False)`
- **Input:** `edges`, a list of 2-tuples of vertex names; `directed`, a bool.
- **Output:** `dict[str, list[str]]`. If `directed=False`, every edge `(u, v)` must
  appear on **both** sides: `v` in `graph[u]` *and* `u` in `graph[v]`. If
  `directed=True`, `(u, v)` appears only as `v` in `graph[u]`. Every vertex that occurs
  anywhere in `edges` must be a key of `graph`, even if its neighbour list ends up empty.
- **Hint:** this is the adjacency-list representation from the slides, a `dict` of
  lists, not a matrix. Two edges between the same pair of vertices (a multigraph) are
  simply two entries in the list.

#### `degrees(graph)`
- **Input:** `graph`, an undirected adjacency list.
- **Output:** `dict[str, int]`: the degree of every vertex of `graph`, including
  vertices with an empty neighbour list (degree 0).
- **Hint:** every undirected edge is already stored in both neighbour lists, so the
  degree of `v` can be read from `graph[v]` alone.

#### `in_out_degree(graph)`
- **Input:** `graph`, a directed adjacency list.
- **Output:** `(in_degree, out_degree)`, two `dict[str, int]`, keyed by every vertex.
- **Hint:** `out_degree[v]` is the length of `graph[v]`; `in_degree` needs one pass over
  every neighbour list in `graph`, counting how often each vertex is mentioned.
- **Self-check:** `sum(in_degree.values()) == sum(out_degree.values()) == len(edges)` —
  every directed edge contributes exactly one unit of out-degree and one unit of
  in-degree, somewhere.

*Think about it:* the in-degree sum always equals the out-degree sum. Can a directed
graph have exactly **one** vertex with deg⁻(v) ≠ deg⁺(v)? Exactly **three**? Why, or why
not?

---

## Task 3: Finding your way around a graph (depth-first search)

To check whether a graph is connected, you need to actually *walk* it, not just look at
degrees. The standard way is **depth-first search (DFS)**: start at a vertex, follow an
edge to an unvisited neighbour, and keep going as deep as possible; when you are stuck
(every neighbour is already visited), backtrack to the most recent vertex that still has
an unvisited neighbour and continue from there. The vertices you can reach this way are
exactly the vertices in the same connected component as the one you started from.

So that a hand-trace and a running program always agree, use one fixed tie-break rule
whenever a vertex has more than one unvisited neighbour: **visit them in alphabetical
(sorted) order.**

#### `dfs(graph, start)`
- **Input:** an adjacency list (undirected or directed), a `start` vertex.
- **Output:** `list[str]`, the vertices reachable from `start`, in the order you first
  visit them.
- **Ties:** when a vertex has several unvisited neighbours, visit them in **sorted**
  order — this is exactly what makes your hand-trace on the handout and your code agree, not just
  on the *set* of vertices but on the *order* too.

#### `connected_components(graph)`
- **Input:** an adjacency list.
- **Output:** `list[set[str]]`, one set per maximal connected component.
- **Hint:** repeatedly call `dfs` from any vertex that is not yet in any component you
  have found.
- **Self-check:** the components must **partition** the vertex set of the graph — their
  union is exactly `set(graph)`, and no two components share a vertex. Check this with
  set operations on your own output.

#### `is_weakly_connected(graph)`
- **Input:** a directed adjacency list.
- **Output:** `bool`, true exactly when treating every directed edge as undirected (its
  "shadow") gives a single connected component.
- **Hint:** build the undirected shadow of the graph — for every edge `u → v`, add `v` to
  `u`'s *and* `u` to `v`'s neighbour list in a fresh adjacency list — then reuse
  `connected_components` on the shadow.

---

## Task 4: Does an Eulerian path exist?

An **Eulerian circuit** uses every edge of a graph exactly once and returns to its
starting vertex; an **Eulerian path** uses every edge exactly once but may end somewhere
else.

#### `eulerian_type(graph, directed=False)`
- **Input:** an adjacency list; `directed`.
- **Output:** one of the literal strings `"circuit"`, `"path"`, `"none"`.
- **Hint:** reuse `degrees`/`in_out_degree` and
  `connected_components`/`is_weakly_connected` from Tasks 1 and 3.
  The undirected and directed rules are genuinely different — write them as two clearly
  separate branches, do not try to force them into one shared formula.
- Run it on the graphs from the
  handout: your function's verdict must agree with what you derived by hand, for **all**
  of G1, G3, G4, G5a, G5b and Königsberg. If any of them disagree, do not assume the code
  is the one that is wrong — recheck your hand reasoning too; either could be the bug.
- **Self-checks** (these must hold for *any* implementation, not just a correct one — if
  one of them fails, you have found a bug, in your code or in your by-hand reasoning):
  1. Delete any single edge from a graph your function currently calls `"circuit"`; it
     must now return `"path"` or `"none"`, **never** `"circuit"` again. Removing one
     edge can only break the even-degree condition at its two endpoints — it can never
     *fix* a connectivity problem that was not already there. Try this on every
     graph from the handout that your function calls `"circuit"`.
  2. Before calling your function, count the odd-degree vertices (undirected) or the
     excess (out − in) of every vertex (directed) yourself. If an undirected graph has
     anything other than 0 or 2 odd-degree vertices, your function must return `"none"`.
     If a directed graph has any vertex with an excess of +2, −2, or anything besides
     0/+1/−1, it must also return `"none"` — a single vertex with excess 2 makes an
     Eulerian path just as impossible as four odd-degree vertices do in the undirected
     case, even though its in+out degree *sum* can still be even.
  3. A disconnected (or, for directed graphs, not weakly connected) graph must always
     come back `"none"`, no matter what the degrees say. Test this directly on G1.
  4. For a directed graph, reverse every single edge. If the original graph was
     `"circuit"`, the reversed graph must still be `"circuit"` (in-degree and out-degree
     simply swap roles at every vertex; weak connectivity is unaffected by reversal).
     Try this on every directed graph from the handout that your function calls
     `"circuit"`.

