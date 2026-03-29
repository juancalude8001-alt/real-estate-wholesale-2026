#!/usr/bin/env python3
"""
Real Estate Wholesale System
Offer & Contract Generator
Production-Ready
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
from enum import Enum

class OfferType(Enum):
    AGGRESSIVE = "aggressive"
    BALANCED = "balanced"
    SAFE = "safe"

# ============================================
# OFFER GENERATOR
# ============================================

class OfferGenerator:
    """
    Generate customized offers for each property
    Three offer strategy options for flexibility
    """
    
    @staticmethod
    def generate_offers(property_data: Dict, analysis: Dict) -> List[Dict]:
        """
        Generate 3 offers for a single property
        """
        mao = analysis.get("mao", 0)
        address = property_data.get("address", "")
        opening_bid = property_data.get("opening_bid", 0)
        
        offers = []
        
        # Offer A: AGGRESSIVE (Maximum profit to wholesaler)
        offer_a_price = mao * 0.95
        offers.append({
            "offer_type": "aggressive",
            "offer_price": round(offer_a_price, 2),
            "offer_price_formatted": f"${offer_a_price:,.0f}",
            "strategy": "Maximum Profit Strategy",
            "description": "Lowest price - highest profit for you",
            "seller_motivation_message": "This offer reflects the speed and convenience of a cash transaction",
            "likelihood_percent": 30,
            "assignment_fee": 10000,
            "closing_timeline_days": 14,
            "earnest_money_percent": 1.0,
            "discount_vs_opening": f"{((opening_bid - offer_a_price) / opening_bid * 100):.1f}%",
            "rationale": "Leverages seller's auction anxiety and need for certainty",
        })
        
        # Offer B: BALANCED (Likely to be accepted)
        offer_b_price = mao
        offers.append({
            "offer_type": "balanced",
            "offer_price": round(offer_b_price, 2),
            "offer_price_formatted": f"${offer_b_price:,.0f}",
            "strategy": "Balanced Strategy",
            "description": "Fair price with good profit potential",
            "seller_motivation_message": "This offer represents fair market value with certainty of close",
            "likelihood_percent": 60,
            "assignment_fee": 10000,
            "closing_timeline_days": 14,
            "earnest_money_percent": 1.0,
            "discount_vs_opening": f"{((opening_bid - offer_b_price) / opening_bid * 100):.1f}%",
            "rationale": "Highest probability of acceptance while maintaining solid profit",
        })
        
        # Offer C: SAFE (Highest price we can offer)
        offer_c_price = mao * 1.05
        offers.append({
            "offer_type": "safe",
            "offer_price": round(offer_c_price, 2),
            "offer_price_formatted": f"${offer_c_price:,.0f}",
            "strategy": "Competitive Strategy",
            "description": "Most competitive - highest acceptance rate",
            "seller_motivation_message": "This is a competitive offer backed by our speed and reliability",
            "likelihood_percent": 80,
            "assignment_fee": 10000,
            "closing_timeline_days": 14,
            "earnest_money_percent": 1.0,
            "discount_vs_opening": f"{((opening_bid - offer_c_price) / opening_bid * 100):.1f}%",
            "rationale": "Competitive pricing to maximize deal closure probability",
        })
        
        return offers

# ============================================
# CALL SCRIPT GENERATOR
# ============================================

class CallScriptGenerator:
    """
    Generate customized outreach call scripts
    """
    
    @staticmethod
    def generate_script(property_data: Dict, analysis: Dict, offer_data: Dict) -> str:
        """
        Generate a professional call script
        """
        address = property_data.get("address", "")
        city = property_data.get("city", "")
        offer_price = offer_data.get("offer_price_formatted", "$0")
        opening_bid = property_data.get("opening_bid", 0)
        days_remaining = property_data.get("time_remaining_days", 0)
        
        script = f"""
