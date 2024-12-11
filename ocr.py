import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = '/bin/tesseract'
def extract_text_with_segmentation(image_path, languages="fra+ara"):
    """
    Extracts text from an image and segments it based on spatial proximity.

    :param image_path: Path to the ID card image.
    :param languages: Languages for Tesseract OCR (default: French and Arabic).
    :return: A list of segmented text blocks.
    """
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale for better OCR results
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Optional: Apply adaptive thresholding for binarization
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Find contours to isolate text blocks
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_blocks = []
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Skip very small or large areas (noise or full image area)
        if w * h < 100 or w * h > 0.8 * image.shape[0] * image.shape[1]:
            continue

        # Crop the text region
        text_region = image[y:y+h, x:x+w]

        # Run OCR on the cropped region
        text = pytesseract.image_to_string(text_region, lang=languages).strip()
        
        if text:  # Only include non-empty results
            text_blocks.append({"text": text, "bbox": (x, y, w, h)})

    # Sort blocks top-to-bottom, left-to-right for better readability
    text_blocks = sorted(text_blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))

    return text_blocks

def visualize_text_blocks(image_path, text_blocks):
    """
    Visualizes text blocks on the image for debugging purposes.

    :param image_path: Path to the ID card image.
    :param text_blocks: List of text blocks with bounding boxes.
    """
    image = cv2.imread(image_path)

    for block in text_blocks:
        x, y, w, h = block["bbox"]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image, block["text"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
        )

    cv2.imshow("Text Blocks", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Usage Example
image_path = "images/card.jpeg"  # Replace with your image path
text_blocks = extract_text_with_segmentation(image_path)

# Print extracted and segmented text
for i, block in enumerate(text_blocks):
    print(f"Block {i + 1}: {block['text']}")

# Optional: Visualize text blocks on the image
visualize_text_blocks(image_path, text_blocks)
