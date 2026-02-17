# ==========================================
# 🌍 Translation Service (NLLB + LangDetect)
# ==========================================

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect
import torch


# ==========================================
# 🔹 Load Model (Singleton Style)
# ==========================================

MODEL_NAME = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("✅ Translation Model Loaded")


# ==========================================
# 🔹 Language Mapping
# ==========================================

LANG_MAP = {
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


# ==========================================
# 🔹 Internal Translate Function
# ==========================================

def _translate(text, source_lang, target_lang):

    tokenizer.src_lang = source_lang

    inputs = tokenizer(text, return_tensors="pt")

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang)
    )

    return tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]


# ==========================================
# 🔹 User → English
# ==========================================

def user_to_english(text):

    try:
        detected_lang = detect(text)
    except:
        detected_lang = "en"

    if detected_lang not in LANG_MAP:
        detected_lang = "en"

    source_lang = LANG_MAP.get(detected_lang, "eng_Latn")
    target_lang = "eng_Latn"

    translated_text = _translate(text, source_lang, target_lang)

    return translated_text, detected_lang


# ==========================================
# 🔹 English → User
