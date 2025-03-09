from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import co

def create_playlist_generator_agent():
    def generate_playlist(state: AgentState) -> AgentState:
        """Music playlist generator that creates personalized playlists"""
        
        with console.status("[bold blue]Creating your playlist...", spinner="dots") as status:
            try:
                # Initialize state if needed
                if "messages" not in state:
                    state["messages"] = []
                
                # Get playlist state from state, initialize if None
                playlist_state = state.get("playlist_state", {})
                
                # If playlist state is empty or new conversation
                if not playlist_state or "current_question" not in playlist_state:
                    # Define questions
                    questions = [
                        "What genres do you enjoy? (e.g., Rock, Pop, Jazz, etc.)",
                        "Any favorite artists or bands?",
                        "What's your current mood? (e.g., Energetic, Relaxed, Focused, etc.)",
                        "What's the occasion? (e.g., Workout, Study, Party, etc.)",
                        "Any specific era preference? (e.g., 80s, 90s, Modern, etc.)",
                        "Preferred tempo? (Slow, Medium, Fast)",
                        "Any specific themes or topics you'd like in the lyrics?"
                    ]
                    
                    # Initialize new playlist state
                    state["playlist_state"] = {
                        "current_question": 0,
                        "questions": questions,
                        "answers": {}
                    }
                    playlist_state = state["playlist_state"]
                    
                    # Add the initial question
                    state["messages"].append({
                        "role": "assistant",
                        "content": "Let's create your perfect playlist! I'll ask you a few questions.\n\n" + questions[0]
                    })
                    return state
                
                # Get current question and answers
                current_question = playlist_state.get("current_question", 0)
                questions = playlist_state.get("questions", [])
                answers = playlist_state.get("answers", {})
                
                # Validate state
                if not questions:
                    raise ValueError("Questions list is empty")
                
                # Get the last user message
                user_messages = [msg for msg in state.get("messages", []) if msg.get("role") == "user"]
                if not user_messages:
                    raise ValueError("No user message found")
                
                # Store the answer to the current question
                user_answer = user_messages[-1]["content"]
                answers[questions[current_question]] = user_answer
                playlist_state["answers"] = answers
                
                if current_question < len(questions) - 1:
                    # Move to next question
                    current_question += 1
                    playlist_state["current_question"] = current_question
                    state["playlist_state"] = playlist_state
                    
                    # Add next question
                    state["messages"].append({
                        "role": "assistant",
                        "content": questions[current_question]
                    })
                    return state
                
                # All questions answered, generate playlist
                prompt = f"""Create a personalized music playlist based on these preferences:

                Genre Preferences: {answers[questions[0]]}
                Favorite Artists: {answers[questions[1]]}
                Current Mood: {answers[questions[2]]}
                Occasion: {answers[questions[3]]}
                Era Preference: {answers[questions[4]]}
                Tempo Preference: {answers[questions[5]]}
                Lyrical Themes: {answers[questions[6]]}

                Create a curated playlist with:
                1. 15-20 song recommendations
                2. Brief explanation for each song choice
                3. How it matches the preferences
                4. Suggested listening order
                5. Any special notes or transitions between songs"""

                response = co.generate(
                    prompt=prompt,
                    max_tokens=1000,
                    temperature=0.7,
                )
                
                playlist = response.generations[0].text.strip()
                
                # Store the generated playlist and preferences
                state["playlist_results"] = {
                    "preferences": answers,
                    "playlist": playlist
                }
                
                # Store preferences before clearing playlist state
                state["music_preferences"] = answers
                # Clear the questionnaire state
                state.pop("playlist_state", None)
                
                # Add the playlist to messages
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Here's your personalized playlist!\n\n{playlist}\n\n" +
                    "Would you like to:\n" +
                    "1. Save this playlist\n" +
                    "2. Generate another with different preferences\n" +
                    "3. Refine this playlist"
                })
                
            except Exception as e:
                console.print(f"\n[red]Error in playlist generation: {str(e)}[/red]")
                # Ensure messages list exists
                if "messages" not in state:
                    state["messages"] = []
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Sorry, I encountered an error while creating your playlist. Please try again."
                })
                # Reset the playlist state
                state["playlist_state"] = None
        
        return state

    return generate_playlist 