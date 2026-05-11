import streamlit as st  # type: ignore[import-not-found]
import requests  # type: ignore[import-not-found]

st.set_page_config(page_title="Email Tone Adapter", page_icon="📧", layout="wide")
API_URL = "http://localhost:8000/api/v1"

TONE_OPTIONS = {
    "formal": "Formal - Professional, respectful",
    "friendly": "Friendly - Warm, approachable",
    "urgent": "Urgent - Time-sensitive, direct",
    "apologetic": "Apologetic - Sincere",
    "persuasive": "Persuasive - Convincing",
    "neutral": "Neutral - Balanced"
}

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
                    payload = {"key_points": points, "recipient": recipient, "sender_name": sender, "tone": selected_tone, "context": context, "email_length": length, "include_subject": True}
                    res = requests.post(f"{API_URL}/generate", json=payload)
                    result = res.json()
                    st.success("Done!")
                    if result.get("subject"): st.text_input("Subject", result["subject"])
                    st.text_area("Body", result["body"], height=300)
                    st.metric("Words", result["word_count"])
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
                    res = requests.post(f"{API_URL}/generate/batch", json={"key_points": pts, "recipient": r2, "sender_name": s2, "tones": tones2})
                    result = res.json()
                    cols = st.columns(len(tones2))
                    for idx, t in enumerate(tones2):
                        with cols[idx]:
                            st.subheader(t.title())
                            em = result["emails"].get(t, {})
                            if em.get("subject"): st.caption(f"**Sub:** {em['subject']}")
                            st.text_area("Body", em.get("body",""), height=400, key=f"c{t}")
                except Exception as e: st.error(str(e))

with tab3:
    txt = st.text_area("Paste email here", height=200)
    t3 = st.selectbox("Target Tone", options=list(TONE_OPTIONS.keys()), key="t3")
    if st.button("Adapt"):
        if not txt: st.error("Paste email")
        else:
            with st.spinner():
                try:
                    res = requests.post(f"{API_URL}/adapt-tone", json={"email_text": txt, "target_tone": t3})
                    r = res.json()
                    c1, c2 = st.columns(2)
                    with c1: st.text_area("Original", txt, height=300)
                    with c2: st.text_area("Adapted", r["body"], height=300)
                except Exception as e: st.error(str(e))