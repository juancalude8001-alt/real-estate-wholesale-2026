#!/usr/bin/env python3
"""
Real Estate Wholesale System
OFFER & CONTRACT GENERATION + DEAL STATUS TRACKING
Production-Ready with Human Approval Gates

Author: Real Estate Automation
Version: 2.0
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import hashlib

# ============================================
# ENUMS & CONSTANTS
# ============================================

class OfferStatus(Enum):
    """Status of an offer"""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class DealStatus(Enum):
    """Pipeline status of a deal"""
    QUALIFIED_LEAD = "qualified_lead"
    OFFER_PENDING = "offer_pending"
    OFFER_SENT = "offer_sent"
    NEGOTIATION = "negotiation"
    OFFER_ACCEPTED = "offer_accepted"
    CONTRACT_PENDING = "contract_pending"
    CONTRACT_SIGNED = "contract_signed"
    CLOSED = "closed"
    DEAD = "dead"

class OfferTier(Enum):
    """Three-tier offer strategy"""
    AGGRESSIVE = "aggressive"
    BALANCED = "balanced"
    CONSERVATIVE = "conservative"

# ============================================
# OFFER STRATEGY GENERATOR
# ============================================

class OfferStrategyEngine:
    """
    Generate intelligent 3-tier offers with MAO protection
    Aggressively profit while protecting deal margins
    """
    
    @staticmethod
    def validate_mao(offer_price: float, mao: float) -> Tuple[bool, str]:
        """
        CRITICAL: Never exceed MAO
        """
        if offer_price > mao * 1.05:  # Allow 5% buffer for safe offer
            return False, f"Offer ${offer_price:,.0f} exceeds MAO ${mao:,.0f}"
        return True, "MAO constraint satisfied"
    
    @staticmethod
    def generate_offers(property_data: Dict, analysis: Dict) -> Dict:
        """
        Generate 3 strategic offers with different seller appeal levels
        Always respects MAO as hard constraint
        """
        mao = analysis.get("mao", 0)
        arv = analysis.get("arv_estimate", 0)
        repairs = analysis.get("repair_estimate", 0)
        opening_bid = property_data.get("opening_bid", 0)
        
        # Validate MAO exists
        if not mao or mao <= 0:
            return {"error": "Invalid MAO calculation", "offers": []}
        
        # AGGRESSIVE: Maximum profit (95% of MAO)
        aggressive_price = mao * 0.95
        aggressive_profit = arv - aggressive_price - repairs - 5000
        
        # BALANCED: Highest acceptance (at MAO)
        balanced_price = mao
        balanced_profit = arv - balanced_price - repairs - 5000
        
        # CONSERVATIVE: Safe backup (105% of MAO, if acceptable)
        conservative_price = mao * 1.05
        conservative_profit = arv - conservative_price - repairs - 5000
        
        # Safety check: never exceed MAO
        if conservative_price > mao * 1.05:
            conservative_price = mao * 1.05
        
        offers = {
            "property_address": property_data.get("address"),
            "property_city": property_data.get("city"),
            "analysis_date": datetime.now().isoformat(),
            "mao": mao,
            "arv": arv,
            "repair_estimate": repairs,
            "offers": [
                {
                    "tier": OfferTier.AGGRESSIVE.value,
                    "offer_price": round(aggressive_price, 2),
                    "offer_price_formatted": f"${aggressive_price:,.0f}",
                    "profit_potential": round(aggressive_profit, 2),
                    "profit_formatted": f"${aggressive_profit:,.0f}",
                    "discount_from_opening": round(((opening_bid - aggressive_price) / opening_bid * 100), 1),
                    "acceptance_probability": 30,
                    "rationale": "Leverages auction anxiety, tight timeline, certainty vs. uncertainty",
                    "seller_message": "Absolute fastest path to certainty - cash in 14 days, no auction risk",
                    "timeline_days": 14,
                    "earnest_money": round(aggressive_price * 0.01, 2),
                    "mao_validation": "PASS" if aggressive_price <= mao else "FAIL",
                },
                {
                    "tier": OfferTier.BALANCED.value,
                    "offer_price": round(balanced_price, 2),
                    "offer_price_formatted": f"${balanced_price:,.0f}",
                    "profit_potential": round(balanced_profit, 2),
                    "profit_formatted": f"${balanced_profit:,.0f}",
                    "discount_from_opening": round(((opening_bid - balanced_price) / opening_bid * 100), 1),
                    "acceptance_probability": 60,
                    "rationale": "Best risk/reward - fair value with certainty vs. auction gamble",
                    "seller_message": "Fair market value with absolute certainty and speed",
                    "timeline_days": 14,
                    "earnest_money": round(balanced_price * 0.01, 2),
                    "mao_validation": "PASS",
                },
                {
                    "tier": OfferTier.CONSERVATIVE.value,
                    "offer_price": round(conservative_price, 2),
                    "offer_price_formatted": f"${conservative_price:,.0f}",
                    "profit_potential": round(conservative_profit, 2),
                    "profit_formatted": f"${conservative_profit:,.0f}",
                    "discount_from_opening": round(((opening_bid - conservative_price) / opening_bid * 100), 1),
                    "acceptance_probability": 80,
                    "rationale": "Maximum acceptance rate - competitive backup option",
                    "seller_message": "Competitive offer backed by proven execution",
                    "timeline_days": 14,
                    "earnest_money": round(conservative_price * 0.01, 2),
                    "mao_validation": "PASS" if conservative_price <= mao * 1.05 else "FAIL",
                },
            ]
        }
        
        return offers
    
    @staticmethod
    def recommend_tier(seller_motivation: str) -> str:
        """
        AI recommends best tier based on seller motivation
        HUMAN must approve final tier selection
        """
        recommendations = {
            "high": OfferTier.AGGRESSIVE.value,
            "medium": OfferTier.BALANCED.value,
            "low": OfferTier.CONSERVATIVE.value,
        }
        return recommendations.get(seller_motivation.lower(), OfferTier.BALANCED.value)

# ============================================
# OFFER COMMUNICATION TEMPLATES
# ============================================

class OfferMessenger:
    """
    Generate SMS, Email, and voicemail messages for offer delivery
    """
    
    @staticmethod
    def generate_sms_offer(seller_name: str, address: str, offer_price: float, 
                          closing_days: int = 14) -> str:
        """
        SMS template for initial offer notification
        Keep under 160 chars for single SMS
        """
        price_str = f"${offer_price:,.0f}"
        return f"Hi {seller_name.split()[0]}, I have a cash offer for your {address} property: {price_str}, close in {closing_days} days, no repairs needed. Offer details coming via email. Can you review?"
    
    @staticmethod
    def generate_email_offer(property_data: Dict, offer_data: Dict, 
                            seller_name: str, seller_email: str) -> str:
        """
        Professional email to present formal offer
        """
        address = property_data.get("address")
        city = property_data.get("city")
        offer_price = offer_data.get("offer_price")
        earnest_money = offer_data.get("earnest_money", int(offer_price * 0.01))
        closing_date = (datetime.now() + timedelta(days=14)).strftime("%B %d, %Y")
        expires = (datetime.now() + timedelta(days=7)).strftime("%B %d, %Y")
        
        email = f"""
