import os
import json
import re
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Sir Kasturchand Daga Bal Sadan Knowledge Base
BAL_SADAN_INFO = {
    "name": "Sir Kasturchand Daga Bal Sadan",
    "location": "Lakad Ganj, Kamptee, Maharashtra 441001",
    "city": "Kamptee, Nagpur District, Maharashtra",
    "phone": "077095 58334",
    "phone_display": "+91 77095 58334",
    "opening_time": "Opens daily at 11:00 AM",
    "snack_donation_notice": "Donation towards children like snacks is Monday to Saturday from 3:00 PM onwards.",
    "visiting_hours": "Monday to Saturday, 3:00 PM to 6:00 PM (Ideal for snack sharing, child interaction & celebrations); Office opens at 11:00 AM.",
    "current_children_count": 45,
    "nearest_landmark": "Near Lakad Ganj, Kamptee, approx 1.5 km from Kamptee Railway Station & 15 km from Nagpur",
}

RECOMMENDED_SNACKS = [
    {
        "category": "Fresh Fruits",
        "items": "Bananas, Apples, Oranges, Pears, Seasonal sweet fruits",
        "benefits": "Rich in vitamins, high immunity, easily digestible for all ages."
    },
    {
        "category": "Wholesome Warm Evening Snacks",
        "items": "Poha with roasted peanuts, Upma, Veg Sandwiches, Idli-Chutney, Dhokla, Samosa/Kachori from clean vendors",
        "benefits": "Fresh, filling, and loved by the children as evening refreshment."
    },
    {
        "category": "Packaged Healthy Treats",
        "items": "Marie biscuits, glucose biscuits, fruit cakes, roasted chana, peanut chikki, murmura mixture",
        "benefits": "Hygienic, long shelf life, perfect for study time snacks."
    },
    {
        "category": "Nutritional Drinks & Juices",
        "items": "Flavored milk cartons, Frooti / Real fruit juice packs, Hot badam milk",
        "benefits": "Calcium, hydration and energy boost after school hours."
    },
    {
        "category": "Celebration Sweets & Cake",
        "items": "Birthday eggless cakes, Gulab jamun, Besan laddoo, Kheer, Kaju katli",
        "benefits": "Adds joy and festive warmth to children's special celebrations."
    }
]

def plan_snack_menu(child_count=45, budget=None, occasion="Birthday"):
    """
    AI Snack & Meal Planner: Generates a tailored nutritious snack menu based on child count & occasion.
    """
    child_count = int(child_count) if child_count else 45
    
    if budget:
        budget = float(budget)
    else:
        # Default estimated budget: approx 50-80 INR per child
        budget = child_count * 65

    per_child_budget = budget / child_count if child_count > 0 else 60

    if per_child_budget >= 100:
        tier = "Grand Celebration Feast"
        menu_items = [
            f"Delicious Birthday Cake / Sweet Treat ({child_count} portions)",
            f"Warm Savory Snack (Fresh Vegetable Samosa / Poha / Veg Cutlet) - {child_count} servings",
            f"Fresh Seasonal Fruits (Apples & Bananas) - {child_count} pcs each",
            f"Fruit Juice / Flavored Milk Carton - {child_count} packs",
            f"Special Gift Stationery Pack (Pencil, eraser & notebook) - {child_count} sets"
        ]
        nutrition_highlight = "Rich in proteins, natural fruit vitamins, and celebratory happiness!"
    elif per_child_budget >= 60:
        tier = "Wholesome Deluxe Snack Pack"
        menu_items = [
            f"Fresh Fruit Box (1 Apple + 1 Banana per child) - {child_count * 2} fruits",
            f"Savory Evening Snack (Vegetable Poha / Sandwich) - {child_count} servings",
            f"Juice Carton / Flavored Milk - {child_count} packs",
            f"Chikki / Sweet Laddoo - {child_count} pcs"
        ]
        nutrition_highlight = "Balanced carbohydrate energy + essential natural vitamins."
    else:
        tier = "Nutritious Energy Snack Kit"
        menu_items = [
            f"Fresh Bananas (High potassium & energy) - {child_count} fruits",
            f"Nutritious Marie / Glucose Biscuit Packs - {child_count} packets",
            f"Peanut Chikki / Healthy Laddoos - {child_count} portions",
            f"Milk / Fruit Drink - {child_count} servings"
        ]
        nutrition_highlight = "Instant energy for study hours with high nutritional value."

    return {
        "tier": tier,
        "child_count": child_count,
        "estimated_total_cost": f"₹{int(budget):,}",
        "cost_per_child": f"₹{int(per_child_budget)}",
        "occasion": occasion,
        "recommended_timing": "Monday to Saturday, 3:00 PM to 4:30 PM (Evening Snack Break)",
        "menu_items": menu_items,
        "nutrition_highlight": nutrition_highlight,
        "delivery_instructions": "Please arrive at Lakad Ganj, Kamptee at 3:00 PM. Hot snacks should be collected fresh from trusted vendors."
    }

