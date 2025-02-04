from flask import Flask, request, jsonify
import time

# Constants
LOG_FILE_PATH = "/sdcard/DCIM/tuba9.txt"  # Updated file path
API_OWNER = "Benjamin1337"
API_TYPE = "ossint"
API_KEY = "benjaminXroot"
MAX_RESULTS = 1000

app = Flask(__name__)

# Function to search logs
def search_logs(keyword):
    results = []
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                if keyword in line:
                    results.append(line.strip())  # Remove extra spaces/newlines
                    if len(results) >= MAX_RESULTS:
                        break
    except Exception as e:
        return [], str(e)

    return results, None

# API Route
@app.route("/api", methods=["GET"])
def handle_search():
    start_time = time.time()

    # Validate API Key
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "Forbidden: Invalid API Key"}), 403

    # Validate search parameter
    keyword = request.args.get("search")
    if not keyword:
        return jsonify({"error": "Query parameter 'search' is required"}), 400

    # Search logs
    results, error = search_logs(keyword)
    if error:
        return jsonify({"error": f"Internal server error: {error}"}), 500

    response = {
        "api_owner": API_OWNER,
        "type": API_TYPE,
        "results": results
    }

    elapsed_time = round(time.time() - start_time, 2)
    print(f"Search completed in {elapsed_time} seconds. Keyword: '{keyword}', Results: {len(results)}")

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9977, debug=True)
