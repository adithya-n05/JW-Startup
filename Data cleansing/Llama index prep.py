import json

def prepare_for_llamaindex(input_filename, output_filename):
    # Load the JSON data
    with open(input_filename, 'r') as f:
        data = json.load(f)
    
    # Prepare the formatted data for LlamaIndex
    llama_data = []

    for document in data:
        content = document.get("content", "")
        images = document.get("images", [])
        metadata = document.get("metadata", {})

        # Prepare the document structure as needed for LlamaIndex
        llama_document = {
            "text": content,
            "images": images,
            "title": metadata.get("title", ""),
            "url": metadata.get("url", ""),
            "source": metadata.get("source", ""),
            "snippet": metadata.get("snippet", ""),
        }

        llama_data.append(llama_document)

    # Save the prepared data into a new JSON file
    with open(output_filename, 'w') as f:
        json.dump(llama_data, f, indent=4)

    print(f"Data prepared for LlamaIndex and saved to {output_filename}")

# Example usage
input_filename = 'Data cleansing/Cleansed data/text/cleaned_articles.json'
output_filename = 'Data cleansing/Cleansed data/text/llamaindex_prepared_data.json'
prepare_for_llamaindex(input_filename, output_filename)