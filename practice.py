import time
import numpy as np
import matplotlib

matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting
import matplotlib.pyplot as plt


def time_complexity_visualizer(algorithm, n_min, n_max):
    times = []
    input_sizes = list(range(n_min, n_max + 1))

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Running Time (seconds)')
    ax.set_title('Time Complexity Visualization (Live)')
    line = ax.plot([], [], '-')  # Initialize an empty line

    for i , n in enumerate(input_sizes):
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)

        # Update the plot with new data
        line[0].set_data(input_sizes[:i + 1], times)
        ax.relim()  
        ax.autoscale_view() 
        plt.draw()  
        plt.pause(0.1)  

    plt.ioff()  
    plt.show()

def linear_search(n):
    """A simple linear search algorithm that runs in O(n) time."""
    arr = list(range(n))
    target = n - 1
    for i in arr:
        if i == target:
            return i
    return -1
# visualize the time complexity of linear search
#time_complexity_visualizer(linear_search, 0,100)


def constant_search(n):
    """A simple constant time search algorithm that runs in O(1) time."""
    arr = list(range(n))
    target = n - 1
    if target in arr:
        return target
    return -1
# visualize the time complexity of constant search
#time_complexity_visualizer(constant_search, 0,100)

# binary search algorithm that runs in O(log n) time
def binary_search(n):
    """A binary search algorithm that runs in O(log n) time."""
    arr = list(range(n))
    target = n - 1
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return arr[mid]
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
# visualize the time complexity of binary search
#time_complexity_visualizer(binary_search, 0,100)


users = [{"id":1},{"id" : 2}, {"id":3},{"id":2}]

def find_unique_users(users):
    unique_users = []
    for i in range(len(users)):
        seen = False
        for j in range(len(unique_users)):
            if users[i]["id"] == unique_users[j]["id"]:
                seen = True
                break
        if not seen:
            unique_users.append(users[i])
    return unique_users

# plot the time complexity of finding unique users
time_complexity_visualizer(find_unique_users, 10, 100)


# #optimised version of finding unique users using a set for O(1) lookups
def find_unique_users_optimized(users):
    seen_ids = set()
    unique_users = []
    for user in users:
        if user["id"] not in seen_ids:
            seen_ids.add(user["id"])
            unique_users.append(user)
    return unique_users
# plot the time complexity of finding unique users using the optimized version
#time_complexity_visualizer(find_unique_users_optimized, 10, 10000)
