import json

def remove_duplicate_websites(data):
    seen_links = set()

    # Define a function to remove duplicates from a specific type of results
    def prune_results(results):
        unique_results = []
        for result in results:
            if result["link"] not in seen_links:
                seen_links.add(result["link"])
                unique_results.append(result)
            else:
                print(f"Duplicate found and removed: {result['title']} - {result['link']}")
        return unique_results

    switch = {
        "organic_results": "organic_results",
        "news_results": "news_results",
        "video_results": "video_results",
        "images_results": "images_results",
        "related_questions": "related_questions",
        "related_searches": "related_searches",
        "top_stories": "top_stories",
        "tweets_results": "tweets_results",
        "events_results": "events_results",
        "videos_carousel": "videos_carousel",
        "podcasts_results": "podcasts_results",
        "featured_videos": "featured_videos"
    }

    for key in switch:
        if key in data:
            data[key] = prune_results(data[key])

    return data

# Load the data from the JSON file
filename = "Web Scraper/json processing/merged_results.json"  # Replace with your actual filename
with open(filename, 'r') as f:
    data = json.load(f)

# Remove duplicate websites based on the 'link' field
cleaned_data = remove_duplicate_websites(data)

# Save the cleaned data back to a JSON file
output_filename = "cleaned_websites.json"  # Replace with your desired output filename
with open(output_filename, 'w') as f:
    json.dump(cleaned_data, f, indent=4)
    print(f"Cleaned data saved to {output_filename}")