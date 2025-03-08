from typing import TypedDict, List, Optional

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