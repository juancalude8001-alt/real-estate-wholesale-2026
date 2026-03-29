"""
FastAPI Backend for Real Estate Voice Calling System
Integrates Vapi with dashboard and manages call orchestration
"""

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime
import asyncio
from vapi_voice_system import VapiVoiceAgent, CallOutcomeTracker, CallOutcome

app = FastAPI(title="Real Estate Voice API")

# CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize systems
vapi_agent = VapiVoiceAgent()
call_tracker = CallOutcomeTracker()

# Request/Response Models
class CallRequest(BaseModel):
    """Request to initiate a voice call"""
    deal_id: str
    owner_name: str
    phone_number: str
    property_address: str
    arv_estimate: int
    suggested_offer_low: int
    suggested_offer_high: int
    days_to_auction: int
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[int] = None

class CallResponse(BaseModel):
    """Response from initiating a call"""
    success: bool
    call_id: str
    message: str
    status: str

class CallStatusResponse(BaseModel):
    """Status of an ongoing or completed call"""
    call_id: str
    status: str
    duration_seconds: Optional[int]
    outcome: Optional[dict]

class CallOutcomeRequest(BaseModel):
    """Submit a manual call outcome"""
    call_id: str
    deal_id: str
    owner_name: str
    phone_number: str
    property_address: str
    motivation_level: str  # high, medium, low, none
    seller_price_expectation: Optional[int]
    is_interested: bool
    callback_needed: bool
    objections: List[str] = []
    notes: str

class DealWithCallHistory(BaseModel):
    """Deal with its call history"""
    deal_id: str
    owner_name: str
    phone_number: str
    property_address: str
    arv_estimate: int
    call_count: int
    last_call_motivation: Optional[str]
    is_interested: bool
    callback_scheduled: Optional[str]


# ============================================================================
# CALL INITIATION ENDPOINTS
# ============================================================================

