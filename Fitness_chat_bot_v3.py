# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
# from langchain.tools import tool
# from flask import Flask, request, jsonify

# # Load environment variables
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize the language model
# llm = ChatGroq(
#     model="mixtral-8x7b-32768",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )

# # Define the BMI calculation tool
# @tool
# def calculate_bmi(height_cm: float, weight_kg: float) -> float:
#     """Calculate the Body Mass Index (BMI) given height in centimeters and weight in kilograms."""
#     height_m = height_cm / 100
#     bmi = weight_kg / (height_m ** 2)
#     return round(bmi, 2)

# # Bind tools to the language model
# tools = [calculate_bmi]
# llm_with_tools = llm.bind_tools(tools)

# # Set up the system message
# system_message = SystemMessage(content="""You are a fitness chatbot. You can engage in general fitness-related conversations. 
# When asked about BMI, use the provided tool to calculate it accurately. 
# When asked about the calories and protein in a meal, provide estimated values based on common nutritional knowledge. 
# If the meal description is unclear, ask for more details. Respond only with a JSON tool call object or the final answer, without additional text or XML tags like <tool-use>.""")

# # Initialize conversation history
# conversation_history = [system_message]

# # Define the chatbot response function
# def chatbot_response(user_input):
#     conversation_history.append(HumanMessage(content=user_input))
    
#     while True:
#         response = llm_with_tools.invoke(conversation_history)
        
#         # Check if the response has tool calls
#         if hasattr(response, 'tool_calls') and response.tool_calls:
#             for tool_call in response.tool_calls:
#                 tool_name = tool_call["name"]
#                 tool_args = tool_call["args"]
                
#                 if tool_name == "calculate_bmi":
#                     try:
#                         # Ensure tool_args is a dict and extract parameters
#                         if isinstance(tool_args, dict):
#                             height_cm = float(tool_args.get('height_cm', 0))
#                             weight_kg = float(tool_args.get('weight_kg', 0))
#                             # Ensure non-negative values
#                             if height_cm <= 0 or weight_kg <= 0:
#                                 raise ValueError("Height and weight must be positive numbers")
#                             result = calculate_bmi.invoke({"height_cm": height_cm, "weight_kg": weight_kg})
#                         else:
#                             raise ValueError("Invalid tool arguments format")
#                         conversation_history.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
#                     except (ValueError, TypeError) as e:
#                         conversation_history.append(ToolMessage(content=f"Error: {str(e)}", tool_call_id=tool_call["id"]))
#                         return f"Error: {str(e)}"
#                 else:
#                     conversation_history.append(ToolMessage(content="Error: Unknown tool", tool_call_id=tool_call["id"]))
#                     return "Error: Unknown tool"
#         else:
#             # If no tool calls, return the final response
#             if hasattr(response, 'content') and response.content:
#                 conversation_history.append(AIMessage(content=response.content))
#                 return response.content
#             else:
#                 return "Error: No response generated by the model."

# # Flask API endpoint
# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     user_input = data.get('message', '')
#     if not user_input:
#         return jsonify({'error': 'No message provided'}), 400
#     try:
#         response = chatbot_response(user_input)
#         return jsonify({'response': response})
#     except Exception as e:
#         return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# # Serve the HTML file
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

# if __name__ == "__main__":
#     app.run(debug=True)


from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize the language model (without tools)
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Set up the system message (updated to handle BMI and nutrition without tools)
system_message = SystemMessage(content="""You are a fitness chatbot. You can engage in general fitness-related conversations. 
When asked about BMI, calculate it accurately using the formula: BMI = weight (kg) / (height (m)²), where height is in meters (convert cm to m by dividing by 100). 
When asked about the calories and protein in a meal, provide estimated values based on common nutritional knowledge. 
If the meal description is unclear, ask for more details. Provide concise, accurate, and friendly responses.""")

# Initialize conversation history
conversation_history = [system_message]

# Define the chatbot response function
def chatbot_response(user_input):
    conversation_history.append(HumanMessage(content=user_input))
    
    response = llm.invoke(conversation_history)
    
    if hasattr(response, 'content') and response.content:
        conversation_history.append(AIMessage(content=response.content))
        return response.content
    else:
        return "Error: No response generated by the model."

# Flask API endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    try:
        response = chatbot_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# Serve the HTML file
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True)