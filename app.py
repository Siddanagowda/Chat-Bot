from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc
import uuid
import traceback
from code_examples import BINARY_SEARCH
from formatted_content import ICC_CHAMPIONS_TROPHY, AI_INFORMATION, COFFEE_GUIDE
from content_guardian import ContentGuardian

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
try:
    # Configure generation parameters
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config
    )
except Exception as e:
    print(f"Error initializing Gemini model: {str(e)}")
    raise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize the content guardian
content_guardian = ContentGuardian()

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('ChatMessage', backref='chat', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat()
        }

class ChatMessage(db.Model):
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(36), db.ForeignKey('chat.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'content': self.content,
            'is_user': self.is_user,
            'timestamp': self.timestamp.isoformat()
        }

def init_db():
    # Drop all tables
    with app.app_context():
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

# Initialize database tables
init_db()

def format_response(text):
    """Format the response text to be more readable."""
    # Split into sections based on common patterns
    sections = []
    current_section = []
    
    for line in text.split('\n'):
        # Check if line looks like a header
        if line.strip() and (line.startswith('#') or line.isupper() or line.endswith(':')):
            if current_section:
                sections.append('\n'.join(current_section))
                current_section = []
            current_section.append(f"## {line.strip('#').strip()}")
        else:
            # Format list items
            line = line.strip()
            if line.startswith('*') or line.startswith('-'):
                current_section.append(line)
            elif line:
                # Break long paragraphs into bullet points
                if len(line) > 100:
                    sentences = line.split('. ')
                    for sentence in sentences:
                        if sentence:
                            current_section.append(f"* {sentence.strip()}")
                else:
                    current_section.append(line)
    
    if current_section:
        sections.append('\n'.join(current_section))
    
    # Join sections with double newlines for spacing
    return '\n\n'.join(sections)

def create_structured_prompt(query):
    """Create a prompt that encourages well-structured responses."""
    return f"""Please provide information about {query} in a clear, organized format following these guidelines:

1. Start with a brief overview as a main heading using '#'
2. Break down the information into logical sections using '##' for section headers
3. Use '###' for subsections if needed
4. For each section:
   - Use bullet points (*) for key points
   - Keep points concise and clear
   - Include relevant examples where appropriate

5. Include these sections if relevant:
   - Definition/Overview
   - Types/Categories
   - Key Components
   - Applications/Uses
   - Benefits/Advantages
   - Challenges/Limitations
   - Best Practices
   - Future Trends

6. Format Guidelines:
   - Use markdown formatting
   - Break long paragraphs into bullet points
   - Keep sentences clear and concise
   - Use spacing between sections
   - Include relevant emojis at section headers for visual appeal


Examples:

    1. For Code Format Requests:
    If the user asks about code or programming concepts, format your response like this:
    User: "Show me how to write a Python function for factorial"
    Response: ```python
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        return n * factorial(n-1)
    ```
    I've created a recursive factorial function. Here's how it works:
    1. Base case: If n is 0 or 1, return 1
    2. Recursive case: Multiply n by factorial of (n-1)

    2. For Information Requests:
    If the user asks for information or explanations, structure your response like this:
    User: "What is machine learning?"
    Response: 
    📚 Machine Learning Overview:
    • Definition: A branch of AI that enables systems to learn from data
    • Key Components:
    - Data collection and preprocessing
    - Model training and validation
    - Performance evaluation
    • Common Applications:
    - Image recognition
    - Natural language processing
    - Predictive analytics

    3. For Greetings and Casual Conversation:
    If the user sends a greeting or casual message, respond warmly like this:
    User: "Good morning!"
    Response: "Good morning! 🌅 I hope you're having a great day. I'm here to help you with:
    • Programming questions
    • Technical explanations
    • General information
    What would you like to know about?"

Please structure the response about {query} following these guidelines and example to ensure maximum readability and understanding."""

@app.route('/')
def home():
    # Get all chats ordered by creation date
    chats = Chat.query.order_by(desc(Chat.created_at)).all()
    return render_template('index.html', chats=chats)

