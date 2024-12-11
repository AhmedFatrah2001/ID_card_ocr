# ID Card Information Extraction Tool

## Overview
This project uses Pytesseract to extract information from ID cards through a two-step process of zone creation and OCR scanning.

## Prerequisites
- Python 3.7+
- Tesseract OCR
- Required Python packages:
  - pytesseract
  - opencv-python

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/id-card-ocr.git
cd id-card-ocr
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
- `zones_creation.py`: Creates scanning zones with labels on ID card images
- `zones_ocr.py`: Performs OCR scanning on predefined zones

## Usage
1. Create zones for your ID card:
```bash
python zones_creation.py --input your_id_card.jpg
```

2. Extract text from the defined zones:
```bash
python zones_ocr.py --input your_id_card.jpg
```

## Configuration
Modify the zone coordinates and labels in `zones_creation.py` to match your specific ID card layout.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.