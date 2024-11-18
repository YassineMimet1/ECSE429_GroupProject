import requests
import time
import json

BASE_URL = "http://localhost:4567"

# Function to create Todos
def create_todos(num_todos):
    times = []
    for i in range(num_todos):
        payload = {"title": f"Todo {i+1}", "doneStatus": False, "description": f"Description {i+1}"}
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/todos", json=payload)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Function to update Todos
def update_todos(num_todos):
    times = []
    for i in range(1, num_todos + 1):
        payload = {"title": f"Updated Todo {i}", "doneStatus": True, "description": f"Updated Description {i}"}
        start_time = time.time()
        response = requests.put(f"{BASE_URL}/todos/{i}", json=payload)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Function to delete Todos
def delete_todos(num_todos):
    times = []
    for i in range(1, num_todos + 1):
        start_time = time.time()
        response = requests.delete(f"{BASE_URL}/todos/{i}")
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Performance Test
def performance_test():
    test_sizes = [10, 20, 50, 100]  # Different numbers of objects to test
    results = []

    for size in test_sizes:
        print(f"\nTesting with {size} Todos...")

        print("Creating Todos...")
        create_times = create_todos(size)

        print("Updating Todos...")
        update_times = update_todos(size)

        print("Deleting Todos...")
        delete_times = delete_todos(size)

        results.append({
            "num_objects": size,
            "create_times": create_times,
            "update_times": update_times,
            "delete_times": delete_times
        })

    # Save results to file
    with open("todos_performance_results.json", "w") as file:
        json.dump(results, file, indent=4)
    print("\nResults saved to todos_performance_results.json")

if __name__ == "__main__":
    performance_test()
