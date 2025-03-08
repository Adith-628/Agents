# Multi-Agent AI Assistant

A sophisticated AI assistant system that leverages multiple specialized agents to handle different tasks. Currently supports research analysis and image generation workflows.

## Features

### 1. Research Assistant Workflow

- **Researcher Agent**: Gathers and summarizes information about queries.
- **Analyzer Agent**: Processes research findings and identifies key patterns.
- **Writer Agent**: Creates well-structured, coherent responses.

### 2. Image Generation Workflow

- **Prompt Enhancement Agent**: Interactive prompt refinement with user preferences for:
  - Art style selection
  - Mood and atmosphere
  - Color palette
  - Perspective and composition
- **Image Generator Agent**: Creates images using Stability AI's API.

### 3. General Features

- Interactive command-line interface with Rich text formatting.
- Multiple workflow support.
- Error handling and graceful degradation.
- Session management.
- Clear and informative output display.

## Prerequisites

- Python 3.8 or higher.
- Cohere API key.
- Stability AI API key.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/multi-agent-assistant.git
   cd multi-agent-assistant
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```env
   COHERE_API_KEY=your_cohere_api_key
   STABILITY_API_KEY=your_stability_api_key
   ```

## Project Structure

```
project_root/
├── src/
│   ├── agents/
│   │   ├── researcher.py         # Research gathering agent
│   │   ├── analyzer.py           # Analysis processing agent
│   │   ├── writer.py             # Response composition agent
│   │   ├── prompt_enhancer.py    # Image prompt enhancement agent
│   │   └── image_generator.py    # Image generation agent
│   ├── core/
│   │   ├── state.py              # State management
│   │   └── workflow.py           # Workflow definitions
│   ├── utils/
│   │   ├── display.py            # Output formatting
│   │   └── console.py            # Console utilities
│   └── config/
│       └── settings.py           # Configuration management
├── main.py                        # Application entry point
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
```

## Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. Select a workflow:
   - Option 1: Research Assistant.
   - Option 2: Image Generator.
   - Option 3: Exit.

### Research Assistant Workflow

1. Enter your query.
2. The system will:
   - Research the topic.
   - Analyze the findings.
   - Generate a comprehensive response.

### Image Generator Workflow

1. Describe the image you want to create.
2. Follow the interactive prompt enhancement process:
   - Choose art style.
   - Select mood/atmosphere.
   - Specify color preferences.
   - Define perspective.
   - Add any additional details.
3. Review and confirm the enhanced prompt.
4. Wait for image generation.
5. Find the generated image in the `generated_images` directory.

### Commands

- Type `quit` or `exit` to return to workflow selection.
- Type `clear` to clear chat history.
- Press `Ctrl+C` to exit the program.

## Error Handling

- The system includes comprehensive error handling for:
  - API failures.
  - Invalid inputs.
  - Network issues.
  - File system operations.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Create a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Cohere](https://cohere.ai/) for the language model API.
- [Stability AI](https://stability.ai/) for the image generation API.
- [Rich](https://rich.readthedocs.io/) for beautiful terminal formatting.
- [LangGraph](https://github.com/langchain-ai/langgraph) for workflow management.

## Support

For support, please open an issue in the GitHub repository or contact [your-email@example.com].
