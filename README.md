# 🤖 MSBLAM Chatbot

A sophisticated chatbot application built with Flask and Google's Gemini AI, featuring a modern UI, chat history, and formatted responses. Created by [@Siddanagowda](https://github.com/Siddanagowda).

## ✨ Features

- **🧠 AI-Powered Conversations**: Utilizes Google's Gemini AI for intelligent responses
- **🛡️ Content Guardian**: Built-in content moderation system for safe interactions
- **💾 Chat History**: Persistent storage of conversations using SQLite
- **🎨 Modern UI**:
  - ChatGPT-like interface
  - Dark/Light mode toggle
  - Responsive design for mobile and desktop
  - Sidebar for chat history
- **📝 Formatted Responses**: 
  - Well-structured output with headers and bullet points
  - Code snippets with syntax highlighting
  - Markdown support
  - Time-aware greetings
- **📚 Pre-formatted Content**:
  - Common code examples (e.g., binary search)
  - Structured information about various topics

## 📋 Prerequisites

- Python 3.7+
- Google Gemini API key

## 🚀 Installation

1. Clone the repository:
```bash
git clone <https://github.com/Siddanagowda/Chat-Bot>
cd chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API key and settings
# DO NOT commit your .env file to version control!
```

Your `.env` file should contain:
```plaintext
GOOGLE_API_KEY=your_gemini_api_key_here
```

⚠️ **Important**: Never commit your `.env` file or share your API keys. The `.gitignore` file is set up to prevent this.

## 🏃‍♂️ Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

- `app.py`: Main Flask application and API routes
- `code_examples.py`: Collection of formatted code examples
- `formatted_content.py`: Pre-formatted content for common topics
- `content_guardian.py`: Content moderation system
- `templates/`: HTML templates
  - `index.html`: Main chat interface
- `.env`: Environment variables
- `requirements.txt`: Python dependencies
- `chat_history.db`: SQLite database for chat storage

## 📖 Usage

1. **🆕 Starting a New Chat**:
   - Click the "New Chat" button in the sidebar
   - Type your message and press Enter or click Send

2. **📜 Viewing Chat History**:
   - All previous chats appear in the sidebar
   - Click any chat to load its messages

3. **💡 Special Features**:
   - **👋 Smart Greetings**:
     - Time-aware responses (morning/afternoon/evening)
     - Friendly welcome messages with menu options
   - **🛡️ Content Guardian**:
     - Built-in content moderation
     - Safe response handling
     - Inappropriate content filtering
   - **💬 Response Types**:
     - Code examples with syntax highlighting
     - Structured information with bullet points
     - Casual conversation with context-aware responses

4. **🌓 Theme Toggle**:
   - Click the theme toggle button to switch between dark and light modes

## 🛑 Stopping the Server

- Press `Ctrl+C` in the terminal to stop the Flask server
- Alternatively, find and terminate the Python process:
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID <process_id> /F
  ```

## 💽 Database Schema

### Chat Table
- `id`: String (UUID, primary key)
- `title`: String (chat title)
- `created_at`: DateTime

### ChatMessage Table
- `id`: Integer (primary key)
- `chat_id`: String (foreign key to Chat)
- `content`: Text (message content)
- `is_user`: Boolean (true if user message)
- `timestamp`: DateTime

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

* **🤖 Google Gemini AI**: For providing the powerful language model that powers our chatbot's responses
* **🌶️ Flask**: The lightweight WSGI web application framework that made this project possible
* **🗄️ SQLite**: For providing a reliable and easy-to-use database solution
* **🎨 Tailwind CSS**: For the modern and responsive UI components
* **🛡️ Content Guardian**: For ensuring safe and appropriate interactions
* **🐍 Python Community**: For the excellent packages and tools that were used in this project:
  - `python-dotenv`: For environment variable management
  - `flask-sqlalchemy`: For elegant database interactions
  - `google-generativeai`: For seamless integration with Gemini AI
* **🌟 Open Source Community**: For providing invaluable resources and inspiration
* **👥 Contributors**: Thanks to all who have contributed to making this project better
