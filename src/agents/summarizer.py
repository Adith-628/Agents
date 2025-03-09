from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

def create_summarizer_agent():
    def summarize(state: AgentState) -> AgentState:
        """Summarizer agent that creates concise summaries of long texts"""
        
        with console.status("[bold blue]Summarizing...", spinner="dots") as status:
            try:
                # Get the text to summarize
                text_to_summarize = state["messages"][-1]["content"]
                
                # Handle empty or invalid input
                if not text_to_summarize or len(text_to_summarize.strip()) < 10:
                    raise ValueError("Text is too short to summarize")

                # Create summary with different lengths
                summaries = {}
                
                # Generate summaries of different lengths
                for length in ["short", "medium", "long"]:
                    tokens = 100 if length == "short" else 200 if length == "medium" else 300
                    
                    response = co.generate(
                        prompt=f"""Create a {length} summary of this text: {text_to_summarize}
                        Focus on the most important points and maintain coherence.
                        For a {length} summary, be {'very concise' if length == 'short' 
                        else 'moderately detailed' if length == 'medium' 
                        else 'comprehensive'}.""",
                        max_tokens=tokens,
                        temperature=0.7,
                    )
                    
                    summaries[length] = response.generations[0].text.strip()
                
                state["summaries"] = summaries
                
                # Add the medium summary to messages by default
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Here's a summary:\n\n{summaries['medium']}\n\n" +
                    "(Type 'short' or 'long' to see other summary lengths)"
                })
                
            except ValueError as ve:
                console.print(f"\n[yellow]Warning: {ve}[/yellow]")
                state["messages"].append({
                    "role": "assistant",
                    "content": "The provided text is too short to summarize meaningfully."
                })
            except Exception as e:
                console.print(f"\n[red]Error in summarization: {e}[/red]")
                state["messages"].append({
                    "role": "assistant",
                    "content": "I encountered an error while creating the summary. Please try again."
                })
        
        return state

    return summarize 