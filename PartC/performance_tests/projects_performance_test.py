import requests
import time
import json
import psutil
from threading import Thread

BASE_URL = "http://localhost:4567"

system_metrics = []

def monitor_resources(interval=0.5):
    """Continuously monitor CPU and memory usage."""
    global system_metrics
    while True:
        system_metrics.append({
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent
        })
        time.sleep(interval)

def create_projects(num):
    start_time = time.time()
    for i in range(num):
        payload = {
            "title": f"Project {i+1}",
            "description": f"Description {i+1}",
            "completed": False,
            "active": True
        }
        requests.post(f"{BASE_URL}/projects", json=payload)
    return time.time() - start_time

def update_projects(num):
    start_time = time.time()
    for i in range(1, num + 1):
        payload = {
            "title": f"Updated Project {i}",
            "description": f"Updated Description {i}",
            "completed": True,
            "active": False
        }
        requests.put(f"{BASE_URL}/projects/{i}", json=payload)
    return time.time() - start_time

def delete_projects(num):
    start_time = time.time()
    for i in range(1, num + 1):
        requests.delete(f"{BASE_URL}/projects/{i}")
    return time.time() - start_time

def performance_test():
    global system_metrics
    test_sizes = [10, 100, 500, 1000]
    results = []

    for size in test_sizes:
        system_metrics = []

        monitor_thread = Thread(target=monitor_resources)
        monitor_thread.daemon = True 
        monitor_thread.start()

        create_time = create_projects(size)
        update_time = update_projects(size)
        delete_time = delete_projects(size)

        time.sleep(1)

        peak_cpu_percent = max([m["cpu_percent"] for m in system_metrics])
        peak_memory_percent = max([m["memory_percent"] for m in system_metrics])

        results.append({
            "num_objects": size,
            "create_time": create_time,
            "update_time": update_time,
            "delete_time": delete_time,
            "peak_cpu_percent": peak_cpu_percent,
            "peak_memory_percent": peak_memory_percent
        })

        time.sleep(5)  # Delay between tests for system stabilization

    with open("projects_performance_results.json", "w") as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    performance_test()
