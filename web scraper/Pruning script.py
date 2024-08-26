import json

def display_and_select_websites(data):
    all_websites = []
    for entry in data:
        if "organic_results" in entry:
            all_websites.extend(entry["organic_results"])
    
    index = 0
    while index < len(all_websites):
        print(f"\nDisplaying websites {index + 1} to {min(index + 10, len(all_websites))}:\n")
        for i in range(index, min(index + 10, len(all_websites))):
            website = all_websites[i]
            print(f"{i + 1}. {website['title']}\n   {website['link']}\n   Snippet: {website['snippet']}\n")
        
        selection = input(f"Enter the numbers of the websites to remove (comma-separated), or press Enter to keep all: ").strip()
        if selection:
            indices_to_remove = sorted([int(x) - 1 for x in selection.split(",") if x.isdigit()], reverse=True)
            for i in indices_to_remove:
                if index <= i < index + 10:
                    print(f"Removing: {all_websites[i]['title']}")
                    del all_websites[i]
        else:
            print("No websites removed in this batch.")
        
        index += 10
    
    print("\nFinal list of websites after removal:")
    for i, website in enumerate(all_websites):
        print(f"{i + 1}. {website['title']}\n   {website['link']}\n")

    return all_websites

# Load the data from the JSON file
filename = "Jeff_Wilson_Professor_Dumpster_google_results pruning.json"
with open(filename, 'r') as f:
    data = json.load(f)

# Display websites and allow for selection and removal
final_websites = display_and_select_websites(data)

# Save the filtered results back to a JSON file if needed
output_filename = "filtered_websites.json"
with open(output_filename, 'w') as f:
    json.dump(final_websites, f, indent=4)
    print(f"Filtered websites saved to {output_filename}")