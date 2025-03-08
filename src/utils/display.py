import time
from .console import console, clear_screen

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
                if state.get("workflow_type") == "research":
                    # Show research workflow output
                    if state and state.get("research_results"):
                        console.print("\n[bold magenta]Research Findings:[/bold magenta]")
                        console.print(state["research_results"])
                    
                    if state and state.get("analysis_results"):
                        console.print("\n[bold yellow]Analysis:[/bold yellow]")
                        console.print(state["analysis_results"])
                
                elif state.get("workflow_type") == "image":
                    # Show image generation workflow output
                    if state and state.get("enhanced_prompt"):
                        console.print("\n[bold magenta]Enhanced Prompt:[/bold magenta]")
                        console.print(state["enhanced_prompt"])
                    
                    if state and state.get("image_path"):
                        console.print("\n[bold yellow]Image Generated:[/bold yellow]")
                        console.print(f"Saved to: {state['image_path']}")
                
                console.print("\n[bold green]Final Response:[/bold green]")
                content = message["content"]
                for char in content:
                    console.print(char, end="", style="green")
                    time.sleep(0.01)
                console.print()
    
    console.print("\n[blue]-------------------[/blue]") 