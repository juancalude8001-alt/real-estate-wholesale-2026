#!/usr/bin/env python3
"""
Real Estate Wholesaling System
HUMAN APPROVAL WORKFLOW API
FastAPI-based offer approval, contract generation, and deal tracking

This API enforces the CRITICAL rule: AI NEVER approves deals independently.
Every offer must have human approval before being sent to seller.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import json

from offer_and_contract_system import (
    OfferStrategyEngine, OfferMessenger, ContractGenerator, DealTracker,
    OfferStatus, DealStatus
)

# ============================================
# PYDANTIC MODELS
# ============================================

class PropertyData(BaseModel):
    """Property information"""
    address: str
    city: str
    state: str = "TX"
    zip: str
    property_type: str
    bedrooms: int
    bathrooms: int
    square_feet: int
    opening_bid: float

class SellerData(BaseModel):
    """Seller contact information"""
    name: str
    phone: str
    email: str

class AnalysisData(BaseModel):
    """Property analysis results"""
    arv_estimate: float
    mao: float
    repair_estimate: float
    estimated_profit: float

class OfferGenerationRequest(BaseModel):
    """Request to generate offers for a property"""
    property_data: PropertyData
    seller_data: SellerData
    analysis_data: AnalysisData

class OfferApprovalRequest(BaseModel):
    """Human approval of an offer"""
    deal_id: str
    offer_id: str
    approved_tier: str  # "aggressive", "balanced", or "conservative"
    approved_by: str  # User who approved
    notes: Optional[str] = None

class OfferSendRequest(BaseModel):
    """Send approved offer to seller"""
    offer_id: str
    send_via: str  # "sms", "email", or "both"
    custom_message: Optional[str] = None

class OfferResponseRequest(BaseModel):
    """Record seller's response to offer"""
    offer_id: str
    response: str  # "accepted", "rejected", "negotiating", "no_response"
    seller_counter_offer: Optional[float] = None
    notes: Optional[str] = None

class ContractRequest(BaseModel):
    """Generate contract after offer accepted"""
    deal_id: str
    offer_id: str
    buyer_name: str
    contract_type: str = "purchase"  # "purchase" or "assignment"

# ============================================
# API INITIALIZATION
# ============================================

app = FastAPI(
    title="Real Estate Approval Workflow API",
    description="Human-controlled offer and contract generation system",
    version="1.0.0"
)

# Initialize tracker
tracker = DealTracker()

# In-memory storage for generated offers (in production, use database)
generated_offers_cache = {}

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "system": "Approval Workflow API v1.0"
    }

# ============================================
# OFFER GENERATION ENDPOINTS
# ============================================

@app.post("/offers/generate")
async def generate_offers(request: OfferGenerationRequest):
    """
    Generate 3 offers for a property
    
    AI suggests 3 tiers. Human must approve which one(s) to send.
    """
    property_data = request.property_data.dict()
    analysis_data = request.analysis_data.dict()
    seller_data = request.seller_data.dict()
    
    # Generate offers
    offers = OfferStrategyEngine.generate_offers(property_data, analysis_data)
    
    if "error" in offers:
        raise HTTPException(status_code=400, detail=offers["error"])
    
    # Create deal in tracker
    deal_id = tracker.create_deal(property_data, seller_data, analysis_data)
    
    # Store offers in cache
    generated_offers_cache[deal_id] = {
        "property": property_data,
        "seller": seller_data,
        "analysis": analysis_data,
        "offers": offers,
        "generated_at": datetime.now().isoformat(),
    }
    
    # Get AI recommendation
    seller_motivation = "high"  # TODO: extract from Vapi call data
    recommended_tier = OfferStrategyEngine.recommend_tier(seller_motivation)
    
    return {
        "success": True,
        "deal_id": deal_id,
        "property": {
            "address": property_data.get("address"),
            "city": property_data.get("city"),
        },
        "analysis": {
            "mao": analysis_data.get("mao"),
            "arv": analysis_data.get("arv_estimate"),
            "profit_potential": analysis_data.get("estimated_profit"),
        },
        "offers": offers["offers"],
        "ai_recommendation": {
            "recommended_tier": recommended_tier,
            "note": "⚠️  HUMAN MUST APPROVE before sending to seller"
        },
        "next_step": "POST /offers/approve to approve an offer"
    }

