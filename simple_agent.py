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
    research_results: str  # Add this to store research findings
    analysis_results: str  # Add this to store analysis
    final_response: str    # Add this to store final response

def create_researcher_agent():
    def research(state: AgentState) -> AgentState:
        """Research agent that gathers information"""
        
        last_message = state["messages"][-1]["content"]
        
        with console.status("[bold green]Researching...", spinner="dots") as status:
            try:
                response = co.generate(
                    prompt=f"""As a research agent, gather and summarize key information about: {last_message}
                    Focus on collecting factual information and important details.""",
                    max_tokens=300,
                    temperature=0.7,
                )
                
                state["research_results"] = response.generations[0].text.strip()
                
            except Exception as e:
                console.print(f"\n[red]Error in research: {e}[/red]")
        
        return state

    return research

def create_analyzer_agent():
    def analyze(state: AgentState) -> AgentState:
        """Analyzer agent that processes research results"""
        
        with console.status("[bold blue]Analyzing...", spinner="dots") as status:
            try:
                response = co.generate(
                    prompt=f"""As an analytical agent, analyze this research: {state['research_results']}
                    Identify patterns, implications, and draw meaningful conclusions.""",
                    max_tokens=300,
                    temperature=0.7,
                )
                
                state["analysis_results"] = response.generations[0].text.strip()
                
            except Exception as e:
                console.print(f"\n[red]Error in analysis: {e}[/red]")
        
        return state

    return analyze

def create_writer_agent():
    def write(state: AgentState) -> AgentState:
        """Writer agent that creates the final response"""
        
        with console.status("[bold yellow]Composing response...", spinner="dots") as status:
            try:
                response = co.generate(
                    prompt=f"""As a writing agent, create a well-structured response using:
                    Research: {state['research_results']}
                    Analysis: {state['analysis_results']}
                    Make it engaging and easy to understand.""",
                    max_tokens=300,
                    temperature=0.7,
                )
                
                state["messages"].append({
                    "role": "assistant",
                    "content": response.generations[0].text.strip()
                })
                
            except Exception as e:
                console.print(f"\n[red]Error in writing: {e}[/red]")
        
        return state

    return write

def create_workflow():
    workflow = Graph()
    
    # Add all agents
    workflow.add_node("researcher", create_researcher_agent())
    workflow.add_node("analyzer", create_analyzer_agent())
    workflow.add_node("writer", create_writer_agent())
    workflow.add_node("output", lambda state: dict(state))
    
    # Set the entry point
    workflow.set_entry_point("researcher")
    
    # Connect the agents in sequence
    workflow.add_edge("researcher", "analyzer")
    workflow.add_edge("analyzer", "writer")
    workflow.add_edge("writer", "output")
    
    workflow.set_finish_point("output")
    
    return workflow.compile()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_chat_history(messages, state=None):
    clear_screen()
    console.print("\n[bold blue]=== Chat History ===[/bold blue]")
    console.print("[blue]-------------------[/blue]")
    
    # Print all previous messages normally
    if len(messages) > 2:
        for message in messages[:-2]:
            role = "[bold cyan]You[/bold cyan]" if message["role"] == "user" else "[bold green]Assistant[/bold green]"
            console.print(f"\n{role}:")
            console.print(message["content"])
    
    # Print the latest exchange with details
    if messages:
        latest_messages = messages[-2:] if len(messages) >= 2 else messages
        
        for message in latest_messages:
            if message["role"] == "user":
                console.print(f"\n[bold cyan]You:[/bold cyan]")
                console.print(f"{message['content']}")
            else:
                # Show the work of each agent if available
                if state and state.get("research_results"):
                    console.print("\n[bold magenta]Research Findings:[/bold magenta]")
                    console.print(state["research_results"])
                
                if state and state.get("analysis_results"):
                    console.print("\n[bold yellow]Analysis:[/bold yellow]")
                    console.print(state["analysis_results"])
                
                console.print("\n[bold green]Final Response:[/bold green]")
                content = message["content"]
                for char in content:
                    console.print(char, end="", style="green")
                    time.sleep(0.01)
                console.print()
    
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
            
            # Update chat history and display with state
            if result and "messages" in result:
                chat_history = result["messages"]
                print_chat_history(chat_history, result)
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Gracefully shutting down...[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]An error occurred: {e}[/red]")
            console.print("Please try again.")

if __name__ == "__main__":
    main() 