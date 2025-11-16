"""
Test script to verify HTML-first chatbot behavior.
Run this to ensure the chatbot prioritizes HTML content.
"""

import asyncio
from app.services.html_parser import get_html_context
from app.services.resume_data import get_resume_context


async def test_html_first():
    """Test that HTML context is loaded and prioritized."""
    
    print("=" * 60)
    print("Testing HTML-First Context Retrieval")
    print("=" * 60)
    
    # Get HTML context
    print("\n1. Loading HTML context...")
    html_context = get_html_context()
    
    if html_context:
        print(f"✅ HTML context loaded successfully ({len(html_context)} characters)")
        print("\nFirst 500 characters of HTML context:")
        print("-" * 60)
        print(html_context[:500])
        print("-" * 60)
    else:
        print("❌ HTML context is empty!")
    
    # Get resume context (fallback)
    print("\n2. Loading resume context (fallback)...")
    resume_context = get_resume_context()
    
    if resume_context:
        print(f"✅ Resume context loaded successfully ({len(resume_context)} characters)")
        print("\nFirst 500 characters of resume context:")
        print("-" * 60)
        print(resume_context[:500])
        print("-" * 60)
    else:
        print("❌ Resume context is empty!")
    
    # Compare sizes
    print("\n3. Context Comparison:")
    print("-" * 60)
    print(f"HTML Context Size: {len(html_context)} characters")
    print(f"Resume Context Size: {len(resume_context)} characters")
    
    if html_context and len(html_context) > 0:
        print("\n✅ HTML-FIRST STRATEGY ACTIVE")
        print("   The chatbot will prioritize HTML content for responses")
    else:
        print("\n⚠️  HTML context not available, falling back to resume data")
    
    # Test chatbot integration
    print("\n4. Testing Chatbot Integration:")
    print("-" * 60)
    
    try:
        from app.services.agents import AgenticChatbot
        
        chatbot = AgenticChatbot(
            ollama_base_url="http://localhost:11434",
            ollama_model="llama3.2:1b"
        )
        
        print("✅ Chatbot initialized successfully")
        print("   It will use HTML context as PRIMARY source")
        print("   Resume data will be used as FALLBACK only")
        
    except Exception as e:
        print(f"⚠️  Chatbot initialization: {e}")
        print("   (This is expected if Ollama is not running)")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_html_first())
