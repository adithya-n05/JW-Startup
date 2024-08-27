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

    # Check and prune duplicates in each result type
    if "organic_results" in data:
        data["organic_results"] = prune_results(data["organic_results"])

    if "news_results" in data:
        data["news_results"] = prune_results(data["news_results"])

    if "video_results" in data:
        data["video_results"] = prune_results(data["video_results"])

    if "images_results" in data:
        data["images_results"] = prune_results(data["images_results"])

    if "related_questions" in data:
        data["related_questions"] = prune_results(data["related_questions"])

    if "related_searches" in data:
        data["related_searches"] = prune_results(data["related_searches"])

    if "top_stories" in data:
        data["top_stories"] = prune_results(data["top_stories"])

    if "tweets_results" in data:
        data["tweets_results"] = prune_results(data["tweets_results"])

    if "events_results" in data:
        data["events_results"] = prune_results(data["events_results"])

    if "videos_carousel" in data:
        data["videos_carousel"] = prune_results(data["videos_carousel"])

    if "podcasts_results" in data:
        data["podcasts_results"] = prune_results(data["podcasts_results"])

    if "featured_videos" in data:
        data["featured_videos"] = prune_results(data["featured_videos"])

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