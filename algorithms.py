
def linear_search(n):
    """O(n) - search for a value that is not present (worst case)."""
    arr = list(range(n))
    target = -1
    for value in arr:
        if value == target:
            return True
    return False


def binary_search(n):
    """O(log n) - search a sorted array for a value that is not present."""
    arr = list(range(n))
    target = -1
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False


def bubble_sort(n):
    """O(n^2) - sort a reverse-ordered list (worst case for bubble sort)."""
    arr = list(range(n, 0, -1))
    length = len(arr)
    for i in range(length):
        for j in range(0, length - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def nested_loops(n):
    """O(n^2) - a generic double loop with no sorting/searching involved."""
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count


def selection_sort(n):
    """O(n^2) - sort a reverse-ordered list."""
    arr = list(range(n, 0, -1))
    length = len(arr)
    for i in range(length):
        min_idx = i
        for j in range(i + 1, length):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(n):
    """O(n^2) - sort a reverse-ordered list (worst case for insertion sort)."""
    arr = list(range(n, 0, -1))
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(n):
    """O(n log n) - sort a reverse-ordered list using merge sort."""
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

    return _merge_sort(arr)


# Registry mapping the query-param name to its function and complexity description. This is used to validate the query param and to call the function.
ALGORITHMS = {
    "linear_search": {"func": linear_search, "complexity": "O(n)"},
    "binary_search": {"func": binary_search, "complexity": "O(log n)"},
    "bubble_sort": {"func": bubble_sort, "complexity": "O(n^2)"},
    "nested_loops": {"func": nested_loops, "complexity": "O(n^2)"},
    "selection_sort": {"func": selection_sort, "complexity": "O(n^2)"},
    "insertion_sort": {"func": insertion_sort, "complexity": "O(n^2)"},
    "merge_sort": {"func": merge_sort, "complexity": "O(n log n)"},
}
