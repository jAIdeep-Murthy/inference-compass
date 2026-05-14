import re
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from models import ModelMetadata, load_catalog

SYNONYM_MAP = {
    "chat": ["chatbot", "conversation", "assistant", "talk"],
    "coding": ["code", "developer", "programming", "script", "function"],
    "rag": ["retrieval", "document", "knowledge base", "search", "legal", "pdf"],
    "reasoning": ["logic", "math", "think", "chain of thought", "complex"],
    "summarization": ["summarize", "summary", "shorten", "tldr", "compress"],
    "multilingual": ["language", "translate", "french", "spanish", "chinese", "hindi"],
    "agents": ["agent", "tool", "function calling", "autonomous", "workflow"],
    "instruction-following": ["instructions", "follow", "prompt", "precise"]
}


@dataclass
class RecommendationResult:
    """
    Represents a scored recommendation for a specific model.
    """
    model: ModelMetadata
    score: int
    reason: str


def get_recommendations(
    use_case_text: str,
    priority: str,
    context_need: str,
    task_types: List[str],
    catalog: List[ModelMetadata] = None
) -> List[RecommendationResult]:
    """
    Calculates recommendation scores for all models in the catalog based on user requirements.
    Performs context filtering, keyword matching, exact tag matching, and priority boosting.
    
    Args:
        use_case_text (str): Free-text description of what the user is building.
        priority (str): "speed", "cost", or "quality".
        context_need (str): "short", "medium", or "long".
        task_types (List[str]): Selected specific task categories.
        catalog (List[ModelMetadata]): Optional pre-loaded catalog.
        
    Returns:
        List[RecommendationResult]: Top 3 recommended models sorted by score descending.
    """
    if catalog is None:
        catalog = load_catalog()

    # 1. Filter models by minimum context_length based on context_need
    # short: >= 2048, medium: >= 4096, long: >= 32768
    min_context = 2048
    if context_need == "medium":
        min_context = 4096
    elif context_need == "long":
        min_context = 32768

    filtered_models = [m for m in catalog if m.context_length >= min_context]
    
    # If filtering was too restrictive (shouldn't happen with our catalog), fallback to all
    if not filtered_models:
        filtered_models = catalog

    scored_results: List[RecommendationResult] = []
    use_case_lower = use_case_text.lower()

    for model in filtered_models:
        score = 0
        matched_tags = set()

        # Keyword match use_case_text against each model's best_for list
        for tag in model.best_for:
            # Exact tag match = 2pts
            if re.search(r'\b' + re.escape(tag) + r'\b', use_case_lower):
                score += 2
                matched_tags.add(tag)

            # Synonym match = 1pt per matching synonym
            synonyms = SYNONYM_MAP.get(tag, [])
            for syn in synonyms:
                if syn in use_case_lower:
                    score += 1
                    matched_tags.add(tag)

        # Award 2pts for each item in task_types that matches model's best_for
        for task in task_types:
            if task in model.best_for:
                score += 2
                matched_tags.add(task)

        # Priority boost
        priority_boost_reason = ""
        if priority == "speed" and model.latency_tier == "fast":
            score += 3
            priority_boost_reason = "Blazing fast latency"
        elif priority == "cost" and model.cost_tier == "cheap":
            score += 3
            priority_boost_reason = "Highly cost-effective"
        elif priority == "quality" and model.size == "large":
            score += 3
            priority_boost_reason = "Elite reasoning quality"

        # Context alignment bonus
        if context_need == "long" and model.context_length >= 65536:
            score += 2
        elif context_need == "short" and model.context_length <= 8192:
            score += 2
        elif context_need == "medium" and 4096 <= model.context_length <= 32768:
            score += 2

        # Construct human-readable reason
        if not priority_boost_reason:
            priority_boost_reason = f"{model.latency_tier.capitalize()} latency & {model.cost_tier} cost"

        display_tags = list(matched_tags) if matched_tags else model.best_for[:3]
        reason_str = f"{priority_boost_reason} — standout choice for {', '.join(display_tags)}."

        scored_results.append(RecommendationResult(model=model, score=score, reason=reason_str))

    # Sort descending by score. If ties, favor context length or larger model as tiebreaker
    scored_results.sort(key=lambda r: (r.score, r.model.context_length), reverse=True)

    return scored_results[:3]
