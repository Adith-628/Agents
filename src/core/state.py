from typing import TypedDict, List, Optional, Dict

class MessageDict(TypedDict):
    role: str
    content: str

class AgentState(TypedDict):
    messages: List[MessageDict]
    current_task: str
    task_status: str
    workflow_type: str
    research_results: Optional[str]
    analysis_results: Optional[str]
    final_response: Optional[str]
    enhanced_prompt: Optional[str]
    image_path: Optional[str]
    # New fields for image generation
    style_preference: Optional[str]
    num_samples: Optional[int]
    image_width: Optional[int]
    image_height: Optional[int]
    image_metadata: Optional[Dict]
    # New fields for summarizer
    summaries: Optional[Dict[str, str]]
    # New fields for code explainer
    code_explanation: Optional[str]
    # New fields for translation
    translation_results: Optional[Dict]
    target_language: Optional[str]
    # New fields for grammar checking
    grammar_analysis: Optional[Dict]
    check_type: Optional[str]
    # New fields for playlist generator
    music_preferences: Optional[Dict]
    playlist_state: Optional[Dict]
    playlist_results: Optional[Dict] 