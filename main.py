import BellmanFord
import Dijkstra
import time

# Function for printing the menu to the console
def user_menu():
    print("\n")
    print("="*50)
    print("GPS ROUTING ANALYSIS SYSTEM")
    print("=" * 50)
    print("1. Run Dijkstra Algorithm")
    print("2. Run Bellman-Ford Algorithm")
    print("3. Run Both Algorithms")
    print("4. Exit")
    print("=" * 50)
    print("\n")

# Function to make loading dots appear
def loading_dots(text, dots = 3):
    print(text, end="\n", flush=True)
    for i in range(dots):
        time.sleep(0.5)
        print(".", end="\n", flush=True)
    print("\n")

# Function to run Dijkstra's Algorithm
def run_dijkstra(start, end):
    result = Dijkstra.Dijkstra(start_node=start, end_node=end)
    if isinstance(result, str):
        print(result)
    else:
        # If it is a dictionary, print the results safely
        print(f"Time Taken: {result['time_taken_seconds']} seconds")
        print(f"Total Cost: {result['total_cost']}")
        print(f"Path: {' -> '.join(result['path_sequence'])}")
# Function to run Bellman-Ford's Algorithm
def run_bellmanford(start, end):

    # Create an instance of the BellmanFordRouting class
    bf = BellmanFord.BellmanFordRouting()

    # Load the data for the Bellman-Ford Algorithm
    try:
        bf.load_graph(r"database/roadNet-PA.txt")
    except FileNotFoundError:
        print("Error: File data not found")

    distances, predecessors = bf.find_shortest_paths(int(start), int(end))
    if distances:
        
        print(f"Distance to node {int(end)}: {distances.get(int(end), 'Unreachable')}")
        route = bf.get_route(predecessors, int(end))
        print(f"Path: {route}")

def main():

    # While loop to cycle through menu options 1 to 4
    while True:

        user_menu()
        user_option = input("Enter an option: ")

        # Provides the user with a few short pre-tested paths
        if(user_option == "1") or (user_option == "2") or (user_option == "3"):
            print("\nHere are a few short paths you may choose if desired: 7->389, 0->6354, 2->1060215")

        if user_option == "1":
            print("\nResults for Dijkstra's algorithm")
            print("=" * 50)

            try:
                source_node = input("Enter the start node: ")
                target_node = input("Enter the end node: ")
                loading_dots("Calculating route. This may take a few minutes")
                run_dijkstra(source_node, target_node)

            except ValueError:
                print("Error: Please enter a valid node")

        elif user_option == "2":
            print("\nResults for Bellman-Ford's algorithm")
            print("=" * 50)

            try:
                source_node = input("Enter the source node: ")
                target_node = input("Enter the target node: ")
                loading_dots("Calculating route. This may take a few minutes")
                run_bellmanford(source_node, target_node)

            except ValueError:
                print("Error: Please enter a valid node")

        elif user_option == "3":
            print("Results for Both Algorithms")
            print("=" * 50)

            try:
                source_node = input("Enter the start node: ")
                target_node = input("Enter the end node: ")
                loading_dots("Calculating route. This may take a few minutes")

                print("\nResults for Dijkstra's algorithm")
                print("=" * 50)
                run_dijkstra(source_node, target_node)

                print("\nResults for Bellman-Ford's algorithm")
                print("=" * 50)
                run_bellmanford(source_node, target_node)

            except ValueError:
                print("Error: Please enter a valid node")

        elif user_option == "4":
            print("\nThank you for using our system.")
            break

        else:
            print("\nYou entered an invalid option. Please try again.")
            continue

if __name__ == '__main__':
    main()
