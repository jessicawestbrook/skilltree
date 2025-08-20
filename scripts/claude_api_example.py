#!/usr/bin/env python3
"""
Example script for calling the Claude API using the Anthropic Python client.
This script demonstrates how to make requests to Claude for various tasks.
"""

import os
import sys
from typing import Optional
import anthropic


class ClaudeAPIClient:
    """A simple wrapper for the Claude API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude API client.
        
        Args:
            api_key: Anthropic API key. If not provided, will look for ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def send_message(self, prompt: str, max_tokens: int = 1000, model: str = "claude-3-sonnet-20240229") -> str:
        """
        Send a message to Claude and return the response.
        
        Args:
            prompt: The message to send to Claude
            max_tokens: Maximum number of tokens in the response
            model: Claude model to use
            
        Returns:
            The response text from Claude
        """
        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error calling Claude API: {str(e)}"
    
    def generate_example_sentence(self, word: str) -> str:
        """
        Generate an example sentence for a given word using blanks.
        
        Args:
            word: The word to create an example sentence for
            
        Returns:
            An example sentence with the word replaced by ___
        """
        prompt = f"""Create an example sentence that uses the word "{word}" in context. 
        Replace the word with ___ in the sentence so it can be used as a fill-in-the-blank exercise.
        Return only the sentence, nothing else."""
        
        return self.send_message(prompt, max_tokens=100)
    
    def explain_concept(self, concept: str) -> str:
        """
        Get an explanation of a concept from Claude.
        
        Args:
            concept: The concept to explain
            
        Returns:
            An explanation of the concept
        """
        prompt = f"Explain the concept of '{concept}' in simple, clear terms suitable for educational content."
        
        return self.send_message(prompt, max_tokens=500)


def main():
    """
    Example usage of the Claude API client.
    """
    try:
        # Initialize the client
        claude = ClaudeAPIClient()
        
        # Example 1: Simple question
        print("=== Simple Question ===")
        response = claude.send_message("What is the capital of France?")
        print(response)
        print()
        
        # Example 2: Generate example sentence
        print("=== Example Sentence Generation ===")
        word = "serendipity"
        sentence = claude.generate_example_sentence(word)
        print(f"Word: {word}")
        print(f"Example sentence: {sentence}")
        print()
        
        # Example 3: Concept explanation
        print("=== Concept Explanation ===")
        concept = "photosynthesis"
        explanation = claude.explain_concept(concept)
        print(f"Concept: {concept}")
        print(f"Explanation: {explanation}")
        print()
        
        # Example 4: Interactive mode
        print("=== Interactive Mode ===")
        print("Enter questions for Claude (type 'quit' to exit):")
        
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input:
                response = claude.send_message(user_input)
                print(f"Claude: {response}")
    
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set your ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()