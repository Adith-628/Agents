import requests
import os
import base64
from typing import Dict
from ..core.state import AgentState
from ..utils.console import console
from ..config.settings import stability_api_key
from PIL import Image
from io import BytesIO
from datetime import datetime

def create_image_generator_agent():
    def generate_image(state: AgentState) -> AgentState:
        """Generate image using Stability AI with enhanced features"""
        
        enhanced_prompt = state["enhanced_prompt"]
        
        with console.status("[bold green]Generating image...", spinner="dots") as status:
            try:
                # Add style modifiers based on preferences
                style_modifiers = {
                    "Photorealistic": ", photorealistic, highly detailed, 8k resolution",
                    "Digital Art": ", digital art, clean lines, vibrant colors",
                    "Oil Painting": ", oil painting, textured, artistic, masterpiece",
                    "Watercolor": ", watercolor painting, soft edges, flowing colors",
                    "Anime/Manga": ", anime style, manga art, cel shaded",
                    "3D Rendered": ", 3D rendered, octane render, realistic lighting",
                    "Sketch": ", pencil sketch, hand-drawn, detailed linework"
                }

                # Add quality and detail modifiers
                enhanced_prompt += ", high quality, detailed, masterpiece, best quality"
                
                # Add style modifier if present in state
                if "style_preference" in state:
                    enhanced_prompt += style_modifiers.get(state["style_preference"], "")

                # Validate prompt length
                if len(enhanced_prompt) > 1000:
                    enhanced_prompt = enhanced_prompt[:997] + "..."

                # Allow for multiple image variations
                num_samples = state.get("num_samples", 1)
                if num_samples > 4:  # Limit to 4 images max
                    num_samples = 4

                body = {
                    "text_prompts": [{"text": enhanced_prompt}],
                    "cfg_scale": 7,
                    "height": state.get("image_height", 512),
                    "width": state.get("image_width", 512),
                    "samples": num_samples,
                    "steps": state.get("steps", 30),
                }
                
                # Using Stability AI API
                url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
                
                headers = {
                    "Authorization": f"Bearer {stability_api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
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

                    # Add image metadata
                    state["image_metadata"] = {
                        "prompt": enhanced_prompt,
                        "settings": body,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    error_msg = response.json().get('message', f"API returned status code: {response.status_code}")
                    raise Exception(error_msg)
                
            except requests.exceptions.RequestException as e:
                error_msg = "Network error occurred while generating image"
                console.print(f"\n[red]{error_msg}: {e}[/red]")
                state["messages"].append({
                    "role": "assistant",
                    "content": error_msg
                })
            except Exception as e:
                console.print(f"\n[red]Error in image generation: {e}[/red]")
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Sorry, I encountered an error: {str(e)}"
                })
        
        return state

    return generate_image 