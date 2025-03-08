from langgraph.graph import Graph
from ..agents.researcher import create_researcher_agent
from ..agents.analyzer import create_analyzer_agent
from ..agents.writer import create_writer_agent
from ..agents.prompt_enhancer import create_prompt_enhancer_agent
from ..agents.image_generator import create_image_generator_agent

def create_research_workflow():
    workflow = Graph()
    
    # Add research agents
    workflow.add_node("researcher", create_researcher_agent())
    workflow.add_node("analyzer", create_analyzer_agent())
    workflow.add_node("writer", create_writer_agent())
    workflow.add_node("output", lambda state: dict(state))
    
    # Connect the agents in sequence
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "analyzer")
    workflow.add_edge("analyzer", "writer")
    workflow.add_edge("writer", "output")
    workflow.set_finish_point("output")
    
    return workflow.compile()

def create_image_workflow():
    workflow = Graph()
    
    # Add image generation agents
    workflow.add_node("prompt_enhancer", create_prompt_enhancer_agent())
    workflow.add_node("image_generator", create_image_generator_agent())
    workflow.add_node("output", lambda state: dict(state))
    
    # Connect the agents in sequence
    workflow.set_entry_point("prompt_enhancer")
    workflow.add_edge("prompt_enhancer", "image_generator")
    workflow.add_edge("image_generator", "output")
    workflow.set_finish_point("output")
    
    return workflow.compile() 