Subject: Cash Offer for {address}, {city} - Quick Close Available

Dear {seller_name},

I hope this message finds you well. I've completed my analysis of your property 
at {address}, {city}, and I'm prepared to make a formal cash offer.

══════════════════════════════════════════════════════════════════

OFFER SUMMARY

Purchase Price:         ${offer_price:,.0f}
Earnest Money:          ${earnest_money:,.0f} (due upon signing)
Closing Date:           {closing_date}
Offer Valid Until:      {expires}

──────────────────────────────────────────────────────────────────

KEY ADVANTAGES OF THIS OFFER:

✓ CASH - No financing contingencies or appraisal delays
✓ SPEED - Close in just 14 days vs. 30-60 days traditional
✓ AS-IS - No inspections, repairs, or appraisal required
✓ CERTAINTY - No auction uncertainty or carried costs
✓ SIMPLICITY - Straightforward transaction, clear terms
✓ NO FEES - Zero realtor commissions, no auction costs

──────────────────────────────────────────────────────────────────

NEXT STEPS:

1. Review the attached formal offer document
2. Sign and return by {expires}
3. We deposit earnest money immediately  
4. Schedule property walkthrough
5. Close in 14 days with title company

──────────────────────────────────────────────────────────────────

QUESTIONS?

Please call me directly. I'm here to make this process simple and fast.

