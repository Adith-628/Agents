from langgraph.graph import Graph
from ..agents.researcher import create_researcher_agent
from ..agents.analyzer import create_analyzer_agent
from ..agents.writer import create_writer_agent
from ..agents.prompt_enhancer import create_prompt_enhancer_agent
from ..agents.image_generator import create_image_generator_agent
from ..agents.summarizer import create_summarizer_agent
from ..agents.code_explainer import create_code_explainer_agent
from ..agents.translator import create_translator_agent
from ..agents.grammar_checker import create_grammar_checker_agent
from ..agents.playlist_generator import create_playlist_generator_agent

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

def create_summary_workflow():
    """Create a workflow for text summarization"""
    workflow = Graph()
    
    # Create the summarizer function
    summarizer = create_summarizer_agent()
    
    # Add nodes to the graph
    workflow.add_node("summarizer", summarizer)
    workflow.add_node("output", lambda state: dict(state))
    
    # Set up the workflow
    workflow.set_entry_point("summarizer")
    workflow.add_edge("summarizer", "output")
    workflow.set_finish_point("output")
    
    # Return the compiled workflow
    return workflow.compile()

def create_code_explanation_workflow():
    """Create a workflow for code explanation"""
    workflow = Graph()
    
    # Create the code explainer function
    code_explainer = create_code_explainer_agent()
    
    # Add nodes to the graph
    workflow.add_node("code_explainer", code_explainer)
    workflow.add_node("output", lambda state: dict(state))
    
    # Set up the workflow
    workflow.set_entry_point("code_explainer")
    workflow.add_edge("code_explainer", "output")
    workflow.set_finish_point("output")
    
    # Return the compiled workflow
    return workflow.compile()

def create_translation_workflow():
    """Create a workflow for translation"""
    workflow = Graph()
    
    translator = create_translator_agent()
    
    workflow.add_node("translator", translator)
    workflow.add_node("output", lambda state: dict(state))
    
    workflow.set_entry_point("translator")
    workflow.add_edge("translator", "output")
    workflow.set_finish_point("output")
    
    return workflow.compile()

def create_grammar_workflow():
    """Create a workflow for grammar checking"""
    workflow = Graph()
    
    grammar_checker = create_grammar_checker_agent()
    
    workflow.add_node("grammar_checker", grammar_checker)
    workflow.add_node("output", lambda state: dict(state))
    
    workflow.set_entry_point("grammar_checker")
    workflow.add_edge("grammar_checker", "output")
    workflow.set_finish_point("output")
    
    return workflow.compile()

def create_playlist_workflow():
    """Create a workflow for playlist generation"""
    workflow = Graph()
    
    playlist_generator = create_playlist_generator_agent()
    
    workflow.add_node("playlist_generator", playlist_generator)
    workflow.add_node("output", lambda state: dict(state))
    
    workflow.set_entry_point("playlist_generator")
    workflow.add_edge("playlist_generator", "output")
    workflow.set_finish_point("output")
    
    return workflow.compile() 