import requests
import os
import base64
from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import stability_api_key
from PIL import Image
from io import BytesIO

def create_image_generator_agent():
    def generate_image(state: AgentState) -> AgentState:
        """Generate image using Stability AI"""
        
        enhanced_prompt = state["enhanced_prompt"]
        
        with console.status("[bold green]Generating image...", spinner="dots") as status:
            try:
                # Using Stability AI API
                url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
                
                headers = {
                    "Authorization": f"Bearer {stability_api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                body = {
                    "text_prompts": [{"text": enhanced_prompt}],
                    "cfg_scale": 7,
                    "height": 512,
                    "width": 512,
                    "samples": 1,
                    "steps": 30,
                }
                
                response = requests.post(url, headers=headers, json=body)
                
                if response.status_code == 200:
                    # Create images directory if it doesn't exist
                    if not os.path.exists("generated_images"):
                        os.makedirs("generated_images")
                    
                    # Get the base64 image data and decode it
                    image_data = response.json()["artifacts"][0]["base64"]
                    image_bytes = base64.b64decode(image_data)
                    
                    # Generate unique filename
                    image_path = f"generated_images/image_{len(os.listdir('generated_images')) + 1}.png"
                    
                    # Save the image using binary write mode
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
                    
                    state["image_path"] = image_path
                    state["messages"].append({
                        "role": "assistant",
                        "content": f"Image generated and saved as: {image_path}\nPrompt used: {enhanced_prompt}"
                    })
                else:
                    error_msg = response.json().get('message', f"API returned status code: {response.status_code}")
                    raise Exception(error_msg)
                
            except Exception as e:
                console.print(f"\n[red]Error in image generation: {e}[/red]")
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Sorry, I encountered an error while generating the image: {str(e)}"
                })
        
        return state

    return generate_image 