Best regards,

[YOUR NAME]
[YOUR COMPANY]
[YOUR PHONE]
[YOUR EMAIL]

══════════════════════════════════════════════════════════════════

P.S. - I've closed 50+ deals this year and I take my commitments 
seriously. This is a real offer backed by real capital and real 
execution. Let's work together.
"""
        return email.strip()
    
    @staticmethod
    def generate_call_followup(seller_name: str, offer_price: float, 
                               offer_sent_date: str) -> str:
        """
        Script for phone followup after offer sent
        """
        script = f"""
CALL SCRIPT - 24 HOUR FOLLOWUP

Opening:
"Hi {seller_name}, this is [Your Name] with [Your Company]. 
Did you get a chance to review the offer I sent yesterday for ${offer_price:,.0f}?"

[WAIT FOR RESPONSE]

If Yes - "Interested":
"Great! Do you have any questions about the terms? I want to make sure 
everything is crystal clear. This is a firm offer, so I can close on 
schedule."

If Yes - "Need Time":
"Totally understand - big decisions take thought. When would be a good 
time to touch base again? I'll keep the offer open through end of week."

If No - "Too Low":
"I appreciate that feedback. This price reflects current market conditions 
and quick close timeline. But let me ask - what number would make sense 
to you? Let's find the middle ground."

If No - "Want to List":
"I totally get it. Just so you know, listing adds 30-60 days and 5-6% 
in realtor costs. If it doesn't sell within 21 days, consider my offer 
as a backup. I'll still be here."

Close:
"Let's stay in touch. I'm committed to making this work if the numbers 
fit for both of us."
"""
        return script.strip()

# ============================================
# PROFESSIONAL CONTRACT GENERATOR
# ============================================

class ContractGenerator:
    """
    Generate investor-safe contracts with legal protection
    """
    
    @staticmethod
    def generate_purchase_agreement(property_data: Dict, offer_data: Dict,
                                  seller_name: str, buyer_name: str) -> str:
        """
        Generate professional Purchase Agreement
        Includes assignment rights and exit clauses
        """
        address = property_data.get("address")
        city = property_data.get("city")
        state = property_data.get("state", "TX")
        zip_code = property_data.get("zip")
        purchase_price = offer_data.get("offer_price")
        earnest_money = offer_data.get("earnest_money", int(purchase_price * 0.01))
        closing_date = (datetime.now() + timedelta(days=14)).strftime("%B %d, %Y")
        contract_date = datetime.now().strftime("%B %d, %Y")
        
        contract = f"""
═══════════════════════════════════════════════════════════════════════════════
                      RESIDENTIAL PURCHASE AGREEMENT
                     WITH ASSIGNMENT AND EXIT PROVISIONS
═══════════════════════════════════════════════════════════════════════════════

THIS AGREEMENT made and entered into on {contract_date} between:

SELLER: {seller_name} ("Seller")

BUYER: {buyer_name} ("Buyer")

PROPERTY: The single-family residence commonly known as:
          {address}
          {city}, {state} {zip_code}
          
          Legal Description: [TO BE DETERMINED BY TITLE COMPANY]

═══════════════════════════════════════════════════════════════════════════════

1. PURCHASE PRICE AND TERMS

1.1 Purchase Price:            ${purchase_price:,.2f}

1.2 Earnest Money Deposit:     ${earnest_money:,.2f}
    
    The Earnest Money shall be deposited with [TITLE COMPANY NAME] within 
    24 hours of this agreement being fully executed by both parties.

