import json
import webbrowser

def display_and_select_websites(data, output_filename):
    # Prepare a list to store all links from the various sections of the data
    all_websites = []

    # Collect all relevant types of results
    result_types = [
        "organic_results", "news_results", "video_results", "images_results", 
        "related_questions", "related_searches", "top_stories", 
        "tweets_results", "events_results", "featured_snippet", 
        "videos_carousel", "podcasts_results", "featured_videos"
    ]
    
    for result_type in result_types:
        if result_type in data:
            all_websites.extend(data[result_type])

    index = 0
    batch_size = 20  # Display around 20 lines, depending on content length

    while index < len(all_websites):
        print(f"\nDisplaying websites {index + 1} to {min(index + batch_size, len(all_websites))}:\n")
        for i in range(index, min(index + batch_size, len(all_websites))):
            website = all_websites[i]
            print(f"{i + 1}. {website['title']}\n   {website['link']}\n   Snippet: {website['snippet'][:150]}...\n")  # Display only the first 150 characters of the snippet

        preview_selection = input(f"Enter the number of the website you want to preview, or press Enter to skip preview: ").strip()
        if preview_selection and preview_selection.isdigit():
            preview_index = int(preview_selection) - 1
            if index <= preview_index < index + batch_size:
                webbrowser.open(all_websites[preview_index]['link'])
                input("Press Enter after reviewing the site to continue...")

        selection = input(f"Enter the numbers of the websites to remove (comma-separated), or press Enter to keep all: ").strip()
        if selection:
            indices_to_remove = sorted([int(x) - 1 for x in selection.split(",") if x.isdigit()], reverse=True)
            for i in indices_to_remove:
                if index <= i < index + batch_size:
                    print(f"Removing: {all_websites[i]['title']}")
                    del all_websites[i]
        
            # Save the filtered results after each batch
            with open(output_filename, 'w') as f:
                json.dump(all_websites, f, indent=4)
                print(f"Filtered websites saved to {output_filename}")
        else:
            print("No websites removed in this batch.")
        
        index += batch_size
    
    print("\nFinal list of websites after removal:")
    for i, website in enumerate(all_websites):
        print(f"{i + 1}. {website['title']}\n   {website['link']}\n")

    return all_websites

# Load the data from the JSON file
filename = "Web Scraper/json processing/duplicates_removed.json"  # Update with your actual file path if different
with open(filename, 'r') as f:
    data = json.load(f)

# Set the output filename
output_filename = "filtered_websites.json"  # Update with your desired output filename

# Display websites and allow for selection and removal
final_websites = display_and_select_websites(data, output_filename)