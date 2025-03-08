from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
import cohere
from ..config.settings import co

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