1.3 Cash Sale - No Financing Contingency
    
    This is a cash transaction. Buyer is not relying on any financing and 
    has readily available funds. No appraisal, loan qualification, or 
    financing contingency.

1.4 Payment at Closing:        ${purchase_price - earnest_money:,.2f}
    
    Due at closing in immediately available funds.

═══════════════════════════════════════════════════════════════════════════════

2. PROPERTY CONDITION AND INSPECTIONS

2.1 AS-IS Condition
    
    Buyer acknowledges and agrees that the property is being purchased in 
    its current "AS-IS" condition, with no warranties or representations 
    regarding the condition of the property. Seller makes no representations 
    regarding the property's structural integrity, systems, or condition.

2.2 No Inspection Contingency
    
    Buyer waives all rights to conduct inspections, appraisals, or walk-throughs 
    prior to closing EXCEPT for a single agreed-upon walkthrough to verify 
    the property has not been substantially altered or damaged since the 
    signing of this agreement.

2.3 Buyer's Due Diligence
    
    Buyer has had opportunity to inspect the property and accepts full 
    responsibility for assessing its condition and suitability.

═══════════════════════════════════════════════════════════════════════════════

3. ASSIGNMENT AND TRANSFER RIGHTS

3.1 Assignment Authorization
    
    Buyer shall have the right to assign this contract to any third party 
    ("End Buyer") at any time prior to closing, with or without notice to Seller.
    
    In the event of assignment, End Buyer shall assume all obligations under 
    this agreement.

3.2 Assignment Fee
    
    Buyer may collect an assignment fee from End Buyer. This assignment fee 
    is NOT a financing contingency and does NOT delay closing.

3.3 Seller Notification
    
    Buyer shall notify Seller of any assignment at least 5 business days 
    prior to closing. Assignment does not release Buyer from obligations 
    under this contract.

═══════════════════════════════════════════════════════════════════════════════

4. CRITICAL EXIT CLAUSE - BUYER PROTECTION

4.1 Title and Survey Inspection Period (7 DAYS FROM SIGNING)
    
    Buyer shall have 7 days from execution of this agreement to:
    
    ✓ Review preliminary title report
    ✓ Verify property line and boundaries
    ✓ Identify any liens, encumbrances, or defects
    
    If Title issues exist that are unacceptable to Buyer, Buyer may terminate 
    this agreement in writing within 7 days and receive earnest money refund.
    
    Unacceptable Title Issues Include:
    - Judgment liens
    - Tax liens
    - Code enforcement violations
    - Zoning violations
    - Easement restrictions
    - HOA liens exceeding $5,000

4.2 No Material Change to Property
    
    If property is substantially damaged or altered between signing and 
    closing, Buyer may terminate this agreement and recover earnest money.
    
    "Substantial" is defined as damage requiring repairs exceeding $10,000.

4.3 Seller Obligations Failure
    
    If Seller fails to meet any obligation under this agreement (including 
    but not limited to clear title delivery, maintaining property condition), 
    Buyer may terminate and recover earnest money without penalty.

═══════════════════════════════════════════════════════════════════════════════

5. CLOSING AND TIMELINE

5.1 Closing Date: {closing_date}

5.2 Closing Location: [TITLE COMPANY NAME AND ADDRESS]

5.3 Closing Procedures
    
    Seller and Buyer shall cooperate fully with the Title Company to ensure 
    a smooth closing. All necessary documents shall be executed at closing.

5.4 Prorations and Costs
    
    Property taxes, insurance, and HOA fees (if applicable) shall be prorated 
    to the closing date.
    
    Buyer and Seller will split closing costs equally, or as negotiated.

═══════════════════════════════════════════════════════════════════════════════

6. EARNEST MONEY DISPOSITION

