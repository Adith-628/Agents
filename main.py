from langgraph.graph import Graph
from src.core.workflow import create_research_workflow, create_image_workflow, create_translation_workflow, create_grammar_workflow
from src.core.state import AgentState
from src.utils.console import console, clear_screen
from src.utils.display import print_chat_history
from src.agents.summarizer import create_summarizer_agent
from src.agents.code_explainer import create_code_explainer_agent
import re

def create_summary_workflow():
    """Create a workflow for text summarization"""
    workflow = Graph()
    
    # Create the summarizer function
    summarizer = create_summarizer_agent()
    
    # Add nodes to the graph
    workflow.add_node("summarizer", summarizer)
    workflow.add_node("output", lambda state: dict(state))
    
    # Set up the workflow
    workflow.set_entry_point("summarizer")
    workflow.add_edge("summarizer", "output")
    workflow.set_finish_point("output")
    
    # Return the compiled workflow
    return workflow.compile()

def create_code_explanation_workflow():
    """Create a workflow for code explanation"""
    workflow = Graph()
    
    # Create the code explainer function
    code_explainer = create_code_explainer_agent()
    
    # Add nodes to the graph
    workflow.add_node("code_explainer", code_explainer)
    workflow.add_node("output", lambda state: dict(state))
    
    # Set up the workflow
    workflow.set_entry_point("code_explainer")
    workflow.add_edge("code_explainer", "output")
    workflow.set_finish_point("output")
    
    # Return the compiled workflow
    return workflow.compile()

def main():
    # Create workflows
    research_chain = create_research_workflow()
    image_chain = create_image_workflow()
    summary_chain = create_summary_workflow()
    code_chain = create_code_explanation_workflow()
    translation_chain = create_translation_workflow()
    grammar_chain = create_grammar_workflow()
    
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
            console.print("3. [bold]Text Summarizer[/bold] - Create concise summaries")
            console.print("4. [bold]Code Explainer[/bold] - Analyze and explain code")
            console.print("5. [bold]Translator[/bold] - Translate between languages")
            console.print("6. [bold]Grammar Checker[/bold] - Check and improve text")
            console.print("7. [bold]Exit[/bold]")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "7":
                console.print("\n[yellow]Thank you for using the AI Assistant! Goodbye![/yellow]")
                break
            elif choice == "1":
                current_workflow = ("research", research_chain)
                console.print("\n[green]Research Assistant activated! Ask me anything...[/green]")
            elif choice == "2":
                current_workflow = ("image", image_chain)
                console.print("\n[green]Image Generator activated! Describe the image you want to create...[/green]")
                console.print("""[dim]Tips:
- Use 'style:TYPE' to specify style (e.g. 'style:Anime')
- Use 'samples:N' for multiple images (max 4)
- Use 'size:WxH' for custom dimensions[/dim]""")
            elif choice == "3":
                current_workflow = ("summary", summary_chain)
                console.print("\n[green]Text Summarizer activated! Paste the text you want to summarize...[/green]")
                console.print("[dim]Type 'short' or 'long' after summary to see different lengths[/dim]")
            elif choice == "4":
                current_workflow = ("code", code_chain)
                console.print("\n[green]Code Explainer activated! Paste your code...[/green]")
                console.print("[dim]You can paste code directly or use markdown code blocks[/dim]")
            elif choice == "5":
                current_workflow = ("translation", translation_chain)
                console.print("\n[green]Translator activated![/green]")
                console.print("""[dim]Format: text to translate | target language
Example: Hello, how are you? | Spanish[/dim]""")
            elif choice == "6":
                current_workflow = ("grammar", grammar_chain)
                console.print("\n[green]Grammar Checker activated![/green]")
                console.print("""[dim]Add flags for specific checks:
--grammar: Grammar only
--style: Writing style
--tone: Tone analysis[/dim]""")
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
            
            # Initialize variables with default values
            style = None
            samples = 1
            width = 512
            height = 512
            check_type = "all"
            target_lang = None
            summary_type = None
            
            # Process special commands for image generation
            if current_workflow[0] == "image":
                # Parse style preference (handle common typos)
                style_match = re.search(r'st?yle:(\w+)', user_input, re.IGNORECASE)  # Matches both 'style:' and 'syle:'
                if style_match:
                    style = style_match.group(1)
                    user_input = re.sub(r'st?yle:\w+', '', user_input, flags=re.IGNORECASE).strip()
                    
                # Parse number of samples
                samples_match = re.search(r'samples:(\d+)', user_input)
                if samples_match:
                    samples = min(int(samples_match.group(1)), 4)
                    user_input = re.sub(r'samples:\d+', '', user_input).strip()
                    
                # Parse image dimensions
                size_match = re.search(r'size:(\d+)x(\d+)', user_input)
                if size_match:
                    width = min(int(size_match.group(1)), 1024)
                    height = min(int(size_match.group(2)), 1024)
                    user_input = re.sub(r'size:\d+x\d+', '', user_input).strip()
            
            # Process special commands for summarizer
            elif current_workflow[0] == "summary":
                last_word = user_input.split()[-1].lower()
                if last_word in ['short', 'long']:
                    summary_type = last_word
                    user_input = ' '.join(user_input.split()[:-1])
            
            # Process translation input
            elif current_workflow[0] == "translation":
                parts = user_input.split("|")
                if len(parts) > 1:
                    text = parts[0].strip()
                    target_lang = parts[1].strip()
                    user_input = text
            
            # Process grammar checker flags
            elif current_workflow[0] == "grammar":
                if "--grammar" in user_input:
                    check_type = "grammar"
                    user_input = user_input.replace("--grammar", "").strip()
                elif "--style" in user_input:
                    check_type = "style"
                    user_input = user_input.replace("--style", "").strip()
                elif "--tone" in user_input:
                    check_type = "tone"
                    user_input = user_input.replace("--tone", "").strip()
            
            # Create initial state with chat history and new message
            initial_state = AgentState(
                messages=chat_history + [{
                    "role": "user",
                    "content": user_input
                }],
                current_task="process",
                task_status="in_progress",
                workflow_type=current_workflow[0],
                # Add additional state for all workflows
                style_preference=style,
                num_samples=samples,
                image_width=width,
                image_height=height,
                target_language=target_lang,
                check_type=check_type
            )
            
            # Run the workflow
            if current_workflow[1] is not None:
                result = dict(current_workflow[1].invoke(initial_state))
                
                # Handle summary type selection after generation
                if current_workflow[0] == "summary" and "summaries" in result:
                    if summary_type and summary_type in result["summaries"]:
                        result["messages"][-1]["content"] = f"Here's the {summary_type} summary:\n\n{result['summaries'][summary_type]}"
                
                # Update chat history and display
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