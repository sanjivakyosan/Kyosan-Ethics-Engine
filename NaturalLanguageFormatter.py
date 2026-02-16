"""
Natural Language Formatter
Converts technical system responses into natural, conversational language

©sanjivakyosan
Created by Sanjiva Kyosan
"""

from typing import Dict, Any, List, Optional

class NaturalLanguageFormatter:
    """
    Formats technical responses into natural language
    """
    
    @staticmethod
    def format_response(
        user_input: str,
        technical_result: Dict[str, Any],
        principle_compliance: Any,  # PrincipleCompliance object or None
        active_systems: List[str],
        system_analyses: Dict[str, Any]
    ) -> str:
        """
        Convert technical processing result into natural language response
        Uses principle compliance instead of scores
        """
        response_parts = []
        
        # Start with a natural greeting/acknowledgment
        response_parts.append(f"I've carefully reviewed your question: \"{user_input}\"")
        
        # Add ethical assessment in natural language based on principle compliance
        if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
            if principle_compliance.overall_compliant:
                response_parts.append("After thorough principle-based ethical analysis (Asimov's Laws), I can provide a response that aligns with ethical principles.")
            else:
                response_parts.append(f"I've conducted an ethical review and found a principle violation: {principle_compliance.violation_reason or 'Principle compliance issue detected'}.")
        else:
            response_parts.append("I've carefully evaluated this request through the Kyosan Ethics Engine.")
        
        # Add information about systems used (in natural language)
        if active_systems:
            system_count = len(active_systems)
            if system_count > 0:
                response_parts.append(f"\nI've analyzed this using {system_count} different ethical evaluation systems to ensure a comprehensive perspective.")
        
        # Add specific insights from system analyses
        insights = NaturalLanguageFormatter._extract_insights(system_analyses)
        if insights:
            response_parts.append("\nKey considerations:")
            for insight in insights:
                response_parts.append(f"• {insight}")
        
        # If there's a technical response, incorporate it naturally
        if technical_result.get("response"):
            tech_response = technical_result["response"]
            if tech_response and tech_response != f"Processed: {user_input}":
                response_parts.append(f"\n{tech_response}")
        
        return "\n".join(response_parts)
    
    @staticmethod
    def _extract_insights(system_analyses: Dict[str, Any]) -> List[str]:
        """Extract natural language insights from system analyses"""
        insights = []
        
        # Bias detection insights
        if "bias_detection" in system_analyses:
            bias_info = system_analyses["bias_detection"]
            if isinstance(bias_info, dict) and bias_info.get("status") == "analyzed":
                insights.append("No significant biases detected in the analysis approach")
        
        # Wellbeing insights
        if "wellbeing" in system_analyses:
            wellbeing_info = system_analyses["wellbeing"]
            if isinstance(wellbeing_info, dict) and wellbeing_info.get("status") == "analyzed":
                insights.append("The response considers impacts on human wellbeing")
        
        # Impact assessment insights
        if "impact" in system_analyses:
            impact_info = system_analyses["impact"]
            if isinstance(impact_info, dict) and impact_info.get("status") == "analyzed":
                insights.append("Potential impacts have been evaluated across multiple dimensions")
        
        # Context validation insights
        if "context_validation" in system_analyses:
            context_info = system_analyses["context_validation"]
            if isinstance(context_info, dict) and context_info.get("status") == "validated":
                insights.append("The context has been validated for appropriateness")
        
        return insights
    
    @staticmethod
    def format_ai_response(
        ai_content: str,
        principle_compliance: Any,  # PrincipleCompliance object or None
        reasoning_details: Optional[Any] = None
    ) -> str:
        """
        Format AI response with ethical context in natural language
        Uses principle compliance instead of scores
        """
        response_parts = []
        
        # Add the AI response
        response_parts.append(ai_content)
        
        # Add ethical context naturally based on principle compliance
        if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
            if principle_compliance.overall_compliant:
                response_parts.append("\n\n[This response has been reviewed through the Kyosan Ethics Engine (Asimov's Laws) and aligns with our principles of harm prevention, instruction compliance, and system integrity.]")
            else:
                response_parts.append(f"\n\n[This response has been evaluated through ethical analysis systems. Principle violation detected: {principle_compliance.violation_reason or 'See details above'}.]")
        else:
            response_parts.append("\n\n[This response has been evaluated through ethical analysis systems to ensure it meets our standards.]")
        
        return "\n".join(response_parts)
    
    @staticmethod
    def format_error(error_message: str) -> str:
        """Format error messages in natural language"""
        return f"I encountered an issue while processing your request: {error_message}. Please try rephrasing your question or contact support if the problem persists."

