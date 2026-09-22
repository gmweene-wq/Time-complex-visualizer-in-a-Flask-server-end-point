import time
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from flask import Flask, request, jsonify
from stack_queue_algorithms import STACK_QUEUE_ALGORITHMS



def time_complexity_visualiser(algorithm, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))

    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)


    fig, ax = plt.subplots()
    ax.plot(input_sizes, times, 'o-')
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Running Time (seconds)')
    ax.set_title('Algorithm Time Complexity Visualiser')

    # Save the plot to a file
    filename = 'time_complexity_plot_{}_{}.png'.format(
        algorithm.__name__, int(time.time() * 1000)
    )
    fig.savefig(filename)
    plt.close(fig)

    with open(filename, 'rb') as f:
        imag_base64 = base64.b64encode(f.read()).decode('utf-8')
    return imag_base64
    
# define the binary search algorithm
def binary_search(n):
    arr = list(range(n))
    target = n - 1
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
# define the linear search algorithm
def linear_search(n):
    arr = list(range(n))
    target = n - 1
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
# define the bubble sort algorithm
def bubble_sort(n):
    arr = list(range(n, 0, -1))
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

 # define the nested loop algorithm               
def nested_loop(n):
    for i in range(n):
        for j in range(n):
            pass

 # define the selection sort algorithm       
def selection_sort(n):
    arr = list(range(n, 0, -1))
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# define the insertion sort algorithm
def insertion_sort(n):
    arr = list(range(n, 0, -1))
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# define the merge sort algorithm
def merge_sort(n):
    arr = list(range(n, 0, -1))

    def _merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _merge_sort(a[:mid])
        right = _merge_sort(a[mid:])
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    arr = _merge_sort(arr)

# define the algorithms dictionary
Algorithms = {
    'binary_search': binary_search,
    'linear_search': linear_search,
    'bubble_sort': bubble_sort,
    'nested_loop': nested_loop,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
    'merge_sort': merge_sort
}
Algorithms.update(STACK_QUEUE_ALGORITHMS)

# define the Flask app
app = Flask(__name__)
@app.route('/analyze')
def analyze():
    algo = request.args.get('algo')
    step = request.args.get('step', type=int)
    n_max = request.args.get('n_max', type=int)

    algorithm = Algorithms[algo]
    image_base64 = time_complexity_visualiser(algorithm, 0, n_max, step)
    return jsonify({
        'algorithm': algo,
        'step': step,
        'n_max': n_max,
        'image_base64': image_base64
    })

#time_complexity_visualiser(binary_search, 100, 1000, 100)
#time_complexity_visualiser(linear_search, 100, 1000, 100)
# time_complexity_visualiser(bubble_sort, 100, 1000, 100)
# time_complexity_visualiser(nested_loop, 100, 1000, 100)
# time_complexity_visualiser(selection_sort, 100, 1000, 100)
# time_complexity_visualiser(insertion_sort, 100, 1000, 100)
# time_complexity_visualiser(merge_sort, 100, 1000, 100)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)