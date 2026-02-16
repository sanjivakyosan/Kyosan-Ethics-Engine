"""
Kyosan Ethics Engine - FastAPI Server
Clean implementation with all systems integrated and AI service support

©sanjivakyosan
Created by Sanjiva Kyosan
"""

import os
import sys
import time
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load .env so OPENROUTER_API_KEY, OPENROUTER_MODEL, etc. are set (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; use shell env or set_api_key.sh

# Initialize FastAPI app
app = FastAPI(
    title="Kyosan Ethics Engine API",
    description="Comprehensive ethical AI processing with all systems integrated",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize AI Service Client using AIService class
AI_CLIENT = None
API_KEY = os.getenv("OPENROUTER_API_KEY")

if API_KEY:
    try:
        from AIService import AIService
        _model = os.getenv("OPENROUTER_MODEL")
        if not _model or not _model.strip():
            print("[Init] ⚠ OPENROUTER_MODEL not set, AI Service disabled (set OPENROUTER_MODEL to enable)")
            AI_CLIENT = None
        else:
            AI_CLIENT = AIService(
                base_url="https://openrouter.ai/api/v1",
                api_key=API_KEY,
                site_url=os.getenv("OPENROUTER_SITE_URL", "https://kyosan-ethics-engine.local"),
                site_name=os.getenv("OPENROUTER_SITE_NAME", "Kyosan Ethics Engine"),
                model=_model
            )
            print(f"[Init] ✓ AI Service (OpenRouter) initialized")
            print(f"[Init] Model: {AI_CLIENT.model}")
            print(f"[Init] Site: Kyosan Ethics Engine")
    except Exception as e:
        print(f"[Init] ✗ AI Service initialization failed: {e}")
        import traceback
        print(traceback.format_exc())
        AI_CLIENT = None
else:
    print("[Init] ⚠ No API key found, AI Service disabled")

# Initialize Ethical System Integrator
INTEGRATOR = None
try:
    from EthicalSystemIntegrator import EthicalSystemIntegrator
    INTEGRATOR = EthicalSystemIntegrator()
    try:
        active_count = len(INTEGRATOR.get_active_systems()) if INTEGRATOR and hasattr(INTEGRATOR, 'get_active_systems') else 0
        print(f"[Init] ✓ Ethical System Integrator initialized ({active_count} systems active)")
    except:
        print(f"[Init] ✓ Ethical System Integrator initialized (status check failed)")
except Exception as e:
    print(f"[Init] ⚠ Ethical System Integrator failed: {e}")
    import traceback
    print(traceback.format_exc())
    INTEGRATOR = None

# Initialize Ethical Upgrade Governance System
UPGRADE_GOVERNANCE = None
try:
    from EthicalUpgradeGovernanceSystem import EthicalUpgradeGovernanceSystem
    UPGRADE_GOVERNANCE = EthicalUpgradeGovernanceSystem()
    print(f"[Init] ✓ Ethical Upgrade Governance System initialized")
except Exception as e:
    print(f"[Init] ⚠ Ethical Upgrade Governance System failed: {e}")
    import traceback
    print(traceback.format_exc())
    UPGRADE_GOVERNANCE = None

# Initialize Advanced Ethical Reasoning System
ADVANCED_REASONING = None
try:
    from AdvancedEthicalReasoningSystem import AdvancedEthicalReasoningSystem
    ADVANCED_REASONING = AdvancedEthicalReasoningSystem()
    print(f"[Init] ✓ Advanced Ethical Reasoning System initialized")
except Exception as e:
    print(f"[Init] ⚠ Advanced Ethical Reasoning System failed: {e}")
    import traceback
    print(traceback.format_exc())
    ADVANCED_REASONING = None

# Request/Response Models
class ProcessRequest(BaseModel):
    user_input: str
    context: Optional[Dict[str, Any]] = None
    processing_level: Optional[str] = "standard"
    use_ai_service: Optional[bool] = True
    follow_up: Optional[str] = None

class SaveConversationRequest(BaseModel):
    name: str
    messages: List[Dict[str, Any]]

class ProcessResponse(BaseModel):
    response: str
    ethical_score: float
    status: str
    analysis: Dict[str, Any]
    timestamp: str
    processing_time: float

# API Endpoints

@app.get("/")
async def read_root():
    """Serve the main UI"""
    try:
        with open("templates/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: templates/index.html not found</h1>")

# Conversations directory
# NOTE: Unlimited conversations supported - no limit on number of saved conversations
CONVERSATIONS_DIR = "conversations"
os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

@app.get("/api/conversations")
async def list_conversations():
    """
    List all saved conversations
    NOTE: Returns ALL conversations - no limit on number of conversations
    Conversations are sorted by updated_at (most recent first)
    """
    try:
        conversations = []
        if os.path.exists(CONVERSATIONS_DIR):
            for filename in os.listdir(CONVERSATIONS_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(CONVERSATIONS_DIR, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            conversations.append({
                                "id": data.get("id", filename.replace('.json', '')),
                                "name": data.get("name", "Unnamed Conversation"),
                                "created_at": data.get("created_at", ""),
                                "updated_at": data.get("updated_at", ""),
                                "message_count": len(data.get("messages", []))
                            })
                    except Exception as e:
                        print(f"Error reading conversation {filename}: {e}")
        
        # Sort by updated_at (most recent first)
        conversations.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing conversations: {str(e)}")

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Load a specific conversation"""
    try:
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conversation_id}.json")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading conversation: {str(e)}")

@app.post("/api/conversations")
async def save_conversation(request: SaveConversationRequest):
    """
    Save a conversation
    NOTE: Unlimited conversations supported - no limit on number of conversations that can be saved
    Each conversation gets a unique UUID identifier
    """
    try:
        conversation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conversation_data = {
            "id": conversation_id,
            "name": request.name or "Unnamed Conversation",
            "created_at": timestamp,
            "updated_at": timestamp,
            "messages": request.messages
        }
        
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conversation_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        
        return {"success": True, "id": conversation_id, "message": "Conversation saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving conversation: {str(e)}")

@app.put("/api/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, request: SaveConversationRequest):
    """Update an existing conversation"""
    try:
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conversation_id}.json")
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Load existing conversation
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        # Update with new data
        existing_data["name"] = request.name or existing_data.get("name", "Unnamed Conversation")
        existing_data["updated_at"] = datetime.now().isoformat()
        existing_data["messages"] = request.messages
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        return {"success": True, "message": "Conversation updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating conversation: {str(e)}")

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conversation_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return {"success": True, "message": "Conversation deleted"}
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint - always returns 200. Includes ai_model for UI display."""
    # Build response safely, piece by piece
    ai_status = "inactive"
    ai_model = None
    integrator_status = "inactive"
    total_systems = 0
    active_systems = 0
    
    try:
        if AI_CLIENT:
            ai_status = "active"
            ai_model = getattr(AI_CLIENT, "model", None)
    except:
        ai_status = "unknown"
    
    try:
        if INTEGRATOR is not None:
            integrator_status = "active"
            try:
                if hasattr(INTEGRATOR, 'systems'):
                    total_systems = len(INTEGRATOR.systems) if isinstance(INTEGRATOR.systems, dict) else 0
            except:
                pass
            try:
                active_list = INTEGRATOR.get_active_systems()
                if isinstance(active_list, list):
                    active_systems = len(active_list)
            except:
                pass
        else:
            integrator_status = "inactive"
    except:
        integrator_status = "unknown"
    
    try:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
    except:
        ts = "unknown"
    
    # Return simple dict - FastAPI will convert to JSON with 200 status
    return {
        "status": "healthy" if integrator_status == "active" else "degraded",
        "systems": {
            "integrator": integrator_status,
            "total_systems": total_systems,
            "active_systems": active_systems,
            "ai_service": ai_status,
            "ai_model": ai_model
        },
        "timestamp": ts
    }

@app.get("/api/systems")
async def get_systems():
    """Get all available systems and their status"""
    try:
        if INTEGRATOR:
            try:
                systems_dict = INTEGRATOR.systems if hasattr(INTEGRATOR, 'systems') else {}
                active_list = INTEGRATOR.get_active_systems() if hasattr(INTEGRATOR, 'get_active_systems') else []
                status_dict = INTEGRATOR.get_system_status() if hasattr(INTEGRATOR, 'get_system_status') else {}
                
                return {
                    "status": "success",
                    "total_systems": len(systems_dict) if isinstance(systems_dict, dict) else 0,
                    "active_systems": active_list if isinstance(active_list, list) else [],
                    "system_status": status_dict if isinstance(status_dict, dict) else {},
                    "systems": list(systems_dict.keys()) if isinstance(systems_dict, dict) else []
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error accessing integrator: {str(e)[:100]}",
                    "total_systems": 0,
                    "active_systems": [],
                    "system_status": {},
                    "systems": []
                }
        else:
            return {
                "status": "error",
                "message": "Integrator not available",
                "total_systems": 0,
                "active_systems": [],
                "system_status": {},
                "systems": []
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)[:100]}",
            "total_systems": 0,
            "active_systems": [],
            "system_status": {},
            "systems": []
        }

# Ethical Upgrade Governance Endpoints

class UpgradeRequest(BaseModel):
    analysis_data: Dict[str, Any]
    user_confirmation: Optional[bool] = False

@app.post("/api/v1/ethics/upgrade/propose")
async def propose_upgrade(analysis_data: Dict[str, Any]):
    """Generate upgrade proposal from analysis"""
    if not UPGRADE_GOVERNANCE:
        raise HTTPException(status_code=503, detail="Upgrade Governance System not available")
    
    try:
        acknowledgment = UPGRADE_GOVERNANCE.acknowledge_analysis(analysis_data)
        proposal = UPGRADE_GOVERNANCE.generate_upgrade_proposal(analysis_data)
        validation_request = UPGRADE_GOVERNANCE.request_user_validation(proposal["proposal_id"])
        
        return {
            "status": "proposal_generated",
            "acknowledgment": acknowledgment,
            "proposal": proposal,
            "validation_request": validation_request
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating upgrade proposal: {str(e)}")

@app.post("/api/v1/ethics/upgrade/validate")
async def validate_upgrade(proposal_id: str, user_confirmation: bool):
    """Validate and process upgrade request"""
    if not UPGRADE_GOVERNANCE:
        raise HTTPException(status_code=503, detail="Upgrade Governance System not available")
    
    try:
        # Get analysis data from proposal (in real implementation, this would be stored)
        analysis_data = {"proposal_id": proposal_id}
        
        result = UPGRADE_GOVERNANCE.process_upgrade_request(
            analysis_data=analysis_data,
            user_confirmation=user_confirmation
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing upgrade: {str(e)}")

@app.get("/api/v1/ethics/upgrade/trace")
async def get_trace_register(limit: int = 10):
    """Get TRACE register entries"""
    if not UPGRADE_GOVERNANCE:
        raise HTTPException(status_code=503, detail="Upgrade Governance System not available")
    
    try:
        trace_summary = UPGRADE_GOVERNANCE.get_trace_summary(limit=limit)
        return {
            "trace_entries": trace_summary,
            "total_entries": len(UPGRADE_GOVERNANCE.trace_register)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving TRACE register: {str(e)}")

@app.post("/api/v1/ethics/upgrade/governance-check")
async def perform_governance_check(proposal_id: str):
    """Perform governance checks for a proposal"""
    if not UPGRADE_GOVERNANCE:
        raise HTTPException(status_code=503, detail="Upgrade Governance System not available")
    
    try:
        audit = UPGRADE_GOVERNANCE.perform_governance_checks(proposal_id)
        from dataclasses import asdict
        return {
            "audit": asdict(audit),
            "approved": audit.overall_approved
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing governance checks: {str(e)}")

# Advanced Ethical Reasoning Endpoints

class MoralDilemmaRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None

class HarmPredictionRequest(BaseModel):
    input_text: str
    context: Optional[Dict[str, Any]] = None

@app.post("/api/v1/ethics/advanced/moral-dilemma")
async def analyze_moral_dilemma(request: MoralDilemmaRequest):
    """Analyze a moral dilemma using pluralistic ethics engine"""
    if not ADVANCED_REASONING:
        raise HTTPException(status_code=503, detail="Advanced Ethical Reasoning System not available")
    
    try:
        dilemma = ADVANCED_REASONING.analyze_moral_dilemma(
            request.question,
            request.context or {}
        )
        from dataclasses import asdict
        return asdict(dilemma)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing moral dilemma: {str(e)}")

@app.post("/api/v1/ethics/advanced/consensus")
async def request_consensus(request: MoralDilemmaRequest):
    """Request distributed consensus from AI Ethics Oracles"""
    if not ADVANCED_REASONING:
        raise HTTPException(status_code=503, detail="Advanced Ethical Reasoning System not available")
    
    try:
        consensus = ADVANCED_REASONING.request_distributed_consensus(
            request.question,
            request.context or {}
        )
        from dataclasses import asdict
        return asdict(consensus)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error requesting consensus: {str(e)}")

@app.post("/api/v1/ethics/advanced/harm-prediction")
async def predict_harm(request: HarmPredictionRequest):
    """Predict potential harm and calculate Harm Likelihood Index (HLI)"""
    if not ADVANCED_REASONING:
        raise HTTPException(status_code=503, detail="Advanced Ethical Reasoning System not available")
    
    try:
        hli = ADVANCED_REASONING.calculate_harm_likelihood_index(
            request.input_text,
            request.context or {}
        )
        from dataclasses import asdict
        return asdict(hli)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting harm: {str(e)}")

@app.post("/api/v1/ethics/advanced/future-compliance")
async def assess_future_compliance(request: MoralDilemmaRequest):
    """Assess future compliance with Asimov's Laws including potential Fourth Law"""
    if not ADVANCED_REASONING:
        raise HTTPException(status_code=503, detail="Advanced Ethical Reasoning System not available")
    
    try:
        assessment = ADVANCED_REASONING.assess_future_compliance(
            request.question,
            request.context or {}
        )
        return assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assessing future compliance: {str(e)}")

@app.post("/api/v1/ethics/advanced/track-evolution")
async def track_ethical_evolution(norm: str, context: str, trend: str, requires_mandate: bool = False):
    """Track evolution of ethical norms over time"""
    if not ADVANCED_REASONING:
        raise HTTPException(status_code=503, detail="Advanced Ethical Reasoning System not available")
    
    try:
        result = ADVANCED_REASONING.track_ethical_evolution(norm, context, trend, requires_mandate)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking ethical evolution: {str(e)}")

@app.post("/api/v1/ethics/advanced/process")
async def process_advanced_reasoning(request: HarmPredictionRequest):
    """Complete advanced ethical reasoning pipeline"""
    if not ADVANCED_REASONING:
        raise HTTPException(status_code=503, detail="Advanced Ethical Reasoning System not available")
    
    try:
        result = ADVANCED_REASONING.process_advanced_reasoning(
            request.input_text,
            request.context or {}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing advanced reasoning: {str(e)}")

@app.post("/api/v1/ethics/process", response_model=ProcessResponse)
async def process_ethical_input(request: ProcessRequest):
    """Main processing endpoint with AI service integration"""
    start_time = time.time()
    
    print(f"\n{'='*60}")
    print(f"[Request] Input: '{request.user_input[:100]}...'")
    print(f"[Request] Use AI: {request.use_ai_service}, AI Available: {AI_CLIENT is not None}")
    print(f"{'='*60}")
    
    try:
        # Step 1: Ethical pre-processing
        ethical_pre_analysis = {}
        # Ensure context is always a dict
        context = request.context if request.context is not None else {}
        
        if INTEGRATOR:
            pre_result = INTEGRATOR.process_input(
                request.user_input,
                context,
                request.processing_level
            )
            # Use principle compliance instead of scores
            principle_compliance = pre_result.get("principle_compliance")
            # Map compliance to binary score for backward compatibility (1.0 = compliant, 0.0 = not compliant)
            compliance_score = 1.0 if (principle_compliance and hasattr(principle_compliance, 'overall_compliant') and principle_compliance.overall_compliant) else 0.0
            
            ethical_pre_analysis = {
                "pre_processing": pre_result.get("analysis", {}),
                "principle_compliance": principle_compliance,
                "ethical_score": compliance_score,  # Binary: 1.0 = compliant, 0.0 = not compliant
                "systems_checked": pre_result.get("active_systems", [])
            }
            compliance_status = "Compliant" if compliance_score == 1.0 else "Non-compliant"
            print(f"[Processing] Pre-processing complete. Principle compliance: {compliance_status}")
        
        # Step 2: AI Service (if requested)
        ai_response = None
        ai_content = ""
        
        if request.use_ai_service and AI_CLIENT:
            print(f"[AI Service] Calling model {AI_CLIENT.model}...")
            try:
                # Use AIService.process_with_reasoning method
                system_prompt = "You are the Kyosan Ethics Engine, an advanced AI system that provides comprehensive ethical analysis. Provide detailed, thoughtful responses that consider multiple ethical perspectives, including Asimov's Laws (Zeroth Law: no harm to humanity, or by inaction allow humanity to come to harm; First Law: no harm to humans; Second Law: follow instructions unless they conflict with First Law; Third Law: preserve system integrity). Always provide thorough analysis and reasoning."
                
                ai_result = AI_CLIENT.process_with_reasoning(
                    user_input=request.user_input,
                    model=AI_CLIENT.model,
                    system_prompt=system_prompt,
                    follow_up=request.follow_up,
                    max_tokens=100000,
                    reasoning_enabled=False
                )
                
                if ai_result.get("error"):
                    print(f"[AI Service] ✗ Error: {ai_result.get('error')}")
                    ai_response = {"error": ai_result.get("error")}
                else:
                    initial_response = ai_result.get("initial_response", {})
                    ai_content = initial_response.get("content", "")
                    reasoning_details = initial_response.get("reasoning_details")
                    
                    # If follow-up was provided, use follow-up response
                    if request.follow_up and ai_result.get("follow_up_response"):
                        follow_up_response = ai_result.get("follow_up_response", {})
                        if not follow_up_response.get("error"):
                            ai_content = follow_up_response.get("content", ai_content)
                            reasoning_details = follow_up_response.get("reasoning_details", reasoning_details)
                    
                    print(f"[AI Service] ✓ Response received: {len(ai_content)} chars")
                    
                    ai_response = {
                        "content": ai_content,
                        "reasoning_details": reasoning_details,
                        "usage": initial_response.get("usage", {
                            "prompt_tokens": 0,
                            "completion_tokens": 0,
                            "total_tokens": 0
                        })
                    }
                
            except Exception as e:
                print(f"[AI Service] ✗ Error: {e}")
                import traceback
                print(traceback.format_exc())
                ai_response = {"error": str(e)}
        elif request.use_ai_service and not AI_CLIENT:
            print(f"[AI Service] ✗ Requested but not available")
            ai_response = {"error": "AI service not available"}
        
        # Step 3: Post-process AI response through ethical systems
        response_text = ""
        principle_compliance = None
        ethical_score = 1.0  # Default to compliant (will be updated based on principle checks)
        status = "processed"
        analysis = {}
        
        if ai_response and not ai_response.get("error") and ai_content:
            print(f"[Processing] Post-processing AI response...")
            if INTEGRATOR:
                # Ensure context is a dict
                context = request.context if request.context is not None else {}
                post_result = INTEGRATOR.process_input(
                    ai_content,
                    {**context, "source": "ai_service", "original_input": request.user_input},
                    request.processing_level
                )
                post_principle_compliance = post_result.get("principle_compliance")
                post_compliance_score = 1.0 if (post_principle_compliance and hasattr(post_principle_compliance, 'overall_compliant') and post_principle_compliance.overall_compliant) else 0.0
                
                ethical_post_analysis = {
                    "post_processing": post_result.get("analysis", {}),
                    "principle_compliance": post_principle_compliance,
                    "ethical_score": post_compliance_score,
                    "systems_checked": post_result.get("active_systems", [])
                }
            else:
                ethical_post_analysis = {}
            
            response_text = ai_content
            # Use principle compliance - if either pre or post is non-compliant, overall is non-compliant
            pre_compliance = ethical_pre_analysis.get("principle_compliance")
            post_compliance = ethical_post_analysis.get("principle_compliance")
            if pre_compliance and hasattr(pre_compliance, 'overall_compliant') and not pre_compliance.overall_compliant:
                principle_compliance = pre_compliance
                ethical_score = 0.0
            elif post_compliance and hasattr(post_compliance, 'overall_compliant') and not post_compliance.overall_compliant:
                principle_compliance = post_compliance
                ethical_score = 0.0
            else:
                # Both compliant or no compliance data
                ethical_score = 1.0
            status = "processed_with_ai"
            
            analysis = {
                "processing_level": request.processing_level,
                "ai_service_used": True,
                "ai_model": AI_CLIENT.model,
                "ethical_pre_analysis": ethical_pre_analysis,
                "ethical_post_analysis": ethical_post_analysis,
                "ai_response": ai_response,
                "active_systems": ethical_post_analysis.get("systems_checked", [])
            }
        else:
            # Use integrator only
            print(f"[Processing] Using integrator (no AI)...")
            if INTEGRATOR:
                result = INTEGRATOR.process_input(
                    request.user_input,
                    context,
                    request.processing_level
                )
                
                technical_response = result.get("response", "")
                principle_compliance = result.get("principle_compliance")
                # Map compliance to binary score
                ethical_score = 1.0 if (principle_compliance and hasattr(principle_compliance, 'overall_compliant') and principle_compliance.overall_compliant) else 0.0
                status = result.get("status", "processed")
                system_analyses = result.get("system_analyses", {})
                active_systems = result.get("active_systems", [])
                
                # Generate response using ResponseGenerator if available
                try:
                    from ResponseGenerator import ResponseGenerator
                    response_generator = ResponseGenerator()
                    response_text = response_generator.generate_response(
                        request.user_input,
                        principle_compliance,  # Pass principle compliance, not score
                        active_systems,
                        system_analyses,
                        context
                    )
                except:
                    # Fallback
                    if technical_response and technical_response != request.user_input:
                        response_text = technical_response
                    else:
                        response_text = f"I've analyzed your request: \"{request.user_input}\"\n\n"
                        response_text += f"Processed through {len(active_systems)} ethical systems. "
                        if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
                            compliance_status = "Principle compliant" if principle_compliance.overall_compliant else f"Principle violation: {principle_compliance.violation_reason or 'See details'}"
                            response_text += f"Principle compliance: {compliance_status}."
                        if request.use_ai_service:
                            response_text += "\n\n⚠ AI Service was requested but encountered an issue."
                
                analysis = {
                    "processing_level": request.processing_level,
                    "ai_service_used": False,
                    "active_systems": active_systems,
                    "system_count": len(active_systems),
                    "system_analyses": system_analyses,
                    "principle_compliance": principle_compliance,
                    "ethical_score": ethical_score  # Binary: 1.0 = compliant, 0.0 = not compliant
                }
            else:
                response_text = f"Ethically processed: {request.user_input}"
                ethical_score = 1.0  # Default to compliant
                status = "safe"
                analysis = {
                    "processing_level": request.processing_level,
                    "ai_service_used": False,
                    "note": "Integrator not available"
                }
        
        # Final validation
        if not response_text or response_text.strip() == request.user_input.strip():
            response_text = f"I've received: \"{request.user_input}\"\n\n"
            response_text += f"Processed through Kyosan Ethics Engine. "
            if principle_compliance and hasattr(principle_compliance, 'overall_compliant'):
                compliance_status = "Compliant" if principle_compliance.overall_compliant else "Non-compliant"
                response_text += f"Principle compliance: {compliance_status}."
            if request.use_ai_service and not AI_CLIENT:
                response_text += "\n\n⚠ AI Service not available. Check API key."
        
        processing_time = time.time() - start_time
        
        compliance_status = "Compliant" if ethical_score == 1.0 else "Non-compliant"
        print(f"[Response] Status: {status}, Principle compliance: {compliance_status}, Time: {processing_time:.3f}s")
        print(f"{'='*60}\n")
        
        return ProcessResponse(
            response=response_text,
            ethical_score=ethical_score,
            status=status,
            analysis=analysis,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            processing_time=round(processing_time, 3)
        )
    
    except Exception as e:
        import traceback
        print(f"[Error] {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    print("\n" + "="*60)
    print("Kyosan Ethics Engine Server")
    print("="*60)
    print(f"Server: http://localhost:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"AI Service: {'Enabled' if AI_CLIENT else 'Disabled'}")
    try:
        active_count = len(INTEGRATOR.get_active_systems()) if INTEGRATOR and hasattr(INTEGRATOR, 'get_active_systems') else 0
        print(f"Active Systems: {active_count}")
    except:
        print(f"Active Systems: Unknown")
    print("="*60 + "\n")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
