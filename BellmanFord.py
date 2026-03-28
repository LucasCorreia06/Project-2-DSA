import time

class BellmanFordRouting:
    def __init__(self):
        self.edges = []
        self.nodes = set()

    def load_graph(self, file_path):
        """Loads the graph from the given SNAP text file."""
        print(f"Loading graph from {file_path}...")
        with open(file_path, 'r') as f:
            for line in f:
                # Skip comments at the top of the file
                if line.startswith('#'):
                    continue
                
                parts = line.strip().split()
                if len(parts) == 2:
                    u, v = int(parts[0]), int(parts[1])
                    # We assign a default weight of 1 to all edges 
                    self.edges.append((u, v, 1))
                    self.nodes.add(u)
                    self.nodes.add(v)
                    
        print(f"Graph loaded. Nodes: {len(self.nodes)}, Edges: {len(self.edges)}")

    def find_shortest_paths(self, source, target=None):
        """
        Executes the Bellman-Ford algorithm to find shortest paths from the source node
        to all other nodes in the network.
        """
        print(f"Starting Bellman-Ford algorithm from source node {source}...")
        start_time = time.time()
        
        # Initialize distances to infinity, except for the source
        dist = {node: float('inf') for node in self.nodes}
        dist[source] = 0
        
        # Predecessor dictionary to reconstruct the actual route later
        predecessor = {node: None for node in self.nodes}
        
        num_nodes = len(self.nodes)
        
        # Relax all edges |V| - 1 times
        # Time Complexity: O(V * E)
        for i in range(num_nodes - 1):
            updated = False
            target_dist_before = dist.get(target)
            for u, v, weight in self.edges:
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    predecessor[v] = u
                    updated = True
            
            # EARLY STOPPING OPTIMIZATION: 
            # If no distances were updated in an entire pass, we have found all shortest paths.
            if target is not None and dist.get(target) != float("inf"):
                print(f"Target stabilized at iteration {i + 1}")
                break
            if not updated:
                print(f"Early stopping at iteration {i + 1} (No changes detected).")
                break
                
        # Optional: Check for negative weight cycles 
        # (Not strictly necessary here since road weights are positive, but required for a complete Bellman-Ford)
        if target is None:
            for u, v, weight in self.edges:
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    print("Warning: Graph contains a negative-weight cycle.")
                    return None, None
                
        end_time = time.time()
        print(f"Bellman-Ford completed in {end_time - start_time:.4f} seconds.")
        
        return dist, predecessor

    def get_route(self, predecessor, target):
        """Reconstructs the path from the source to the target node."""
        if predecessor.get(target) is None and target not in predecessor.values():
            return "No path exists."
            
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = predecessor[curr]
            
        return path[::-1]  # Reverse the list to get Source -> Target


# === How to run this with your dataset ===
if __name__ == "__main__":
    routing = BellmanFordRouting()
    
    # Load the text file (ensure you've unzipped the .txt.gz file first)
    routing.load_graph(r"database/roadNet-PA.txt")
    
    # Find paths from Node VAR
    distances, predecessors = routing.find_shortest_paths(0, 922000)
    
    # Target a specific intersection (e.g., Node 309)
    if distances:
         target_node = 922000
         print(f"Distance to node {target_node}: {distances.get(target_node, 'Unreachable')}")
         route = routing.get_route(predecessors, target_node)
         print(f"Route: {route}")