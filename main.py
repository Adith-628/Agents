from src.core.workflow import create_research_workflow, create_image_workflow
from src.core.state import AgentState
from src.utils.console import console, clear_screen
from src.utils.display import print_chat_history

def main():
    # Create workflows
    research_chain = create_research_workflow()
    image_chain = create_image_workflow()
    
    # Initialize empty chat history
    chat_history = []
    current_workflow = None
    
    clear_screen()
    console.print("\n[bold blue]=== Welcome to the AI Assistant! ===[/bold blue]")
    
    while True:
        if not current_workflow:
            console.print("\n[yellow]Please select a workflow:[/yellow]")
            console.print("1. [bold]Research Assistant[/bold] - Research and analyze topics")
            console.print("2. [bold]Image Generator[/bold] - Generate images from descriptions")
            console.print("3. [bold]Exit[/bold]")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "3":
                console.print("\n[yellow]Thank you for using the AI Assistant! Goodbye![/yellow]")
                break
            elif choice == "1":
                current_workflow = ("research", research_chain)
                console.print("\n[green]Research Assistant activated! Ask me anything...[/green]")
            elif choice == "2":
                current_workflow = ("image", image_chain)
                console.print("\n[green]Image Generator activated! Describe the image you want to create...[/green]")
            else:
                console.print("\n[red]Invalid choice. Please try again.[/red]")
                continue
        
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                current_workflow = None
                chat_history = []
                clear_screen()
                continue
            
            if user_input.lower() == 'clear':
                chat_history = []
                clear_screen()
                continue
            
            if not user_input:
                continue
            
            # Create initial state with chat history and new message
            initial_state = AgentState(
                messages=chat_history + [{
                    "role": "user",
                    "content": user_input
                }],
                current_task="process",
                task_status="in_progress",
                workflow_type=current_workflow[0]
            )
            
            # Run the workflow
            result = dict(current_workflow[1].invoke(initial_state))
            
            # Update chat history and display with state
            if result and "messages" in result:
                chat_history = result["messages"]
                print_chat_history(chat_history, result)
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Returning to workflow selection...[/yellow]")
            current_workflow = None
            chat_history = []
        except Exception as e:
            console.print(f"\n[red]An error occurred: {e}[/red]")
            console.print("Please try again.")

if __name__ == "__main__":
    main() 