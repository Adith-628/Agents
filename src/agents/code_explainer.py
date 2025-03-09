from typing import Dict
import re
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

def create_code_explainer_agent():
    def explain_code(state: AgentState) -> AgentState:
        """Code explainer agent that analyzes and explains code snippets"""
        
        with console.status("[bold blue]Analyzing code...", spinner="dots") as status:
            try:
                # Get the code from the last message
                code_content = state["messages"][-1]["content"]
                
                # Extract code blocks if they exist
                code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', code_content, re.DOTALL)
                
                if not code_blocks:
                    # If no code blocks found, treat the entire content as code
                    code_blocks = [code_content]
                
                explanations = []
                
                for code_block in code_blocks:
                    # Detect programming language
                    language_hints = {
                        'def ': 'Python',
                        'function ': 'JavaScript',
                        'class ': 'Object-Oriented Code',
                        'import ': 'Python',
                        'console.': 'JavaScript',
                        'print': 'Python',
                        'var ': 'JavaScript',
                        'let ': 'JavaScript',
                        'const ': 'JavaScript'
                    }
                    
                    detected_language = 'Code'
                    for hint, lang in language_hints.items():
                        if hint in code_block:
                            detected_language = lang
                            break
                    
                    response = co.generate(
                        prompt=f"""Analyze this {detected_language} code and provide:
                        1. A high-level overview of what the code does
                        2. Key components and their purposes
                        3. Potential improvements or best practices
                        4. Any security considerations
                        
                        Code:
                        {code_block}
                        """,
                        max_tokens=500,
                        temperature=0.7,
                    )
                    
                    explanations.append(response.generations[0].text.strip())
                
                # Combine all explanations
                final_explanation = "\n\n".join(explanations)
                
                state["code_explanation"] = final_explanation
                state["messages"].append({
                    "role": "assistant",
                    "content": final_explanation
                })
                
            except Exception as e:
                console.print(f"\n[red]Error in code explanation: {e}[/red]")
                state["messages"].append({
                    "role": "assistant",
                    "content": f"I encountered an error while analyzing the code: {str(e)}"
                })
        
        return state

    return explain_code 