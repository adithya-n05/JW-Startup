import json

def count_scraped_websites(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        # Initialize counters
        total_websites = 0
        news_results = 0
        video_results = 0
        image_results = 0
        related_questions = 0
        related_searches = 0
        answer_box = 0
        top_stories = 0
        tweets_results = 0
        events_results = 0
        featured_snippet = 0
        videos_carousel = 0
        podcasts_results = 0
        featured_videos = 0

        # Count entries in each category
        if "organic_results" in data:
            total_websites += len(data["organic_results"])

        if "news_results" in data:
            total_websites += len(data["news_results"])
            news_results += len(data["news_results"])

        if "video_results" in data:
            total_websites += len(data["video_results"])
            video_results += len(data["video_results"])

        if "images_results" in data:
            total_websites += len(data["images_results"])
            image_results += len(data["images_results"])

        if "related_questions" in data:
            related_questions += len(data["related_questions"])

        if "related_searches" in data:
            related_searches += len(data["related_searches"])

        if "answer_box" in data:
            answer_box += len(data["answer_box"])

        if "top_stories" in data:
            top_stories += len(data["top_stories"])

        if "tweets_results" in data:
            tweets_results += len(data["tweets_results"])

        if "events_results" in data:
            events_results += len(data["events_results"])

        if "featured_snippet" in data:
            featured_snippet += len(data["featured_snippet"])

        if "videos_carousel" in data:
            videos_carousel += len(data["videos_carousel"])

        if "podcasts_results" in data:
            podcasts_results += len(data["podcasts_results"])

        if "featured_videos" in data:
            featured_videos += len(data["featured_videos"])

        # Output the results
        print(f"Total websites scraped: {total_websites}")
        print(f"Total number of news results: {news_results}")
        print(f"Total number of video results: {video_results}")
        print(f"Total number of image results: {image_results}")
        print(f"Total number of related questions: {related_questions}")
        print(f"Total number of related searches: {related_searches}")
        print(f"Total number of answer boxes: {answer_box}")
        print(f"Total number of top stories: {top_stories}")
        print(f"Total number of tweets: {tweets_results}")
        print(f"Total number of events results: {events_results}")
        print(f"Total number of featured snippets: {featured_snippet}")
        print(f"Total number of videos in carousel: {videos_carousel}")
        print(f"Total number of podcast results: {podcasts_results}")
        print(f"Total number of featured videos: {featured_videos}")

        return total_websites

    except FileNotFoundError:
        print(f"File {filename} not found.")
        return 0
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return 0

filename = "Web Scraper/json processing/filtered_websites.json"
count_scraped_websites(filename)