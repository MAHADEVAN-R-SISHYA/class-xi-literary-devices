import streamlit as st
import re
from collections import defaultdict
from textblob import TextBlob

st.set_page_config(page_title="Literary Devices Detector – Class XI", layout="wide")

# ----------------------
# School Branding
# ----------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.image("school_logo.png", width=120)
with col2:
    st.markdown("## **SISHYA SCHOOL, HOSUR**")
    st.markdown("### 📖 Literary Devices Detector & Explanation – Class XI")

st.markdown("*Understand how writers use language to create meaning* ✨")
st.markdown("---")

# ----------------------
# Input Section
# ----------------------
st.header("✍️ Enter Text (Poetry / Prose Extract)")
text = st.text_area(
    "Paste 2–6 lines from your lesson:",
    height=180,
    placeholder="Example: The wind whispered through the silent trees..."
)

analyze = st.button("🔍 Detect Literary Devices")

# ----------------------
# Helper Functions
# ----------------------
def detect_simile(t):
    return re.findall(r"\b(as|like)\b[^.]*", t, re.IGNORECASE)

def detect_metaphor(t):
    # simplistic metaphor detection: 'is a', 'was a'
    return re.findall(r"\b(is|was|are|were) a\b[^.]*", t, re.IGNORECASE)

def detect_personification(t):
    keywords = ["whispered", "laughed", "wept", "danced", "spoke", "cried", "shouted", "sang"]
    return [k for k in keywords if k in t.lower()]

def detect_hyperbole(t):
    keywords = ["thousand", "millions", "forever", "never", "always"]
    return [k for k in keywords if k in t.lower()]

def detect_oxymoron(t):
    return re.findall(r"\b(deafening silence|bitter sweet|cruel kindness)\b", t, re.IGNORECASE)

def detect_alliteration(t):
    words = re.findall(r"\b[a-zA-Z]+\b", t.lower())
    allit = []
    for i in range(len(words)-2):
        if words[i][0] == words[i+1][0] == words[i+2][0]:
            allit.append(" ".join(words[i:i+3]))
    return list(set(allit))

def detect_assonance(t):
    # simplistic: repeated vowel sounds
    vowels = 'aeiou'
    words = re.findall(r"\b[a-zA-Z]+\b", t.lower())
    vowel_words = [w for w in words if any(v in w for v in vowels)]
    return vowel_words[:5]

def detect_consonance(t):
    # simplistic: repeated consonants
    consonants = 'bcdfghjklmnpqrstvwxyz'
    words = re.findall(r"\b[a-zA-Z]+\b", t.lower())
    consonant_words = [w for w in words if any(c in w for c in consonants)]
    return consonant_words[:5]

def detect_repetition(t):
    words = re.findall(r"\b[a-zA-Z]+\b", t.lower())
    return [w for w, c in defaultdict(int, ((w, words.count(w)) for w in set(words))).items() if c > 2]

def detect_imagery(t):
    # simplistic: sensory words
    sensory_words = ["bright", "dark", "cold", "hot", "sweet", "bitter", "smooth", "loud", "silent"]
    return [w for w in sensory_words if w in t.lower()]

def detect_symbolism(t):
    symbols = ["dove", "rose", "night", "sun", "river"]
    return [w for w in symbols if w in t.lower()]

def detect_irony(t):
    keywords = ["unexpected", "contrary", "surprise", "opposite"]
    return [k for k in keywords if k in t.lower()]

# ----------------------
# Analysis Section
# ----------------------
if analyze:
    if text.strip() == "":
        st.warning("Please enter a text extract.")
    else:
        st.header("📚 Detected Literary Devices")

        results = {}
        results["Simile"] = detect_simile(text)
        results["Metaphor"] = detect_metaphor(text)
        results["Personification"] = detect_personification(text)
        results["Hyperbole"] = detect_hyperbole(text)
        results["Oxymoron"] = detect_oxymoron(text)
        results["Alliteration"] = detect_alliteration(text)
        results["Assonance"] = detect_assonance(text)
        results["Consonance"] = detect_consonance(text)
        results["Repetition"] = detect_repetition(text)
        results["Imagery"] = detect_imagery(text)
        results["Symbolism"] = detect_symbolism(text)
        results["Irony"] = detect_irony(text)

        found_any = False

        for device, items in results.items():
            if items:
                found_any = True
                with st.expander(f"🔹 {device}"):
                    for i in items:
                        st.markdown(f"• **Example:** {i}")

                    definitions = {
                        "Simile": "A simile compares two unlike things using 'like' or 'as'.",
                        "Metaphor": "A metaphor makes a direct comparison without 'like' or 'as'.",
                        "Personification": "Gives human qualities to non-living things or abstract ideas.",
                        "Hyperbole": "Deliberate exaggeration for effect.",
                        "Oxymoron": "Combining contradictory terms for effect.",
                        "Alliteration": "Repetition of initial consonant sounds.",
                        "Assonance": "Repetition of vowel sounds.",
                        "Consonance": "Repetition of consonant sounds inside or end of words.",
                        "Repetition": "Reinforces an idea by repeating words/phrases.",
                        "Imagery": "Words that appeal to the senses.",
                        "Symbolism": "Objects or words that represent deeper meanings.",
                        "Irony": "Contrast between expectation and reality."
                    }
                    st.info(definitions[device])

        if not found_any:
            st.info("No recognized literary devices detected. Try a different extract or longer text.")

        # ----------------------
        # Tone & Writing Help
        # ----------------------
        st.markdown("---")
        st.header("🧠 Writing Insight (AI Support)")

        sentiment = TextBlob(text).sentiment
        st.write(f"**Emotional Tone:** Polarity {round(sentiment.polarity,2)}")

        if sentiment.polarity > 0.2:
            st.success("The tone appears positive or hopeful.")
        elif sentiment.polarity < -0.2:
            st.warning("The tone appears serious, sad, or intense.")
        else:
            st.info("The tone appears neutral or reflective.")

        st.subheader("✏️ Exam Tip")
        st.markdown(
            "When writing answers, always **quote the line**, **name the device**, and **explain its effect** on meaning or emotion."
        )

# ----------------------
# Footer
# ----------------------
st.markdown("---")
st.caption("CBSE Class XI | English Literature | SISHYA SCHOOL, HOSUR | AI-assisted learning")
