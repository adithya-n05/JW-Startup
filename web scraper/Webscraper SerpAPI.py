import json
from serpapi import GoogleSearch
import signal
import sys
import os

def fetch_google_results(query):
    api_key = os.getenv('SERPAPI_KEY')  # Retrieve the SerpApi key from the environment variables
    
    if not api_key:
        print("Error: SERPAPI_KEY environment variable not set.")
        sys.exit(1)
    
    num_results_per_page = 10
    start = 0
    filename = f"{query.replace(' ', '_')}_google_results.json"
    
    with open(filename, 'w') as f:
        json.dump([], f)
    
    try:
        while True:
            params = {
                "engine": "google",
                "q": query,
                "hl": "en",
                "gl": "us",
                "google_domain": "google.com",
                "num": str(num_results_per_page),
                "start": str(start),
                "api_key": api_key
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            
            page_data = {}

            # Collect Organic Results
            if "organic_results" in results:
                page_data["organic_results"] = results["organic_results"]

            # Collect News Results
            if "news_results" in results:
                page_data["news_results"] = results["news_results"]

            # Collect Video Results
            if "video_results" in results:
                page_data["video_results"] = results["video_results"]

            # Collect Image Results
            if "images_results" in results:
                page_data["images_results"] = results["images_results"]

            # Collect Related Questions (People Also Ask)
            if "related_questions" in results:
                page_data["related_questions"] = results["related_questions"]

            # Collect Related Searches
            if "related_searches" in results:
                page_data["related_searches"] = results["related_searches"]

            # Collect Answer Box
            if "answer_box" in results:
                page_data["answer_box"] = results["answer_box"]

            # Collect Top Stories (News Carousel)
            if "top_stories" in results:
                page_data["top_stories"] = results["top_stories"]

            # Collect Tweets
            if "tweets_results" in results:
                page_data["tweets_results"] = results["tweets_results"]

            # Collect Events
            if "events_results" in results:
                page_data["events_results"] = results["events_results"]

            # Collect Featured Snippet
            if "featured_snippet" in results:
                page_data["featured_snippet"] = results["featured_snippet"]

            # Collect Videos Carousel
            if "videos_carousel" in results:
                page_data["videos_carousel"] = results["videos_carousel"]

            # Collect Podcasts
            if "podcasts_results" in results:
                page_data["podcasts_results"] = results["podcasts_results"]

            # Collect Featured Videos
            if "featured_videos" in results:
                page_data["featured_videos"] = results["featured_videos"]

            if page_data:
                with open(filename, 'r+') as f:
                    current_data = json.load(f)
                    current_data.append(page_data)
                    f.seek(0)
                    json.dump(current_data, f, indent=4)
                
                # Log the results for debugging
                total_results_this_page = sum(len(page_data.get(key, [])) for key in page_data)
                print(f"Page number: {int(start/10)}")
                print(f"Results fetched this page: {total_results_this_page}")
                print(f"Results saved to {filename}")
                
            
            start += num_results_per_page

            if total_results_this_page < 0:
                print("Fewer results returned than expected, stopping.")
                break

    except KeyboardInterrupt:
        print("\nProcess interrupted. Saving and exiting.")
        sys.exit(0)

# Example usage
queries = ["The craziest OkCupid date ever"]
for query in queries:
    fetch_google_results(query)

# from serpapi import GoogleSearch

# def fetch_google_results(query, total_results=1000, api_key='bbd3497b28da09256090cb720f896de8e73a7483cf2d7856f9eab61cb52c3e14'):
#     all_results = []
#     num_results_per_page = 10
#     start = 0

#     while len(all_results) < total_results:
#         params = {
#             "engine": "google",
#             "q": query,
#             "hl": "en",
#             "gl": "us",
#             "google_domain": "google.com",
#             "num": str(num_results_per_page),
#             "start": str(start),
#             "api_key": api_key
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()

#         total_results_count = results.get("search_information", {}).get("total_results", 0)
#         print(f"Total results available according to Google: {total_results_count}")

#         # Collecting all types of results
#         result_types = ["organic_results", "news_results", "video_results", "images_results", "ads"]
#         for result_type in result_types:
#             if result_type in results:
#                 all_results.extend(results[result_type])

#         # Log details for debugging
#         total_results_this_page = sum(len(results.get(result_type, [])) for result_type in result_types)
#         print(f"Results fetched this page: {total_results_this_page}")
#         print(f"Total results collected so far: {len(all_results)}")

#         # Increment to the next set of results
#         start += num_results_per_page

#         # Break the loop if fewer results than expected are returned
#         if total_results_this_page <= 1:
#             print("Fewer results returned than expected, stopping.")
#             break

#     return all_results

# # Example usage
# query = "Jeff Wilson Professor Dumpster"
# api_key = "bbd3497b28da09256090cb720f896de8e73a7483cf2d7856f9eab61cb52c3e14"
# results = fetch_google_results(query, total_results=100, api_key=api_key)

# print(f"Total results fetched: {len(results)}")

# import json
# from serpapi import GoogleSearch

# def scrape_google_results(query, num_results=1000, api_key='bbd3497b28da09256090cb720f896de8e73a7483cf2d7856f9eab61cb52c3e14'):
#     search = GoogleSearch({
#         "q": query,
#         "num": 10,  # Number of results per page (10 is the maximum allowed by SerpApi)
#         "api_key": api_key,
#     })

#     all_results = []
#     page_num = 0
#     total_results = 0

#     while total_results < num_results:
#         search.params_dict["start"] = page_num * 10
#         page_results = search.get_dict()
#         page_data = {}

#         # Collect Organic Results
#         if "organic_results" in page_results:
#             page_data["organic_results"] = page_results["organic_results"]
#             total_results += len(page_results["organic_results"])

#         # Collect News Results
#         if "news_results" in page_results:
#             page_data["news_results"] = page_results["news_results"]
#             total_results += len(page_results["news_results"])

#         # Collect Video Results
#         if "video_results" in page_results:
#             page_data["video_results"] = page_results["video_results"]
#             total_results += len(page_results["video_results"])

#         # Collect Image Results
#         if "images_results" in page_results:
#             page_data["images_results"] = page_results["images_results"]
#             total_results += len(page_results["images_results"])

#         # Collect Related Questions (People Also Ask)
#         if "related_questions" in page_results:
#             page_data["related_questions"] = page_results["related_questions"]

#         # Collect Related Searches
#         if "related_searches" in page_results:
#             page_data["related_searches"] = page_results["related_searches"]

#         # Collect Answer Box
#         if "answer_box" in page_results:
#             page_data["answer_box"] = page_results["answer_box"]

#         # Collect Top Stories (News Carousel)
#         if "top_stories" in page_results:
#             page_data["top_stories"] = page_results["top_stories"]

#         # Collect Tweets
#         if "tweets_results" in page_results:
#             page_data["tweets_results"] = page_results["tweets_results"]

#         # Collect Events
#         if "events_results" in page_results:
#             page_data["events_results"] = page_results["events_results"]

#         # Collect Featured Snippet
#         if "featured_snippet" in page_results:
#             page_data["featured_snippet"] = page_results["featured_snippet"]

#         # Collect Videos Carousel
#         if "videos_carousel" in page_results:
#             page_data["videos_carousel"] = page_results["videos_carousel"]

#         # Collect Podcasts
#         if "podcasts_results" in page_results:
#             page_data["podcasts_results"] = page_results["podcasts_results"]

#         # Collect Featured Videos
#         if "featured_videos" in page_results:
#             page_data["featured_videos"] = page_results["featured_videos"]

#         if page_data:  # Only append if there is some data collected
#             all_results.append(page_data)

#         # Increment the page number for the next set of results
#         page_num += 1

#         # Break the loop if there are no more results to fetch
#         if len(page_results.get("organic_results", [])) < 10:
#             break

#     # Save all results to a JSON file
#     with open(f"{query}_google_results.json", "w") as file:
#         json.dump(all_results, file, indent=4)

#     return all_results

# # Example usage
# query = "Jeff Wilson Professor Dumpster"
# api_key = "bbd3497b28da09256090cb720f896de8e73a7483cf2d7856f9eab61cb52c3e14"
# results = scrape_google_results(query, num_results=1000, api_key=api_key)

# # Print a summary of the results
# print(f"Total results fetched: {len(results)}")