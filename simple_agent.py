import cohere
from typing import Dict, TypedDict
from langgraph.graph import Graph
from dotenv import load_dotenv
import os
import time
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner

# Initialize Rich console for better formatting
console = Console()

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
        
        # Use console.status() for the spinner
        with console.status("[bold green]Thinking...", spinner="dots") as status:
            try:
                # Generate response using Cohere
                response = co.generate(
                    prompt=f"As a helpful AI assistant, please respond to: {last_message}",
                    max_tokens=300,
                    temperature=0.7,
                )
                
                # Add the response to messages
                state["messages"].append({
                    "role": "assistant",
                    "content": response.generations[0].text.strip()
                })
                
            except Exception as e:
                console.print(f"\n[red]Error generating response: {e}[/red]")
        
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

def print_chat_history(messages):
    clear_screen()
    console.print("\n[bold blue]=== Chat History ===[/bold blue]")
    console.print("[blue]-------------------[/blue]")
    
    # Print all previous messages normally
    if len(messages) > 2:
        for message in messages[:-2]:  # All messages except the last exchange
            role = "[bold cyan]You[/bold cyan]" if message["role"] == "user" else "[bold green]Assistant[/bold green]"
            console.print(f"\n{role}:")
            console.print(message["content"])
    
    # Print the latest exchange with animation for assistant's response
    if messages:
        # Get the last exchange
        latest_messages = messages[-2:] if len(messages) >= 2 else messages
        
        for message in latest_messages:
            if message["role"] == "user":
                console.print(f"\n[bold cyan]You:[/bold cyan]")
                console.print(f"{message['content']}")
            else:
                console.print("\n[bold green]Assistant:[/bold green]")
                console.print("[bold yellow]--- Latest Response ---[/bold yellow]")
                # Print the assistant's response character by character
                content = message["content"]
                for char in content:
                    console.print(char, end="", style="green")
                    time.sleep(0.01)
                console.print()
                console.print("[bold yellow]-------------------[/bold yellow]")
    
    console.print("\n[blue]-------------------[/blue]")

def main():
    # Create the workflow
    chain = create_workflow()
    
    # Initialize empty chat history
    chat_history = []
    
    clear_screen()
    console.print("\n[bold blue]=== Welcome to the AI Research Assistant! ===[/bold blue]")
    console.print("\n[yellow]Commands:[/yellow]")
    console.print("- Type [bold]'quit'[/bold] or [bold]'exit'[/bold] to end the conversation")
    console.print("- Type [bold]'clear'[/bold] to clear the chat history")
    console.print("- Press [bold]Ctrl+C[/bold] to exit at any time")
    console.print("\n[green]Ready to chat! Ask me anything...[/green]\n")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit']:
                console.print("\n[yellow]Thank you for chatting! Goodbye![/yellow]")
                break
            
            # Check for clear command
            if user_input.lower() == 'clear':
                chat_history = []
                clear_screen()
                continue
            
            # Skip empty inputs
            if not user_input:
                continue
            
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
                print_chat_history(chat_history)
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Gracefully shutting down...[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]An error occurred: {e}[/red]")
            console.print("Please try again.")

if __name__ == "__main__":
    main() 