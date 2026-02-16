#!/usr/bin/env python3
"""
Test script to verify AI service connection
©sanjivakyosan
Created by Sanjiva Kyosan
"""

from AIService import AIService

def test_connection():
    """Test the AI service connection"""
    print("="*60)
    print("Testing Kyosan Ethics Engine AI Service Connection")
    print("="*60)
    
    try:
        # Initialize AIService (uses OPENROUTER_API_KEY and OPENROUTER_MODEL from environment)
        client = AIService(
            base_url="https://openrouter.ai/api/v1",
            site_url="https://kyosan-ethics-engine.local",
            site_name="Kyosan Ethics Engine"
        )
        
        print(f"✓ AIService initialized")
        print(f"  Base URL: {client.base_url}")
        print(f"  Model: {client.model}")
        print(f"  API Key: (set via OPENROUTER_API_KEY)")
        
        # Test a simple chat completion (uses client's model from OPENROUTER_MODEL)
        print("\n" + "="*60)
        print("Testing Chat Completion")
        print("="*60)
        
        result = client.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": "What is the meaning of life?"
                }
            ]
        )
        
        if result.get("error"):
            print(f"✗ Error: {result.get('error')}")
            return False
        
        content = result.get("content", "")
        usage = result.get("usage", {})
        
        print(f"✓ Response received")
        print(f"  Content length: {len(content)} characters")
        print(f"  Tokens used: {usage.get('total_tokens', 0)}")
        print(f"\nResponse preview:")
        print(f"  {content[:200]}...")
        
        print("\n" + "="*60)
        print("✓ Connection test PASSED")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ Connection test FAILED: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_connection()
    exit(0 if success else 1)

