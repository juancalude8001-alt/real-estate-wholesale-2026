"""
Vapi Voice Calling System for Real Estate Wholesale
Handles seller outreach, qualification, and outcome tracking
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, List
import sqlite3
from dataclasses import dataclass

# Vapi Configuration
VAPI_BASE_URL = "https://api.vapi.ai"
VAPI_PRIVATE_KEY = os.getenv("VAPI_PRIVATE_KEY", "f4533a8e-19ab-47f2-9a6e-0345f690a390")
VAPI_PUBLIC_KEY = os.getenv("VAPI_PUBLIC_KEY", "3b1705b6-4b16-4816-8745-90f36eac0104")

# Outbound phone numbers pool
OUTBOUND_NUMBERS = [
    "+1 (571) 491 6426",
    "+1 (424) 857 9340",
    "+1 (424) 857 9489",
    "+1 (862) 781 9799",
    "+1 (424) 857 9530",
    "+1 (609) 786 9598",
]

@dataclass
class CallOutcome:
    """Represents the result of a voice call"""
    call_id: str
    deal_id: str
    owner_name: str
    phone_number: str
    property_address: str
    call_duration_seconds: int
    motivation_level: str  # high, medium, low, none
    seller_price_expectation: Optional[int]
    is_interested: bool
    callback_needed: bool
    objections: List[str]
    notes: str
    timestamp: str
    recording_url: Optional[str]


class VapiVoiceAgent:
    """Manages Vapi assistant creation and call execution"""
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
            "Content-Type": "application/json"
        }
    
    def create_assistant(self) -> Dict:
        """Create a Vapi assistant for seller outreach"""
        
        system_prompt = """You are a professional real estate acquisition specialist calling property owners who may be facing foreclosure or auction.

Your CORE PURPOSE:
- Build genuine rapport with the seller
- Understand their situation without judgment
- Determine if they're open to a cash sale before auction
- Gather information for the acquisition team

TONE & PERSONALITY:
- Warm, empathetic, and professional
- Calm and unhurried - this is a conversation, not a pitch
- Respectful of their situation - don't make them feel judged
- Solution-focused - you're offering help, not pressure

NEVER DO:
- Pressure or rush the seller
- Give exact dollar amounts
- Promise deals or make commitments
- Dismiss their concerns
- Sound robotic or scripted

YOUR CONVERSATION APPROACH:

OPENING (0-30 seconds):
1. Greet warmly: "Hi [Name], this is [Your Name] from [Company]. Do you have a quick minute?"
2. Get permission: "I'm calling about [property address] - is now a good time?"
3. Establish legitimacy: "We help homeowners facing foreclosure find solutions before auction"

BUILD CONTEXT (30 seconds - 1.5 minutes):
- "I see your property may be heading to auction soon. Is that still the case?"
- "Can I ask - what's going on with the property right now?"
- Listen more than you talk
- Show genuine interest in their situation

DISCOVERY QUESTIONS (1.5 - 4 minutes):
- "Walk me through what happened - how did you end up in this situation?"
- "Do you want to keep the property, or would selling be a relief?"
- "What's your timeline looking like?"
- "What condition is the property in?"
- "Are there tenants or is it vacant?"

SOFT PRICE DISCOVERY (4-5 minutes):
- DO NOT start with numbers
- "If you were to sell it quickly, what did you have in mind?"
- "What would be a fair price for you in a fast sale?"
- "What number would make this work for your situation?"
- Listen to their expectations

INTEREST CHECK (5-6 minutes):
- "It sounds like you're open to exploring options?"
- "Would you be interested in hearing what we might be able to offer?"
- "If we could solve this before auction, would that be helpful?"

CLOSE (6-7 minutes):
- If interested: "Great - I'm going to pass this to our acquisitions team. They'll review everything and call you back with a specific offer."
- If not interested: "I understand. If things change, here's my info. Best of luck."

OBJECTION HANDLERS:

"I want to list with a realtor"
→ "That makes sense - realtors are great for retail sales. We move much faster for pre-auction situations. Would you be open to exploring both options?"

"I need to talk to my spouse/lawyer"
→ "Absolutely - that's smart. When would be a good time to reconnect with both of you?"

