import requests
import pandas as pd
from tqdm import tqdm
# Replace with your GitHub personal access token if you have one
GITHUB_TOKEN = 'sometoken'  # Optional, but recommended for higher rate limits


# GitHub API URL
API_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/pulls'

# Headers for authentication (optional but recommended)
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_pull_requests_for_repo(api_url, headers, num_prs=3):
    # Send GET request to GitHub API
    response = requests.get(api_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        prs = response.json()
        return prs[:num_prs]  # Return the specified number of PRs
    else:
        print(f'Failed to fetch pull requests: {response.status_code}')
        return []

# Fetch the PRs
pull_requests = get_pull_requests_for_repo(API_URL, headers)

def fetch_and_save_pull_requests(input_csv_path, output_csv_path):
    # Load the input CSV file
    df = pd.read_csv(input_csv_path)
    
    # Initialize an empty list to store the fetched pull requests
    all_prs_ids = []
    repos_names = []
    # Iterate over each row in the DataFrame
    for index, row in tqdm(df.iterrows(), total=len(df)):
        owner, repo = row['repo_name'].split('/')
        
        # Fetch the pull requests for the current repository
        api_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
        prs = get_pull_requests_for_repo(api_url, headers)
        
        # Add the fetched pull requests to the list
        all_prs_ids.extend([pr['number'] for pr in prs])
        repos_names.extend([row['repo_name'] for _ in prs])
    
    # Convert the list of pull requests to a DataFrame
    prs_df = pd.DataFrame({"repo name": repos_names, "pull request id": all_prs_ids})
    
    # Save the DataFrame to a new CSV file
    prs_df.to_csv(output_csv_path, index=False)


input_csv_path = '/Users/uri/Documents/Workspace/coaching/RulesEvaluator/Analysis/1000pythonhighstarsrepos.csv'
output_csv_path = '/Users/uri/Documents/Workspace/coaching/RulesEvaluator/Analysis/1000pythonhighstarsrepos_prs.csv'

fetch_and_save_pull_requests(input_csv_path, output_csv_path)
