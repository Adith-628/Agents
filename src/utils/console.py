from rich.console import Console

# Initialize Rich console for better formatting
console = Console()

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear') 