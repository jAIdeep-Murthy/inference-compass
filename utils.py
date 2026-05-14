import os
import time
from typing import Tuple
import streamlit as st
from openai import OpenAI


def get_api_key():
    """
    Retrieves the Featherless API key, attempting Streamlit secrets first,
    then falling back to environment variables.
    """
    try:
        return st.secrets["FEATHERLESS_API_KEY"]
    except Exception:
        return os.getenv("FEATHERLESS_API_KEY")


def generate_api_snippet(model_id: str) -> str:
    """
    Generates the exact Python code snippet for calling the specified model
    via the Featherless AI API.
    
    Args:
        model_id (str): The exact Featherless model ID string.
        
    Returns:
        str: Formatted Python code snippet.
    """
    template = f"""from openai import OpenAI

client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key="YOUR_FEATHERLESS_API_KEY"
)

response = client.chat.completions.create(
    model="{model_id}",
    messages=[{{"role": "user", "content": "Your prompt here"}}]
)
print(response.choices[0].message.content)"""
    return template


def run_live_inference(model_id: str, prompt: str, api_key: str) -> Tuple[str, float]:
    """
    Executes a chat completion call against the Featherless AI API and calculates latency.
    
    Args:
        model_id (str): The exact model ID to query.
        prompt (str): User prompt text.
        api_key (str): Valid Featherless API key.
        
    Returns:
        Tuple[str, float]: (Model response text, Latency in milliseconds)
    """
    client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=api_key
    )
    
    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        latency = (time.time() - start_time) * 1000.0  # Convert to ms
        content = response.choices[0].message.content
        return content, latency
    except Exception as e:
        latency = (time.time() - start_time) * 1000.0
        return f"Error executing inference: {str(e)}", latency
