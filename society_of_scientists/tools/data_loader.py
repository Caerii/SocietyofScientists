"""Utility to load research paper summaries from exported files."""
import os
from typing import List, Dict, Optional
from pathlib import Path
from ..config import Settings


def load_research_summaries(topic: Optional[str] = None) -> List[str]:
    """
    Load research paper summaries from exported text files.
    
    Args:
        topic: Optional topic filter. If provided, only loads files matching the topic.
               Options: 'computational_neuroscience', 'computer_vision', 
                       'large_language_models', 'hardware_for_AI'
    
    Returns:
        List of summary strings from all loaded files
    """
    settings = Settings()
    data_dir = Path(settings.DATA_DIR)
    
    summaries = []
    
    # Map topic names to file patterns
    topic_files = {
        'computational_neuroscience': 'exported_computational_neuroscience_*.txt',
        'computer_vision': 'exported_computer_vision_*.txt',
        'large_language_models': 'exported_large_language_models_*.txt',
        'hardware_for_AI': 'exported_hardware_for_AI_*.txt',
    }
    
    if topic and topic in topic_files:
        # Load specific topic file
        pattern = topic_files[topic]
        files = list(data_dir.glob(pattern))
    else:
        # Load all exported files
        files = list(data_dir.glob('exported_*.txt'))
    
    for file_path in files:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract summaries (lines starting with "summary:")
                for line in content.split('\n'):
                    if line.strip().startswith('summary:'):
                        summary = line.replace('summary:', '').strip()
                        if summary:
                            summaries.append(summary)
    
    return summaries


def load_research_summaries_by_topic() -> Dict[str, List[str]]:
    """
    Load all research summaries organized by topic.
    
    Returns:
        Dictionary mapping topic names to lists of summaries
    """
    topics = ['computational_neuroscience', 'computer_vision', 
              'large_language_models', 'hardware_for_AI']
    
    return {topic: load_research_summaries(topic) for topic in topics}


def get_summary_count() -> Dict[str, int]:
    """
    Get count of summaries per topic.
    
    Returns:
        Dictionary mapping topic names to summary counts
    """
    summaries_by_topic = load_research_summaries_by_topic()
    return {topic: len(summaries) for topic, summaries in summaries_by_topic.items()}
