import os
import json
from collections import defaultdict

def merge_json_files(folder_path):
    # Create a dictionary to store merged data for each result type
    merged_data = defaultdict(list)

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for entry in data:
                    # Merge the results for each type
                    if "organic_results" in entry:
                        merged_data["organic_results"].extend(entry["organic_results"])

                    if "news_results" in entry:
                        merged_data["news_results"].extend(entry["news_results"])

                    if "video_results" in entry:
                        merged_data["video_results"].extend(entry["video_results"])

                    if "images_results" in entry:
                        merged_data["images_results"].extend(entry["images_results"])

                    if "related_questions" in entry:
                        merged_data["related_questions"].extend(entry["related_questions"])

                    if "related_searches" in entry:
                        merged_data["related_searches"].extend(entry["related_searches"])

                    if "answer_box" in entry:
                        merged_data["answer_box"].append(entry["answer_box"])

                    if "top_stories" in entry:
                        merged_data["top_stories"].extend(entry["top_stories"])

                    if "tweets_results" in entry:
                        merged_data["tweets_results"].extend(entry["tweets_results"])

                    if "events_results" in entry:
                        merged_data["events_results"].extend(entry["events_results"])

                    if "featured_snippet" in entry:
                        merged_data["featured_snippet"].append(entry["featured_snippet"])

                    if "videos_carousel" in entry:
                        merged_data["videos_carousel"].extend(entry["videos_carousel"])

                    if "podcasts_results" in entry:
                        merged_data["podcasts_results"].extend(entry["podcasts_results"])

                    if "featured_videos" in entry:
                        merged_data["featured_videos"].extend(entry["featured_videos"])

    return merged_data

def save_merged_data(merged_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(merged_data, file, indent=4)

if __name__ == "__main__":
    # Define the path to the folder containing JSON files
    folder_path = '/Users/adithyanarayanan/Library/CloudStorage/Dropbox/Documents/Career/Internships/Jeff Wilson Startup (beyond)/JW-Startup/Web Scraper/mergedata'  # Replace with your folder path

    # Define the output file path
    output_file = 'merged_results.json'

    # Merge the JSON files and save the result
    merged_data = merge_json_files(folder_path)
    save_merged_data(merged_data, output_file)

    print(f"Merged data has been saved to {output_file}")