from flask import Flask, request, jsonify
import os
import uuid
import cv2
from detect_image import find_image_in_image, draw

app = Flask(__name__)

UPLOAD_FOLDER = "input-images"
OUTPUT_FOLDER = "output-images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/detect", methods=["POST"])
def detect():
    if "source" not in request.files or "template" not in request.files:
        return (
            jsonify({"error": "Both 'source' and 'template' files are required."}),
            400,
        )

    source_file = request.files["source"]
    template_file = request.files["template"]

    source_filename = os.path.join(
        UPLOAD_FOLDER, f"{uuid.uuid4()}_{source_file.filename}"
    )
    template_filename = os.path.join(
        UPLOAD_FOLDER, f"{uuid.uuid4()}_{template_file.filename}"
    )

    source_file.save(source_filename)
    template_file.save(template_filename)

    try:
        coords, template_width, template_height = find_image_in_image(
            source_filename, template_filename
        )
        output_filename = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}.png")
        center_x, center_y = draw(
            source_filename, coords, template_width, template_height, output_filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # clean up the created files
    return jsonify(
        {
            "x": coords[0],
            "y": coords[1],
            "output_image": output_filename,
            "template_width": template_width,
            "template_height": template_height,
            "center_x": center_x,
            "center_y": center_y,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