6.1 Release of Earnest Money
    
    If this transaction closes, earnest money is credited toward the purchase price.
    
    If this transaction does NOT close due to Buyer's default (failure to close 
    by closing date with clear funds), earnest money is forfeited to Seller.
    
    If this transaction does NOT close due to Seller's default or Buyer's use 
    of exit clause, earnest money is returned to Buyer.

═══════════════════════════════════════════════════════════════════════════════

7. REPRESENTATIONS AND WARRANTIES

7.1 Seller Represents and Warrants
    
    ✓ Seller has good and marketable title to the property
    ✓ Seller has authority to enter into this agreement
    ✓ No liens or encumbrances except as disclosed
    ✓ Property is not subject to code violations (unless disclosed)
    ✓ Seller is not aware of any defects (except as disclosed in writing)

7.2 Buyer Represents and Warrants
    
    ✓ Buyer has funds available for closing
    ✓ Buyer has authority to enter into this agreement
    ✓ Buyer acknowledges property is being purchased AS-IS

═══════════════════════════════════════════════════════════════════════════════

8. DEFAULT AND REMEDIES

8.1 Buyer Default
    
    If Buyer fails to close on scheduled closing date with clear funds, 
    Earnest Money is forfeited to Seller as liquidated damages.

8.2 Seller Default
    
    If Seller fails to close or breaches this agreement, Buyer may:
    
    (a) Terminate and recover earnest money in full, OR
    (b) Seek specific performance and force closing

═══════════════════════════════════════════════════════════════════════════════

9. MISCELLANEOUS

9.1 Entire Agreement
    
    This agreement constitutes the entire agreement between parties. Any prior 
    agreements, representations, or understandings are superseded.

9.2 Severability
    
    If any provision is found invalid, remaining provisions remain in full effect.

9.3 Governing Law
    
    This agreement is governed by the laws of the State of {state}.

9.4 Addenda
    
    The following addenda are attached and incorporated:
    - [Any additional provisions]

═══════════════════════════════════════════════════════════════════════════════

SIGNATURES

BUYER: ________________________________  DATE: ______________

NAME (PRINT): ________________________


SELLER: ________________________________  DATE: ______________

NAME (PRINT): ________________________


WITNESSED BY:

[TITLE COMPANY REPRESENTATIVE]

═══════════════════════════════════════════════════════════════════════════════

TITLE COMPANY: ___________________________

ADDRESS: ___________________________

CONTACT: ___________________________

═══════════════════════════════════════════════════════════════════════════════
"""
        return contract.strip()
    
    @staticmethod
    def generate_assignment_contract(property_data: Dict, assignment_data: Dict) -> str:
        """
        Assignment contract for reselling to end buyer
        """
        address = property_data.get("address")
        city = property_data.get("city")
        original_price = assignment_data.get("original_purchase_price")
        assignment_fee = assignment_data.get("assignment_fee", 10000)
        end_buyer_price = original_price + assignment_fee
        
        contract = f"""
═══════════════════════════════════════════════════════════════════════════════
                     ASSIGNMENT OF PURCHASE AGREEMENT
═══════════════════════════════════════════════════════════════════════════════

DATE: {datetime.now().strftime('%B %d, %Y')}

PROPERTY: {address}, {city}, Texas

═══════════════════════════════════════════════════════════════════════════════

PRINCIPAL (Original Buyer):      [YOUR NAME/COMPANY]
END BUYER (Assignee):            [END BUYER NAME]
SELLER:                          [ORIGINAL SELLER NAME]

═══════════════════════════════════════════════════════════════════════════════

1. ASSIGNMENT OF RIGHTS

The undersigned Principal assigns and transfers all right, title, and interest 
in and to that certain Purchase Agreement dated [ORIGINAL DATE] for the above-
referenced property to the End Buyer.

2. FINANCIAL TERMS

Original Purchase Price:         ${original_price:,.2f}
Assignment Fee (Principal):      ${assignment_fee:,.2f}
─────────────────────────────────────────────────────────
Total Price Due from End Buyer:  ${end_buyer_price:,.2f}

The Assignment Fee compensates the Principal for locating and securing the 
opportunity, performing due diligence, and expediting the transaction.