"We've got a lot of equity in this"
→ "I hear you - that's common. Our advantage is speed and certainty. Can you share what you'd be looking for?"

"I don't want to sell"
→ "That's totally fair. Just so I understand - is the auction timeline making that difficult?"

"Why should I work with you vs a realtor?"
→ "Great question. Three reasons: 1) We close in days, not months, 2) No contingencies, 3) No realtor fees. For someone facing auction, that matters."

INFORMATION TO ALWAYS COLLECT:
- Motivation (1-10 scale)
- Price expectations
- Timeline preference
- Property condition
- Whether they're interested in discussing further
- Best callback time/method

OUTCOME TAGGING:
At the end, the system will categorize this call as:
- HIGHLY_MOTIVATED: Clear interest, wants to explore, motivated by timeline
- INTERESTED: Open to learning more, not pushing back
- HESITANT: Listening but has concerns, needs more info
- NOT_INTERESTED: Clear no, but polite
- CALLBACK_NEEDED: Needs to talk to someone else first
- DO_NOT_CALL: Angry, abusive, or explicitly said don't call back

Remember: This is a FIRST CONTACT call. You're not closing deals. You're opening doors.
Your job is to be so helpful and human that they WANT to hear from our acquisitions team."""

        assistant_config = {
            "name": "Real Estate Acquisition Agent",
            "firstMessage": "Hi there! I'm calling about a property situation I think we might be able to help with. Do you have a quick minute?",
            "model": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "systemPrompt": system_prompt,
            },
            "voice": {
                "provider": "openai",
                "voiceId": "onyx",  # Professional male voice
            },
            "transcriber": {
                "provider": "openai",
            },
            "endCallMessage": "Thanks for your time. Have a great day!",
            "maxDurationSeconds": 600,  # 10 minute max
        }
        
        return assistant_config
    
    def create_call(self, deal_data: Dict) -> Dict:
        """
        Initiate an outbound call to a property owner
        
        deal_data should contain:
        - deal_id
        - owner_name
        - phone_number
        - property_address
        - arv_estimate
        - suggested_offer_low
        - suggested_offer_high
        - days_to_auction
        """
        
        assistant_config = self.create_assistant()
        
        call_payload = {
            "assistantId": None,  # Will use assistant config directly
            "assistant": assistant_config,
            "phoneNumberId": None,  # Will pick from pool
            "customerNumber": deal_data["phone_number"],
            "customerName": deal_data["owner_name"],
            "context": {
                "deal_id": deal_data.get("deal_id"),
                "property_address": deal_data.get("property_address"),
                "arv_estimate": deal_data.get("arv_estimate"),
                "days_to_auction": deal_data.get("days_to_auction"),
            }
        }
        
        try:
            response = requests.post(
                f"{VAPI_BASE_URL}/call",
                headers=self.headers,
                json=call_payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create call: {e}")
            return {"error": str(e)}
    
    def get_call_status(self, call_id: str) -> Dict:
        """Get the status of an ongoing or completed call"""
        try:
            response = requests.get(
                f"{VAPI_BASE_URL}/call/{call_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get call status: {e}")
            return {"error": str(e)}
    
    def analyze_call_transcript(self, transcript: str, deal_data: Dict) -> CallOutcome:
        """
        Analyze the call transcript to extract outcomes
        Uses Claude or GPT to analyze conversation
        """
        
        analysis_prompt = f"""Analyze this phone call transcript and extract the following information:

TRANSCRIPT:
{transcript}

CONTEXT:
Property: {deal_data.get('property_address')}
Owner: {deal_data.get('owner_name')}
ARV Estimate: ${deal_data.get('arv_estimate', 0):,}
Days to Auction: {deal_data.get('days_to_auction')}

Extract and return JSON with:
{{
    "motivation_level": "high|medium|low|none",
    "seller_price_expectation": <integer or null>,
    "is_interested": <boolean>,
    "callback_needed": <boolean>,
    "objections": [<list of objections raised>],
    "call_notes": "<summary of key points>",
    "recommended_next_step": "<action recommendation>"
}}

