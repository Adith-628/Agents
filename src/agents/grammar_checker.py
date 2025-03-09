from typing import Dict
import re
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

def create_grammar_checker_agent():
    def check_grammar(state: AgentState) -> AgentState:
        """Grammar checker agent that analyzes and improves text"""
        
        with console.status("[bold blue]Checking grammar and style...", spinner="dots") as status:
            try:
                text = state["messages"][-1]["content"]
                check_type = state.get("check_type", "all")
                
                analysis_prompts = {
                    "grammar": "Check for grammatical errors and provide corrections.",
                    "style": "Analyze writing style and suggest improvements for clarity and impact.",
                    "tone": "Evaluate the tone and suggest adjustments for the intended audience.",
                    "all": "Provide a comprehensive analysis of grammar, style, and tone."
                }
                
                prompt = f"""Analyze this text and {analysis_prompts.get(check_type, analysis_prompts['all'])}

                Text: {text}
                
                Provide:
                1. Identified issues
                2. Suggested corrections
                3. Overall improvement recommendations
                4. Revised version of the text"""
                
                response = co.generate(
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.7,
                )
                
                analysis = response.generations[0].text.strip()
                
                state["grammar_analysis"] = {
                    "original_text": text,
                    "analysis": analysis,
                    "check_type": check_type
                }
                
                state["messages"].append({
                    "role": "assistant",
                    "content": analysis
                })
                
            except Exception as e:
                console.print(f"\n[red]Error in grammar checking: {e}[/red]")
                state["messages"].append({
                    "role": "assistant",
                    "content": "Sorry, I encountered an error while checking the text. Please try again."
                })
        
        return state

    return check_grammar 