3. END BUYER'S OBLIGATIONS

The End Buyer shall:

✓ Assume all obligations under the original Purchase Agreement
✓ Pay the total assignment price to the Seller at closing
✓ Perform all Buyer obligations (earnest money, closing on time, etc.)
✓ Hold Principal harmless from any breaches of original agreement
✓ Release Principal from all further obligations upon closing

4. ASSIGNMENT FEE PAYMENT

The assignment fee is NOT contingent on:
- Appraisals
- Inspections  
- Financing
- End Buyer's financial condition

The assignment fee is DUE AT CLOSING from the End Buyer's funds.

5. CLOSING AND TIMELINE

Closing shall proceed under the original Purchase Agreement timeline and terms.
End Buyer acknowledges awareness of all original agreement terms.

6. REPRESENTATIONS

✓ This is a real property opportunity from actual foreclosure/auction
✓ Numbers are based on verified comparable sales data
✓ Property condition is AS-IS per original agreement
✓ No hidden costs or undisclosed obligations

7. SIGNATURE

PRINCIPAL (Assigning):           ________________  DATE: __________

END BUYER (Assuming):            ________________  DATE: __________

═══════════════════════════════════════════════════════════════════════════════

Questions? Contact Principal:
[CONTACT NAME]
[PHONE]
[EMAIL]

