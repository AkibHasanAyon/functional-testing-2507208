"""Flask application serving the functional testing frontend."""

import os
import json
from flask import Flask, render_template, request, jsonify
import target

app = Flask(__name__)

# Map function names to their callables
FUNCTIONS = {
    "is_adult": target.is_adult,
    "celsius_to_fahrenheit": target.celsius_to_fahrenheit,
    "count_vowels": target.count_vowels,
    "invert": target.invert,
    "greet": target.greet,
    "find_max": target.find_max,
    "get_price": target.get_price,
    "swap": target.swap,
    "common_items": target.common_items,
    "is_leap_year": target.is_leap_year,
    "to_int": target.to_int,
    "divide": target.divide,
    "power": target.power,
    "square_root": target.square_root,
    "factorial": target.factorial,
    "average": target.average,
}


def parse_arg(value, type_hint):
    """Parse a string argument into the expected Python type."""
    if type_hint == "int":
        return int(value)
    elif type_hint == "float":
        return float(value)
    elif type_hint == "bool":
        if value.lower() in ("true", "1", "yes"):
            return True
        elif value.lower() in ("false", "0", "no"):
            return False
        raise ValueError(f"Cannot parse '{value}' as bool")
    elif type_hint == "str":
        return str(value)
    elif type_hint == "list":
        return json.loads(value)
    elif type_hint == "dict":
        return json.loads(value)
    elif type_hint == "set":
        return set(json.loads(value))
    elif type_hint == "tuple":
        return tuple(json.loads(value))
    elif type_hint == "none_or_str":
        if value.lower() == "none" or value.strip() == "":
            return None
        return str(value)
    elif type_hint == "any":
        # Try int, then float, then string
        try:
            return int(value)
        except (ValueError, TypeError):
            pass
        try:
            return float(value)
        except (ValueError, TypeError):
            pass
        return value
    return value


@app.route("/")
def index():
    """Render the main frontend page."""
    sha = os.environ.get("COMMIT_SHA", "dev")
    return render_template("index.html", sha=sha)


@app.route("/run", methods=["POST"])
def run_function():
    """Execute a target.py function and return the result as JSON."""
    data = request.get_json()
    func_name = data.get("function")
    args = data.get("args", {})

    if func_name not in FUNCTIONS:
        return jsonify({"error": f"Unknown function: {func_name}",
                        "type": "ValueError"}), 400

    func = FUNCTIONS[func_name]

    try:
        # Parse arguments based on function
        if func_name == "is_adult":
            result = func(parse_arg(args["age"], "int"))

        elif func_name == "celsius_to_fahrenheit":
            result = func(parse_arg(args["celsius"], "float"))

        elif func_name == "count_vowels":
            result = func(args["text"])

        elif func_name == "invert":
            result = func(parse_arg(args["flag"], "bool"))

        elif func_name == "greet":
            name = args.get("name", "")
            result = func(parse_arg(name, "none_or_str"))

        elif func_name == "find_max":
            result = func(parse_arg(args["numbers"], "list"))

        elif func_name == "get_price":
            prices = parse_arg(args["prices"], "dict")
            result = func(prices, args["item"])

        elif func_name == "swap":
            result = func(parse_arg(args["pair"], "tuple"))

        elif func_name == "common_items":
            set_a = parse_arg(args["set_a"], "set")
            set_b = parse_arg(args["set_b"], "set")
            result = func(set_a, set_b)
            result = list(result)  # Convert set to list for JSON

        elif func_name == "is_leap_year":
            result = func(parse_arg(args["year"], "int"))

        elif func_name == "to_int":
            result = func(parse_arg(args["value"], "any"))

        elif func_name == "divide":
            a = parse_arg(args["a"], "float")
            b = parse_arg(args["b"], "float")
            result = func(a, b)

        elif func_name == "power":
            base = parse_arg(args["base"], "float")
            exponent = parse_arg(args["exponent"], "float")
            result = func(base, exponent)

        elif func_name == "square_root":
            result = func(parse_arg(args["x"], "float"))

        elif func_name == "factorial":
            result = func(parse_arg(args["n"], "int"))

        elif func_name == "average":
            result = func(parse_arg(args["numbers"], "list"))

        else:
            return jsonify({"error": "Function not implemented",
                            "type": "NotImplementedError"}), 400

        # Convert tuple to list for JSON serialization
        if isinstance(result, tuple):
            result = list(result)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 400


@app.route("/health")
def health():
    """Return the deployed commit SHA."""
    sha = os.environ.get("COMMIT_SHA", "dev")
    return jsonify({"sha": sha})


if __name__ == "__main__":
    app.run(debug=True)
