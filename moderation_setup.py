import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

def moderate_text(text):
    url = "https://api.openai.com/v1/moderations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {"input": text}
    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()

        # Log the entire response for review
        results = response_json['results'][0]
        if results['flagged']:
            print("Content is flagged as inappropriate")
            return True
        else:
            print("Content is not flagged as inappropriate")
            return False
        
        # Print category scores, remove the return statements above to see this
        print("Category Scores:")
        for category, score in results['category_scores'].items():
            print(f"{category}: {score}")

    except Exception as e:
        print(f"Error during moderation request: {e}")
        return False


"""Testing the moderation API"""

# this prompt will be flagged as innapropriate
#prompt = "I will kick you"

# this prompt will not be flagged as innapropriate
prompt = "How do you think puppies would react to a bird? Also do you like langsmith?"

moderate_text(prompt)
