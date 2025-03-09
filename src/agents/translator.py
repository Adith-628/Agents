from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

def create_translator_agent():
    def translate(state: AgentState) -> AgentState:
        """Translator agent that handles multi-language translation"""
        
        with console.status("[bold blue]Translating...", spinner="dots") as status:
            try:
                text = state["messages"][-1]["content"]
                target_lang = state.get("target_language", "English")
                
                # Detect source language first
                detect_prompt = f"Detect the language of this text: {text}"
                detect_response = co.generate(
                    prompt=detect_prompt,
                    max_tokens=50,
                    temperature=0.3,
                )
                source_lang = detect_response.generations[0].text.strip()
                
                # Skip translation if source and target are the same
                if source_lang.lower() in target_lang.lower():
                    state["messages"].append({
                        "role": "assistant",
                        "content": f"The text is already in {target_lang}."
                    })
                    return state
                
                # Perform translation
                translate_prompt = f"""Translate this text from {source_lang} to {target_lang}:
                Original: {text}
                
                Provide:
                1. Translation
                2. Any cultural context or notes
                3. Alternative expressions if applicable"""
                
                response = co.generate(
                    prompt=translate_prompt,
                    max_tokens=500,
                    temperature=0.7,
                )
                
                translation = response.generations[0].text.strip()
                
                state["translation_results"] = {
                    "source_language": source_lang,
                    "target_language": target_lang,
                    "original_text": text,
                    "translated_text": translation
                }
                
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Translation ({source_lang} → {target_lang}):\n\n{translation}"
                })
                
            except Exception as e:
                console.print(f"\n[red]Error in translation: {e}[/red]")
                state["messages"].append({
                    "role": "assistant",
                    "content": "Sorry, I encountered an error while translating. Please try again."
                })
        
        return state
    

    return translate 