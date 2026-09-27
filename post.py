from datetime import datetime

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


# ---------------------------------------------------------------------
# Database setup (SQLAlchemy ORM only -- no raw SQL strings anywhere,
# per the teacher's instruction: writing plain SQL directly in the app
# opens the door to SQL injection, so every query here goes through the
# ORM instead of string-built SQL).
# ---------------------------------------------------------------------
DATABASE_URL = "sqlite:///analysis.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class AnalysisResult(Base):
    """One saved analysis request: which algorithm, and what input range."""

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    algorithm = Column(String(50), nullable=False)
    n_min = Column(Integer, nullable=False)
    n_max = Column(Integer, nullable=False)
    n_step = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "algorithm": self.algorithm,
            "n_min": self.n_min,
            "n_max": self.n_max,
            "n_step": self.n_step,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def init_db():
    """Create the analysis_results table if it doesn't exist yet."""
    Base.metadata.create_all(engine)


def save_analysis(algorithm, n_min, n_max, n_step):
    """Insert a new analysis record (algorithm + input range) and return
    it as a dict, including the auto-generated id and created_at."""
    session = SessionLocal()
    try:
        record = AnalysisResult(
            algorithm=algorithm,
            n_min=n_min,
            n_max=n_max,
            n_step=n_step,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.to_dict()
    finally:
        session.close()


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

# define the Flask app
app = Flask(__name__)
init_db()  # create the analysis_results table if it doesn't exist yet


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    algo = data.get('algo')
    n_min = data.get('n_min', 0)
    n_max = data.get('n_max')
    n_step = data.get('n_step')

    if not algo:
        return jsonify({'error': 'algo is required in the request body'}), 400
    if algo not in Algorithms:
        return jsonify({
            'error': 'Unknown algorithm: {}'.format(algo),
            'supported_algorithms': sorted(Algorithms.keys())
        }), 400
    if n_max is None:
        return jsonify({'error': 'n_max is required in the request body'}), 400
    if n_step is None:
        return jsonify({'error': 'n_step is required in the request body'}), 400

    try:
        n_min = int(n_min)
        n_max = int(n_max)
        n_step = int(n_step)
    except (TypeError, ValueError):
        return jsonify({'error': 'n_min, n_max and n_step must be integers'}), 400

    # algo has already been validated against Algorithms above, so there's
    # nothing left to compute here -- just persist the request parameters.
    saved_record = save_analysis(
        algorithm=algo,
        n_min=n_min,
        n_max=n_max,
        n_step=n_step,
    )

    return jsonify(saved_record), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)