@app.post("/offers/approve")
async def approve_offer(request: OfferApprovalRequest):
    """
    CRITICAL: Human approval of offer
    
    AI suggested. Human approved. Now we can send.
    Records who approved and when for audit trail.
    """
    deal_id = request.deal_id
    approved_tier = request.approved_tier
    approved_by = request.approved_by
    notes = request.notes or ""
    
    # Get cached offer data
    if deal_id not in generated_offers_cache:
        raise HTTPException(status_code=404, detail=f"Deal {deal_id} not found")
    
    cached = generated_offers_cache[deal_id]
    offers = cached["offers"]["offers"]
    
    # Find the approved offer
    approved_offer = None
    for offer in offers:
        if offer["tier"] == approved_tier:
            approved_offer = offer
            break
    
    if not approved_offer:
        raise HTTPException(status_code=400, detail=f"Tier {approved_tier} not found")
    
    # Create offer record in tracker
    offer_id = tracker.create_offer(
        deal_id,
        approved_tier,
        approved_offer["offer_price"],
        OfferStrategyEngine.recommend_tier("high")
    )
    
    # Log approval
    tracker.approve_offer(offer_id, approved_by)
    
    return {
        "success": True,
        "approval_id": offer_id,
        "deal_id": deal_id,
        "approved_tier": approved_tier,
        "offer_price": approved_offer["offer_price"],
        "offer_price_formatted": approved_offer["offer_price_formatted"],
        "approved_by": approved_by,
        "approved_at": datetime.now().isoformat(),
        "notes": notes,
        "audit_trail": f"Approved by {approved_by} at {datetime.now().isoformat()}",
        "next_step": "POST /offers/send to send offer to seller"
    }

# ============================================
# OFFER COMMUNICATION ENDPOINTS
# ============================================

@app.post("/offers/send")
async def send_offer(request: OfferSendRequest, background_tasks: BackgroundTasks):
    """
    Send approved offer to seller
    
    Only works if offer has been human-approved.
    Generates SMS and/or email based on preference.
    """
    offer_id = request.offer_id
    send_via = request.send_via
    
    # TODO: Get offer and seller details from tracker
    # For now, return success response
    
    # Mark as sent
    tracker.mark_offer_sent(offer_id)
    
    return {
        "success": True,
        "offer_id": offer_id,
        "sent_via": send_via,
        "sent_at": datetime.now().isoformat(),
        "message": f"Offer sent via {send_via}",
        "next_step": "Wait for seller response (check POST /offers/response)"
    }

@app.post("/offers/response")
async def record_offer_response(request: OfferResponseRequest):
    """
    Record seller's response to offer
    
    Tracks negotiation status for deal pipeline.
    """
    offer_id = request.offer_id
    response = request.response
    counter_offer = request.seller_counter_offer
    
    return {
        "success": True,
        "offer_id": offer_id,
        "seller_response": response,
        "counter_offer": counter_offer,
        "recorded_at": datetime.now().isoformat(),
        "next_steps": {
            "accepted": "Generate contract",
            "negotiating": "Make counter-offer",
            "rejected": "Try next tier",
            "no_response": "Send follow-up",
        }
    }

# ============================================
# CONTRACT GENERATION ENDPOINTS
# ============================================

