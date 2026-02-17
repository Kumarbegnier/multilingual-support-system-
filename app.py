# ==============================
# 🌍 Multilingual Support System
# ==============================

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect
import torch
from config import MONGO_URI


# ==============================
# 🔹 MongoDB Connection
# ==============================

client = MongoClient(MONGO_URI)
db = client["test"]
tickets = db["supporttickets"]

tickets.create_index("ticketNumber", unique=True)

print("✅ Connected to MongoDB Atlas")


# ==============================
# 🔹 Load Translation Model
# ==============================

model_name = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("✅ NLLB Model Loaded")


# ==============================
# 🔹 Language Mapping
# ==============================

lang_map = {
    "hi": "hin_Deva",
    "en": "eng_Latn",
    "bn": "ben_Beng",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "ml": "mal_Mlym",
    "kn": "kan_Knda",
    "gu": "guj_Gujr",
    "mr": "mar_Deva",
    "pa": "pan_Guru",
    "ur": "urd_Arab"
}


# ==============================
# 🔹 Translation Functions
# ==============================

def user_to_english(text):
    try:
        detected_lang = detect(text)
    except:
        detected_lang = "en"

    if detected_lang not in lang_map:
        detected_lang = "en"

    source_lang = lang_map.get(detected_lang, "eng_Latn")
    target_lang = "eng_Latn"

    tokenizer.src_lang = source_lang

    inputs = tokenizer(text, return_tensors="pt")

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang)
    )

    translated_text = tokenizer.batch_decode(
        translated_tokens, skip_special_tokens=True
    )[0]

    return translated_text, detected_lang


def english_to_user_lang(text, target_lang_code):

    if target_lang_code not in lang_map:
        target_lang_code = "en"

    source_lang = "eng_Latn"
    target_lang = lang_map.get(target_lang_code, "eng_Latn")

    tokenizer.src_lang = source_lang

    inputs = tokenizer(text, return_tensors="pt")

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang)
    )

    translated_text = tokenizer.batch_decode(
        translated_tokens, skip_special_tokens=True
    )[0]

    return translated_text


# ==============================
# 🔹 Ticket Utilities
# ==============================

def generate_ticket_number():
    current_year = datetime.now(timezone.utc).year

    last_ticket = tickets.find_one(
        {"ticketNumber": {"$regex": f"^TKT-{current_year}-"}},
        sort=[("ticketNumber", -1)]
    )

    if last_ticket:
        last_number = int(last_ticket["ticketNumber"].split("-")[-1])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"TKT-{current_year}-{new_number:05d}"


# ==============================
# 🔹 Create Ticket
# ==============================

def create_ticket_with_user_message(user_id, user_email, user_input):

    english_text, detected_lang = user_to_english(user_input)

    while True:
        try:
            ticket_number = generate_ticket_number()

            ticket = {
                "ticketNumber": ticket_number,
                "user": user_id,
                "subject": {
                    "raw": user_input,
                    "en": english_text,
                    "lang": detected_lang
                },
                "category": "support",
                "priority": "medium",
                "status": "open",
                "userPreferredLang": detected_lang,
                "messages": [
                    {
                        "sender": "user",
                        "senderId": user_id,
                        "senderName": user_email,
                        "lang": detected_lang,
                        "raw": user_input,
                        "en": english_text,
                        "createdAt": datetime.now(timezone.utc)
                    }
                ],
                "isDeleted": False,
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            }

            tickets.insert_one(ticket)

            print("\n✅ Support Ticket Created Successfully")
            print("Ticket Number:", ticket_number)
            print("User Raw:", user_input)
            print("Translated (English):", english_text)

            return ticket_number

        except DuplicateKeyError:
            print("Duplicate detected... retrying 🔁")
            continue


# ==============================
# 🔹 Admin Reply
# ==============================

def admin_reply_by_ticket_number():

    ticket_number = input("\nEnter Ticket Number: ").strip()
    ticket = tickets.find_one({"ticketNumber": ticket_number})

    if not ticket:
        print("❌ Ticket not found")
        return

    admin_input = input("Enter Admin Reply (English only): ")
    user_lang = ticket.get("userPreferredLang", "en")

    translated_reply = english_to_user_lang(admin_input, user_lang)

    reply_message = {
        "sender": "admin",
        "senderName": "Admin",
        "lang": "en",
        "raw": admin_input,
        "translated": translated_reply,
        "createdAt": datetime.now(timezone.utc)
    }

    tickets.update_one(
        {"ticketNumber": ticket_number},
        {
            "$push": {"messages": reply_message},
            "$set": {
                "status": "closed",
                "updatedAt": datetime.now(timezone.utc)
            }
        }
    )

    print("\n✅ Admin Reply Sent & Ticket Closed")
    print("Ticket:", ticket_number)
    print("Admin (English):", admin_input)
    print("Reply Sent To User:", translated_reply)


# ==============================
# 🔹 CLI MENU
# ==============================

def main():
    while True:

        print("\n===== SUPPORT SYSTEM =====")
        print("1. User Create Ticket")
        print("2. Admin Reply to Ticket")
        print("3. Exit")

        choice = input("Select Option: ")

        if choice == "1":
            user_input = input("\nEnter User Support Message: ")

            create_ticket_with_user_message(
                user_id="user123",
                user_email="user@test.com",
                user_input=user_input
            )

        elif choice == "2":
            admin_reply_by_ticket_number()

        elif choice == "3":
            print("🚀 System Stopped")
            break

        else:
            print("❌ Invalid Option")


if __name__ == "__main__":
    main()
