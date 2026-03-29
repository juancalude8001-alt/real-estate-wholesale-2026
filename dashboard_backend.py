447
#!/usr/bin/env python3
"""
LOCAL DASHBOARD BACKEND API
Runs in Tasklet sandbox for testing/demo
Serves all endpoints needed by the real estate dashboard
Updated: 2026-03-29 - Fix Railway deployment configuration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import sqlite3

app = FastAPI(title="Real Estate Dashboard API")

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# DATA MODELS
# ============================================================

class Offer(BaseModel):
    id: str
    deal_id: str
    tier: str  # aggressive, balanced, conservative
    price: float
    acceptance_probability: int
    estimated_profit: float
    closing_days: int
    terms: List[str]
    created_at: str
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    sent_at: Optional[str] = None
    status: str  # draft, approved, sent, accepted, rejected

class Contract(BaseModel):
    id: str
    deal_id: str
    offer_id: str
    type: str  # purchase, assignment
    generated_at: str
    document_url: str
    status: str  # draft, sent, signed, executed
    seller_signed_at: Optional[str] = None

class DealStatus(BaseModel):
    deal_id: str
    stage: str
    substatus: str
    last_update: str
    notes: str

# ============================================================
# SAMPLE DATA
# ============================================================

SAMPLE_OFFERS = {
    "1": [  # Deal 4205 Lakewood Drive
        {
            "id": "off_001_agg",
            "deal_id": "1",
            "tier": "aggressive",
            "price": 150000,
            "acceptance_probability": 30,
            "estimated_profit": 52500,
            "closing_days": 14,
            "terms": ["Cash offer", "No inspections", "As-is purchase", "Fast closing"],
            "created_at": "2026-03-29T15:30:00Z",
            "status": "draft"
        },
        {
            "id": "off_001_bal",
            "deal_id": "1",
            "tier": "balanced",
            "price": 158500,
            "acceptance_probability": 60,
            "estimated_profit": 48000,
            "closing_days": 14,
            "terms": ["Cash offer", "No inspections", "As-is purchase", "Fast closing"],
            "created_at": "2026-03-29T15:30:00Z",
            "status": "approved",
            "approved_by": "user",
            "approved_at": "2026-03-29T16:00:00Z"
        },
        {
            "id": "off_001_con",
            "deal_id": "1",
            "tier": "conservative",
            "price": 166500,
            "acceptance_probability": 85,
            "estimated_profit": 45000,
            "closing_days": 14,
            "terms": ["Cash offer", "No inspections", "As-is purchase", "Fast closing"],
            "created_at": "2026-03-29T15:30:00Z",
            "status": "draft"
        }
    ],
    "2": [  # Deal 8721 Maple Avenue
        {
            "id": "off_002_agg",
            "deal_id": "2",
            "tier": "aggressive",
            "price": 325000,
            "acceptance_probability": 25,
            "estimated_profit": 79000,
            "closing_days": 21,
            "terms": ["Cash offer", "No inspections", "As-is", "Multi-unit", "Assignment allowed"],
            "created_at": "2026-03-28T10:00:00Z",
            "status": "draft"
        },
        {
            "id": "off_002_bal",
            "deal_id": "2",
            "tier": "balanced",
            "price": 349000,
            "acceptance_probability": 55,
            "estimated_profit": 71500,
            "closing_days": 21,
            "terms": ["Cash offer", "No inspections", "As-is", "Multi-unit", "Assignment allowed"],
            "created_at": "2026-03-28T10:00:00Z",
            "status": "draft"
        },
        {
            "id": "off_002_con",
            "deal_id": "2",
            "tier": "conservative",
            "price": 370000,
            "acceptance_probability": 75,
            "estimated_profit": 67000,
            "closing_days": 21,
            "terms": ["Cash offer", "No inspections", "As-is", "Multi-unit", "Assignment allowed"],
            "created_at": "2026-03-28T10:00:00Z",
            "status": "draft"
        }
    ]
}

SAMPLE_CONTRACTS = {
    "1": [
        {
            "id": "con_001_pur",
            "deal_id": "1",
            "offer_id": "off_001_bal",
            "type": "purchase",
            "generated_at": "2026-03-29T16:15:00Z",
            "document_url": "/documents/purchase_agreement_1.pdf",
            "status": "sent"
        }
    ]
}

SAMPLE_DEAL_STATUS = {
    "1": {
        "deal_id": "1",
        "stage": "offer_sent",
        "substatus": "Balanced offer sent via SMS + email on Mar 29",
        "last_update": "2026-03-29T16:30:00Z",
        "notes": "Seller responded with interest. Price expectation: $165K. Phone call scheduled for tomorrow."
    },
    "2": {
        "deal_id": "2",
        "stage": "voice_call",
        "substatus": "Vapi AI call completed. Seller interested in offer.",
        "last_update": "2026-03-28T14:00:00Z",
        "notes": "High motivation confirmed. Needs to discuss with spouse. Callback scheduled Wed 3pm."
    },
    "3": {
        "deal_id": "3",
        "stage": "qualified",
        "substatus": "Ready for voice outreach",
        "last_update": "2026-03-29T07:00:00Z",
        "notes": "Strong deal (8-day auction). Recommend aggressive offer."
    }
}

# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/api/deals")
async def get_deals():
    """Get all deals (from sample data)"""
    return {
        "1": {
            "id": "1",
            "address": "4205 Lakewood Drive",
            "city": "Dallas",
            "property_type": "Single Family",
            "opening_bid": 195000,
            "arv_estimate": 275000,
            "repair_estimate": 35000,
            "mao": 158500,
            "estimated_profit": 48000,
            "deal_score": 92,
            "deal_tier": "gold",
            "discount_from_arv_percent": 29,
            "time_remaining_days": 8,
            "auction_date": "2026-04-06",
            "bedrooms": 4,
            "bathrooms": 2,
            "square_feet": 2400,
            "year_built": 1998,
            "photo_count": 24,
            "owner_name": "John Martinez",
            "phone_number": "214-555-0102",
            "seller_email": "john.martinez@email.com",
            "seller_motivation": "high",
            "voice_status": "interested"
        },
        "2": {
            "id": "2",
            "address": "8721 Maple Avenue",
            "city": "Fort Worth",
            "property_type": "Multi Family (4-Plex)",
            "opening_bid": 420000,
            "arv_estimate": 620000,
            "repair_estimate": 85000,
            "mao": 349000,
            "estimated_profit": 71500,
            "deal_score": 88,
            "deal_tier": "gold",
            "discount_from_arv_percent": 32,
            "time_remaining_days": 12,
            "auction_date": "2026-04-10",
            "bedrooms": 8,
            "bathrooms": 4,
            "square_feet": 4800,
            "year_built": 2005,
            "photo_count": 31,
            "owner_name": "Sarah Anderson",
            "phone_number": "817-555-0203",
            "seller_email": "sarah.a@email.com",
            "seller_motivation": "medium",
            "voice_status": "called"
        },
        "3": {
            "id": "3",
            "address": "3344 Oak Ridge Road",
            "city": "Houston",
            "property_type": "Single Family",
            "opening_bid": 165000,
            "arv_estimate": 240000,
            "repair_estimate": 28000,
            "mao": 140000,
            "estimated_profit": 35000,
            "deal_score": 75,
            "deal_tier": "silver",
            "discount_from_arv_percent": 31,
            "time_remaining_days": 5,
            "auction_date": "2026-04-03",
            "bedrooms": 3,
            "bathrooms": 1.5,
            "square_feet": 1850,
            "year_built": 1995,
            "photo_count": 18,
            "owner_name": "Michael Chen",
            "phone_number": "713-555-0304",
            "seller_email": "mchen@email.com",
            "seller_motivation": "high"
        }
    }

@app.get("/api/offers/all")
async def get_all_offers():
    """Get all offers"""
    all_offers = []
    for deal_id, offers in SAMPLE_OFFERS.items():
        all_offers.extend(offers)
    return all_offers

@app.post("/offers/generate")
async def generate_offers(request: dict):
    """Generate 3-tier offers for a deal"""
    deal_id = request.get("deal_id")
    mao = request.get("mao")
    arv = request.get("arv")
    seller_motivation = request.get("seller_motivation", "medium")
    
    # Calculate three offer tiers
    aggressive_price = int(mao * 0.95)  # 5% below MAO
    balanced_price = int(mao)
    conservative_price = int(mao * 1.05)  # 5% above MAO
    
    offers = [
        {
            "id": f"off_{deal_id}_agg_{datetime.now().timestamp()}",
            "deal_id": deal_id,
            "tier": "aggressive",
            "price": aggressive_price,
            "acceptance_probability": 30,
            "estimated_profit": int((arv * 0.7) - request.get("repairs", 0) - aggressive_price - 10000),
            "closing_days": 14,
            "terms": ["Cash offer", "No inspections", "As-is purchase", "Fast closing"],
            "created_at": datetime.now().isoformat() + "Z",
            "status": "draft"
        },
        {
            "id": f"off_{deal_id}_bal_{datetime.now().timestamp()}",
            "deal_id": deal_id,
            "tier": "balanced",
            "price": balanced_price,
            "acceptance_probability": 60,
            "estimated_profit": int((arv * 0.7) - request.get("repairs", 0) - balanced_price - 10000),
            "closing_days": 14,
            "terms": ["Cash offer", "No inspections", "As-is purchase", "Fast closing"],
            "created_at": datetime.now().isoformat() + "Z",
            "status": "draft"
        },
        {
            "id": f"off_{deal_id}_con_{datetime.now().timestamp()}",
            "deal_id": deal_id,
            "tier": "conservative",
            "price": conservative_price,
            "acceptance_probability": 80,
            "estimated_profit": int((arv * 0.7) - request.get("repairs", 0) - conservative_price - 10000),
            "closing_days": 14,
            "terms": ["Cash offer", "No inspections", "As-is purchase", "Fast closing"],
            "created_at": datetime.now().isoformat() + "Z",
            "status": "draft"
        }
    ]
    
    # Store offers
    if deal_id not in SAMPLE_OFFERS:
        SAMPLE_OFFERS[deal_id] = []
    SAMPLE_OFFERS[deal_id] = offers
    
    return {"offers": offers}

@app.post("/offers/approve")
async def approve_offer(request: dict):
    """Approve an offer"""
    offer_id = request.get("offer_id")
    deal_id = request.get("deal_id")
    approved_by = request.get("approved_by")
    
    if deal_id in SAMPLE_OFFERS:
        for offer in SAMPLE_OFFERS[deal_id]:
            if offer["id"] == offer_id:
                offer["status"] = "approved"
                offer["approved_by"] = approved_by
                offer["approved_at"] = datetime.now().isoformat() + "Z"
                return {"status": "approved", "offer": offer}
    
    raise HTTPException(status_code=404, detail="Offer not found")

@app.post("/offers/send")
async def send_offer(request: dict):
    """Send offer to seller (SMS + Email)"""
    offer_id = request.get("offer_id")
    deal_id = request.get("deal_id")
    
    if deal_id in SAMPLE_OFFERS:
        for offer in SAMPLE_OFFERS[deal_id]:
            if offer["id"] == offer_id:
                offer["status"] = "sent"
                offer["sent_at"] = datetime.now().isoformat() + "Z"
                
                # Update deal status
                if deal_id not in SAMPLE_DEAL_STATUS:
                    SAMPLE_DEAL_STATUS[deal_id] = {
                        "deal_id": deal_id,
                        "stage": "offer_sent",
                        "substatus": f"{offer['tier']} offer sent via SMS + email",
                        "last_update": datetime.now().isoformat() + "Z",
                        "notes": f"Offer price: ${offer['price']:,}"
                    }
                else:
                    SAMPLE_DEAL_STATUS[deal_id]["stage"] = "offer_sent"
                    SAMPLE_DEAL_STATUS[deal_id]["substatus"] = f"{offer['tier']} offer sent via SMS + email"
                    SAMPLE_DEAL_STATUS[deal_id]["last_update"] = datetime.now().isoformat() + "Z"
                
                return {
                    "status": "sent",
                    "message": f"Offer of ${offer['price']:,} sent to seller via SMS and email",
                    "offer": offer
                }
    
    raise HTTPException(status_code=404, detail="Offer not found")

@app.post("/contracts/generate")
async def generate_contract(request: dict):
    """Generate purchase contract"""
    deal_id = request.get("deal_id")
    offer_id = request.get("offer_id")
    seller_name = request.get("seller_name")
    purchase_price = request.get("purchase_price")
    
    contract = {
        "id": f"con_{deal_id}_{datetime.now().timestamp()}",
        "deal_id": deal_id,
        "offer_id": offer_id,
        "type": "purchase",
        "generated_at": datetime.now().isoformat() + "Z",
        "document_url": f"/documents/purchase_agreement_{deal_id}.pdf",
        "status": "draft"
    }
    
    if deal_id not in SAMPLE_CONTRACTS:
        SAMPLE_CONTRACTS[deal_id] = []
    SAMPLE_CONTRACTS[deal_id].append(contract)
    
    return {
        "contract": contract,
        "message": f"Purchase agreement generated for ${purchase_price:,}. Ready to send to seller."
    }

@app.get("/api/contracts/all")
async def get_all_contracts():
    """Get all contracts"""
    all_contracts = []
    for deal_id, contracts in SAMPLE_CONTRACTS.items():
        all_contracts.extend(contracts)
    return all_contracts

@app.get("/api/deals/status/all")
async def get_all_deal_status():
    """Get status for all deals"""
    return list(SAMPLE_DEAL_STATUS.values())

@app.get("/api/calls/stats")
async def get_call_stats():
    """Get voice calling statistics"""
    return {
        "total_calls": 12,
        "connected": 8,
        "interested": 5,
        "callbacks_needed": 2,
        "not_interested": 1,
        "connect_rate": 67,
        "interest_rate": 42,
        "average_duration_minutes": 7,
        "average_seller_expectation": 165000
    }

@app.get("/")
async def root():
        return {"status": "ok", "message": "Real Estate Dashboard API is running"}
@app.get("/health")
async def health():
        """Health check"""
        return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Dashboard Backend API Starting...")
    print("📍 http://localhost:8000")
    print("📊 Health check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)
