# Fitness Chatbot - Your Personal Fitness Assistant

Welcome to the Fitness Chatbot project! This is an interactive, web-based chatbot designed to assist users with fitness-related queries, including BMI calculations, meal nutrition estimates (calories and protein), and general fitness tips. Built with Python, Flask, LangChain, and Groq’s `mixtral-8x7b-32768` model, it features a sleek, responsive, and visually appealing user interface tailored for fitness enthusiasts.

## Features

- **BMI Calculator**: Calculate your Body Mass Index (BMI) accurately using height and weight inputs, with contextual health advice.
- **Nutritional Insights**: Provide estimated calories and protein for meals, along with nutritional tips to support fitness goals.
- **Conversation Memory**: Maintains context across interactions, allowing follow-up questions and personalized responses.
- **Stunning UI**: Full-screen, responsive design with modern aesthetics, using a fitness-inspired color palette (#393449 dark purple and #F7F7F0 off-white, accented with green #4CAF50 and blue #2196F3).
- **Easy Accessibility**: Runs locally via a Flask server, accessible through any web browser on desktops, tablets, or mobiles.

## Getting Started

Follow these steps to set up and run the Fitness Chatbot on your local machine.

### Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)
- A Groq API key (required for the language model)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/fitness-chatbot.git
   cd fitness-chatbot

2. **Create Virtual Environment**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies Install the required Python packages using pip:**
   ```bash
   pip install flask langchain langchain-groq groq python-dotenv

4. **Set Up Your Groq API Key**
  Create a .env file in the project root:
  ```bash
  GROQ_API_KEY=your_groq_api_key_here
  ```
  Replace your_groq_api_key_here with your actual Groq API key (obtainable from the Groq website).

5.**Run the Application Start the Flask server**
6. **Access the Chatbot Open your web browser and navigate to http://127.0.0.1:5000 to interact with the chatbot.**

# Project Structure
```bash
fitness-chatbot/
├── fitness_chatbot.py      # Flask backend with chatbot logic
├── static/
│   ├── index.html          # HTML for the chatbot UI
│   ├── style.css           # CSS for styling the UI
│   └── script.js           # JavaScript for frontend interactivity
├── .env                    # Environment variables (e.g., Groq API key)
└── README.md               # This file

```

# Usage
Type fitness-related queries into the input field, such as:
“I am 180cm tall and weigh 83kg. What is my BMI?”
“How many calories are in a turkey and cheese sandwich on whole grain bread and an apple?”
“Can you suggest a workout plan for weight loss?”
The chatbot will respond with formatted, context-aware answers, remembering previous interactions for follow-ups.

# Acknowledgments
Thanks to the LangChain and Groq communities for their powerful tools and models.
Inspiration drawn from fitness apps and AI chatbots for a user-friendly design.
