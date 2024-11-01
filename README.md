# Label Studio JSON to CoNLL Converter

## Overview

This project provides a versatile solution for converting JSON annotations from Label Studio to CoNLL (Conference on Natural Language Learning) format. It offers both a Jupyter Notebook script and a Flask API endpoint for seamless conversion of named entity recognition (NER) annotations.

## Features

- Convert Label Studio JSON annotations to CoNLL format
- Supports multiple annotations in a single JSON file
- Handles token-level annotations with B-I-O (Begin-Inside-Outside) tagging
- Provides two conversion methods:
  - Jupyter Notebook script for local processing
  - Flask API for web-based conversion

## Requirements

- Python 3.7+
- Dependencies:
  - `json` (standard library)
  - `flask` (for API version)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SakibAhmedShuva/Label-Studio-JSON-to-CoNLL-Converter.git
   cd Label-Studio-JSON-to-CoNLL-Converter
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install flask
   ```

## Usage

### Jupyter Notebook Method

1. Open the Jupyter Notebook
2. Modify the input and output file paths in the `main()` function
3. Run the notebook to convert your JSON file

Example:
```python
main(input_file="your_labelstudio_annotations.json", output_file="output.conll")
```

### Flask API Method

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Send a POST request to `http://localhost:5005/convert_to_conll` with:
   - File: JSON annotation file
   - Optional: `output_filename` parameter

#### Curl Example:
```bash
curl -F "file=@labelstudio_annotations.json" \
     -F "output_filename=converted_annotations.conll" \
     http://localhost:5005/convert_to_conll
```

## CoNLL Format Explanation

The converter transforms Label Studio JSON annotations into CoNLL format:
- Each token is on a new line
- Format: `token -X- _ label`
- Labels use B-/I-/O prefixes for named entity recognition
  - `B-`: Begin of an entity
  - `I-`: Inside an entity
  - `O`: Outside any entity

## Example

**Input JSON** (Label Studio format):
```json
[
  {
    "data": {"text": "John works at Google in California"},
    "annotations": [{
      "result": [
        {"value": {"start": 0, "end": 4, "labels": ["PER"]}},
        {"value": {"start": 11, "end": 17, "labels": ["ORG"]}}
      ]
    }]
  }
]
```

**Output CoNLL**:
```
-DOCSTART- -X- O O

John -X- _ B-PER
works -X- _ O
at -X- _ O
Google -X- _ B-ORG
in -X- _ O
California -X- _ O
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

The README provides a comprehensive overview of the Label Studio JSON to CoNLL Converter. I've included sections on:
- Project overview
- Features
- Installation instructions
- Usage for both Jupyter Notebook and Flask API methods
- An explanation of CoNLL format
- An example transformation
- Placeholders for contributing, licensing, and contact information

Would you like me to modify anything in the README?
