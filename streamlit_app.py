import streamlit as st
import os
from groq import Groq
from app.utils.tone_lexicon import TONE_DEFINITIONS

# Cloud ke liye API key streamlit secrets se lega, local ke liye .env se
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_default")

st.set_page_config(page_title="Email Tone Adapter", page_icon="📧", layout="wide")

TONE_OPTIONS = {
    "formal": "Formal - Professional, respectful",
    "friendly": "Friendly - Warm, approachable",
    "urgent": "Urgent - Time-sensitive, direct",
    "apologetic": "Apologetic - Sincere",
    "persuasive": "Persuasive - Convincing",
    "neutral": "Neutral - Balanced"
}

# Helper function: AI se email generate karwao
def generate_email_logic(points, recipient, sender, tone, context, length):
    client = Groq(api_key=GROQ_API_KEY)
    tone_config = TONE_DEFINITIONS.get(tone, TONE_DEFINITIONS["neutral"])
    
    sys_msg = f"You are an expert {tone} email writer. Guidelines: {tone_config['description']}. Use transitions: {', '.join(tone_config['transition_words'])}. Avoid: {', '.join(tone_config['avoid_words'])}."
    points_str = '\n'.join(f"- {p}" for p in points)
    user_msg = f"Write a {length} {tone} email.\nTo: {recipient}\nFrom: {sender}\nPoints:\n{points_str}\nContext: {context or 'None'}\n\nFormat:\nSubject: [subject]\n[Email body]"
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": user_msg}],
        max_tokens=1000, temperature=0.7
    )
    return response.choices[0].message.content

# Helper function: Tone adapt karo
def adapt_tone_logic(email_text, target_tone):
    client = Groq(api_key=GROQ_API_KEY)
    tone_config = TONE_DEFINITIONS.get(target_tone, TONE_DEFINITIONS["neutral"])
    sys_msg = f"Rewrite this email to be {target_tone}. Guidelines: {tone_config['description']}. Keep ALL facts."
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": email_text}],
        max_tokens=1000, temperature=0.7
    )
    return response.choices[0].message.content

# ---------------- UI CODE ----------------
st.title("📧 Email Tone Adaptation System")
tab1, tab2, tab3 = st.tabs(["✍️ Generate", "🔄 Compare", "🎯 Adapt"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        recipient = st.text_input("Recipient Name*")
        sender = st.text_input("Your Name*")
        selected_tone = st.selectbox("Tone*", options=list(TONE_OPTIONS.keys()), format_func=lambda x: TONE_OPTIONS[x])
        length = st.selectbox("Length", ["short", "medium", "long"])
    with col2:
        st.write("**Key Points***")
        points = []
        for i in range(4):
            p = st.text_input(f"Point {i+1}", key=f"p{i}")
            if p: points.append(p)
        context = st.text_area("Context (Optional)")

    if st.button("Generate Email", type="primary", use_container_width=True):
        if not recipient or not sender or not points:
            st.error("Fill required fields!")
        else:
            with st.spinner("Generating..."):
                try:
                    raw_text = generate_email_logic(points, recipient, sender, selected_tone, context, length)
                    subject = "No Subject"
                    if "Subject:" in raw_text:
                        parts = raw_text.split("Subject:", 1)
                        sub_parts = parts[1].split("\n", 1)
                        subject = sub_parts[0].strip()
                        body = sub_parts[1].strip() if len(sub_parts) > 1 else ""
                    else:
                        body = raw_text.strip()
                    
                    st.success("Done!")
                    st.text_input("Subject", subject)
                    st.text_area("Body", body, height=300)
                    st.metric("Words", len(body.split()))
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    r2 = st.text_input("Recipient", key="r2")
    s2 = st.text_input("Sender", key="s2")
    kp2 = st.text_area("Key Points (one per line)", key="kp2")
    tones2 = st.multiselect("Tones", options=list(TONE_OPTIONS.keys()), default=["formal", "friendly"])
    if st.button("Compare"):
        if not all([r2, s2, kp2]): st.error("Fill all")
        else:
            with st.spinner():
                try:
                    pts = [p.strip() for p in kp2.split('\n') if p.strip()]
                    cols = st.columns(len(tones2))
                    for idx, t in enumerate(tones2):
                        with cols[idx]:
                            st.subheader(t.title())
                            raw_text = generate_email_logic(pts, r2, s2, t, None, "medium")
                            if "Subject:" in raw_text:
                                parts = raw_text.split("Subject:", 1)
                                sub_parts = parts[1].split("\n", 1)
                                st.caption(f"**Sub:** {sub_parts[0].strip()}")
                                body = sub_parts[1].strip() if len(sub_parts) > 1 else ""
                            else:
                                body = raw_text.strip()
                            st.text_area("Body", body, height=400, key=f"c{t}")
                except Exception as e: st.error(str(e))

with tab3:
    txt = st.text_area("Paste email here", height=200)
    t3 = st.selectbox("Target Tone", options=list(TONE_OPTIONS.keys()), key="t3")
    if st.button("Adapt"):
        if not txt: st.error("Paste email")
        else:
            with st.spinner():
                try:
                    new_body = adapt_tone_logic(txt, t3)
                    c1, c2 = st.columns(2)
                    with c1: st.text_area("Original", txt, height=300)
                    with c2: st.text_area("Adapted", new_body, height=300)
                except Exception as e: st.error(str(e))
