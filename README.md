# Time Complexity Visualizer

A Flask server that benchmarks algorithms across a range of input sizes,
plots how their runtime grows, and returns the plot as a base64-encoded
image alongside the raw timing data.

## Setup

```bash
pip install -r requirements.txt
python3 app.py
```

The server runs on `http://localhost:8000`.

## Endpoint

```
GET /analyze?algo=<name(s)>&step=<int>&n_max=<int>
```

- **algo** — one algorithm name, or a comma-separated list to compare
  several on the same plot (e.g. `algo=linear_search,bubble_sort`)
- **step** — increment between successive values of `n`
- **n_max** — largest `n` to test (minimum is always 0). Accepts plain
  integers or comma-formatted numbers like `10,000`.

### Example

```
http://localhost:8000/analyze?algo=linear_search&step=10&n_max=1000
```

### Supported algorithms

| Name             | Complexity   |
|------------------|--------------|
| linear_search    | O(n)         |
| binary_search    | O(log n)     |
| bubble_sort      | O(n^2)       |
| nested_loops     | O(n^2)       |
| selection_sort   | O(n^2)       |
| insertion_sort   | O(n^2)       |
| merge_sort       | O(n log n)   |

### Response

```json
{
  "algorithms": ["linear_search"],
  "step": 10,
  "n_max": 1000,
  "n_values": [0, 10, 20, ...],
  "timings": { "linear_search": [0.0000026, 0.0000024, ...] },
  "image_path": "/absolute/path/to/static/plots/linear_search_20260101_120000.png",
  "image_base64": "iVBORw0KGgoAAAANS..."
}
```

`image_path` is where the PNG snapshot was saved on disk (also kept in
`static/plots/`), and `image_base64` is the same image encoded as a
base64 string, ready to render directly in a browser or client with:

```html
<img src="data:image/png;base64,<image_base64 value>" />
```

## Notes

- Each algorithm builds its own worst-case input internally (e.g. a
  reverse-sorted list for the sorting algorithms, a target that doesn't
  exist for the searches), so the timings reflect worst-case behavior.
- There's a safety cap of 200 data points per request (`n_max // step`).
  Some of these algorithms are O(n^2) or worse, so a very small step
  combined with a very large n_max could otherwise make a single
  request run for a very long time.
