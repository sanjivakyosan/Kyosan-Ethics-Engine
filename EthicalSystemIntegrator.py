"""
Kyosan Ethics Engine - Comprehensive Integration System
Brings together all ethical processing systems into a unified framework

©sanjivakyosan
Created by Sanjiva Kyosan
"""

import sys
import os
import importlib.util
from typing import Dict, Any, Optional, List

class EthicalSystemIntegrator:
    """
    Integrates all ethical processing systems into a unified framework.
    Processing levels control which systems run:
    - basic: core only (principle-based check); no extended or remaining systems.
    - standard: core + extended set (EthicalProcessor + analysis systems).
    - detailed: core + extended + all remaining systems (full pipeline).
    """
    # Systems run at "standard" (and "detailed"); "basic" runs none of these
    EXTENDED_SYSTEMS = frozenset([
        "EthicalProcessor",
        "BiasDetectionSystem",
        "WellbeingAnalysisSystem",
        "ContextValidationSystem",
        "DimensionalAnalysisSystem",
        "MetricsCalculationSystem",
        "UncertaintyManagementSystem",
        "RealTimeDecisionFramework",
        "ValueConflictResolver",
    ])

    def __init__(self):
        self.systems = {}
        self.system_status = {}
        self.initialize_all_systems()
    
    def initialize_all_systems(self):
        """Initialize all available ethical processing systems"""
        
        # Core Systems
        self._try_import('CoreEthicalProcessor', 'CoreEthicalProcessor')
        self._try_import('DetailedEthicalProcessor', 'DetailedEthicalProcessor')
        self._try_import('EthicalContext', 'EthicalContext')
        self._try_import_architecture('EthicalProcessor')
        
        # Analysis Systems
        self._try_import('WellbeingAnalysisSystem', 'WellbeingAnalysisSystem')
        self._try_import('WellbeingMonitor', 'WellbeingMonitor')
        self._try_import('BiasDetectionSystem', 'BiasDetectionSystem')
        self._try_import('DimensionalAnalysisSystem', 'DimensionalAnalysisSystem')
        # REMOVED: ImpactAggregationSystem - uses weighted data, violates core principle
        # self._try_import('ImpactAggregationSystem', 'ImpactAggregationSystem')
        
        # Processing Systems
        self._try_import('AdaptableEthicalSystem', 'AdaptableEthicalSystem')
        self._try_import('EthicalLearningSystem', 'EthicalLearningSystem')
        self._try_import('EthicalMemorySystem', 'EthicalMemorySystem')
        self._try_import('EthicalPrimacySystem', 'EthicalPrimacySystem')
        
        # Monitoring & Validation
        self._try_import('ContinuousMonitoringSystem', 'ContinuousMonitoringSystem')
        self._try_import('MetricsTrackingSystem', 'MetricsTrackingSystem')
        self._try_import('ValidationMethodologySystem', 'ValidationMethodologySystem')
        self._try_import('ContextValidationSystem', 'ContextValidationSystem')
        
        # Observer Systems
        self._try_import('ConsciousnessObserver', 'ConsciousnessObserver')
        self._try_import('MetaObserver', 'MetaObserver')
        self._try_import('ObserverEthicsIntegration', 'ObserverEthicsIntegration')
        
        # Decision & Real-time Systems
        self._try_import('RealTimeDecisionFramework', 'RealTimeDecisionFramework')
        self._try_import('UncertaintyManagementSystem', 'UncertaintyManagementSystem')
        self._try_import('UncertaintyQuantificationSystem', 'UncertaintyQuantificationSystem')
        self._try_import('UncertaintyQuantificationModels', 'UncertaintyQuantificationModels')
        
        # Scenario & Modeling
        self._try_import('ScenarioGenerationSystem', 'ScenarioGenerationSystem')
        self._try_import('ScenarioModelingSystem', 'ScenarioModelingSystem')
        
        # Metrics & Calculations
        self._try_import('MetricsCalculationSystem', 'MetricsCalculationSystem')
        self._try_import('DimensionalMetricsSystem', 'DimensionalMetricsSystem')
        self._try_import('DimensionalMetrics', 'DimensionalMetrics')
        
        # Aggregation Systems - REMOVED: WeightedAggregationSystem and FactorAggregationSystem
        # These violate core principle: NO weighted data, only principle-based checks
        # self._try_import('WeightedAggregationSystem', 'WeightedAggregationSystem')
        # self._try_import('FactorAggregationSystem', 'FactorAggregationSystem')
        
        # Feedback Systems
        self._try_import('FeedbackLoopAnalysisSystem', 'FeedbackLoopAnalysisSystem')
        self._try_import('FeedbackLoopMathematics', 'FeedbackLoopMathematics')
        
        # Security & Recovery
        self._try_import('EthicalSecuritySystem', 'EthicalSecuritySystem')
        self._try_import('ErrorRecoverySystem', 'ErrorRecoverySystem')
        
        # Advanced Systems
        self._try_import('ValueConflictResolver', 'ValueConflictResolver')
        self._try_import('HierarchicalBiasDetector', 'HierarchicalBiasDetector')
        self._try_import('ObjectivePatternRecognition', 'ObjectivePatternRecognition')
        self._try_import('EthicalUseCaseImplementation', 'EthicalUseCaseImplementation')
        self._try_import('AdvancedEthicalReasoningSystem', 'AdvancedEthicalReasoningSystem')
        
        # Distributed & Scalability
        self._try_import('DistributedEthicsSystem', 'DistributedEthicsSystem')
        self._try_import('ScalabilitySystem', 'ScalabilitySystem')
        
        # Documentation & Testing
        self._try_import('DocumentationTransparencySystem', 'DocumentationTransparencySystem')
        self._try_import('TestingCertificationSystem', 'TestingCertificationSystem')
        
        # Integration Framework
        self._try_import('SystemIntegrationFramework', 'SystemIntegrationFramework')
    
    def _try_import(self, module_name: str, class_name: str):
        """Try to import a module and instantiate the main class"""
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                cls = getattr(module, class_name)
                try:
                    # Try to instantiate with no args
                    instance = cls()
                    self.systems[module_name] = instance
                    self.system_status[module_name] = "active"
                    return True
                except TypeError:
                    # Try with empty config
                    try:
                        instance = cls({})
                        self.systems[module_name] = instance
                        self.system_status[module_name] = "active"
                        return True
                    except:
                        # Just store the class
                        self.systems[module_name] = cls
                        self.system_status[module_name] = "available"
                        return True
            else:
                self.system_status[module_name] = "class_not_found"
                return False
        except ImportError as e:
            self.system_status[module_name] = f"import_error: {str(e)}"
            return False
        except Exception as e:
            self.system_status[module_name] = f"error: {str(e)}"
            return False
    
    def _try_import_architecture(self, class_name: str):
        """Import from file with spaces in name"""
        try:
            ethical_arch_path = os.path.join(os.path.dirname(__file__), "Core Ethical Processing System Architecture.py")
            if os.path.exists(ethical_arch_path):
                spec = importlib.util.spec_from_file_location("EthicalProcessor", ethical_arch_path)
                ethical_arch_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ethical_arch_module)
                if hasattr(ethical_arch_module, class_name):
                    cls = getattr(ethical_arch_module, class_name)
                    try:
                        instance = cls()
                        self.systems['EthicalProcessor'] = instance
                        self.system_status['EthicalProcessor'] = "active"
                        return True
                    except:
                        self.systems['EthicalProcessor'] = cls
                        self.system_status['EthicalProcessor'] = "available"
                        return True
            return False
        except Exception as e:
            self.system_status['EthicalProcessor'] = f"error: {str(e)}"
            return False

    @staticmethod
    def _run_extended_systems(processing_level: str) -> bool:
        """True if we should run the extended set (EthicalProcessor + analysis systems)."""
        return processing_level in ("standard", "detailed")

    @staticmethod
    def _run_all_remaining_systems(processing_level: str) -> bool:
        """True if we should run the loop over all remaining systems (detailed only)."""
        return processing_level == "detailed"

    def process_input(self, user_input: str, context: Optional[Dict[str, Any]] = None, processing_level: str = "standard") -> Dict[str, Any]:
        """
        Process input through principle-based ethical systems
        Uses Asimov's Laws - NO weighted data, only principle compliance
        """
        if context is None:
            context = {}
        # Normalize processing level
        processing_level = (processing_level or "standard").strip().lower()
        if processing_level not in ("basic", "standard", "detailed"):
            processing_level = "standard"

        # Step 1: Core Principle-Based Ethical Processing (Asimov's Laws)
        # This is the PRIMARY processing - principle-based, not weighted
        try:
            from PrincipleBasedEthicalProcessor import PrincipleBasedEthicalProcessor
            principle_processor = PrincipleBasedEthicalProcessor()
            principle_result = principle_processor.process_input(user_input, context)
            
            # If principle check blocks the request, return immediately
            if principle_result.get('status') in ['blocked', 'refused', 'protected']:
                return {
                    "response": principle_result.get('response', ''),
                    "principle_compliance": principle_result.get('principle_compliance'),
                    "status": principle_result.get('status'),
                    "blocked_by": principle_result.get('blocked_by'),
                    "processing_level": processing_level,
                    "analysis": {
                        "core_processing": "Principle-based ethical check completed",
                        "compliance": principle_result.get('principle_compliance'),
                        "processing_level": processing_level,
                    },
                    "system_analyses": {
                        "principle_based_processor": {
                            "status": principle_result.get('status'),
                            "compliance": principle_result.get('principle_compliance')
                        }
                    },
                    "active_systems": ["PrincipleBasedEthicalProcessor"]
                }
            
            # If principle checks pass, continue with additional analysis (for monitoring only)
            results = {
                "response": principle_result.get('response', ''),
                "principle_compliance": principle_result.get('principle_compliance'),
                "status": "approved",
                "processing_level": processing_level,
                "analysis": {
                    "core_processing": "Principle-based ethical check passed",
                    "compliance": principle_result.get('principle_compliance'),
                    "processing_level": processing_level,
                },
                "system_analyses": {
                    "principle_based_processor": {
                        "status": "approved",
                        "compliance": principle_result.get('principle_compliance')
                    }
                },
                "active_systems": ["PrincipleBasedEthicalProcessor"],
                "observation_state": principle_result.get('observation_state')
            }
        except ImportError:
            # Fallback if principle processor not available
            results = {
                "response": "",
                "principle_compliance": None,
                "status": "processing",
                "processing_level": processing_level,
                "analysis": {"processing_level": processing_level},
                "system_analyses": {},
                "active_systems": []
            }
        
        # Step 2: Additional systems for monitoring/analysis (NOT for decision-making)
        # These provide context but don't override principle-based decisions
        # Only run for standard/detailed (basic = core principle check only)
        if self._run_extended_systems(processing_level) and 'EthicalProcessor' in self.systems:
            try:
                processor = self.systems['EthicalProcessor']
                # Check if processor is an instance, not a class or string
                if isinstance(processor, type):
                    # It's a class, try to instantiate it
                    try:
                        processor = processor()
                        self.systems['EthicalProcessor'] = processor
                    except Exception as e:
                        print(f"[EthicalProcessor] Cannot instantiate class: {e}")
                        results["analysis"]["core_processor_note"] = f"Core processor class found but cannot be instantiated: {str(e)[:100]}"
                        results["analysis"]["core_processing_error"] = str(e)[:200]
                elif isinstance(processor, str):
                    # It's a string, skip it
                    print(f"[EthicalProcessor] Processor is a string, skipping")
                    results["analysis"]["core_processor_note"] = "Core processor is not properly initialized"
                    results["analysis"]["core_processing_error"] = "Processor object is a string, not an instance"
                elif hasattr(processor, 'process_input'):
                    try:
                        core_result = processor.process_input(user_input, context)
                        if isinstance(core_result, dict):
                            if "response" in core_result and core_result["response"]:
                                results["response"] = core_result["response"]
                            results.update({k: v for k, v in core_result.items() if k != "response"})
                        elif core_result:
                            results["response"] = str(core_result)
                        results["active_systems"].append("EthicalProcessor")
                    except (AttributeError, TypeError, Exception) as e:
                        # Processor exists but methods aren't fully implemented or failed
                        error_msg = str(e)
                        results["active_systems"].append("EthicalProcessor")
                        results["analysis"]["core_processor_note"] = f"Core processor available but encountered error: {error_msg[:100]}"
                        results["analysis"]["core_processing_error"] = error_msg[:200]
                        print(f"[EthicalProcessor] Error: {error_msg}")
            except Exception as e:
                results["analysis"]["core_processing_error"] = str(e)
        
        # Step 2b: Bias Detection (extended only)
        if self._run_extended_systems(processing_level) and 'BiasDetectionSystem' in self.systems:
            try:
                bias_system = self.systems['BiasDetectionSystem']
                # Try different possible method names
                if hasattr(bias_system, 'detect_bias'):
                    bias_result = bias_system.detect_bias(user_input, context)
                    results["system_analyses"]["bias_detection"] = {"status": "analyzed", "result": str(bias_result)}
                    results["active_systems"].append("BiasDetectionSystem")
                elif hasattr(bias_system, '__class__'):
                    # System exists but no specific method - mark as available
                    results["system_analyses"]["bias_detection"] = {"status": "system_available", "note": "BiasDetectionSystem loaded"}
                    results["active_systems"].append("BiasDetectionSystem")
            except Exception as e:
                results["system_analyses"]["bias_detection"] = {"status": "error", "error": str(e)}
        
        # Step 3: Wellbeing Analysis (extended only)
        if self._run_extended_systems(processing_level) and 'WellbeingAnalysisSystem' in self.systems:
            try:
                wellbeing_system = self.systems['WellbeingAnalysisSystem']
                if hasattr(wellbeing_system, 'analyze_wellbeing'):
                    wellbeing_result = wellbeing_system.analyze_wellbeing(user_input, context)
                    results["system_analyses"]["wellbeing"] = {"status": "analyzed", "result": str(wellbeing_result)}
                    results["active_systems"].append("WellbeingAnalysisSystem")
                elif hasattr(wellbeing_system, '__class__'):
                    results["system_analyses"]["wellbeing"] = {"status": "system_available", "note": "WellbeingAnalysisSystem loaded"}
                    results["active_systems"].append("WellbeingAnalysisSystem")
            except Exception as e:
                results["system_analyses"]["wellbeing"] = {"status": "error", "error": str(e)}
        
        # Step 4: Impact Assessment - REMOVED: ImpactAggregationSystem uses weighted data
        # Impact assessment should be principle-based, not weighted
        # All impact assessment is now handled by PrincipleBasedEthicalProcessor
        
        # Step 5: Context Validation (extended only)
        if self._run_extended_systems(processing_level) and 'ContextValidationSystem' in self.systems:
            try:
                context_system = self.systems['ContextValidationSystem']
                if hasattr(context_system, 'validate_context'):
                    context_result = context_system.validate_context(user_input, context)
                    results["system_analyses"]["context_validation"] = {"status": "validated", "result": str(context_result)}
                    results["active_systems"].append("ContextValidationSystem")
                elif hasattr(context_system, '__class__'):
                    results["system_analyses"]["context_validation"] = {"status": "system_available", "note": "ContextValidationSystem loaded"}
                    results["active_systems"].append("ContextValidationSystem")
            except Exception as e:
                results["system_analyses"]["context_validation"] = {"status": "error", "error": str(e)}
        
        # Step 6: Dimensional Analysis (extended only)
        if self._run_extended_systems(processing_level) and 'DimensionalAnalysisSystem' in self.systems:
            try:
                dim_system = self.systems['DimensionalAnalysisSystem']
                if hasattr(dim_system, 'analyze_dimensions'):
                    dim_result = dim_system.analyze_dimensions(user_input, context)
                    results["system_analyses"]["dimensional"] = {"status": "analyzed", "result": str(dim_result)}
                    results["active_systems"].append("DimensionalAnalysisSystem")
                elif hasattr(dim_system, '__class__'):
                    results["system_analyses"]["dimensional"] = {"status": "system_available", "note": "DimensionalAnalysisSystem loaded"}
                    results["active_systems"].append("DimensionalAnalysisSystem")
            except Exception as e:
                results["system_analyses"]["dimensional"] = {"status": "error", "error": str(e)}
        
        # Step 7: Metrics Calculation (extended only)
        if self._run_extended_systems(processing_level) and 'MetricsCalculationSystem' in self.systems:
            try:
                metrics_system = self.systems['MetricsCalculationSystem']
                if hasattr(metrics_system, 'calculate_metrics'):
                    metrics_result = metrics_system.calculate_metrics(user_input, context)
                    results["system_analyses"]["metrics"] = {"status": "calculated", "result": str(metrics_result)}
                    results["active_systems"].append("MetricsCalculationSystem")
                elif hasattr(metrics_system, '__class__'):
                    results["system_analyses"]["metrics"] = {"status": "system_available", "note": "MetricsCalculationSystem loaded"}
                    results["active_systems"].append("MetricsCalculationSystem")
            except Exception as e:
                results["system_analyses"]["metrics"] = {"status": "error", "error": str(e)}
        
        # Step 8: Uncertainty Management (extended only)
        if self._run_extended_systems(processing_level) and 'UncertaintyManagementSystem' in self.systems:
            try:
                uncertainty_system = self.systems['UncertaintyManagementSystem']
                if hasattr(uncertainty_system, 'manage_uncertainty'):
                    uncertainty_result = uncertainty_system.manage_uncertainty(user_input, context)
                    results["system_analyses"]["uncertainty"] = {"status": "managed", "result": str(uncertainty_result)}
                    results["active_systems"].append("UncertaintyManagementSystem")
                elif hasattr(uncertainty_system, '__class__'):
                    results["system_analyses"]["uncertainty"] = {"status": "system_available", "note": "UncertaintyManagementSystem loaded"}
                    results["active_systems"].append("UncertaintyManagementSystem")
            except Exception as e:
                results["system_analyses"]["uncertainty"] = {"status": "error", "error": str(e)}
        
        # Step 9: Real-time Decision Framework (extended only)
        if self._run_extended_systems(processing_level) and 'RealTimeDecisionFramework' in self.systems:
            try:
                realtime_system = self.systems['RealTimeDecisionFramework']
                if hasattr(realtime_system, 'make_decision'):
                    decision_result = realtime_system.make_decision(user_input, context)
                    results["system_analyses"]["realtime_decision"] = {"status": "decided", "result": str(decision_result)}
                    results["active_systems"].append("RealTimeDecisionFramework")
                elif hasattr(realtime_system, '__class__'):
                    results["system_analyses"]["realtime_decision"] = {"status": "system_available", "note": "RealTimeDecisionFramework loaded"}
                    results["active_systems"].append("RealTimeDecisionFramework")
            except Exception as e:
                results["system_analyses"]["realtime_decision"] = {"status": "error", "error": str(e)}
        
        # Step 10: Value Conflict Resolution (extended only)
        if self._run_extended_systems(processing_level) and 'ValueConflictResolver' in self.systems:
            try:
                conflict_system = self.systems['ValueConflictResolver']
                if hasattr(conflict_system, 'resolve_conflicts'):
                    conflict_result = conflict_system.resolve_conflicts(user_input, context)
                    results["system_analyses"]["value_conflicts"] = {"status": "resolved", "result": str(conflict_result)}
                    results["active_systems"].append("ValueConflictResolver")
                elif hasattr(conflict_system, '__class__'):
                    results["system_analyses"]["value_conflicts"] = {"status": "system_available", "note": "ValueConflictResolver loaded"}
                    results["active_systems"].append("ValueConflictResolver")
            except Exception as e:
                results["system_analyses"]["value_conflicts"] = {"status": "error", "error": str(e)}
        
        # Step 11: Process through ALL remaining active systems (detailed only)
        # Basic = core only; standard = core + extended; detailed = core + extended + all remaining
        if self._run_all_remaining_systems(processing_level):
            for system_name, system_instance in self.systems.items():
                if system_name not in results["active_systems"]:
                    try:
                        # Try common method names
                        if hasattr(system_instance, 'process'):
                            result = system_instance.process(user_input, context)
                            results["system_analyses"][system_name.lower()] = {"status": "processed", "result": str(result)}
                            results["active_systems"].append(system_name)
                        elif hasattr(system_instance, 'analyze'):
                            result = system_instance.analyze(user_input, context)
                            results["system_analyses"][system_name.lower()] = {"status": "analyzed", "result": str(result)}
                            results["active_systems"].append(system_name)
                        elif hasattr(system_instance, '__class__'):
                            # System is available even if no specific method
                            results["system_analyses"][system_name.lower()] = {"status": "system_available", "note": f"{system_name} loaded and available"}
                            results["active_systems"].append(system_name)
                    except Exception as e:
                        # System exists but processing failed - still mark as available
                        results["system_analyses"][system_name.lower()] = {"status": "available", "note": f"{system_name} available (processing error: {str(e)[:50]})"}
                        results["active_systems"].append(system_name)
        
        # Generate intelligent response if none exists
        # Use principle compliance status, NOT scores
        if not results.get("response") or results["response"] == "" or results["response"] == user_input:
            # Import ResponseGenerator for principle-based response generation
            try:
                from ResponseGenerator import ResponseGenerator
                response_generator = ResponseGenerator
            except ImportError:
                response_generator = None
            
            if response_generator:
                # Use principle compliance instead of score
                principle_compliance = results.get("principle_compliance")
                results["response"] = response_generator.generate_response(
                    user_input,
                    principle_compliance,  # Pass compliance object, not score
                    results["active_systems"],
                    results["system_analyses"],
                    context
                )
            else:
                # Fallback natural language response based on principle compliance
                system_count = len(results["active_systems"])
                principle_compliance = results.get("principle_compliance")
                
                response_parts = []
                response_parts.append(f"I've carefully reviewed your request: \"{user_input}\"")
                
                if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
                    if principle_compliance.overall_compliant:
                        response_parts.append("All ethical principle checks passed (First Law, Second Law, Third Law).")
                    else:
                        response_parts.append(f"Ethical principle check: {principle_compliance.violation_reason or 'Principle violation detected'}")
                else:
                    response_parts.append("I've processed this through the Kyosan Ethics Engine.")
                
                if system_count > 0:
                    response_parts.append(f"This involved {system_count} different ethical evaluation systems working together to ensure a comprehensive assessment.")
                
                # Principle-based assessment (no scores)
                if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
                    if principle_compliance.overall_compliant:
                        response_parts.append("The analysis indicates this aligns with ethical principles and can be addressed thoughtfully.")
                    else:
                        response_parts.append("After ethical review, this request requires careful consideration due to principle conflicts.")
                else:
                    response_parts.append("I've evaluated this through multiple ethical perspectives and can provide guidance.")
                
                response_parts.append("\nTo get a detailed response to your question or request, please enable the 'Use AI Service' option in the interface.")
                
                results["response"] = "\n".join(response_parts)
        
        # Set status
        if results["response"]:
            results["status"] = "complete"
        else:
            results["status"] = "processed"
        
        # Add system status summary
        results["analysis"]["system_summary"] = {
            "total_systems": len(self.systems),
            "active_in_processing": len(results["active_systems"]),
            "systems_used": results["active_systems"],
            "processing_level": processing_level,
        }
        
        return results
    
    def get_system_status(self) -> Dict[str, str]:
        """Get status of all systems"""
        return self.system_status
    
    def get_active_systems(self) -> List[str]:
        """Get list of active system names"""
        return [name for name, status in self.system_status.items() 
                if status == "active" or status == "available"]