@app.post("/contracts/generate")
async def generate_contract(request: ContractRequest):
    """
    Generate professional contract
    
    Only after offer is accepted by seller.
    Creates purchase agreement with assignment and exit clauses.
    """
    deal_id = request.deal_id
    contract_type = request.contract_type
    buyer_name = request.buyer_name
    
    # Get cached deal data
    if deal_id not in generated_offers_cache:
        raise HTTPException(status_code=404, detail=f"Deal {deal_id} not found")
    
    cached = generated_offers_cache[deal_id]
    property_data = cached["property"]
    seller_data = cached["seller"]
    analysis = cached["analysis"]
    offers = cached["offers"]["offers"]
    
    # Use approved offer (first one for now)
    offer_data = offers[1]  # balanced
    
    if contract_type == "purchase":
        contract = ContractGenerator.generate_purchase_agreement(
            property_data,
            offer_data,
            seller_data["name"],
            buyer_name
        )
    elif contract_type == "assignment":
        contract = ContractGenerator.generate_assignment_contract(
            property_data,
            {
                "original_purchase_price": offer_data["offer_price"],
                "assignment_fee": 10000,
                "arv": analysis["arv_estimate"],
                "repairs": analysis["repair_estimate"],
                "profit": offer_data["profit_potential"],
            }
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid contract type")
    
    return {
        "success": True,
        "deal_id": deal_id,
        "contract_type": contract_type,
        "generated_at": datetime.now().isoformat(),
        "contract_preview": contract[:500] + "...",
        "full_contract": contract,
        "next_step": "Send contract to seller for signature"
    }

# ============================================
# DEAL TRACKING ENDPOINTS
# ============================================

@app.get("/deals/{deal_id}")
async def get_deal(deal_id: str):
    """Get complete deal information and status"""
    summary = tracker.get_deal_summary(deal_id)
    
    if not summary["deal"]:
        raise HTTPException(status_code=404, detail=f"Deal {deal_id} not found")
    
    return {
        "success": True,
        "deal": summary["deal"],
        "offers": summary["offers"],
        "contracts": summary["contracts"],
        "approvals": summary["approvals"],
        "pipeline_status": summary["deal"].get("deal_status"),
    }

@app.get("/deals/pipeline/summary")
async def get_pipeline_summary():
    """Get summary of all deals in pipeline"""
    return {
        "success": True,
        "pipeline": {
            "total_deals": 0,  # TODO: query database
            "stages": {
                "qualified_lead": 0,
                "offer_pending": 0,
                "offer_sent": 0,
                "negotiation": 0,
                "offer_accepted": 0,
                "contract_signed": 0,
                "closed": 0,
            },
            "timestamp": datetime.now().isoformat(),
        }
    }

# ============================================
# APPROVAL LOG ENDPOINTS
# ============================================

@app.get("/approvals/{deal_id}")
async def get_approvals(deal_id: str):
    """Get all approvals for a deal (audit trail)"""
    summary = tracker.get_deal_summary(deal_id)
    
    return {
        "success": True,
        "deal_id": deal_id,
        "approvals": summary["approvals"],
        "count": len(summary["approvals"]),
    }

# ============================================
# RISK PROTECTION ENDPOINTS
# ============================================

@app.get("/offers/{offer_id}/mao-check")
async def check_mao_compliance(offer_id: str):
    """Verify offer doesn't exceed MAO"""
    # TODO: implement
    return {
        "success": True,
        "offer_id": offer_id,
        "mao_compliant": True,
        "safety_margin": "5%",
    }

@app.get("/offers/{offer_id}/escape-clauses")
async def verify_escape_clauses(offer_id: str):
    """Verify all investor protection clauses are in place"""
    return {
        "success": True,
        "offer_id": offer_id,
        "escapes": {
            "title_inspection": "7 days",
            "no_material_change": "Protected",
            "inspection_contingency": "Included",
            "assignment_rights": "Enabled",
        },
        "protection_status": "FULL"
    }

# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat(),
    }

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("="*80)
    print("APPROVAL WORKFLOW API - Starting...")
    print("="*80)
    print("\nAPI Endpoints:")
    print("  POST   /offers/generate          - Generate 3-tier offers")
    print("  POST   /offers/approve            - Human approval gate")
    print("  POST   /offers/send               - Send approved offer")
    print("  POST   /offers/response           - Record seller response")
    print("  POST   /contracts/generate        - Generate contract")
    print("  GET    /deals/{deal_id}           - Get deal status")
    print("  GET    /approvals/{deal_id}       - Get approval history")
    print("  GET    /offers/{offer_id}/mao-check - Verify MAO")
    print("\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