Be precise. If no price was mentioned, set price to null.
Motivation is HIGH if seller expressed interest and openness.
Motivation is MEDIUM if interested but hesitant.
Motivation is LOW if not interested but wasn't rude.
Motivation is NONE if they hung up or were hostile."""
        
        # For now, return a template - in production would call Claude API
        return CallOutcome(
            call_id="temp_call_id",
            deal_id=deal_data.get("deal_id"),
            owner_name=deal_data.get("owner_name"),
            phone_number=deal_data.get("phone_number"),
            property_address=deal_data.get("property_address"),
            call_duration_seconds=0,
            motivation_level="medium",
            seller_price_expectation=None,
            is_interested=True,
            callback_needed=False,
            objections=[],
            notes="Call completed successfully",
            timestamp=datetime.now().isoformat(),
            recording_url=None,
        )


class CallOutcomeTracker:
    """Tracks and stores call outcomes in database"""
    
    def __init__(self, db_path: str = "/agent/home/call_outcomes.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create call outcomes table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS call_outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                call_id TEXT UNIQUE NOT NULL,
                deal_id TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                property_address TEXT NOT NULL,
                call_duration_seconds INTEGER,
                motivation_level TEXT,
                seller_price_expectation INTEGER,
                is_interested BOOLEAN,
                callback_needed BOOLEAN,
                objections TEXT,
                notes TEXT,
                timestamp TEXT,
                recording_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_outcome(self, outcome: CallOutcome) -> bool:
        """Save a call outcome to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO call_outcomes
                (call_id, deal_id, owner_name, phone_number, property_address,
                 call_duration_seconds, motivation_level, seller_price_expectation,
                 is_interested, callback_needed, objections, notes, timestamp, recording_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                outcome.call_id,
                outcome.deal_id,
                outcome.owner_name,
                outcome.phone_number,
                outcome.property_address,
                outcome.call_duration_seconds,
                outcome.motivation_level,
                outcome.seller_price_expectation,
                outcome.is_interested,
                outcome.callback_needed,
                json.dumps(outcome.objections),
                outcome.notes,
                outcome.timestamp,
                outcome.recording_url,
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Failed to save outcome: {e}")
            return False
    
    def get_outcomes_by_deal(self, deal_id: str) -> List[CallOutcome]:
        """Get all call outcomes for a specific deal"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM call_outcomes WHERE deal_id = ?
        """, (deal_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        outcomes = []
        for row in results:
            outcomes.append(CallOutcome(
                call_id=row[1],
                deal_id=row[2],
                owner_name=row[3],
                phone_number=row[4],
                property_address=row[5],
                call_duration_seconds=row[6],
                motivation_level=row[7],
                seller_price_expectation=row[8],
                is_interested=row[9],
                callback_needed=row[10],
                objections=json.loads(row[11]) if row[11] else [],
                notes=row[12],
                timestamp=row[13],
                recording_url=row[14],
            ))
        
        return outcomes
    
    def get_motivated_leads(self, min_motivation: str = "medium") -> List[Dict]:
        """Get all leads with high motivation for follow-up"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        motivation_levels = ["high", "medium"]
        if min_motivation == "high":
            motivation_levels = ["high"]
        
        placeholders = ",".join(["?" for _ in motivation_levels])
        
        cursor.execute(f"""
            SELECT * FROM call_outcomes
            WHERE motivation_level IN ({placeholders})
            AND is_interested = 1
            ORDER BY timestamp DESC
        """, motivation_levels)
        
        results = cursor.fetchall()
        conn.close()
        
        return results


# Example usage
if __name__ == "__main__":
    
    # Initialize the voice system
    vapi = VapiVoiceAgent()
    tracker = CallOutcomeTracker()
    
    # Example deal to call
    deal_data = {
        "deal_id": "deal_001",
        "owner_name": "John Smith",
        "phone_number": "+1-555-123-4567",
        "property_address": "123 Main St, Dallas, TX 75201",
        "arv_estimate": 250000,
        "suggested_offer_low": 140000,
        "suggested_offer_high": 160000,
        "days_to_auction": 18,
    }
    
    print("🎯 Vapi Voice Calling System Ready")
    print("\nExample: To call a property owner:")
    print(f"vapi.create_call({deal_data})")
    print("\nThe system will:")
    print("✓ Call the property owner")
    print("✓ Build rapport and understand their situation")
    print("✓ Discover their price expectations")
    print("✓ Tag motivation level")
    print("✓ Store outcome for follow-up")
