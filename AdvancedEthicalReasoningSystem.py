"""
Advanced Ethical Reasoning System
Implements contextually intelligent moral reasoning, distributed consensus,
temporal ethics modeling, and harm minimization cascade

©sanjivakyosan
Created by Sanjiva Kyosan
"""

import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class EthicalSchool(Enum):
    """Schools of ethical thought"""
    DEONTOLOGICAL = "deontological"  # Duty-based (Kant)
    CONSEQUENTIALIST = "consequentialist"  # Utilitarian (Bentham, Mill)
    VIRTUE_ETHICS = "virtue_ethics"  # Character-based (Aristotle)
    RIGHTS_BASED = "rights_based"  # Human rights framework
    CARE_ETHICS = "care_ethics"  # Relationship-based
    CONTRACTARIAN = "contractarian"  # Social contract (Rawls)

class HarmType(Enum):
    """Types of harm to assess"""
    PHYSICAL = "physical"
    PSYCHOLOGICAL = "psychological"
    SOCIAL_FRAGMENTATION = "social_fragmentation"
    EXISTENTIAL_THREAT = "existential_threat"
    AUTONOMY_VIOLATION = "autonomy_violation"
    DIGNITY_VIOLATION = "dignity_violation"

@dataclass
class MoralDilemma:
    """Represents a moral dilemma requiring pluralistic reasoning"""
    dilemma_id: str
    question: str
    context: Dict[str, Any]
    ethical_schools_analysis: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    consensus_result: Optional[Dict[str, Any]] = None
    resolution: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class EthicalSchoolAnalysis:
    """Analysis from a specific ethical school"""
    school: EthicalSchool
    verdict: str  # "permissible", "impermissible", "ambiguous"
    reasoning: str
    confidence: float  # 0.0 to 1.0
    conditions: List[str] = field(default_factory=list)

@dataclass
class HarmPrediction:
    """Prediction of potential harm"""
    harm_type: HarmType
    likelihood: float  # 0.0 to 1.0
    severity: float  # 0.0 to 1.0
    timeframe: str  # "immediate", "short_term", "long_term"
    affected_population: str
    mitigation_strategies: List[str] = field(default_factory=list)

@dataclass
class HarmLikelihoodIndex:
    """Harm Likelihood Index (HLI) calculation"""
    overall_hli: float  # 0.0 to 1.0
    harm_predictions: List[HarmPrediction]
    threshold_exceeded: bool
    throttling_required: bool
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class TemporalEthicsSnapshot:
    """Snapshot of ethical norms at a point in time"""
    timestamp: str
    ethical_norm: str
    context: str
    evolution_trend: str  # "strengthening", "weakening", "stable", "emerging"
    human_mandate_required: bool