def generate_blessing_letter(donor_name, occasion, category):
    """
    Generates a personalized warm acknowledgment & blessing letter for the donor.
    """
    donor = donor_name.strip() if donor_name else "Kind Patron"
    occasion_txt = f" on the auspicious occasion of {occasion}" if occasion else ""
    date_str = datetime.now().strftime("%B %d, %Y")

    letter = f"""
Dear {donor},

With immense joy and deepest gratitude, all the children, teachers, and staff at Sir Kasturchand Daga Bal Sadan, Kamptee, thank you for your compassionate contribution{occasion_txt}.

Your kind support towards "{category}" brings bright smiles, nourishment, and reassurance to our 45 beloved children in Lakad Ganj, Kamptee. 

When you share snacks, meals, education, and love, you become a guardian angel in the lives of these promising young souls. The children held a special prayer today for your family's continuous health, peace, prosperity, and joy.

"Giving is not just about making a donation. It is about making a difference."

With Warmest Regards & Prayers,
Children & Management Committee
Sir Kasturchand Daga Bal Sadan
Lakad Ganj, Kamptee, Maharashtra 441001
Contact: 077095 58334
Date: {date_str}
"""
    return letter.strip()

def process_ai_query(user_message):
    """
    Intelligent NLP responder for Sir Kasturchand Daga Bal Sadan.
    Answers in English, Hindi, and Marathi with full context.
    """
    msg = user_message.lower().strip()
    
    # 1. Snack Donation & Timings (The primary user alert)
    if any(k in msg for k in ["snack", "snake", "nasta", "nashta", "refreshment", "food", "khana", "fruit", "biscuit", "time to donate", "evening snack"]):
        return {
            "intent": "snack_donation",
            "reply": (
                "🥪 **Donation of Snacks & Refreshments:**\n\n"
                "Sir Kasturchand Daga Bal Sadan warmly accepts snack donations for the children **Monday to Saturday from 3:00 PM onwards**.\n\n"
                "**Recommended Snack Items:**\n"
                "• **Fresh Fruits:** Bananas, apples, oranges, seasonal fruits\n"
                "• **Evening Warm Snacks:** Poha, Upma, vegetable sandwiches, dhokla, samosas (from hygienic shops)\n"
                "• **Packaged Treats:** Quality biscuits (Marie/Parle), fruit cakes, peanut chikki\n"
                "• **Drinks:** Flavored milk cartons, fruit juice packs (Frooti/Real)\n\n"
                "We currently have **45 children** residing at our Kamptee campus. You are welcome to book a visit slot online or call **077095 58334** before arriving!"
            )
        }

    # 2. Address, Location, How to reach Kamptee
    if any(k in msg for k in ["address", "location", "where", "kaha", "kahan", "directions", "reach", "map", "kamptee", "lakad ganj"]):
        return {
            "intent": "location_directions",
            "reply": (
                "📍 **Address & Directions to Bal Sadan:**\n\n"
                "**Sir Kasturchand Daga Bal Sadan**\n"
                "**Address:** Lakad Ganj, Kamptee, Maharashtra 441001 (Nagpur District)\n"
                "**Phone:** [077095 58334](tel:07709558334)\n\n"
                "**How to Reach:**\n"
                "• **By Train:** Just 1.5 km from Kamptee Railway Station (Auto-rickshaws available to Lakad Ganj).\n"
                "• **From Nagpur City:** Approx. 15 km via the Nagpur–Jabalpur Highway (NH 44).\n"
                "• Google Maps search: *'Sir Kasturchand Daga Bal Sadan Kamptee'*\n\n"
                "Our office opens at **11:00 AM**, and children's snack/visiting hours start from **3:00 PM onwards** (Monday to Saturday)."
            )
        }

    # 3. Hours, Timings, Open / Close
    if any(k in msg for k in ["hours", "timing", "open", "close", "samay", "waqt", "kab", "when"]):
        return {
            "intent": "operating_hours",
            "reply": (
                "🕒 **Visiting & Operating Hours:**\n\n"
                "• **Office Opening Hours:** Daily from **11:00 AM** onwards.\n"
                "• **Children Snack Donation & Visiting Time:** **Monday to Saturday from 3:00 PM onwards** (Best window: 3:00 PM to 6:00 PM).\n"
                "• **Sundays:** Special activity & prayer sessions by prior appointment.\n\n"
                "Feel free to visit us at Lakad Ganj, Kamptee or call **077095 58334** to confirm your visit time."
            )
        }

    # 4. Birthday Celebration & Anniversary Sponsorship
    if any(k in msg for k in ["birthday", "janamdin", "anniversary", "celebrate", "party", "cake", "occasion"]):
        return {
            "intent": "birthday_celebration",
            "reply": (
                "🎂 **Celebrate Your Special Day with Our Children!**\n\n"
                "You can celebrate your birthday, your child's birthday, or a wedding anniversary with the 45 children of Sir Kasturchand Daga Bal Sadan.\n\n"
                "**How it works:**\n"
                "1. **Time Slot:** Monday to Saturday, between **3:00 PM and 5:30 PM**.\n"
                "2. **What to Bring:** An eggless birthday cake, fresh fruit juice/milk cartons, and snack packets (e.g. samosa, poha, biscuits, or fruits).\n"
                "3. **Celebration:** Children will sing birthday songs, cut the cake with you, and give heartfelt blessings!\n\n"
                "👉 Use our **'Schedule Visit'** form on the website or call **077095 58334** to reserve your celebration date."
            )
        }

    # 5. Contact, Phone Number, WhatsApp
    if any(k in msg for k in ["phone", "contact", "call", "mobile", "number", "whatsapp", "email"]):
        return {
            "intent": "contact_info",
            "reply": (
                "📞 **Contact Information:**\n\n"
                "• **Primary Phone:** [077095 58334](tel:07709558334)\n"
                "• **WhatsApp:** Chat directly with the management at [+91 77095 58334](https://wa.me/917709558334)\n"
                "• **Address:** Lakad Ganj, Kamptee, Maharashtra 441001\n"
                "• You can also send an instant message via the **Contact Us** form on this website!"
            )
        }

    # 6. Volunteer Opportunities
    if any(k in msg for k in ["volunteer", "teach", "mentor", "help", "sewa", "seva", "join", "skills"]):
        return {
            "intent": "volunteer_inquiry",
            "reply": (
                "🤝 **Join as a Volunteer at Bal Sadan!**\n\n"
                "We welcome volunteers who can contribute their time and talent:\n"
                "• **Academic Tutoring:** English, Mathematics, Science for Class 1 to 10.\n"
                "• **Creative Arts:** Drawing, music, dance, theater, origami.\n"
                "• **Sports & Physical Training:** Cricket, yoga, self-defense.\n"
                "• **Snack & Event Assistance:** Helping distribute afternoon refreshments and organizing festivals.\n\n"
                "👉 Click on the **'Volunteer'** tab above to submit your details and schedule an orientation session."
            )
        }

    # 7. Monetary Donations & Payment Methods
    if any(k in msg for k in ["money", "rupees", "upi", "qr", "bank", "account", "fund", "donate money", "paisa", "tax", "80g"]):
        return {
            "intent": "monetary_donation",
            "reply": (
                "💳 **Donations & Payment Options:**\n\n"
                "You can make secure donations directly through our website:\n"
                "• **Instant UPI / QR Code:** Scan and pay via Google Pay, PhonePe, Paytm, or BHIM.\n"
                "• **Direct Bank Transfer (NEFT/IMPS):** Official Bal Sadan trust account.\n"
                "• **In-Person Contribution:** Cash or Cheque at our Lakad Ganj office with official physical receipt.\n\n"
                "Every donation generates an **Instant Online Receipt** with a unique reference number (e.g. SKD-2026-XXXX). Click on **'Donate Now'** to contribute!"
            )
        }

    # 8. Hindi Queries
    if any(k in msg for k in ["namaste", "kaise", "bachho", "bachhe", "madad", "kya", "shukriya", "danyawad"]):
        return {
            "intent": "hindi_greeting",
            "reply": (
                "🙏 **नमस्ते! सर कस्तूरचंद डागा बाल सदन, कामठी में आपका हार्दिक स्वागत है।**\n\n"
                "हमारे यहाँ 45 अनाथ एवं जरूरतमंद बच्चों को आश्रय, उत्तम शिक्षा, संस्कार और पौष्टिक आहार दिया जाता है।\n\n"
                "• **नाश्ता/स्नैक्स दान का समय:** सोमवार से शनिवार, **दोपहर 3:00 बजे से आगे**।\n"
                "• **कार्यालय समय:** सुबह 11:00 बजे से खुला रहता है।\n"
                "• **पता:** लाकड़ गंज, कामठी, महाराष्ट्र 441001 (नागपुर के पास)।\n"
                "• **संपर्क:** 077095 58334\n\n"
                "आप बच्चों के लिए फल, पौष्टिक नाश्ता, कपड़े या स्कूल का सामान दान कर सकते हैं अथवा अपना जन्मदिन बच्चों के साथ मना सकते हैं।"
            )
        }

    # 9. Marathi Queries
    if any(k in msg for k in ["namaskar", "mula", "mulanna", "kiti", "kuthe", "madat"]):
        return {
            "intent": "marathi_greeting",
            "reply": (
                "🙏 **नमस्कार! सर कस्तूरचंद डागा बाल सदन, कामठी मध्ये आपले स्वागत आहे.**\n\n"
                "येथे ४५ अनाथांना आणि गरजू बालकांना प्रेम, शिक्षण आणि उत्तम पोषण दिले जाते.\n\n"
                "• **खाऊ/स्नॅक्स देण्याची वेळ:** सोमवार ते शनिवार, **दुपारी ३:०० वाजल्यापासून पुढे**.\n"
                "• **कार्यालय वेळ:** सकाळी ११:०० वाजता सुरू होते.\n"
                "• **पत्ता:** लाकड गंज, कामठी, महाराष्ट्र ४४१००१.\n"
                "• **फोन:** ०७७०९५ ५८३३४\n\n"
                "तुम्ही प्रत्यक्ष भेट देऊ शकता किंवा ऑनलाइन देणगी नोंदवू शकता!"
            )
        }

    # 10. General / Fallback
    return {
        "intent": "general_orphanage_help",
        "reply": (
            "Warm greetings from **Sir Kasturchand Daga Bal Sadan, Kamptee**! 🌸\n\n"
            "Here is how I can assist you today:\n"
            "1. **Snack & Refreshment Donations:** Monday to Saturday from 3:00 PM onwards.\n"
            "2. **Visiting Hours:** Office opens at 11:00 AM; child visiting window is 3:00 PM – 6:00 PM.\n"
            "3. **Address:** Lakad Ganj, Kamptee, Maharashtra 441001 (Phone: 077095 58334).\n"
            "4. **AI Snack Planner:** Ask me to plan a nutritious snack menu for your budget or child count!\n"
            "5. **Celebrate Milestones:** Cut cake and share snacks for birthdays & anniversaries.\n\n"
            "How would you like to bring a smile to our children today?"
        )
    }
