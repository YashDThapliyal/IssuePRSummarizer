import re
import requests
import streamlit as st
from groq import Groq 


def parse_github_url(url):
    pattern = r"https://github\.com/([^/]+)/([^/]+)/(pull|issues)/(\d+)"
    match = re.match(pattern, url)
    if match:
        return match.groups()
    return None


def get_pr_or_issue_data(owner, repo, type, number, token=None):
    if type == "pull":
        api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}"
    else:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}"
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching PR/issue data: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return None


def get_comments(owner, repo, type, number, token=None):
    if type == "pull":
        comments_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}/comments"
    else:
        comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}/comments"
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(comments_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching comments: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return []


def process_query_with_groq(context, groq_api_key):
    if not context.strip():
        return "No content available to summarize."

    prompt = f"""
    You are a helpful assistant tasked with summarizing GitHub issues or pull requests. 
    Based on the following GitHub conversation (including the PR/issue description and comments), provide:
    1. **A summary**: Key points discussed in the issue or PR.
    2. **Next steps**: Concrete recommendations or actions to take.
    
    GitHub Content:
    {context}
    """

    try:
        client = Groq(api_key=groq_api_key)  
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=4096,
            top_p=1,
            stream=False,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error during summarization: {e}"


def inject_fonts():
    custom_fonts = """
    <style>
        html, body, [class*="css"]  {
            font-family: 'Helvetica', sans-serif;
        }
    </style>
    """
    st.markdown(custom_fonts, unsafe_allow_html=True)


def main():
    inject_fonts()  
    
    st.sidebar.title("Settings")
    groq_api_key = st.sidebar.text_input("Enter GROQ API Key:", type="password")
    github_token = st.sidebar.text_input("Enter GitHub Token:", type="password")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info("This app summarizes GitHub issues and pull requests, along with their comments, to provide insights and next steps.")

    st.title("GitHub PR/Issue Summarizer")
    st.write("Enter the GitHub URL below to get started.")
    
    github_url = st.text_input("Enter GitHub pull request or issue URL:")
    
    if not groq_api_key:
        st.warning("Please enter your GROQ API Key in the sidebar to proceed.")
        return

    if github_url:
        parsed_url = parse_github_url(github_url)
        
        if parsed_url:
            owner, repo, type, number = parsed_url

            if type == "pull":
                st.info("This is a pull request. Summarizing PR details.")
            elif type == "issues":
                st.info("This is an issue. Summarizing issue details.")
            else:
                st.error("Could not determine if this is a PR or issue. Please check the URL.")
                return

            data = get_pr_or_issue_data(owner, repo, type, number, token=github_token)
            

            comments = get_comments(owner, repo, type, number, token=github_token)
            
            if data:
                st.subheader("Details:")
                st.markdown(f"""
                - **State:** {data['state'].capitalize()}
                - **Author:** {data['user']['login']}
                - **Created:** {data['created_at']}
                - **Labels:** {', '.join([f'`{label["name"]}`' for label in data.get('labels', [])])}
                """)
                
                body = data.get('body', 'No description available.').strip()
                comments_text = "\n".join([f"{c['user']['login']}: {c['body']}" for c in comments])
                full_context = f"Issue/PR Description:\n{body}\n\nComments:\n{comments_text}"
                
                summary = process_query_with_groq(full_context, groq_api_key)

                st.subheader("Summary:")
                if summary.startswith("Error"):
                    st.error(summary)
                else:
                    st.markdown(summary)
            else:
                st.error("Failed to fetch data from GitHub API")
        else:
            st.error("Invalid GitHub URL")
    
    st.markdown("---")
    st.write("**Made by Yash Thapliyal in 2025**")

if __name__ == "__main__":
    main()
