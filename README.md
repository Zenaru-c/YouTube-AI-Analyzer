# 🎥 YouTube AI Analyzer

YouTube AI Analyzer is a web-based tool that allows users to input a YouTube video URL and receive an AI-generated sentiment analysis based solely on the video’s comment section. The project is built to help users quickly assess the general reception of a video using natural language processing techniques.

---

## 🚀 Features

- 🔗 Input a YouTube video URL and get instant feedback.
- 💬 Sentiment analysis based on user comments (Good, Bad, or Questionable).
- 🧠 Custom AI prompt designed for brief, clear insights.
- 👤 User authentication system (Register/Login).
- 🔒 Security settings allow users to delete their account.

---

## 📊 How It Works

1. **URL Input**: User submits a YouTube URL.
2. **Comment Scraping**: The video ID is extracted using a regex pattern, and comments are fetched via the YouTube API.
3. **AI Analysis**: Comments are sent to an AI model with a tailored prompt:
    ```
    Based on the provided comments, do you believe the video is good, bad or questionable?
    Answer by saying one of these words (good, bad, questionable), and explain in 2 sentences why.
    ```
4. **Result**: The result is displayed along with a short explanation.

---

## 🧪 Manual Testing (Acceptance Test Summary)

The application was tested manually for the following flows:

- ✅ **User Registration**:
  - Correct inputs → Redirect to dashboard with accurate data.
  - Invalid email or duplicate → Error message prompts retry.
- ✅ **Login**:
  - Valid credentials → Access to dashboard.
  - Invalid credentials → Error shown and retry prompt.
- ✅ **YouTube AI Analysis**:
  - Correct YouTube URL → Analysis result shown.
  - Invalid/empty URL → Error message or no result.
- ✅ **Security Settings**: Account deletion successfully tested.

> 🔍 Testing was done manually after each file was completed and integrated into the project.

---

## 👤 User Roles

Only one user group is supported: **Basic user** (with login or registration access).

---

## 🌐 Technologies Used

- Python (Flask)
- OpenAI API
- YouTube Data API
- SQL for database
- HTML/CSS/JavaScript for frontend

---

## 🧾 License

This project is licensed under the **MIT License**, allowing open-source use and modification.

### Why MIT?

- ✅ Simple and permissive.
- ✅ Compatible with open-source tools and libraries used (e.g., Flask, BeautifulSoup).
- ✅ Encourages community collaboration.
- 🆚 Compared to alternatives:
  - **GPL**: Too restrictive for integration in other projects.
  - **Apache 2.0**: Overhead for a project of this size.

---

## 📈 Future Improvements

- UI enhancements (e.g., charts, dark mode).
- Multi-user dashboard view.
- Support for analyzing video metadata (titles/descriptions).
- Token optimization or upgrade for larger comment batches.

---

## 🛠️ Installation & Usage

```bash
git clone https://github.com/yourusername/youtube-ai-analyzer.git
cd youtube-ai-analyzer
pip install -r requirements.txt
python app.py
