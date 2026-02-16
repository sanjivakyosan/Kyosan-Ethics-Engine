"""
AI Service Integration for Kyosan Ethics Engine
Connects to external AI services (OpenRouter, OpenAI, etc.) with ethical oversight

©sanjivakyosan
Created by Sanjiva Kyosan
"""

import os
from typing import Optional, Dict, Any, List
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class AIService:
    """
    Service for connecting to external AI APIs with ethical processing
    """
    def __init__(
        self, 
        base_url: Optional[str] = None, 
        api_key: Optional[str] = None,
        site_url: Optional[str] = None,
        site_name: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize AI service client
        
        Args:
            base_url: API base URL (defaults to OpenRouter)
            api_key: API key (or set OPENROUTER_API_KEY)
            site_url: Site URL for rankings on openrouter.ai (optional)
            site_name: Site name for rankings on openrouter.ai (optional)
            model: Model ID to use (or set OPENROUTER_MODEL). Required to use the API.
        """
        self.base_url = base_url or "https://openrouter.ai/api/v1"
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key required. Set OPENROUTER_API_KEY environment variable or pass api_key parameter.")
        
        # Set up extra headers for OpenRouter rankings
        self.extra_headers = {}
        if site_url:
            self.extra_headers["HTTP-Referer"] = site_url
        elif os.getenv("OPENROUTER_SITE_URL"):
            self.extra_headers["HTTP-Referer"] = os.getenv("OPENROUTER_SITE_URL")
        else:
            # Default site URL for Kyosan Ethics Engine
            self.extra_headers["HTTP-Referer"] = "https://kyosan-ethics-engine.local"
        
        if site_name:
            self.extra_headers["X-Title"] = site_name
        elif os.getenv("OPENROUTER_SITE_NAME"):
            self.extra_headers["X-Title"] = os.getenv("OPENROUTER_SITE_NAME")
        else:
            # Default site name for Kyosan Ethics Engine
            self.extra_headers["X-Title"] = "Kyosan Ethics Engine"
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        self.model = model or os.getenv("OPENROUTER_MODEL")
        if not self.model or not self.model.strip():
            raise ValueError(
                "Model required. Set OPENROUTER_MODEL environment variable or pass the model parameter."
            )

    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        reasoning_enabled: bool = False,
        max_tokens: int = 100000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a chat completion with optional reasoning
        
        Args:
            messages: List of message dictionaries
            model: Model name (default: client's model from OPENROUTER_MODEL or constructor)
            reasoning_enabled: Enable reasoning mode (if supported by the model)
            max_tokens: Maximum tokens in response (default: 100000)
            **kwargs: Additional parameters for the API call
        
        Returns:
            Dictionary with response and reasoning details
        """
        extra_body = {}
        if reasoning_enabled:
            extra_body["reasoning"] = {"enabled": True}
        
        # Prepare kwargs - set max_tokens if not already in kwargs
        call_kwargs = kwargs.copy()
        if "max_tokens" not in call_kwargs:
            call_kwargs["max_tokens"] = max_tokens
        
        try:
            print(f"[AIService] Sending request to OpenAI client...")
            print(f"[AIService] Messages count: {len(messages)}")
            print(f"[AIService] Extra headers: {self.extra_headers}")
            
            # Prepare extra_headers - always include if configured
            call_extra_headers = self.extra_headers if self.extra_headers else {}
            effective_model = model if model is not None else self.model

            response = self.client.chat.completions.create(
                model=effective_model,
                messages=messages,
                extra_headers=call_extra_headers,
                extra_body=extra_body if extra_body else {},
                **call_kwargs
            )
            
            print(f"[AIService] Response received from API")
            print(f"[AIService] Response choices: {len(response.choices)}")
            
            # Extract response
            message = response.choices[0].message
            
            result = {
                "content": message.content,
                "role": message.role,
                "model": effective_model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                }
            }
            
            print(f"[AIService] Content length: {len(result['content'])} chars")
            print(f"[AIService] Tokens used: {result['usage']['total_tokens']}")
            
            # Add reasoning details if available
            if hasattr(message, 'reasoning_details') and message.reasoning_details:
                result["reasoning_details"] = message.reasoning_details
                print(f"[AIService] Reasoning details included")
            
            return result
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"[AIService] Exception occurred: {str(e)}")
            print(f"[AIService] Traceback: {error_trace[-500:]}")
            return {
                "error": str(e),
                "content": None,
                "error_details": error_trace[-500:] if len(error_trace) > 500 else error_trace
            }
    
    def process_with_reasoning(
        self,
        user_input: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        follow_up: Optional[str] = None,
        max_tokens: int = 100000,
        reasoning_enabled: bool = False
    ) -> Dict[str, Any]:
        """
        Process user input with reasoning, optionally with a follow-up
        
        Args:
            user_input: Initial user input
            model: Model to use (default: client's model from OPENROUTER_MODEL or constructor)
            system_prompt: Optional system prompt
            follow_up: Optional follow-up question
        
        Returns:
            Dictionary with responses and reasoning
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # First API call with reasoning
        print(f"[AIService] Making chat completion call to {self.base_url}")
        print(f"[AIService] Model: {model or self.model}, Max tokens: {max_tokens}")
        
        response1 = self.chat_completion(
            messages=messages,
            model=model,
            reasoning_enabled=reasoning_enabled,
            max_tokens=max_tokens
        )
        
        print(f"[AIService] Chat completion response received")
        print(f"[AIService] Has error: {bool(response1.get('error'))}")
        print(f"[AIService] Has content: {bool(response1.get('content'))}")
        
        if response1.get("error"):
            print(f"[AIService] Error in response: {response1.get('error')}")
            return response1
        
        # Prepare messages for potential follow-up
        messages.append({
            "role": "assistant",
            "content": response1["content"],
            "reasoning_details": response1.get("reasoning_details")
        })
        
        result = {
            "initial_response": response1,
            "messages": messages
        }
        
        # If follow-up provided, make second call
        if follow_up:
            messages.append({
                "role": "user",
                "content": follow_up
            })
            
            response2 = self.chat_completion(
                messages=messages,
                model=model,
                reasoning_enabled=True,
                max_tokens=max_tokens
            )
            
            result["follow_up_response"] = response2
            result["messages"] = messages
        
        return result

