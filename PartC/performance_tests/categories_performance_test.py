import requests
import time
import json

BASE_URL = "http://localhost:4567"

# Function to create Categories
def create_categories(num_categories):
    times = []
    for i in range(num_categories):
        payload = {"title": f"Category {i+1}", "description": f"Description {i+1}"}
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/categories", json=payload)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Function to update Categories
def update_categories(num_categories):
    times = []
    for i in range(1, num_categories + 1):
        payload = {"title": f"Updated Category {i}", "description": f"Updated Description {i}"}
        start_time = time.time()
        response = requests.put(f"{BASE_URL}/categories/{i}", json=payload)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Function to delete Categories
def delete_categories(num_categories):
    times = []
    for i in range(1, num_categories + 1):
        start_time = time.time()
        response = requests.delete(f"{BASE_URL}/categories/{i}")
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times

# Performance Test
def performance_test():
    test_sizes = [10, 20, 50, 100]
    results = []

    for size in test_sizes:
        print(f"\nTesting with {size} Categories...")

        print("Creating Categories...")
        create_times = create_categories(size)

        print("Updating Categories...")
        update_times = update_categories(size)

        print("Deleting Categories...")
        delete_times = delete_categories(size)

        results.append({
            "num_objects": size,
            "create_times": create_times,
            "update_times": update_times,
            "delete_times": delete_times
        })

    # Save results to file
    with open("categories_performance_results.json", "w") as file:
        json.dump(results, file, indent=4)
    print("\nResults saved to categories_performance_results.json")

if __name__ == "__main__":
    performance_test()
