import time

class MinHeap:
    #Min-Heap Priority Queue.
    def __init__(self):
        self.heap = []
        self.pos = {} 

    def is_empty(self):
        return len(self.heap) == 0

    def push(self, node, dist):
        self.heap.append([dist, node])
        self.pos[node] = len(self.heap) - 1
        self._up(len(self.heap) - 1)

    def pop(self):
        if self.is_empty():
            return None
        min = self.heap[0]
        last = self.heap.pop()
        
        if not self.is_empty():
            self.heap[0] = last
            self.pos[last[1]] = 0
            self._down(0)
            
        del self.pos[min[1]]
        return min


    def contains(self, node):
        return node in self.pos
    
    def update(self, node, dist):
        if node in self.pos:
            id = self.pos[node]
            if dist < self.heap[id][0]:
                self.heap[id][0] = dist
                self._up(id)

    def _up(self, id):
        parent_id = (id - 1) // 2
        while id > 0 and self.heap[id][0] < self.heap[parent_id][0]:
            self._swap(id, parent_id)
            id = parent_id
            parent_id = (id - 1) // 2

    def _down(self, id):
        n = len(self.heap)
        while True:
            left = 2 * id + 1
            right = 2 * id + 2
            smallest = id

            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest != id:
                self._swap(id, smallest)
                id = smallest
            else:
                break

    def _swap(self, i, j):
        self.pos[self.heap[i][1]] = j
        self.pos[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


def load_graph_data(filepath):
    #Helper function to load the graph from a text file into memory.
    print(f"Loading graph from {filepath}...")
    graph = {}
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                u, v = parts[0], parts[1]
                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []
                graph[u].append((v, 1))
    return graph


def Dijkstra(start_node, end_node, filepath="roadNet-PA.txt"):

    # 1. Load the graph
    try:
        graph = load_graph_data(filepath)
    except FileNotFoundError:
        return "Error: Dataset not found"

    if start_node not in graph:
        return "Start node do not exist in the dataset."
    
    if end_node not in graph:
        return "End node do not exist in the dataset."

    # start timer after loading data
    start_time = time.time()
    
    # 2. Set up Dijkstra's dependencies
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph}
    
    # 3. Start MinHeap
    pq = MinHeap()
    pq.push(start_node, 0)
    
    # 4. Run the search
    while not pq.is_empty():
        current_dist, current_node = pq.pop()
        
        if current_node == end_node:
            break
        if current_dist == float('inf'):
            break
        if current_dist > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                
                if pq.contains(neighbor):
                    pq.update(neighbor, distance)
                else:
                    pq.push(neighbor, distance)

    #end time when final destination has been reached           
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # 5. Reconstruct the path
    path = []
    curr = end_node
    while curr is not None and distances.get(curr) != float('inf'):
        path.append(curr)
        if curr == start_node:
            break
        curr = previous_nodes.get(curr)
    
    path.reverse()
    
    # 6. Return the final formatted results
    if len(path) > 0 and path[0] == start_node:
        return {
            "time_taken_seconds": round(elapsed_time, 6),
            "total_cost": distances[end_node],
            "path_sequence": path
        }
    else:
        return {
            "time_taken_seconds": round(elapsed_time, 6),
            "total_cost": float('inf'),
            "path_sequence": []
        }


# EXAMPLE USAGE

if __name__ == "__main__":
    
    result = Dijkstra(start_node="0", end_node="6354")
    
    print(f"\n--- Results for Dijkstra's algorithm ---")
    print(f"Time Taken: {result['time_taken_seconds']} seconds")
    print(f"Total Cost: {result['total_cost']}")
    print(f"Path: {' -> '.join(result['path_sequence'])}")
    