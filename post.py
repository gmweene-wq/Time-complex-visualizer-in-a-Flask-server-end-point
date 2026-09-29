import io
import os
import time
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_file
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

# Database setup (SQLite file saved next to post.py)
DATABASE_URL = "sqlite:///analysis.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define the AnalysisResult model for the analysis_results table
class AnalysisResult(Base):
    __tablename__ = "analysis_results"
# table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    algorithm = Column(String(50), nullable=False)
    n_min = Column(Integer, nullable=False)
    n_max = Column(Integer, nullable=False)
    n_step = Column(Integer, nullable=False)
    image = Column(LargeBinary, nullable=False)  # the PNG graph, stored as a BLOB

# method to convert the model instance to a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "algorithm": self.algorithm,
            "n_min": self.n_min,
            "n_max": self.n_max,
            "n_step": self.n_step,
            # raw image bytes can't go in JSON, so just report its size
            "image_size_bytes": len(self.image) if self.image else 0,
        }

# create the analysis_results table if it doesn't exist yet
def init_db():
    Base.metadata.create_all(engine)

# function to save a new analysis record to the database
def save_analysis(algorithm, n_min, n_max, n_step, image):
    session = SessionLocal()
    try:
        record = AnalysisResult(
            algorithm=algorithm,
            n_min=n_min,
            n_max=n_max,
            n_step=n_step,
            image=image,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.to_dict()
    finally:
        session.close()

# function to fetch one record's image (BLOB) by id
def get_analysis_image(record_id):
    session = SessionLocal()
    try:
        record = session.get(AnalysisResult, record_id)
        return record.image if record else None
    finally:
        session.close()


# time the algorithm at each input size and return the graph as PNG bytes
def time_complexity_visualiser(algorithm, n_min, n_max, n_step):
    input_sizes = list(range(n_min, n_max + 1, n_step))
    times = []

    for n in input_sizes:
        start_time = time.perf_counter()
        algorithm(n)
        times.append(time.perf_counter() - start_time)

    fig, ax = plt.subplots()
    ax.plot(input_sizes, times, 'o-')
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Running Time (seconds)')
    ax.set_title('Time Complexity: {}'.format(algorithm.__name__))

    # save the graph into memory (not to a file) and return the raw bytes
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    return buffer.getvalue()


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

# The secret key signs every token.
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", "change-this-dev-secret-key-to-something-long"
)
# Only accept tokens from the Authorization header (not query params)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
# Tokens expire after 1 hour
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# Users who are allowed to log in
USERS = {
    "griphen": generate_password_hash("griphen123"),
}


# Custom 401 messages for every way a token can fail
@jwt.unauthorized_loader
def missing_token(reason):
    # no Authorization header, or not in "Bearer <token>" format
    return jsonify({"error": "I don't know you. You must be a fake hacker!!!!!!!!", "detail": reason}), 401


@jwt.invalid_token_loader
def invalid_token(reason):
    # token was changed, badly formed, or signed with another key
    return jsonify({"error": "I don't know you. Bye!", "detail": reason}), 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    # token is older than JWT_ACCESS_TOKEN_EXPIRES
    return jsonify({"error": "Your token has expired. Log in again."}), 401


init_db()  # create the analysis_results table if it doesn't exist yet

# Log in to get a JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    password_hash = USERS.get(username)
    if password_hash is None or not check_password_hash(password_hash, password or ""):
        return jsonify({'error': "I don't know you. Bye!"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200


# Save an analysis record -- only for users with a valid JWT
@app.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    current_user = get_jwt_identity()  # the username stored in the token

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

    if n_min < 0 or n_max < n_min:
        return jsonify({'error': 'need 0 <= n_min <= n_max'}), 400
    if n_step <= 0:
        return jsonify({'error': 'n_step must be greater than 0'}), 400

# run the algorithm and draw the graph (PNG bytes)
    image_bytes = time_complexity_visualiser(Algorithms[algo], n_min, n_max, n_step)

# save the analysis record (including the image BLOB) to the database
    saved_record = save_analysis(
        algorithm=algo,
        n_min=n_min,
        n_max=n_max,
        n_step=n_step,
        image=image_bytes,
    )
    saved_record['saved_by'] = current_user

    return jsonify(saved_record), 201


# View the image (BLOB) of a saved record  also needs a valid JWT
@app.route('/analyze/<int:record_id>/image', methods=['GET'])
@jwt_required()
def analysis_image(record_id):
    image_bytes = get_analysis_image(record_id)
    if image_bytes is None:
        return jsonify({'error': 'No record with id {}'.format(record_id)}), 404
    return send_file(io.BytesIO(image_bytes), mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)