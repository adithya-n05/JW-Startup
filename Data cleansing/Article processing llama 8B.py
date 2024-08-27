import json
import os
import subprocess

def process_text_with_llama(text, model="llama3.1", instruction="[no prose] Remove information not directly related to the article content and leave only the main article text. Do not add comments or notes. Do not modify the content of the article, leave it as is and solely remove excess information gathered when scraping. Do not respond if there is no content to extract, just leave it empty and move on."):
    # Construct the command to run ollama
    command = [
        "ollama", "run", model,instruction
    ]

    try:
        # Start the subprocess with Popen to stream output
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Send the input text to the process and close stdin
        stdout, stderr = process.communicate(input=text)

        # Stream the output to the terminal in real-time
        cleaned_text = ""
        for line in stdout.splitlines():
            print(line)  # Print to terminal
            cleaned_text += line + "\n"  # Collect the output for return

        if process.returncode != 0:
            print(f"Error: {stderr.strip()}")
            print("Ollama returned non-zero exit status.")
            cleaned_text = text  # Fallback to original text in case of error

        return cleaned_text.strip()

    except Exception as e:
        print(f"Error processing text with LLaMA: {e}")
        return text  # Fallback to original text in case of error

def clean_scraped_articles(input_filename, output_filename):
    # Load the JSON data
    with open(input_filename, 'r') as f:
        data = json.load(f)

    # Open the output file in write mode
    with open(output_filename, 'w') as f:
        f.write("[")  # Start the JSON array

        # Process each article's text
        for i, document in enumerate(data):
            content = document.get("content", "")
            if content:
                print(f"Processing article from {document['metadata']['url']}")
                cleaned_content = process_text_with_llama(content)
                document["content"] = cleaned_content

                # Write the cleaned document to the file
                json.dump(document, f, indent=4)

                if i < len(data) - 1:
                    f.write(",\n")  # Add a comma between documents

        f.write("]")  # End the JSON array

    print(f"Cleaned articles saved to {output_filename}")

# Example usage
input_filename = "Web Scraper/scraped data/scrapedtext.json"  # Input file with scraped data
output_filename = "Data cleansing/Cleansed data/text/cleaned_articles.json"  # Output file to save cleaned articles

clean_scraped_articles(input_filename, output_filename)
