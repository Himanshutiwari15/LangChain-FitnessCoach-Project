from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain.tools import tool

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define the BMI calculation tool
@tool
def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate the Body Mass Index (BMI) given height in centimeters and weight in kilograms."""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

# Bind tools to the language model
tools = [calculate_bmi]
llm_with_tools = llm.bind_tools(tools)

# Set up the system message
system_message = SystemMessage(content="""You are a fitness chatbot. You can engage in general fitness-related conversations. 
When asked about BMI, use the provided tool to calculate it accurately. 
When asked about the calories and protein in a meal, provide estimated values based on common nutritional knowledge. 
If the meal description is unclear, ask for more details.""")

# Initialize conversation history
conversation_history = [system_message]

# Define the chatbot response function
def chatbot_response(user_input):
    conversation_history.append(HumanMessage(content=user_input))
    
    while True:
        response = llm_with_tools.invoke(conversation_history)
        
        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                if tool_name == "calculate_bmi":
                    # Correctly invoke the tool
                    result = calculate_bmi.invoke(tool_args)
                    conversation_history.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
                else:
                    conversation_history.append(ToolMessage(content="Error: Unknown tool", tool_call_id=tool_call["id"]))
        else:
            conversation_history.append(AIMessage(content=response.content))
            return response.content

# Interactive loop for user input
if __name__ == "__main__":
    # Print a welcome message
    print("Welcome to the Fitness Chatbot! Ask me about BMI, meal nutrition, or general fitness. Type 'quit' to exit.")
    
    # Start the conversation loop
    while True:
        # Get user input from the terminal
        user_input = input("You: ").strip()
        
        # Check if the user wants to quit
        if user_input.lower() in ["quit", "exit"]:
            print("Assistant: Goodbye!")
            break
        
        # Get the chatbot's response and print it
        response = chatbot_response(user_input)
        print(f"Assistant: {response}")