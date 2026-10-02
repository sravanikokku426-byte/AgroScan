import json
import time
import streamlit as st
from google import genai 
from google.genai import types 
from twilio.rest import Client as TwilioClient
from prompts import SYSTEM_PROMPT,WELCOME_MESSAGE_TEMPLATE,SUMMARY_REQUEST_PROMPT
MODEL_NAME="gemini-3.8-flash"
st.set_page_config(page_title="AgroScan", page_icon=" 🌱")

GEMINI_API_KEY=st.secrets["GEMINI_API_KEY"]
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FORM = st.secrets["TWILIO_WHATSAPP_FORM"]
TWILIO_CONTENT_SID = st.secrets["TWILIO_CONTENT_SID"]

@st.cache_resource 
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)
@st.cache_resource
def get_twilio_client():
    return TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
 
 
gemini_client=get_gemini_client()
twilio_client = get_twilio_client()
def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])

 
def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])




def ask_gemini(parts):
    for attempt in range(3):
        try:
            response = st.session_state.chat.send_message(parts)
            return response.text

        except Exception as error:
            error_message = str(error)

            if "503" in error_message or "UNAVAILABLE" in error_message:
                if attempt < 2:
                    time.sleep(5)
                    continue

                return (
                    "The AI service is temporarily busy. 🌱 "
                    "Please try again in a few moments."
                )

            return f"Sorry, something went wrong: {error_message}"

 

def clean_whatsapp_text(text):
    if not text:
        return "No crops related  summary available."
    text = " ".join(text.split())  # collapse whitespace/newlines
    return text[:1500] + "..." if len(text) > 1500 else text
 


def send_whatsapp(to_number, user_name, summary):
    # Content template expects {{1}} = name, {{2}} = summary.
    try:
        content_variables = json.dumps(
            {"1": user_name, "2": clean_whatsapp_text(summary)}, ensure_ascii=False
        )
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FORM,
            to=f"whatsapp:{to_number}",
            content_sid=TWILIO_CONTENT_SID,
            content_variables=content_variables,
        )
        return True, message.sid
    except Exception as error:
        return False, str(error)


 
#onboarding

if 'onboarded' not in st.session_state:
    st.title("AgroScan 🌱")
    st.caption("🚜 Helping Farmers Detect Crop Problems with AI")
    with st.form("onboarding_form"):
        name = st.text_input("Your name")
        whatsapp_number = st.text_input(
            "WhatsApp number (with country code)",
            placeholder="+91XXXXXXXXXX",
            help="This is the number AgroScan will text you and help you"
        )
        submitted = st.form_submit_button("Let's go 🚀")
    if submitted:
        if not name.strip() or not whatsapp_number.strip():
            st.warning("please fill in both your name and whatsapp number")
        else:
            st.session_state.name=name.strip() 
            st.session_state.whatsapp_number=whatsapp_number.strip()
            #activate AI 
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            st.session_state.messages = []  #to store the user data
            st.session_state.onboarded = True
            st.rerun()
    st.stop()
#chat interface
    
header_col,button_col=st.columns([5,2],vertical_alignment="center")
with header_col:
    st.title("AgroScan 🌱")
        
with button_col:
    send_disabled = len(st.session_state.messages) <= 1
    if st.button("📤 Send to WhatsApp", disabled=send_disabled, use_container_width=True):
        with st.spinner("Summarizing your crop analysis..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_whatsapp(st.session_state.whatsapp_number, st.session_state.name, summary)
        if success:
            st.success("Sent! Check your WhatsApp 📲")
        else:
            st.error(f"Couldn't send that: {info}")
 
st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.whatsapp_number}")
 
if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)
user_input = st.chat_input(
    "Ask a question, or attach a photo of your crop",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)
if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []
    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append("Analyze this crop image. Identify the visible crop symptoms, "
        "possible pesticide-related damage, possible pests or diseases, "
        "and recommend the next step. Do not estimate pesticide concentration "
        "from the image.")
 
    with st.spinner("Analyzing your crop..."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)





