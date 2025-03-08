from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

def create_prompt_enhancer_agent():
    def enhance_prompt(state: AgentState) -> AgentState:
        """Interactive prompt enhancement agent"""
        
        initial_prompt = state["messages"][-1]["content"]
        
        # Questions to refine the image concept
        questions = [
            {
                "question": "What style would you like for the image?",
                "options": [
                    "Photorealistic",
                    "Digital Art",
                    "Oil Painting",
                    "Watercolor",
                    "Anime/Manga",
                    "3D Rendered",
                    "Sketch",
                    "Other (please specify)"
                ]
            },
            {
                "question": "What mood or atmosphere should the image convey?",
                "options": [
                    "Bright and Cheerful",
                    "Dark and Moody",
                    "Peaceful/Serene",
                    "Dramatic",
                    "Mysterious",
                    "Other (please specify)"
                ]
            },
            {
                "question": "Any specific color palette preferences?",
                "options": [
                    "Warm Colors",
                    "Cool Colors",
                    "Monochromatic",
                    "Vibrant/Colorful",
                    "Pastel",
                    "Other (please specify)"
                ]
            },
            {
                "question": "What should be the main focus or perspective?",
                "options": [
                    "Close-up",
                    "Wide Shot",
                    "Bird's Eye View",
                    "First Person",
                    "Other (please specify)"
                ]
            }
        ]
        
        # Gather user preferences
        preferences = {}
        console.print("\n[bold magenta]Let's refine your image concept![/bold magenta]")
        console.print(f"Initial concept: [cyan]{initial_prompt}[/cyan]\n")
        
        for q in questions:
            console.print(f"\n[bold yellow]{q['question']}[/bold yellow]")
            for i, option in enumerate(q['options'], 1):
                console.print(f"{i}. {option}")
            
            while True:
                try:
                    choice = input("\nEnter your choice (number): ").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(q['options']):
                        selected = q['options'][int(choice) - 1]
                        if selected.startswith("Other"):
                            custom = input("Please specify: ").strip()
                            preferences[q['question']] = custom
                        else:
                            preferences[q['question']] = selected
                        break
                    else:
                        console.print("[red]Please enter a valid number[/red]")
                except ValueError:
                    console.print("[red]Please enter a valid number[/red]")
        
        # Additional details
        console.print("\n[bold yellow]Any additional details you'd like to add? (press Enter to skip)[/bold yellow]")
        additional_details = input().strip()
        
        # Construct the enhanced prompt
        with console.status("[bold blue]Enhancing prompt...", spinner="dots") as status:
            try:
                prompt_template = f"""
                Original concept: {initial_prompt}
                Style: {preferences.get('What style would you like for the image?')}
                Mood: {preferences.get('What mood or atmosphere should the image convey?')}
                Colors: {preferences.get('Any specific color palette preferences?')}
                Perspective: {preferences.get('What should be the main focus or perspective?')}
                Additional details: {additional_details if additional_details else 'None'}
                
                Based on these preferences, create a detailed and creative image generation prompt.
                Focus on creating a cohesive and vivid description that incorporates all the specified elements.
                Make it detailed but keep it concise and clear.
                """
                
                response = co.generate(
                    prompt=prompt_template,
                    max_tokens=300,
                    temperature=0.7,
                )
                
                enhanced_prompt = response.generations[0].text.strip()
                state["enhanced_prompt"] = enhanced_prompt
                
                # Show the enhanced prompt to the user
                console.print("\n[bold green]Enhanced Prompt:[/bold green]")
                console.print(enhanced_prompt)
                
                # Ask for confirmation
                while True:
                    confirm = input("\nWould you like to proceed with this prompt? (yes/no): ").lower().strip()
                    if confirm in ['yes', 'y']:
                        break
                    elif confirm in ['no', 'n']:
                        console.print("\n[yellow]Let's try again![/yellow]")
                        return enhance_prompt(state)  # Restart the process
                    else:
                        console.print("[red]Please enter 'yes' or 'no'[/red]")
                
            except Exception as e:
                console.print(f"\n[red]Error in prompt enhancement: {e}[/red]")
                state["enhanced_prompt"] = initial_prompt  # Fallback to original prompt
        
        return state

    return enhance_prompt 