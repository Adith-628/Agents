from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

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