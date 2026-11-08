![CI](https://github.com/AkibHasanAyon/functional-testing-2507208/actions/workflows/ci.yml/badge.svg)

# Functional Testing Project — 2507208

Practical assignment: Functional testing, CI/CD, and live deployment for 16 Python functions.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/AkibHasanAyon/functional-testing-2507208.git
   cd functional-testing-2507208
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

```bash
pytest --cov=target --cov-branch -v
```

## Live URL

- **Live Application:** [https://functional-testing-2507208.onrender.com](https://functional-testing-2507208.onrender.com)
- **Health & Commit SHA Endpoint:** [https://functional-testing-2507208.onrender.com/health](https://functional-testing-2507208.onrender.com/health)

## Project Structure

```
functional-testing-2507208/
├── .github/workflows/ci.yml   # CI pipeline (Python 3.10–3.12)
├── templates/index.html        # Web frontend
├── tests/test_target.py        # 156 test cases, 100% coverage
├── .gitignore
├── README.md
├── app.py                      # Flask application
├── pytest.ini                  # pytest configuration
├── requirements.txt            # Pinned dependencies
└── target.py                   # Target module (unmodified)
```

## Functions Tested

| # | Function | Type | Description |
|---|----------|------|-------------|
| 1 | `is_adult(age)` | Data | True if age ≥ 18 |
| 2 | `celsius_to_fahrenheit(c)` | Data | °C to °F, rounded 2dp |
| 3 | `count_vowels(text)` | Data | Count vowels, case-insensitive |
| 4 | `invert(flag)` | Data | Boolean NOT |
| 5 | `greet(name)` | Data | Greeting with fallback to Guest |
| 6 | `find_max(numbers)` | Data | Largest in list |
| 7 | `get_price(prices, item)` | Data | Dict lookup with KeyError |
| 8 | `swap(pair)` | Data | Swap two values |
| 9 | `common_items(a, b)` | Data | Set intersection |
| 10 | `is_leap_year(year)` | Data | Leap year check |
| 11 | `to_int(value)` | Data | Convert to int, reject bool |
| 12 | `divide(a, b)` | Math | Division with zero guard |
| 13 | `power(base, exp)` | Math | Exponentiation |
| 14 | `square_root(x)` | Math | Square root, reject negative |
| 15 | `factorial(n)` | Math | n!, reject negative |
| 16 | `average(numbers)` | Math | Mean of list |

## Suspected Bugs in target.py

1. **No type checking on numeric functions** — `is_adult("18")` does a string comparison instead of raising an error; `divide`, `power`, `square_root`, `factorial`, and `celsius_to_fahrenheit` accept any type supporting the operators.
2. **`greet(123)` raises AttributeError** — passing a non-string, non-None value triggers `name.strip()` which fails with `AttributeError` rather than a clean `TypeError`.
3. **`find_max` and `average` use `len()`** — they crash with `TypeError` on generators or iterators, only working with sequences.
