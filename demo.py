from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cohere

app = Flask(__name__)
CORS(app)

# Cảnh báo: Không nên hardcode API key trong mã nguồn thực tế
COHERE_API_KEY = "9xG2YDcb3LpvMwa87rNcOS9cGxPO3sLQFq9ip00a"
co = cohere.Client(COHERE_API_KEY)

# Route test đơn giản để kiểm tra server hoạt động
@app.route("/", methods=["GET"])
def serve_ui():
    return send_from_directory("html", "index.html")

# Route chat chính
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400

    user_message = data["message"]

    try:
        # Gọi Cohere chat endpoint
        response = co.chat(message=user_message)

        bot_reply = response.text if response else "Xin lỗi, tôi không hiểu."

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Chạy server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