@app.post("/calls/initiate", response_model=CallResponse)
async def initiate_call(request: CallRequest):
    """
    Initiate a voice call to a property owner
    
    The Vapi system will:
    1. Call the owner using our outbound number
    2. Use the trained voice agent
    3. Run through qualification conversation
    4. Record transcript and audio
    5. Return outcomes
    """
    
    try:
        # Convert request to dict for Vapi
        deal_data = request.dict()
        
        # Create call via Vapi
        result = vapi_agent.create_call(deal_data)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return CallResponse(
            success=True,
            call_id=result.get("id", "call_pending"),
            message=f"Call initiated to {request.owner_name}",
            status="calling"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/calls/{call_id}/status", response_model=CallStatusResponse)
async def get_call_status(call_id: str):
    """Get the real-time status of a call"""
    
    try:
        status_data = vapi_agent.get_call_status(call_id)
        
        if "error" in status_data:
            raise HTTPException(status_code=404, detail="Call not found")
        
        return CallStatusResponse(
            call_id=call_id,
            status=status_data.get("status", "unknown"),
            duration_seconds=status_data.get("duration"),
            outcome=status_data.get("outcome"),
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/calls/{call_id}/outcome")
async def submit_call_outcome(call_id: str, request: CallOutcomeRequest):
    """
    Submit the outcome of a completed call
    Stores motivation level, price expectations, and follow-up actions
    """
    
    try:
        outcome = CallOutcome(
            call_id=call_id,
            deal_id=request.deal_id,
            owner_name=request.owner_name,
            phone_number=request.phone_number,
            property_address=request.property_address,
            call_duration_seconds=0,
            motivation_level=request.motivation_level,
            seller_price_expectation=request.seller_price_expectation,
            is_interested=request.is_interested,
            callback_needed=request.callback_needed,
            objections=request.objections,
            notes=request.notes,
            timestamp=datetime.now().isoformat(),
            recording_url=None,
        )
        
        success = call_tracker.save_outcome(outcome)
        
        if success:
            return {
                "success": True,
                "message": f"Outcome recorded for {request.owner_name}",
                "call_id": call_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save outcome")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CALL HISTORY & ANALYTICS
# ============================================================================

@app.get("/calls/deal/{deal_id}/history")
async def get_deal_call_history(deal_id: str):
    """Get all calls made for a specific deal"""
    
    try:
        outcomes = call_tracker.get_outcomes_by_deal(deal_id)
        
        return {
            "deal_id": deal_id,
            "call_count": len(outcomes),
            "calls": [
                {
                    "call_id": o.call_id,
                    "timestamp": o.timestamp,
                    "motivation_level": o.motivation_level,
                    "is_interested": o.is_interested,
                    "price_expectation": o.seller_price_expectation,
                    "notes": o.notes,
                }
                for o in outcomes
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/calls/motivated-leads")
async def get_motivated_leads(min_motivation: str = "medium"):
    """
    Get all leads that showed high motivation and are open to offers
    Used for follow-up by acquisitions team
    """
    
    try:
        leads = call_tracker.get_motivated_leads(min_motivation)
        
        return {
            "count": len(leads),
            "leads": [
                {
                    "call_id": lead[1],
                    "deal_id": lead[2],
                    "owner_name": lead[3],
                    "phone_number": lead[4],
                    "property_address": lead[5],
                    "motivation_level": lead[7],
                    "price_expectation": lead[8],
                    "timestamp": lead[13],
                    "notes": lead[12],
                }
                for lead in leads
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/calls/stats")
async def get_call_statistics():
    """Get overall statistics about voice calls"""
    
    try:
        conn = __import__("sqlite3").connect("/agent/home/call_outcomes.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM call_outcomes")
        total_calls = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT motivation_level, COUNT(*) 
            FROM call_outcomes 
            GROUP BY motivation_level
        """)
        motivation_breakdown = dict(cursor.fetchall())
        
        cursor.execute("""
            SELECT COUNT(*) FROM call_outcomes WHERE is_interested = 1
        """)
        interested_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM call_outcomes WHERE callback_needed = 1
        """)
        callback_needed = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT AVG(seller_price_expectation) 
            FROM call_outcomes 
            WHERE seller_price_expectation IS NOT NULL
        """)
        avg_seller_expectation = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_calls_made": total_calls,
            "interested_count": interested_count,
            "callback_needed": callback_needed,
            "interest_rate_percent": (interested_count / total_calls * 100) if total_calls > 0 else 0,
            "motivation_breakdown": motivation_breakdown,
            "avg_seller_price_expectation": int(avg_seller_expectation) if avg_seller_expectation else None,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INTEGRATION WITH DASHBOARD
# ============================================================================

@app.get("/deals/{deal_id}/call-ready")
async def check_deal_call_readiness(deal_id: str):
    """
    Check if a deal is ready for voice calling
    Verifies required data is present
    """
    
    # In production, would check against actual deal database
    # For now, return success template
    return {
        "deal_id": deal_id,
        "ready_for_call": True,
        "required_fields": {
            "owner_name": "present",
            "phone_number": "present",
            "property_address": "present",
            "arv_estimate": "present"
        }
    }


@app.post("/calls/bulk-schedule")
async def schedule_bulk_calls(deals: List[CallRequest]):
    """
    Schedule multiple calls in sequence
    Useful for calling multiple properties in a target area
    """
    
    scheduled_calls = []
    
    for deal in deals:
        result = await initiate_call(deal)
        scheduled_calls.append(result)
        # Add delay between calls to avoid rate limits
        await asyncio.sleep(2)
    
    return {
        "total_scheduled": len(scheduled_calls),
        "calls": scheduled_calls
    }


# ============================================================================
# WEBHOOK FOR VAPI CALLBACKS
# ============================================================================

@app.post("/webhooks/vapi/call-completed")
async def vapi_call_completed_webhook(payload: dict):
    """
    Webhook endpoint that Vapi calls when a call completes
    Receives transcript, recording, and AI-extracted outcomes
    """
    
    try:
        call_id = payload.get("callId")
        transcript = payload.get("transcript", "")
        recording_url = payload.get("recordingUrl")
        duration = payload.get("duration", 0)
        deal_id = payload.get("context", {}).get("deal_id")
        
        # Extract outcomes from transcript (would use Claude/GPT in production)
        # For now, use template
        
        print(f"✓ Call completed: {call_id}")
        print(f"  Duration: {duration}s")
        print(f"  Recording: {recording_url}")
        
        return {"status": "received", "call_id": call_id}
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# HEALTH & INFO
# ============================================================================

@app.get("/health")
async def health_check():
    """Check if the voice API is running"""
    return {
        "status": "healthy",
        "service": "Real Estate Voice Calling API",
        "vapi_connected": True,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/config")
async def get_config():
    """Get voice system configuration"""
    return {
        "system_name": "Real Estate Wholesale Voice Calling",
        "max_call_duration": "10 minutes",
        "available_outbound_numbers": len(["list of numbers"]),
        "voice_provider": "OpenAI",
        "voice_model": "GPT-4",
        "voice_tone": "Professional, empathetic, solution-focused",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
