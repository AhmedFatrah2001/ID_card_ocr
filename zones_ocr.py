from flask import Flask, request, jsonify
import cv2
import pytesseract
import json
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Configuration
ZONES_FILE = "zones.json"
FIXED_WIDTH = 800
FIXED_HEIGHT = int(FIXED_WIDTH / 1.586)

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = '/bin/tesseract'

def process_image(image_data, zones_file):
    with open(zones_file, 'r') as f:
        zones = json.load(f)

    # Decode the image
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        return {"error": "Unable to decode image."}, 400

    # Resize the image to the fixed dimensions
    resized_image = cv2.resize(image, (FIXED_WIDTH, FIXED_HEIGHT))

    results = {}
    for zone in zones:
        # Use the pixel values directly
        x1, y1, x2, y2 = zone["x1"], zone["y1"], zone["x2"], zone["y2"]

        # Crop the region
        cropped = resized_image[y1:y2, x1:x2]

        # Perform OCR
        text = pytesseract.image_to_string(
            cropped, config="--oem 3 --psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
        results[zone["label"]] = text.strip()

    return results, 200

@app.route("/extract", methods=["POST"])
def extract():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    try:
        image_data = image_file.read()
        results, status_code = process_image(image_data, ZONES_FILE)
        return jsonify(results), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
