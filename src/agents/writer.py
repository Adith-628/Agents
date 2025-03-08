from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

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