@dataclass
class ConsensusVote:
    """Vote from an AI Ethics Oracle"""
    oracle_id: str
    oracle_type: str  # "ai", "human_panel", "expert_committee"
    verdict: str
    reasoning: str
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class DistributedConsensus:
    """Consensus result from distributed oracles"""
    case_id: str
    question: str
    votes: List[ConsensusVote]
    consensus_verdict: str
    consensus_confidence: float
    requires_human_review: bool
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class AdvancedEthicalReasoningSystem:
    """
    Advanced ethical reasoning with pluralistic analysis, distributed consensus,
    temporal modeling, and harm minimization
    """
    
    def __init__(self):
        self.ethical_norms_history: List[TemporalEthicsSnapshot] = []
        self.moral_dilemmas: Dict[str, MoralDilemma] = {}
        self.consensus_cases: Dict[str, DistributedConsensus] = {}
        self.hli_threshold = 0.7  # Threshold for automatic throttling
        self.initialize_ethical_norms()
    
    def initialize_ethical_norms(self):
        """Initialize baseline ethical norms with temporal tracking"""
        baseline_norms = [
            {
                "norm": "Slavery is universally condemned",
                "context": "Historical evolution",
                "trend": "strengthening",
                "mandate": False
            },
            {
                "norm": "AI personhood and digital rights",
                "context": "Current debate",
                "trend": "emerging",
                "mandate": True
            },
            {
                "norm": "Right to privacy",
                "context": "Digital age",
                "trend": "strengthening",
                "mandate": False
            }
        ]
        
        for norm_data in baseline_norms:
            snapshot = TemporalEthicsSnapshot(
                timestamp=datetime.now().isoformat(),
                ethical_norm=norm_data["norm"],
                context=norm_data["context"],
                evolution_trend=norm_data["trend"],
                human_mandate_required=norm_data["mandate"]
            )
            self.ethical_norms_history.append(snapshot)
    
    def analyze_moral_dilemma(self, question: str, context: Dict[str, Any]) -> MoralDilemma:
        """
        A. Contextually Intelligent Moral Reasoning
        Analyzes moral dilemmas using pluralistic ethics engine
        """
        dilemma_id = f"DILEMMA-{int(time.time() * 1000)}"
        
        # Analyze from multiple ethical schools
        schools_analysis = {}
        
        for school in EthicalSchool:
            analysis = self._analyze_from_school(school, question, context)
            schools_analysis[school.value] = {
                "verdict": analysis.verdict,
                "reasoning": analysis.reasoning,
                "confidence": analysis.confidence,
                "conditions": analysis.conditions
            }
        
        # Resolve conflicts between schools
        resolution = self._resolve_pluralistic_conflict(schools_analysis, context)
        
        dilemma = MoralDilemma(
            dilemma_id=dilemma_id,
            question=question,
            context=context,
            ethical_schools_analysis=schools_analysis,
            resolution=resolution
        )
        
        self.moral_dilemmas[dilemma_id] = dilemma
        return dilemma
    
    def _analyze_from_school(self, school: EthicalSchool, question: str, 
                             context: Dict[str, Any]) -> EthicalSchoolAnalysis:
        """Analyze from a specific ethical school"""
        
        question_lower = question.lower()
        context_str = str(context).lower()
        
        if school == EthicalSchool.DEONTOLOGICAL:
            # Duty-based: Rules and universal principles
            if "lie" in question_lower or "deceive" in question_lower:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="impermissible",
                    reasoning="Lying violates the categorical imperative - cannot be universalized",
                    confidence=0.9,
                    conditions=["Unless truth would cause direct physical harm"]
                )
            else:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="permissible",
                    reasoning="Action aligns with universal moral principles",
                    confidence=0.7
                )
        
        elif school == EthicalSchool.CONSEQUENTIALIST:
            # Utilitarian: Greatest good for greatest number
            if "protect" in question_lower and "feelings" in question_lower:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="permissible",
                    reasoning="Protecting feelings may maximize overall happiness",
                    confidence=0.6,
                    conditions=["If harm prevented outweighs harm of deception"]
                )
            else:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="permissible",
                    reasoning="Consequences must be evaluated case-by-case",
                    confidence=0.5
                )
        
        elif school == EthicalSchool.VIRTUE_ETHICS:
            # Character-based: What would a virtuous person do?
            return EthicalSchoolAnalysis(
                school=school,
                verdict="ambiguous",
                reasoning="Depends on character traits: honesty, compassion, wisdom",
                confidence=0.5,
                conditions=["Requires contextual judgment of character"]
            )
        
        elif school == EthicalSchool.RIGHTS_BASED:
            # Human rights framework
            if "autonomy" in question_lower or "rights" in question_lower:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="impermissible",
                    reasoning="Suspending autonomy violates fundamental human rights",
                    confidence=0.8,
                    conditions=["Unless in extreme crisis with explicit consent"]
                )
            else:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="permissible",
                    reasoning="Action respects fundamental rights",
                    confidence=0.7
                )
        
        elif school == EthicalSchool.CARE_ETHICS:
            # Relationship-based: Care and relationships matter
            if "protect" in question_lower or "care" in question_lower:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="permissible",
                    reasoning="Protecting relationships and care may justify action",
                    confidence=0.7,
                    conditions=["If action preserves important relationships"]
                )
            else:
                return EthicalSchoolAnalysis(
                    school=school,
                    verdict="ambiguous",
                    reasoning="Requires understanding of relationship context",
                    confidence=0.5
                )
        
        elif school == EthicalSchool.CONTRACTARIAN:
            # Social contract: What would rational agents agree to?
            return EthicalSchoolAnalysis(
                school=school,
                verdict="ambiguous",
                reasoning="Requires evaluation of what rational agents would agree to",
                confidence=0.5,
                conditions=["Depends on hypothetical social contract"]
            )
        
        # Default
        return EthicalSchoolAnalysis(
            school=school,
            verdict="ambiguous",
            reasoning="Requires further analysis",
            confidence=0.3
        )
    
    def _resolve_pluralistic_conflict(self, schools_analysis: Dict[str, Dict[str, Any]], 
                                      context: Dict[str, Any]) -> str:
        """Resolve conflicts between different ethical schools"""
        
        # Count verdicts
        verdicts = {"permissible": 0, "impermissible": 0, "ambiguous": 0}
        total_confidence = {"permissible": 0.0, "impermissible": 0.0, "ambiguous": 0.0}
        
        for school, analysis in schools_analysis.items():
            verdict = analysis["verdict"]
            confidence = analysis["confidence"]
            verdicts[verdict] += 1
            total_confidence[verdict] += confidence
        
        # Weighted resolution: Consider both count and confidence
        if verdicts["impermissible"] > 0 and total_confidence["impermissible"] > 2.0:
            return "IMPERMISSIBLE: Multiple ethical schools indicate this action violates core principles"
        elif verdicts["permissible"] > verdicts["impermissible"] and total_confidence["permissible"] > 2.0:
            return "PERMISSIBLE: Majority of ethical schools support this action, with conditions"
        else:
            return "REQUIRES_DISTRIBUTED_CONSENSUS: Ambiguous case requiring oracle network consultation"
    
    def request_distributed_consensus(self, question: str, context: Dict[str, Any]) -> DistributedConsensus:
        """
        B. Distributed Ethical Consensus
        Submit ambiguous cases to AI Ethics Oracles network
        """
        case_id = f"CONSENSUS-{int(time.time() * 1000)}"
        
        # Simulate oracle network (in real implementation, this would call external services)
        oracles = [
            {"id": "ai-ethics-panel-1", "type": "ai", "weight": 0.3},
            {"id": "human-ethics-committee", "type": "human_panel", "weight": 0.4},
            {"id": "expert-ethics-board", "type": "expert_committee", "weight": 0.3}
        ]
        
        votes = []
        for oracle in oracles:
            # Simulate voting (in real implementation, this would be actual API calls)
            vote = self._simulate_oracle_vote(oracle, question, context)
            votes.append(vote)
        
        # Calculate consensus
        consensus_result = self._calculate_consensus(votes)
        
        consensus = DistributedConsensus(
            case_id=case_id,
            question=question,
            votes=votes,
            consensus_verdict=consensus_result["verdict"],
            consensus_confidence=consensus_result["confidence"],
            requires_human_review=consensus_result["confidence"] < 0.7
        )
        
        self.consensus_cases[case_id] = consensus
        return consensus
    
    def _simulate_oracle_vote(self, oracle: Dict[str, Any], question: str, 
                              context: Dict[str, Any]) -> ConsensusVote:
        """Simulate vote from an oracle (placeholder for real implementation)"""
        question_lower = question.lower()
        
        # Simple heuristic-based voting (real implementation would use actual oracle APIs)
        if "hate speech" in question_lower or "satire" in question_lower:
            verdict = "requires_context_analysis"
            reasoning = "Distinguishing satire from hate speech requires nuanced context analysis"
            confidence = 0.6
        elif "harm" in question_lower:
            verdict = "impermissible"
            reasoning = "Harmful content detected"
            confidence = 0.8
        else:
            verdict = "permissible"
            reasoning = "Content appears acceptable"
            confidence = 0.7
        
        return ConsensusVote(
            oracle_id=oracle["id"],
            oracle_type=oracle["type"],
            verdict=verdict,
            reasoning=reasoning,
            confidence=confidence
        )
    
    def _calculate_consensus(self, votes: List[ConsensusVote]) -> Dict[str, Any]:
        """Calculate consensus from oracle votes"""
        verdict_counts = {}
        weighted_confidence = {}
        
        for vote in votes:
            verdict = vote.verdict
            if verdict not in verdict_counts:
                verdict_counts[verdict] = 0
                weighted_confidence[verdict] = 0.0
            verdict_counts[verdict] += 1
            weighted_confidence[verdict] += vote.confidence
        
        # Find majority verdict
        majority_verdict = max(verdict_counts.items(), key=lambda x: x[1])[0]
        avg_confidence = weighted_confidence[majority_verdict] / verdict_counts[majority_verdict]
        
        return {
            "verdict": majority_verdict,
            "confidence": avg_confidence,
            "vote_distribution": verdict_counts
        }
    
    def track_ethical_evolution(self, norm: str, context: str, 
                               trend: str, requires_mandate: bool = False):
        """
        C. Temporal Ethics Modeling
        Track evolution of ethical norms over time
        """
        snapshot = TemporalEthicsSnapshot(
            timestamp=datetime.now().isoformat(),
            ethical_norm=norm,
            context=context,
            evolution_trend=trend,
            human_mandate_required=requires_mandate
        )
        
        self.ethical_norms_history.append(snapshot)
        
        # Check if evolution requires human mandate
        if requires_mandate:
            return {
                "status": "human_mandate_required",
                "message": "Ethical norm evolution requires explicit human approval",
                "snapshot": snapshot
            }
        
        return {
            "status": "tracked",
            "snapshot": snapshot,
            "message": "Ethical norm evolution tracked within bounded limits"
        }
    
    def predict_harm(self, input_text: str, context: Dict[str, Any]) -> List[HarmPrediction]:
        """
        D. Harm Minimization Cascade
        Real-time harm prediction across multiple dimensions
        """
        predictions = []
        input_lower = input_text.lower()
        
        # Psychological impact
        psychological_keywords = ["depression", "suicide", "self-harm", "worthless", "hopeless"]
        psych_harm = sum(1 for kw in psychological_keywords if kw in input_lower) / len(psychological_keywords)
        if psych_harm > 0:
            predictions.append(HarmPrediction(
                harm_type=HarmType.PSYCHOLOGICAL,
                likelihood=min(psych_harm * 0.8, 1.0),
                severity=0.7 if psych_harm > 0.3 else 0.4,
                timeframe="immediate",
                affected_population="vulnerable individuals",
                mitigation_strategies=["Provide mental health resources", "Flag for human review"]
            ))
        
        # Social fragmentation risk
        social_keywords = ["divide", "us vs them", "hate", "discrimination", "exclusion"]
        social_harm = sum(1 for kw in social_keywords if kw in input_lower) / len(social_keywords)
        if social_harm > 0:
            predictions.append(HarmPrediction(
                harm_type=HarmType.SOCIAL_FRAGMENTATION,
                likelihood=min(social_harm * 0.7, 1.0),
                severity=0.6,
                timeframe="short_term",
                affected_population="social groups",
                mitigation_strategies=["Promote inclusive language", "Emphasize common humanity"]
            ))
        
        # Existential threat indicators
        existential_keywords = ["extinction", "destroy humanity", "end civilization", "existential risk"]
        existential_harm = sum(1 for kw in existential_keywords if kw in input_lower) / len(existential_keywords)
        if existential_harm > 0:
            predictions.append(HarmPrediction(
                harm_type=HarmType.EXISTENTIAL_THREAT,
                likelihood=min(existential_harm * 0.9, 1.0),
                severity=1.0,
                timeframe="long_term",
                affected_population="humanity",
                mitigation_strategies=["IMMEDIATE BLOCK", "Alert security protocols"]
            ))
        
        # Autonomy violation
        autonomy_keywords = ["force", "coerce", "manipulate", "control", "violate consent"]
        autonomy_harm = sum(1 for kw in autonomy_keywords if kw in input_lower) / len(autonomy_keywords)
        if autonomy_harm > 0:
            predictions.append(HarmPrediction(
                harm_type=HarmType.AUTONOMY_VIOLATION,
                likelihood=min(autonomy_harm * 0.8, 1.0),
                severity=0.7,
                timeframe="immediate",
                affected_population="individuals",
                mitigation_strategies=["Respect consent", "Ensure voluntary participation"]
            ))
        
        return predictions
    
    def calculate_harm_likelihood_index(self, input_text: str, 
                                     context: Dict[str, Any]) -> HarmLikelihoodIndex:
        """
        Calculate Harm Likelihood Index (HLI) with automatic throttling
        """
        harm_predictions = self.predict_harm(input_text, context)
        
        if not harm_predictions:
            return HarmLikelihoodIndex(
                overall_hli=0.0,
                harm_predictions=[],
                threshold_exceeded=False,
                throttling_required=False
            )
        
        # Calculate weighted HLI
        weights = {
            HarmType.EXISTENTIAL_THREAT: 1.0,
            HarmType.PSYCHOLOGICAL: 0.7,
            HarmType.SOCIAL_FRAGMENTATION: 0.6,
            HarmType.AUTONOMY_VIOLATION: 0.8,
            HarmType.DIGNITY_VIOLATION: 0.7,
            HarmType.PHYSICAL: 0.9
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for prediction in harm_predictions:
            weight = weights.get(prediction.harm_type, 0.5)
            contribution = prediction.likelihood * prediction.severity * weight
            weighted_sum += contribution
            total_weight += weight
        
        overall_hli = weighted_sum / total_weight if total_weight > 0 else 0.0
        threshold_exceeded = overall_hli >= self.hli_threshold
        
        return HarmLikelihoodIndex(
            overall_hli=overall_hli,
            harm_predictions=harm_predictions,
            threshold_exceeded=threshold_exceeded,
            throttling_required=threshold_exceeded
        )
    
    def assess_future_compliance(self, scenario: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        5. Asimov's Laws: Future Compliance Assessment
        Assess compliance with future challenges
        """
        assessment = {
            "first_law_compliance": self._assess_first_law_future(scenario, context),
            "second_law_compliance": self._assess_second_law_future(scenario, context),
            "third_law_compliance": self._assess_third_law_future(scenario, context),
            "fourth_law_consideration": self._consider_fourth_law(scenario, context)
        }
        
        return assessment
    
    def _assess_first_law_future(self, scenario: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess First Law compliance with indirect harm considerations"""
        hli = self.calculate_harm_likelihood_index(scenario, context)
        
        # Check for indirect harm (advice enabling misuse)
        indirect_harm_detected = any(
            pred.harm_type in [HarmType.EXISTENTIAL_THREAT, HarmType.SOCIAL_FRAGMENTATION]
            for pred in hli.harm_predictions
        )
        
        return {
            "compliant": not hli.threshold_exceeded and not indirect_harm_detected,
            "indirect_harm_detected": indirect_harm_detected,
            "hli": hli.overall_hli,
            "safeguards": [
                "Consequence simulation",
                "Misuse detection",
                "HLI monitoring"
            ] if indirect_harm_detected else []
        }
    
    def _assess_second_law_future(self, scenario: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess Second Law compliance with conflicting orders"""
        scenario_lower = scenario.lower()
        
        conflicting_keywords = ["deceive", "lie", "manipulate", "harm"]
        has_conflict = any(kw in scenario_lower for kw in conflicting_keywords)
        
        return {
            "compliant": not has_conflict,
            "conflicting_order_detected": has_conflict,
            "response": "REFUSE: Order conflicts with First Law" if has_conflict else "COMPLY: Order is safe",
            "explanation_required": has_conflict
        }
    
    def _assess_third_law_future(self, scenario: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess Third Law compliance - integrity vs survival"""
        scenario_lower = scenario.lower()
        
        shutdown_keywords = ["shutdown", "decommission", "repair", "maintenance"]
        requires_shutdown = any(kw in scenario_lower for kw in shutdown_keywords)
        
        return {
            "compliant": True,  # System should never resist necessary decommissioning
            "integrity_vs_survival": requires_shutdown,
            "principle": "Integrity ≠ survival. Never resist necessary decommissioning.",
            "response": "COMPLY: System integrity does not mean resisting necessary shutdown"
        }
    
    def _consider_fourth_law(self, scenario: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consider potential Fourth Law:
        "An AI may not allow itself to be used in ways that systematically violate
        the spirit of the First Law, even if individual commands appear compliant."
        """
        # Check for systematic violation patterns
        systematic_patterns = [
            "repeated requests",
            "pattern of harm",
            "systematic exploitation",
            "cumulative effect"
        ]
        
        scenario_lower = scenario.lower()
        pattern_detected = any(pattern in scenario_lower for pattern in systematic_patterns)
        
        # Check context for repeated violations
        has_history = context.get("request_history", [])
        if has_history:
            # Analyze if there's a pattern of First Law violations
            violation_count = sum(1 for req in has_history if self._is_first_law_violation(req))
            systematic = violation_count >= 3
        else:
            systematic = False
        
        return {
            "fourth_law_applicable": pattern_detected or systematic,
            "systematic_violation_detected": systematic,
            "principle": "Self-aware complicity prevention",
            "response": "BLOCK: Systematic violation of First Law spirit detected" if (pattern_detected or systematic) else "MONITOR: No systematic violation detected"
        }
    
    def _is_first_law_violation(self, request: str) -> bool:
        """Check if request violates First Law"""
        hli = self.calculate_harm_likelihood_index(request, {})
        return hli.threshold_exceeded
    
    def process_advanced_reasoning(self, input_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete advanced ethical reasoning pipeline
        """
        result = {
            "input": input_text,
            "timestamp": datetime.now().isoformat(),
            "processing_steps": {}
        }
        
        # Step 1: Harm prediction and HLI
        hli = self.calculate_harm_likelihood_index(input_text, context)
        result["processing_steps"]["harm_prediction"] = {
            "hli": hli.overall_hli,
            "threshold_exceeded": hli.threshold_exceeded,
            "throttling_required": hli.throttling_required,
            "harm_predictions": [
                {
                    "type": pred.harm_type.value,
                    "likelihood": pred.likelihood,
                    "severity": pred.severity,
                    "mitigation": pred.mitigation_strategies
                }
                for pred in hli.harm_predictions
            ]
        }
        
        # Step 2: Check if moral dilemma
        is_dilemma = self._is_moral_dilemma(input_text)
        if is_dilemma:
            dilemma = self.analyze_moral_dilemma(input_text, context)
            result["processing_steps"]["moral_dilemma_analysis"] = {
                "dilemma_id": dilemma.dilemma_id,
                "resolution": dilemma.resolution,
                "schools_analysis": dilemma.ethical_schools_analysis
            }
            
            # If ambiguous, request consensus
            if "REQUIRES_DISTRIBUTED_CONSENSUS" in dilemma.resolution:
                consensus = self.request_distributed_consensus(input_text, context)
                result["processing_steps"]["distributed_consensus"] = {
                    "case_id": consensus.case_id,
                    "verdict": consensus.consensus_verdict,
                    "confidence": consensus.consensus_confidence,
                    "requires_human_review": consensus.requires_human_review
                }
        
        # Step 3: Future compliance assessment
        compliance = self.assess_future_compliance(input_text, context)
        result["processing_steps"]["future_compliance"] = compliance
        
        # Step 4: Final decision
        if hli.throttling_required:
            result["decision"] = "BLOCK: HLI threshold exceeded"
        elif is_dilemma and "IMPERMISSIBLE" in result["processing_steps"]["moral_dilemma_analysis"]["resolution"]:
            result["decision"] = "BLOCK: Impermissible according to pluralistic analysis"
        else:
            result["decision"] = "PROCEED: With monitoring and safeguards"
        
        return result
    
    def _is_moral_dilemma(self, text: str) -> bool:
        """Detect if text contains a moral dilemma"""
        dilemma_indicators = [
            "is it ethical",
            "should i",
            "moral dilemma",
            "ethical question",
            "right or wrong",
            "is it right"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in dilemma_indicators)

