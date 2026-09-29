# kozpy's open-source release — re-share only with proper credit.

from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

RAZORPAY_IFSC_URL = "https://ifsc.razorpay.com/"

@app.route('/ifsc', methods=['GET'])
def get_ifsc_info():
    ifsc_code = request.args.get('code')

    if not ifsc_code:
        return jsonify({
            "error": "IFSC code is required",
            "message": "Please provide IFSC code using 'code' parameter",
            "credit": "@kozpy"
        }), 400

    if len(ifsc_code) != 11 or not ifsc_code.isalnum():
        return jsonify({
            "error": "Invalid IFSC code format",
            "message": "IFSC code must be 11 alphanumeric characters",
            "credit": "@kozpy"
        }), 400

    try:
        response = requests.get(
            f"{RAZORPAY_IFSC_URL}{ifsc_code}",
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; Flask-IFSC-API/1.0)'}
        )

        if response.status_code == 200:
            data = response.json()
            data['credit'] = "@kozpy"
            return jsonify(data), 200
        elif response.status_code == 404:
            return jsonify({
                "error": "IFSC code not found",
                "message": f"No bank found with IFSC code: {ifsc_code}",
                "credit": "@kozpy"
            }), 404
        else:
            return jsonify({
                "error": "Failed to fetch IFSC information",
                "status_code": response.status_code,
                "message": "Unable to retrieve data from Razorpay API",
                "credit": "@kozpy"
            }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Request timeout",
            "message": "Razorpay API is taking too long to respond",
            "credit": "@kozpy"
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Connection error",
            "message": "Unable to connect to Razorpay API",
            "credit": "@kozpy"
        }), 503
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "API request failed",
            "message": str(e),
            "credit": "@kozpy"
        }), 500
    except json.JSONDecodeError:
        return jsonify({
            "error": "Invalid response from Razorpay API",
            "message": "Unable to parse JSON response",
            "credit": "@kozpy"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "IFSC API is running",
        "credit": "@kozpy"
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "Available endpoints: GET /ifsc?code=IFSC_CODE, GET /health",
        "credit": "@kozpy"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on the server",
        "credit": "@kozpy"
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)