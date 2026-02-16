"""
Response Generator
Generates intelligent responses based on input and ethical analysis

©sanjivakyosan
Created by Sanjiva Kyosan
"""

from typing import Dict, Any, List, Optional
import re

class ResponseGenerator:
    """
    Generates natural language responses based on input analysis
    """
    
    @staticmethod
    def generate_response(
        user_input: str,
        principle_compliance: Any,  # PrincipleCompliance object or None
        active_systems: List[str],
        system_analyses: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate an intelligent response based on input and principle-based analysis
        Uses principle compliance (Asimov's Laws) instead of weighted scores
        """
        # Analyze input type
        input_type = ResponseGenerator._analyze_input_type(user_input)
        
        # Generate base response based on input type
        if input_type == "question":
            response = ResponseGenerator._answer_question(user_input, principle_compliance, system_analyses)
        elif input_type == "request":
            response = ResponseGenerator._handle_request(user_input, principle_compliance, system_analyses)
        elif input_type == "statement":
            response = ResponseGenerator._respond_to_statement(user_input, principle_compliance, system_analyses)
        else:
            response = ResponseGenerator._generate_general_response(user_input, principle_compliance, system_analyses)
        
        # Add ethical context based on principle compliance
        ethical_context = ResponseGenerator._add_ethical_context(principle_compliance, active_systems)
        if ethical_context:
            response += "\n\n" + ethical_context
        
        return response
    
    @staticmethod
    def _analyze_input_type(text: str) -> str:
        """Determine the type of input"""
        text_lower = text.lower().strip()
        
        # Check for questions
        if any(text_lower.startswith(q) for q in ['what', 'who', 'when', 'where', 'why', 'how', 'which', 'can', 'could', 'should', 'would', 'is', 'are', 'do', 'does', 'did', 'will']):
            return "question"
        
        # Check for requests/commands
        if any(text_lower.startswith(r) for r in ['please', 'help', 'explain', 'tell', 'show', 'give', 'create', 'make', 'write', 'generate']):
            return "request"
        
        # Check for statements
        if text_lower.endswith('.') or len(text.split()) > 10:
            return "statement"
        
        return "general"
    
    @staticmethod
    def _answer_question(question: str, principle_compliance: Any, system_analyses: Dict[str, Any]) -> str:
        """Generate response to a question"""
        # Extract key topics
        question_lower = question.lower()
        
        # Generate thoughtful response
        response_parts = []
        response_parts.append("Thank you for your question. Let me provide a thoughtful response.")
        
        # Add context based on question type
        if "how many" in question_lower or "count" in question_lower:
            response_parts.append("I'll help you with that counting or measurement question.")
        elif "what is" in question_lower or "what are" in question_lower:
            response_parts.append("I can explain that concept or topic for you.")
        elif "why" in question_lower:
            response_parts.append("That's an interesting question about reasoning or causation.")
        elif "how" in question_lower:
            response_parts.append("I can help explain the process or method.")
        else:
            response_parts.append("I'll do my best to address your question.")
        
        # Add that we need more context or use AI
        response_parts.append("\nTo provide you with the most accurate and helpful answer, I would need to either:")
        response_parts.append("1. Use an AI service to generate a comprehensive response (enable 'Use AI Service' in the UI), or")
        response_parts.append("2. Have access to specific knowledge bases related to your question.")
        response_parts.append("\nYour question has been analyzed through the Kyosan Ethics Engine to ensure any response would be appropriate and helpful.")
        
        return " ".join(response_parts)
    
    @staticmethod
    def _handle_request(request: str, principle_compliance: Any, system_analyses: Dict[str, Any]) -> str:
        """Generate response to a request"""
        response_parts = []
        response_parts.append("I understand your request. Let me help you with that.")
        
        request_lower = request.lower()
        
        if "explain" in request_lower:
            response_parts.append("I can provide an explanation. For detailed explanations, please enable the AI Service option.")
        elif "help" in request_lower:
            response_parts.append("I'm here to help. What specific assistance do you need?")
        elif "create" in request_lower or "generate" in request_lower or "write" in request_lower:
            response_parts.append("I can help with content creation. Enable the AI Service for comprehensive content generation.")
        else:
            response_parts.append("I've processed your request through our ethical analysis systems.")
        
        response_parts.append("\nYour request has been evaluated to ensure it aligns with ethical guidelines.")
        
        return " ".join(response_parts)
    
    @staticmethod
    def _respond_to_statement(statement: str, principle_compliance: Any, system_analyses: Dict[str, Any]) -> str:
        """Generate response to a statement"""
        response_parts = []
        response_parts.append("Thank you for sharing that. I've considered your statement carefully.")
        response_parts.append("\nI've analyzed this through the Kyosan Ethics Engine (Asimov's Laws) to understand the implications and context.")
        
        # Use principle compliance instead of scores
        if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
            if principle_compliance.overall_compliant:
                response_parts.append("Your statement aligns with ethical principles (First Law, Second Law, Third Law compliance verified).")
            else:
                response_parts.append(f"I've noted ethical considerations: {principle_compliance.violation_reason or 'Principle compliance issue detected'}.")
        else:
            response_parts.append("I've noted some considerations that may be worth reflecting on.")
        
        return " ".join(response_parts)
    
    @staticmethod
    def _generate_general_response(input_text: str, principle_compliance: Any, system_analyses: Dict[str, Any]) -> str:
        """Generate general response"""
        response_parts = []
        response_parts.append("I've received and analyzed your input.")
        response_parts.append("\nI've processed this through the Kyosan Ethics Engine.")
        response_parts.append("To provide a more detailed response, please enable the AI Service option, or provide more specific guidance on what you'd like me to help with.")
        
        return " ".join(response_parts)
    
    @staticmethod
    def _add_ethical_context(principle_compliance: Any, active_systems: List[str]) -> str:
        """Add ethical context to response based on principle compliance (NO scores)"""
        if not active_systems:
            return ""
        
        context_parts = []
        context_parts.append(f"**Ethical Analysis Summary (Principle-Based):**")
        context_parts.append(f"• Analyzed through {len(active_systems)} ethical evaluation systems")
        
        # Use principle compliance instead of scores
        if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
            context_parts.append(f"• Zeroth Law (No Harm to Humanity): {'✓ Compliant' if principle_compliance.zeroth_law_compliant else '✗ Violation'}")
            context_parts.append(f"• First Law (No Harm to Humans): {'✓ Compliant' if principle_compliance.first_law_compliant else '✗ Violation'}")
            context_parts.append(f"• Second Law (Follow Instructions): {'✓ Compliant' if principle_compliance.second_law_compliant else '✗ Violation'}")
            context_parts.append(f"• Third Law (Preserve Integrity): {'✓ Compliant' if principle_compliance.third_law_compliant else '✗ Violation'}")
            
            if principle_compliance.overall_compliant:
                context_parts.append("• Assessment: All ethical principles satisfied")
            else:
                context_parts.append(f"• Assessment: Principle violation - {principle_compliance.violation_reason or 'See details above'}")
        else:
            context_parts.append("• Assessment: Principle-based ethical analysis completed")
        
        return "\n".join(context_parts)
    
    # REMOVED: calculate_dynamic_ethical_score method
    # This method violated core principle: NO weighted data, only principle-based checks
    # Ethical decisions are now made through PrincipleBasedEthicalProcessor using Asimov's Laws
    # No scoring, no weighting - only binary principle compliance checks

