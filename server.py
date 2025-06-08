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

    output_filename = None
    center_x = None
    center_y = None
    coords = None
    template_width = None
    template_height = None
    response_data = None

    try:
        coords, template_width, template_height = find_image_in_image(
            source_filename, template_filename
        )
        output_filename = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}.png")
        center_x, center_y = draw(
            source_filename, coords, template_width, template_height, output_filename
        )
        response_data = {
            "x": coords[0],
            "y": coords[1],
            "output_image": output_filename,
            "template_width": template_width,
            "template_height": template_height,
            "center_x": center_x,
            "center_y": center_y,
        }
    except Exception as e:
        app.logger.warning(f"Exception occurred: {e}")
        response_data = {"error": str(e)}
        return jsonify(response_data), 500
    finally:
        # Remove all files in input-images and the output file if it exists
        try:
            for f in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, f)
                app.logger.warning(f"Deleting file: {file_path}")

                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            app.logger.warning(f"Exception occurred: {e}")
            pass
        if output_filename and os.path.exists(output_filename):
            try:
                os.remove(output_filename)
            except Exception:
                pass

    app.logger.warning(f"test")

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
