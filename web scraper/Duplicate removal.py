import json

def remove_duplicate_websites(data):
    seen_links = set()
    
    for entry in data:
        if "organic_results" in entry:
            unique_results = []
            for website in entry["organic_results"]:
                if website["link"] not in seen_links:
                    seen_links.add(website["link"])
                    unique_results.append(website)
                else:
                    print(f"Duplicate found and removed: {website['title']} - {website['link']}")
            entry["organic_results"] = unique_results

    return data

# Load the data from the JSON file
filename = "Jupe_Jeff_Wilson_google_results.json"
with open(filename, 'r') as f:
    data = json.load(f)

# Remove duplicate websites based on the 'link' field
cleaned_data = remove_duplicate_websites(data)

# Save the cleaned data back to a JSON file
output_filename = "cleaned_websites.json"
with open(output_filename, 'w') as f:
    json.dump(cleaned_data, f, indent=4)
    print(f"Cleaned data saved to {output_filename}")