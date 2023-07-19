# tele_dashboard

A simple dashboard application which allows users to view a simple statistical overview of their Telegram chat data.

![tele_dash](https://github.com/tsu2000/tele_dashboard/assets/106811131/d4172169-8025-4515-a85e-5e95e27251c4)

**Available features**:
- Metrics regarding chat users (≥ 1 message in chat), total number of messages and age of chat group.
- Interactive bar chart which shows the number of messages sent by users, from most to least active.
- Interactive line chart showing of number of daily messages sent over time.
- Interactive scatter plot comparing each user's average number of words per message against the total number of messages sent by the user.
- Word Cloud showing the 100 most frequently used words.
- Chat Sentiment Analysis using NLTK's `SentimentIntensityAnalyzer()` to get an approximate measure of chat toxicity/overall chat sentiment.

**Known limitations**:
- Only accepts `.json` files for processing.
- File size limited to <200MB for now. If multiple files added, around 250MB total. **DO NOT EXCEED THIS YOU WILL 100% CRASH THE APP**
- Chat group age may not be completely accurate for certain chats
- Chat Sentiment Analysis only applies to pure text messages in the group chat, and may take a while to load if `.json` file is very large. Also 'sentiment' is completely subjective and may therefore be inaccurate.

**Link to Web App**:

[<img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg">](<https://tele-dash.streamlit.app>)

**Instructions to export Telegram chats as `.JSON` files**:

[<img src="https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white">](<https://github.com/tsu2000/tele_dashboard/blob/main/instructions.md>)
