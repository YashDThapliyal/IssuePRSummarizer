# GitHub PR/Issue Summarizer

This application summarizes GitHub pull requests (PRs) and issues, including comments, to provide key insights and actionable next steps. It uses the GROQ API for summarization and the GitHub API for data retrieval.

---

## Features

- Summarizes GitHub pull requests and issues, including their comments.
- Provides a concise summary and actionable next steps for better understanding.
- Handles private repositories with authentication using a GitHub Personal Access Token.
- Avoids rate limits by authenticating with a GitHub token.

---

## Prerequisites

- **Python 3.8 or higher**.
- A valid **GROQ API Key** for summarization.
- A **GitHub Personal Access Token** (optional, but recommended for increased API rate limits or private repositories).

---

## Usage

### Enter API Tokens:

- **GROQ API Key**:
  - Enter your [GROQ API Key](https://console.groq.com/keys) in the "Settings" section of the sidebar. 

- **GitHub Token** *(optional)*:
  - Generate a [GitHub Personal Access Token](https://github.com/settings/tokens) with the `repo` scope.
  - Enter the token in the "GitHub Token" field in the sidebar to access private repositories or avoid API rate limits.

---

### Input GitHub URL:

- Paste the GitHub pull request or issue URL (e.g., `https://github.com/owner/repo/pull/123`) into the input box and press Enter.

---

### View Results:

- **Details**:
  - Displays metadata about the PR/issue, including state, author, creation date, and labels.
  
- **Summary**:
  - A concise overview and actionable next steps generated using the GROQ API.

---

## Dependencies

Run the following command in your terminal to install the required dependencies:

```bash
pip install streamlit requests groq
```

---

## Run the Application

Run the following command in your terminal to start the Streamlit application:

```bash
streamlit run app.py
```

---

## MIT License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

**Made by Yash Thapliyal in 2025**