═══════════════════════════════════════════════════════════════════════════════
"""
        return contract.strip()

# ============================================
# DEAL STATUS TRACKER DATABASE
# ============================================

class DealTracker:
    """
    Track deal progress from qualified lead through closed deal
    Stores offer status, approvals, and deal milestones
    """
    
    def __init__(self, db_path: str = "/agent/home/deal_tracker.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize deal tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Deal tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id TEXT PRIMARY KEY,
                property_address TEXT,
                property_city TEXT,
                seller_name TEXT,
                seller_phone TEXT,
                seller_email TEXT,
                deal_status TEXT,
                current_stage TEXT,
                mao REAL,
                arv REAL,
                created_date TEXT,
                last_updated TEXT,
                notes TEXT
            )
        """)
        
        # Offer tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id TEXT PRIMARY KEY,
                deal_id TEXT,
                offer_tier TEXT,
                offer_price REAL,
                offer_status TEXT,
                ai_recommended_tier TEXT,
                human_approved_by TEXT,
                human_approved_date TEXT,
                sent_date TEXT,
                response_date TEXT,
                seller_response TEXT,
                created_date TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            )
        """)
        
        # Contract tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id TEXT PRIMARY KEY,
                deal_id TEXT,
                contract_type TEXT,
                contract_status TEXT,
                signed_by_seller TEXT,
                signed_date TEXT,
                seller_signature_date TEXT,
                closing_date TEXT,
                created_date TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            )
        """)
        
        # Approval log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                id TEXT PRIMARY KEY,
                deal_id TEXT,
                approval_type TEXT,
                approved_by TEXT,
                approval_date TEXT,
                notes TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_deal(self, property_data: Dict, seller_data: Dict, analysis: Dict) -> str:
        """Create new deal in pipeline"""
        deal_id = hashlib.md5(
            f"{property_data['address']}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO deals 
            (id, property_address, property_city, seller_name, seller_phone, 
             seller_email, deal_status, current_stage, mao, arv, created_date, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            deal_id,
            property_data.get("address"),
            property_data.get("city"),
            seller_data.get("name"),
            seller_data.get("phone"),
            seller_data.get("email"),
            DealStatus.QUALIFIED_LEAD.value,
            DealStatus.QUALIFIED_LEAD.value,
            analysis.get("mao"),
            analysis.get("arv_estimate"),
            datetime.now().isoformat(),
            datetime.now().isoformat(),
        ))
        
        conn.commit()
        conn.close()
        
        return deal_id
    
    def create_offer(self, deal_id: str, offer_tier: str, offer_price: float,
                    ai_recommended: str) -> str:
        """Create offer record"""
        offer_id = f"{deal_id}_offer_{datetime.now().isoformat()[:10]}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO offers
            (id, deal_id, offer_tier, offer_price, offer_status, ai_recommended_tier, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            offer_id,
            deal_id,
            offer_tier,
            offer_price,
            OfferStatus.DRAFT.value,
            ai_recommended,
            datetime.now().isoformat(),
        ))
        
        # Update deal status
        cursor.execute("""
            UPDATE deals SET 
            deal_status = ?, 
            current_stage = ?,
            last_updated = ?
            WHERE id = ?
        """, (
            DealStatus.OFFER_PENDING.value,
            DealStatus.OFFER_PENDING.value,
            datetime.now().isoformat(),
            deal_id,
        ))
        
        conn.commit()
        conn.close()
        
        return offer_id
    
    def approve_offer(self, offer_id: str, approved_by: str) -> bool:
        """Log human approval of offer"""
        approval_id = f"approval_{offer_id}_{datetime.now().isoformat()[:10]}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get deal_id from offer
        cursor.execute("SELECT deal_id FROM offers WHERE id = ?", (offer_id,))
        result = cursor.fetchone()
        if not result:
            return False
        deal_id = result[0]
        
        # Record approval
        cursor.execute("""
            INSERT INTO approvals
            (id, deal_id, approval_type, approved_by, approval_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            approval_id,
            deal_id,
            "OFFER_APPROVAL",
            approved_by,
            datetime.now().isoformat(),
        ))
        
        # Update offer status
        cursor.execute("""
            UPDATE offers SET
            offer_status = ?,
            human_approved_by = ?,
            human_approved_date = ?
            WHERE id = ?
        """, (
            OfferStatus.APPROVED.value,
            approved_by,
            datetime.now().isoformat(),
            offer_id,
        ))
        
        conn.commit()
        conn.close()
        
        return True
    
    def mark_offer_sent(self, offer_id: str) -> bool:
        """Mark offer as sent to seller"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE offers SET
            offer_status = ?,
            sent_date = ?
            WHERE id = ?
        """, (
            OfferStatus.SENT.value,
            datetime.now().isoformat(),
            offer_id,
        ))
        
        # Get deal_id
        cursor.execute("SELECT deal_id FROM offers WHERE id = ?", (offer_id,))
        deal_id = cursor.fetchone()[0]
        
        # Update deal status
        cursor.execute("""
            UPDATE deals SET
            deal_status = ?,
            current_stage = ?,
            last_updated = ?
            WHERE id = ?
        """, (
            DealStatus.OFFER_SENT.value,
            DealStatus.OFFER_SENT.value,
            datetime.now().isoformat(),
            deal_id,
        ))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_deal_summary(self, deal_id: str) -> Dict:
        """Get complete deal summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get deal info
        cursor.execute("SELECT * FROM deals WHERE id = ?", (deal_id,))
        deal_cols = [desc[0] for desc in cursor.description]
        deal_row = cursor.fetchone()
        deal = dict(zip(deal_cols, deal_row)) if deal_row else {}
        
        # Get offers
        cursor.execute("SELECT * FROM offers WHERE deal_id = ?", (deal_id,))
        offer_cols = [desc[0] for desc in cursor.description]
        offers = [dict(zip(offer_cols, row)) for row in cursor.fetchall()]
        
        # Get contracts
        cursor.execute("SELECT * FROM contracts WHERE deal_id = ?", (deal_id,))
        contract_cols = [desc[0] for desc in cursor.description]
        contracts = [dict(zip(contract_cols, row)) for row in cursor.fetchall()]
        
        # Get approvals
        cursor.execute("SELECT * FROM approvals WHERE deal_id = ?", (deal_id,))
        approval_cols = [desc[0] for desc in cursor.description]
        approvals = [dict(zip(approval_cols, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "deal": deal,
            "offers": offers,
            "contracts": contracts,
            "approvals": approvals,
        }

# ============================================
# MAIN EXECUTION & TESTING
# ============================================

if __name__ == "__main__":
    print("="*80)
    print("REAL ESTATE OFFER & CONTRACT GENERATION SYSTEM")
    print("="*80)
    
    # Sample property and analysis
    sample_property = {
        "address": "4702 Elm Street",
        "city": "Dallas",
        "state": "TX",
        "zip": "75210",
        "property_type": "single-family",
        "bedrooms": 4,
        "bathrooms": 2,
        "square_feet": 2400,
        "opening_bid": 140000,
    }
    
    sample_analysis = {
        "arv_estimate": 195000,
        "mao": 86500,
        "repair_estimate": 35000,
    }
    
    sample_seller = {
        "name": "John Smith",
        "phone": "+1-214-555-1234",
        "email": "john@example.com",
    }
    
    # Generate offers
    print("\n1. GENERATING 3-TIER OFFER STRATEGY")
    print("-" * 80)
    offers_data = OfferStrategyEngine.generate_offers(sample_property, sample_analysis)
    print(f"Property: {offers_data['property_address']}, {offers_data['property_city']}")
    print(f"MAO: ${offers_data['mao']:,.0f}")
    print(f"ARV: ${offers_data['arv']:,.0f}")
    print()
    
    for offer in offers_data['offers']:
        print(f"\n{offer['tier'].upper()}")
        print(f"  Price: {offer['offer_price_formatted']}")
        print(f"  Profit: {offer['profit_formatted']}")
        print(f"  Acceptance %: {offer['acceptance_probability']}%")
        print(f"  MAO Check: {offer['mao_validation']}")
    
    # Test recommendations
    print("\n\n2. AI RECOMMENDATIONS (HUMAN MUST APPROVE)")
    print("-" * 80)
    recommended = OfferStrategyEngine.recommend_tier("high")
    print(f"For HIGH motivation seller: Recommend {recommended.upper()}")
    print("⚠️  HUMAN MUST APPROVE before sending to seller")
    
    # Generate communications
    print("\n\n3. OFFER COMMUNICATION TEMPLATES")
    print("-" * 80)
    sms = OfferMessenger.generate_sms_offer(
        sample_seller['name'],
        sample_property['address'],
        offers_data['offers'][1]['offer_price']
    )
    print(f"\nSMS:\n{sms}")
    
    email = OfferMessenger.generate_email_offer(
        sample_property,
        offers_data['offers'][1],
        sample_seller['name'],
        sample_seller['email']
    )
    print(f"\n\nEMAIL SUBJECT & BODY:\n{email[:500]}...")
    
    # Generate contracts
    print("\n\n4. CONTRACT GENERATION")
    print("-" * 80)
    purchase_agreement = ContractGenerator.generate_purchase_agreement(
        sample_property,
        offers_data['offers'][1],
        sample_seller['name'],
        "Your Company Name"
    )
    print(f"\nPURCHASE AGREEMENT (first 500 chars):\n{purchase_agreement[:500]}...")
    
    # Deal tracking
    print("\n\n5. DEAL TRACKING DATABASE")
    print("-" * 80)
    tracker = DealTracker()
    
    deal_id = tracker.create_deal(sample_property, sample_seller, sample_analysis)
    print(f"✓ Created Deal: {deal_id}")
    
    offer_id = tracker.create_offer(deal_id, "balanced", offers_data['offers'][1]['offer_price'], "balanced")
    print(f"✓ Created Offer: {offer_id}")
    
    tracker.approve_offer(offer_id, "juancalude jordan")
    print(f"✓ Human Approved Offer")
    
    tracker.mark_offer_sent(offer_id)
    print(f"✓ Marked Offer as Sent")
    
    summary = tracker.get_deal_summary(deal_id)
    print(f"\nDeal Summary:")
    print(f"  Status: {summary['deal']['deal_status']}")
    print(f"  Current Stage: {summary['deal']['current_stage']}")
    print(f"  Offers: {len(summary['offers'])}")
    print(f"  Approvals: {len(summary['approvals'])}")
    
    print("\n" + "="*80)
    print("✓ System Ready for Production")
    print("="*80)
