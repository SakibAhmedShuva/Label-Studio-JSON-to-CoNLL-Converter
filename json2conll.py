from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Directory to save the output files
OUTPUT_DIR = 'output_files'
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure the directory exists

def convert_to_conll(json_data):
    output_lines = ["-DOCSTART- -X- O O\n\n"]
    
    for item in json_data:
        text = item['data']['text']
        annotations = item['annotations'][0]['result'] if item['annotations'] else []
        
        # Sort annotations by start position
        sorted_annotations = sorted(annotations, key=lambda x: x['value']['start'])
        
        # Create list of tokens with their labels
        current_pos = 0
        tokens = []
        prev_label = None
        
        for annotation in sorted_annotations:
            start = annotation['value']['start']
            end = annotation['value']['end']
            label = annotation['value']['labels'][0]
            
            # Add any text before the current annotation as O (Outside) tokens
            if start > current_pos:
                prefix_text = text[current_pos:start]
                prefix_tokens = prefix_text.strip().split()
                for token in prefix_tokens:
                    if token.strip():
                        tokens.append((token, 'O'))
                        prev_label = None  # Reset previous label after O tokens
            
            # Add the annotated token with proper B/I prefix
            annotated_text = text[start:end]
            if annotated_text.strip():
                # If previous label exists and is the same type, use I- prefix
                if prev_label and prev_label.endswith(label):
                    prefix = 'I-'
                else:
                    prefix = 'B-'
                
                tokens.append((annotated_text, f"{prefix}{label}"))
                prev_label = f"{prefix}{label}"
            
            current_pos = end
        
        # Add any remaining text as O tokens
        if current_pos < len(text):
            remaining_text = text[current_pos:]
            remaining_tokens = remaining_text.strip().split()
            for token in remaining_tokens:
                if token.strip():
                    tokens.append((token, 'O'))
        
        # Convert to CONLL format
        for token, label in tokens:
            if token.strip():  # Skip empty tokens
                conll_line = f"{token} -X- _ {label}\n"
                output_lines.append(conll_line)
        
        # Add blank line between sentences
        output_lines.append("\n")
    
    return "".join(output_lines)

@app.route('/convert_to_conll', methods=['POST'])
def convert_to_conll_api():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        
        # Ensure the file is a JSON file
        if file.filename == '' or not file.filename.endswith('.json'):
            return jsonify({"error": "No JSON file uploaded"}), 400
        
        # Read and parse JSON data
        json_data = json.load(file)
        
        # Convert to CONLL format
        conll_output = convert_to_conll(json_data)
        
        # Define the output filename
        output_filename = request.form.get('output_filename', 'output.conll')
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Save the output to a file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(conll_output)
        
        return jsonify({"message": f"File saved successfully", "file_path": output_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5005, debug=True)