═══════════════════════════════════════════════════════════════════════════
CALL SCRIPT FOR: {address}, {city}
═══════════════════════════════════════════════════════════════════════════
OFFER PRICE: {offer_price}
CLOSING TIMELINE: 14 days
EARNEST MONEY: 1% ({int(float(offer_price.replace('$','').replace(',','')) * 0.01):,})
═══════════════════════════════════════════════════════════════════════════

📞 OPENING (15 seconds)

"Hi [Owner Name], this is [Your Name] with [Your Company]. 
I came across your property at {address} that I see is heading to auction 
in {days_remaining} days. Do you have about 5 minutes? I might be able to 
save you a lot of stress and uncertainty."

[PAUSE - Wait for response]


✓ QUALIFICATION (20-30 seconds)

If they seem interested:
"Out of curiosity, what's driving the auction situation? 
Are you looking for a quick exit, or are you open to exploring alternatives?"

[LISTEN - Let them explain their situation]

"I understand. A lot of sellers in your situation haven't had the time to 
properly market the property. We actually specialize in exactly this scenario."


💰 VALUE PROPOSITION (30-45 seconds)

"Here's what we do differently:
- We buy homes AS-IS, no repairs needed
- Zero realtor commissions (usually 5-6% you'd lose)
- Zero auction fees and uncertainty
- We close in just 14 days with cash
- You get a firm offer in writing today

Most sellers in your position lose 15-25% of their equity to auction costs 
and delays. We eliminate all of that."


📝 OFFER STATEMENT (20-30 seconds)

"Based on current market conditions and the property's condition, 
I can offer {offer_price} for a quick close. 

That gives you certainty, speed, and avoids all the auction risks. 
You have a firm offer in your hands by end of business today."

[PAUSE - Let this sink in]


🚫 OBJECTION HANDLING

If: "Your price is too low"

Response: "I understand, and I appreciate that. Our pricing reflects the 
as-is condition and our fast timeline. But when you factor in what you'd 
lose to auction fees, realtor commissions, and carrying costs during a 
traditional sale, you usually come out ahead.

Let me ask - if I could get you this certainty and timeline for just a 
bit more, would that work for you?"


If: "I want to try the auction first"

Response: "That's fair - auctions can work. But they come with risks:
- Only investors show up (not owner-occupants who pay more)
- Auction costs eat 10-15% of the sale price  
- Redemption rights could extend timelines
- You might end up selling for less anyway

Here's my suggestion: keep my offer. If the auction doesn't go well, 
call me back. We'll still be here. Deal?"


If: "Can you give me more time to think?"

Response: "Absolutely. I'll email this offer over to you right now. 
Give it 24 hours. 

But I want to be honest - I can hold this price through [DATE], 
then it may need adjustment based on my other commitments.

Can I call you back tomorrow at this time to answer any questions?"


✓ CLOSE (15-20 seconds)

"So here's what I'm going to do: I'll send over a formal offer with 
all the terms right now. It's straightforward - just the essentials.

You can review it, and we can jump on a quick call tomorrow if you 
have questions. How's [TIME] tomorrow?"

[CONFIRM TIME]

"Perfect. I'll also send over a few references from other sellers 
I've worked with. They're happy to tell you about their experience. 
I appreciate your time, and I look forward to helping you solve 
this quickly."


═══════════════════════════════════════════════════════════════════════════

⏰ CALL TIPS:
- Speak slowly and clearly
- Listen more than you talk (aim for 30/70 ratio)
- Acknowledge their concerns  
- Focus on their benefits, not your profit
- Don't be pushy - confidence sells
- Use pauses strategically
- Send written offer immediately after
- Follow up next day if interested

═══════════════════════════════════════════════════════════════════════════
"""
        return script

# ============================================
# WRITTEN OFFER GENERATOR
# ============================================

class WrittenOfferGenerator:
    """
    Generate a professional written offer document
    """
    
    @staticmethod
    def generate_offer_letter(property_data: Dict, offer_data: Dict) -> str:
        """
        Generate a professional offer letter
        """
        address = property_data.get("address", "")
        city = property_data.get("city", "")
        zip_code = property_data.get("zip", "")
        offer_price = offer_data.get("offer_price", 0)
        offer_type = offer_data.get("offer_type", "balanced")
        
        closing_date = (datetime.now() + timedelta(days=14)).strftime("%B %d, %Y")
        effective_date = datetime.now().strftime("%B %d, %Y")
        expires_date = (datetime.now() + timedelta(days=7)).strftime("%B %d, %Y")
        earnest_money = int(offer_price * 0.01)
        
        letter = f"""
═══════════════════════════════════════════════════════════════════════════
                         CASH OFFER TO PURCHASE
═══════════════════════════════════════════════════════════════════════════

Date: {effective_date}

To: [OWNER NAME/SELLER]

Property Address: {address}, {city}, TX {zip_code}

═══════════════════════════════════════════════════════════════════════════

1. OFFER PRICE & TERMS

Purchase Price:                    ${offer_price:,.2f}
Earnest Money Deposit:             ${earnest_money:,.2f}
Due Upon Signing

OFFER TYPE: {offer_type.upper()}
This is a cash offer - no financing contingencies.


2. PROPERTY CONDITION

Property to be purchased in current "AS-IS" condition.
No repairs required.
No inspection contingency.


3. CLOSING & TIMELINE

Proposed Closing Date:             {closing_date}
Closing Location:                  [Title Company - TBD]

This offer allows for a 14-day closing, providing you with:
✓ Certainty of close
✓ No financing delays
✓ No appraisal contingencies
✓ Professional, straightforward transaction


4. SPECIAL TERMS

- This offer is contingent on property walkthrough
- Earnest money held in escrow by title company
- All closing costs negotiable
- As-is purchase - no repairs or warranties

5. OFFER VALIDITY

This offer is valid through:       {expires_date}

After this date, offer is void unless extended in writing.


6. NEXT STEPS

1. Sign and return this offer by [DATE/TIME]
2. We deposit earnest money immediately
3. Schedule property walkthrough
4. Title search initiated
5. 14-day close

═══════════════════════════════════════════════════════════════════════════

ADVANTAGES OF THIS OFFER:

✓ SPEED - Close in 14 days vs. 30-60 days traditional
✓ CERTAINTY - Cash offer, no financing to fall through
✓ SIMPLICITY - No inspections, appraisals, or contingencies
✓ NO FEES - No realtor commissions, no auction fees
✓ PRIVACY - Discrete transaction, no listing
✓ RELIEF - Avoid auction uncertainty and costs

═══════════════════════════════════════════════════════════════════════════

This offer is made with the genuine intention to close.
We take our commitments seriously and have closed 50+ deals this year.

References available upon request.

═══════════════════════════════════════════════════════════════════════════

Buyer Representative:              [Your Name]
Phone:                             [Your Phone]
Email:                             [Your Email]
Company:                           [Your Company]
License #:                         [If applicable]

═══════════════════════════════════════════════════════════════════════════

SELLER SIGNATURE: ___________________________  DATE: ___________

SELLER PRINTED NAME: ________________________

PHONE: ____________________________________

EMAIL: ____________________________________

═══════════════════════════════════════════════════════════════════════════
"""
        return letter

# ============================================
# ASSIGNMENT CONTRACT GENERATOR
# ============================================

class AssignmentContractGenerator:
    """
    Generate assignment contract for MaxDispo
    """
    
    @staticmethod
    def generate_assignment_contract(property_data: Dict, deal_data: Dict) -> str:
        """
        Generate assignment contract template
        """
        address = property_data.get("address", "")
        city = property_data.get("city", "")
        purchase_price = deal_data.get("purchase_price", 0)
        assignment_fee = deal_data.get("assignment_fee", 10000)
        assigned_price = purchase_price + assignment_fee
        
        contract = f"""
═══════════════════════════════════════════════════════════════════════════
                    ASSIGNMENT OF PURCHASE AGREEMENT
═══════════════════════════════════════════════════════════════════════════

Property: {address}, {city}, Texas

Original Purchase Price:           ${purchase_price:,.2f}
Assignment Fee:                    ${assignment_fee:,.2f}
─────────────────────────────────────────────────────────────────────────
TOTAL INVESTMENT NEEDED:           ${assigned_price:,.2f}


1. ASSIGNMENT TERMS

The undersigned Principal assigns all rights under the Purchase Agreement 
dated [DATE] with the seller [SELLER NAME] for the above property.

The End Buyer [END BUYER NAME] shall:
- Assume all obligations under the original contract
- Pay the assignment fee of ${assignment_fee:,.2f}
- Take title at final closing
- Receive the property in as-is condition


2. BUYER'S PROFIT POTENTIAL

After Repair Value (ARV):          ${deal_data.get('arv', 0):,.2f}
Less: Purchase Price:             -${assigned_price:,.2f}
Less: Estimated Repairs:          -${deal_data.get('repairs', 0):,.2f}
Less: Closing Costs (approx):     -$5,000
─────────────────────────────────────────────────────────────────────────
ESTIMATED PROFIT:                 ${deal_data.get('profit', 0):,.2f}


3. PROPERTY CONDITION

Property Details:
- Type: {property_data.get('property_type', 'N/A')}
- Bedrooms: {property_data.get('bedrooms', 'N/A')}
- Bathrooms: {property_data.get('bathrooms', 'N/A')}
- Square Feet: {property_data.get('square_feet', 'N/A'):,} sq ft
- Condition: AS-IS (No inspections required)


4. CLOSING TIMELINE

Assignment Period:                 14 days
Closing Date:                      [DATE]
Title Company:                     [TITLE COMPANY NAME]


5. THIS IS A REAL OPPORTUNITY

✓ Real property from active foreclosure/auction
✓ Real profit numbers based on comparable sales
✓ Real closing timeline with title company
✓ Real assignment fee (no hidden costs)


═══════════════════════════════════════════════════════════════════════════

Questions? Contact:
[Your Name]
[Your Phone]
[Your Email]

═══════════════════════════════════════════════════════════════════════════
"""
        return contract

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    # Example property
    sample_property = {
        "address": "4702 Elm Street",
        "city": "Dallas",
        "zip": "75210",
        "property_type": "single-family",
        "bedrooms": 5,
        "bathrooms": 3,
        "square_feet": 2800,
        "opening_bid": 135000,
        "time_remaining_days": 17,
    }
    
    sample_analysis = {
        "arv_estimate": 195750,
        "mao": 86775,
        "repair_estimate": 50000,
        "estimated_profit": 75304,
    }
    
    # Generate offers
    print("="*80)
    print("GENERATING 3 OFFERS FOR PROPERTY")
    print("="*80)
    print()
    
    offers = OfferGenerator.generate_offers(sample_property, sample_analysis)
    
    for i, offer in enumerate(offers, 1):
        print(f"\nOFFER {i}: {offer['strategy'].upper()}")
        print(f"Price: {offer['offer_price_formatted']}")
        print(f"Strategy: {offer['description']}")
        print(f"Likelihood: {offer['likelihood_percent']}%")
        print(f"Rationale: {offer['rationale']}")
    
    # Generate call script
    print("\n" + "="*80)
    print("CALL SCRIPT")
    print("="*80)
    script = CallScriptGenerator.generate_script(
        sample_property, 
        sample_analysis, 
        offers[1]  # Balanced offer
    )
    print(script)
    
    # Generate offer letter
    print("\n" + "="*80)
    print("WRITTEN OFFER LETTER")
    print("="*80)
    letter = WrittenOfferGenerator.generate_offer_letter(
        sample_property, 
        offers[1]
    )
    print(letter)
    
    # Save to file
    output = {
        "property": sample_property,
        "analysis": sample_analysis,
        "offers": offers,
        "call_script": script,
        "offer_letter": letter,
        "timestamp": datetime.now().isoformat(),
    }
    
    with open("/agent/home/offers_output.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print("\n✓ Output saved to offers_output.json")
