import cohere
from typing import Dict, TypedDict
from langgraph.graph import Graph
from dotenv import load_dotenv
import os
import time
import sys

# Load environment variables
load_dotenv()

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Define our message structure
class MessageDict(TypedDict):
    role: str
    content: str

# Define our agent state
class AgentState(TypedDict):
    messages: list[MessageDict]
    current_task: str
    task_status: str

def create_researcher_agent():
    def research(state: AgentState) -> AgentState:
        """Research agent that uses Cohere to analyze and respond to queries"""
        
        # Get the last message
        last_message = state["messages"][-1]["content"]
        
        print("\nThinking", end="")
        sys.stdout.flush()
        
        try:
            # Generate response using Cohere
            response = co.generate(
                prompt=f"As a helpful AI assistant, please respond to: {last_message}",
                max_tokens=300,
                temperature=0.7,
            )
            
            # Clear the thinking animation
            print("\r" + " " * 20 + "\r", end="")
            print("Generating response...\n")
            
            # Add the response to messages
            state["messages"].append({
                "role": "assistant",
                "content": response.generations[0].text.strip()
            })
            
        except Exception as e:
            print("\r" + " " * 20 + "\r", end="")
            print(f"Error generating response: {e}")
            
        return state

    return research

def create_workflow():
    workflow = Graph()
    workflow.add_node("researcher", create_researcher_agent())
    workflow.set_entry_point("researcher")
    
    def return_state(state: AgentState) -> Dict:
        return dict(state)
    
    workflow.add_node("output", return_state)
    workflow.add_edge("researcher", "output")
    workflow.set_finish_point("output")
    
    return workflow.compile()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_loading():
    chars = "/—\\|"
    for char in chars:
        sys.stdout.write('\r' + 'Processing ' + char)
        sys.stdout.flush()
        time.sleep(0.1)

def print_chat_history(messages, animate_last=False):
    clear_screen()
    print("\n=== Chat History ===")
    print("-------------------")
    
    # Print all messages except the last one if animating
    messages_to_print = messages[:-1] if animate_last else messages
    
    # Print previous messages normally
    for message in messages_to_print:
        role = "You" if message["role"] == "user" else "Assistant"
        print(f"\n{role}:")
        print(message["content"])
    
    # If animating, print the last message with typing effect
    if animate_last and messages:
        last_message = messages[-1]
        role = "You" if last_message["role"] == "user" else "Assistant"
        print(f"\n{role}:")
        if role == "Assistant":
            print("\n--- Latest Response ---")
            for char in last_message["content"]:
                print(char, end='', flush=True)
                time.sleep(0.01)  # Adjust speed as needed
            print("\n-------------------")
        else:
            print(last_message["content"])

def main():
    # Create the workflow
    chain = create_workflow()
    
    # Initialize empty chat history
    chat_history = []
    
    clear_screen()
    print("\n=== Welcome to the AI Research Assistant! ===")
    print("\nCommands:")
    print("- Type 'quit' or 'exit' to end the conversation")
    print("- Type 'clear' to clear the chat history")
    print("- Press Ctrl+C to exit at any time")
    print("\nReady to chat! Ask me anything...\n")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit']:
                print("\nThank you for chatting! Goodbye!")
                break
            
            # Check for clear command
            if user_input.lower() == 'clear':
                chat_history = []
                clear_screen()
                continue
            
            # Skip empty inputs
            if not user_input:
                continue
            
            print("\nProcessing your request...")
            
            # Create initial state with chat history and new message
            initial_state = AgentState(
                messages=chat_history + [{
                    "role": "user",
                    "content": user_input
                }],
                current_task="research",
                task_status="in_progress"
            )
            
            # Run the workflow
            result = dict(chain.invoke(initial_state))
            
            # Update chat history and display
            if result and "messages" in result:
                chat_history = result["messages"]
                # Show full history with animation for the last message
                print_chat_history(chat_history, animate_last=True)
            
        except KeyboardInterrupt:
            print("\n\nGracefully shutting down...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main() 