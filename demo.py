import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def make_test_drivers(n):
    """Generate n fake, sorted driver records for testing at this input size."""
    return [{"id": f"DRV_{i:05d}", "name": f"Driver_{i}"} for i in range(n)]


def linear_search(driver_list, target_id):
    for driver in driver_list:
        if driver["id"] == target_id:
            return driver
    return None


def binary_search(driver_list, target_id):
    low = 0
    high = len(driver_list) - 1
    while low <= high:
        middle = (low + high) // 2
        middle_id = driver_list[middle]["id"]
        if middle_id == target_id:
            return driver_list[middle]
        if middle_id < target_id:
            low = middle + 1
        else:
            high = middle - 1
    return None


def hashmap_search(driver_map, target_id):
    return driver_map.get(target_id)


input_sizes = list(range(1000, 50001, 2000))
runs = 20


def animate_linear_search():
    x_data, y_data = [], []
    fig, ax = plt.subplots(figsize=(8, 5))
    line, = ax.plot([], [], 'o-', color="#d62728", label="Linear search  O(n)")

    ax.set_xlim(0, max(input_sizes))
    ax.set_ylim(0, 1.5)
    ax.set_xlabel("Number of Drivers (N)")
    ax.set_ylabel("Average Time (ms)")
    ax.set_title("Linear Search — Time vs Input Size")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()

    def update(frame):
        n = input_sizes[frame]
        driver_list = make_test_drivers(n)
        target_id = driver_list[-1]["id"]

        start = time.perf_counter()
        for _ in range(runs):
            linear_search(driver_list, target_id)
        elapsed = ((time.perf_counter() - start) / runs) * 1000

        x_data.append(n)
        y_data.append(elapsed)
        line.set_data(x_data, y_data)
        return line,

    ani = FuncAnimation(fig, update, frames=len(input_sizes), interval=150, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()


def animate_binary_search():
    x_data, y_data = [], []
    fig, ax = plt.subplots(figsize=(8, 5))
    line, = ax.plot([], [], 's-', color="#ff7f0e", label="Binary search  O(log n)")

    ax.set_xlim(0, max(input_sizes))
    ax.set_ylim(0, 0.05)
    ax.set_xlabel("Number of Drivers (N)")
    ax.set_ylabel("Average Time (ms)")
    ax.set_title("Binary Search — Time vs Input Size")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()

    def update(frame):
        n = input_sizes[frame]
        driver_list = make_test_drivers(n)
        target_id = driver_list[-1]["id"]

        start = time.perf_counter()
        for _ in range(runs):
            binary_search(driver_list, target_id)
        elapsed = ((time.perf_counter() - start) / runs) * 1000

        x_data.append(n)
        y_data.append(elapsed)
        line.set_data(x_data, y_data)
        return line,

    ani = FuncAnimation(fig, update, frames=len(input_sizes), interval=150, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()


def animate_hashmap_search():
    x_data, y_data = [], []
    fig, ax = plt.subplots(figsize=(8, 5))
    line, = ax.plot([], [], '^-', color="#2ca02c", label="Hash map search  O(1)")

    ax.set_xlim(0, max(input_sizes))
    ax.set_ylim(0, 0.02)
    ax.set_xlabel("Number of Drivers (N)")
    ax.set_ylabel("Average Time (ms)")
    ax.set_title("Hash Map Search — Time vs Input Size")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()

    def update(frame):
        n = input_sizes[frame]
        driver_list = make_test_drivers(n)
        driver_map = {d["id"]: d for d in driver_list}
        target_id = driver_list[-1]["id"]

        start = time.perf_counter()
        for _ in range(runs):
            hashmap_search(driver_map, target_id)
        elapsed = ((time.perf_counter() - start) / runs) * 1000

        x_data.append(n)
        y_data.append(elapsed)
        line.set_data(x_data, y_data)
        return line,

    ani = FuncAnimation(fig, update, frames=len(input_sizes), interval=150, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    animate_linear_search()
    animate_binary_search()
    animate_hashmap_search()