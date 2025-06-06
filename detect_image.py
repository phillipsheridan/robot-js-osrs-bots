import cv2
import sys
import uuid
import os


def find_image_in_image(source_path: str, template_path: str):
    source = cv2.imread(source_path)
    template = cv2.imread(template_path)
    if source is None:
        raise FileNotFoundError(f"Source image not found: {source_path}")
    if template is None:
        raise FileNotFoundError(f"Template image not found: {template_path}")
    source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(source_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc, template.shape[1], template.shape[0]  # (x, y), width, height


def draw_match_rectangle(
    source_path: str, top_left, template_width, template_height, output_path: str
):
    source = cv2.imread(source_path)
    pt1 = top_left
    pt2 = (top_left[0] + template_width, top_left[1] + template_height)
    cv2.rectangle(source, pt1, pt2, (0, 0, 255), 3)
    cv2.imwrite(output_path, source)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python detect_image.py <sourceImage> <templateImage>")
        sys.exit(1)
    source_path = sys.argv[1]
    template_path = sys.argv[2]
    coords, template_width, template_height = find_image_in_image(
        source_path, template_path
    )
    print(f"Template found at: x={coords[0]}, y={coords[1]}")
    output_path = os.path.join("output-images", f"{uuid.uuid4()}.png")
    draw_match_rectangle(
        source_path, coords, template_width, template_height, output_path
    )
    print(f"Output image with match highlighted saved as {output_path}")
