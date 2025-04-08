Here's a complete implementation of Dijkstra's Algorithm in Java that calculates the shortest paths between vertices in a graph with weights on its edges. The code is divided into multiple parts for better understanding:

1. Define the necessary classes:

```java
import java.util.*;

class Edge {
    int weight;
    int to;

    public Edge(int w, int t) {
        this.weight = w;
        this.to = t;
    }
}

class Vertex implements Comparable<Vertex> {
    int id;
    int dist;
    boolean visited;
    List<Edge> adj; // adjacency list

    public Vertex(int id) {
        this.id = id;
        this.dist = Integer.MAX_VALUE;
        this.visited = false;
        this.adj = new ArrayList<>();
    }

    @Override
    public int compareTo(Vertex o) {
        return this.dist - o.dist;
    }
}
```

2. Implement Dijkstra's Algorithm:

```java
public class Dijkstra {

    private static void dijkstra(List<List<Edge>> graph, int src) {
        Vertex[] v = new Vertex[graph.size()];

        for (int i = 0; i < graph.size(); ++i) {
            v[i] = new Vertex(i);
        }

        Queue<Vertex> q = new PriorityQueue<>(Comparator.comparingInt(v -> v.dist));
        q.addAll(Arrays.asList(v));

        while (!q.isEmpty()) {
            Vertex u = q.poll();

            if (u.visited) continue;
            u.visited = true;

            for (Edge e : u.adj) {
                int w = e.weight;
                int v_id = e.to;
                Vertex v = v[v_id];

                if (u.dist + w < v.dist) {
                    v.dist = u.dist + w;
                    q.remove(v);
                    q.add(v);
                }
            }
        }
    }
}
```

3. Create a main method to test the algorithm:

```java
public class Main {

    public static void main(String[] args) {
        List<List<Edge>> graph = new ArrayList<>();

        // Add vertices and edges to the graph
        addVertexAndEdges(graph, 0, 1, 4);
        addVertexAndEdges(graph, 0, 7, 8);
        addVertexAndEdges(graph, 1, 2, 9);
        addVertexAndEdges(graph, 1, 3, 7);
        addVertexAndEdges(graph, 1, 6, 14);
        addVertexAndEdges(graph, 2, 3, 10);
        addVertexAndEdges(graph, 2, 5, 2);
        addVertexAndEdges(graph, 3, 4, 11);
        addVertexAndEdges(graph, 3, 6, 2);
        addVertexAndEdges(graph, 4, 5, 6);
        addVertexAndEdges(graph, 5, 6, 9);

        // Run Dijkstra's Algorithm and print the shortest paths from vertex 0 to all other vertices
        dijkstra(graph, 0);
        for (int i = 1; i < graph.size(); ++i) {
            System.out.println("From vertex " + i + " to vertex 0: distance = " + graph.get(i).get(0).dist);
        }
    }

    private static void addVertexAndEdges(List<List<Edge>> graph, int id1, int id2, int weight) {
        List<Edge> adjList1 = graph.getOrDefault(id1, new ArrayList<>());
        Edge edge = new Edge(weight, id2);
        adjList1.add(edge);

        List<Edge> adjList2 = graph.getOrDefault(id2, new ArrayList<>());
        adjList2.add(new Edge(weight, id1));
    }
}
```

This implementation uses an adjacency list representation of the graph and a priority queue to find the shortest paths using Dijkstra's Algorithm. The main method tests the algorithm with the following graph:

```markdown
  0 --- 4 --- 5
 /        |    | \
1        3    6   2
 \        |    | /
  7                 14
```

In this example, the shortest path from vertex 0 to all other vertices will be calculated and printed.
