import requests
import time
import json

BASE_URL = "http://localhost:4567"

# Function to create Projects
def create_projects(num_projects):
    times = []
    for i in range(num_projects):
        payload = {
            "title": f"Project {i+1}",
            "description": f"Description {i+1}",
            "completed": False,
            "active": True
        }
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/projects", json=payload)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Function to update Projects
def update_projects(num_projects):
    times = []
    for i in range(1, num_projects + 1):
        payload = {
            "title": f"Updated Project {i}",
            "description": f"Updated Description {i}",
            "completed": True,
            "active": False
        }
        start_time = time.time()
        response = requests.put(f"{BASE_URL}/projects/{i}", json=payload)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Function to delete Projects
def delete_projects(num_projects):
    times = []
    for i in range(1, num_projects + 1):
        start_time = time.time()
        response = requests.delete(f"{BASE_URL}/projects/{i}")
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Performance Test
def performance_test():
    test_sizes = [10, 20, 50, 100]
    results = []

    for size in test_sizes:
        print(f"\nTesting with {size} Projects...")

        print("Creating Projects...")
        create_times = create_projects(size)

        print("Updating Projects...")
        update_times = update_projects(size)

        print("Deleting Projects...")
        delete_times = delete_projects(size)

        results.append({
            "num_objects": size,
            "create_times": create_times,
            "update_times": update_times,
            "delete_times": delete_times
        })

    # Save results to file
    with open("projects_performance_results.json", "w") as file:
        json.dump(results, file, indent=4)
    print("\nResults saved to projects_performance_results.json")

if __name__ == "__main__":
    performance_test()