@app.route('/chat/<chat_id>')
def get_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    messages = ChatMessage.query.filter_by(chat_id=chat_id).order_by(ChatMessage.timestamp).all()
    return jsonify({
        'chat': chat.to_dict(),
        'messages': [msg.to_dict() for msg in messages]
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        chat_id = request.json.get('chat_id')
        
        # Check content safety
        is_safe, violations = content_guardian.check_content(user_message)
        if not is_safe:
            safe_response = content_guardian.get_safe_response(violations)
            warning_message = "⚠️ Your message contains content that may be inappropriate or harmful."
            return jsonify({
                'response': safe_response,
                'warning': warning_message,
                'chat_id': chat_id,
                'violations': [v['name'] for v in violations]
            })
        
        if not chat_id:
            chat_id = str(uuid.uuid4())
            title = ' '.join(user_message.split()[:4]) + '...'
            chat = Chat(id=chat_id, title=title)
            db.session.add(chat)
        
        user_chat = ChatMessage(chat_id=chat_id, content=user_message, is_user=True)
        db.session.add(user_chat)
        
        try:
            # Check for greetings first
            msg = user_message.lower()
            greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
            if any(msg.startswith(greeting) for greeting in greetings):
                # Get current hour to determine appropriate greeting
                current_hour = datetime.now().hour
                if 5 <= current_hour < 12:
                    time_of_day = "morning"
                elif 12 <= current_hour < 17:
                    time_of_day = "afternoon"
                else:
                    time_of_day = "evening"
                    
                response_text = f"Good {time_of_day}! 🌟 I'm your MSBLAM AI assistant, created by [@Siddanagowda](https://github.com/Siddanagowda). I can help you with:\n\n" + \
                              "• Programming questions and code examples\n" + \
                              "• Technical information and explanations\n" + \
                              "• General knowledge queries\n\n" + \
                              "What would you like to know about?"
                response = type('Response', (), {'text': response_text})()
            
            # Check for special content requests
            elif "binary search" in msg:
                response_text = BINARY_SEARCH
                response = type('Response', (), {'text': response_text})()
            elif any(term in msg for term in ["icc champions trophy", "cricket champion trophy"]):
                response_text = ICC_CHAMPIONS_TROPHY
                response = type('Response', (), {'text': response_text})()
            elif any(term in msg for term in ["what is ai", "artificial intelligence", "info about ai"]):
                response_text = AI_INFORMATION
                response = type('Response', (), {'text': response_text})()
            elif any(term in msg for term in ["coffee guide", "about coffee", "types of coffee"]):
                response_text = COFFEE_GUIDE
                response = type('Response', (), {'text': response_text})()
            else:
                # Default to the existing chat behavior
                model = genai.GenerativeModel('gemini-pro')
                prompt = create_structured_prompt(user_message)
                response = model.generate_content(prompt)
                
                # Check AI response for safety before sending
                is_safe, violations = content_guardian.check_content(response.text)
                if not is_safe:
                    warning_message = "⚠️ The AI's response contained potentially inappropriate content."
                    response_text = content_guardian.get_safe_response(violations)
                    return jsonify({
                        'response': response_text,
                        'warning': warning_message,
                        'chat_id': chat_id,
                        'violations': [v['name'] for v in violations]
                    })
                else:
                    response_text = response.text
            
            if not hasattr(response, 'text') or not response.text:
                raise Exception("Empty response from Gemini API")
            
            # Format the response for better readability
            formatted_response = format_response(response_text)
            print(f"Received response from Gemini: {formatted_response[:100]}...")
            
            bot_chat = ChatMessage(chat_id=chat_id, content=formatted_response, is_user=False)
            db.session.add(bot_chat)
            
            db.session.commit()
            
            return jsonify({
                'chat_id': chat_id,
                'response': formatted_response
            })
        except Exception as api_error:
            print(f"Gemini API error: {str(api_error)}")
            traceback.print_exc()
            db.session.rollback()  # Rollback on error
            return jsonify({
                'error': f"API Error: {str(api_error)}"
            }), 500
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        traceback.print_exc()
        db.session.rollback()  # Rollback on error
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/chats', methods=['GET'])
def get_chats():
    chats = Chat.query.order_by(desc(Chat.created_at)).all()
    return jsonify([chat.to_dict() for chat in chats])

@app.route('/chat/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    ChatMessage.query.filter_by(chat_id=chat_id).delete()
    db.session.delete(chat)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
