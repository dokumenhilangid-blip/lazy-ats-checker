import streamlit as st
import nltk
from nltk.corpus import stopwords
import string
import collections

# Ensure stopwords are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def get_keywords(text):
    """
    Tokenizes text, removes punctuation and stopwords, and returns a set of unique keywords.
    """
    if not text:
        return set()
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    # Tokenize (split by whitespace)
    tokens = text.split()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    keywords = {word for word in tokens if word not in stop_words}
    
    return keywords

def calculate_match_score(jd_keywords, resume_keywords):
    """
    Calculates the percentage of JD keywords present in the resume.
    """
    if not jd_keywords:
        return 0.0, set()
    
    intersection = jd_keywords.intersection(resume_keywords)
    score = (len(intersection) / len(jd_keywords)) * 100
    missing_keywords = jd_keywords - resume_keywords
    
    return score, missing_keywords

# Streamlit Page Config
st.set_page_config(page_title="The Lazy ATS Checker", layout="wide", page_icon="🕵️")

# Custom CSS for Hacker Style
st.markdown("""
<style>
    /* Dark Mode Background */
    .stApp {
        background-color: #0e0e0e;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Input Text Areas */
    .stTextArea textarea {
        background-color: #1c1c1c;
        color: #00ff00;
        border: 1px solid #333;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00ff00 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #333;
        color: #00ff00;
        border: 1px solid #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button:hover {
        background-color: #00ff00;
        color: #000;
    }
    
    /* Success/Error Messages */
    .success-msg {
        color: #00ff00;
        font-weight: bold;
    }
    .error-msg {
        color: #ff0000;
        font-weight: bold;
    }
    
    /* Missing Keywords */
    .missing-keyword {
        color: #ff4b4b;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# App Title
st.title("🕵️ The Lazy ATS Checker")
st.markdown("### Hack the system. Get the interview.")

# Input Section
col1, col2 = st.columns(2)

with col1:
    jd_text = st.text_area("Paste Job Description Here", height=300)

with col2:
    resume_text = st.text_area("Paste Your Resume Text Here", height=300)

# Logic Execution
if st.button("Check Match"):
    if not jd_text or not resume_text:
        st.error("Please provide both Job Description and Resume text.")
    else:
        # Process Texts
        jd_keywords = get_keywords(jd_text)
        resume_keywords = get_keywords(resume_text)
        
        # Calculate Score
        score, missing_keywords = calculate_match_score(jd_keywords, resume_keywords)
        
        # Display Results
        st.divider()
        st.markdown(f"## Match Score: {score:.1f}%")
        
        # Display Missing Keywords
        if missing_keywords:
            st.markdown("### Missing Keywords:")
            st.markdown(f'<span class="missing-keyword">{", ".join(sorted(missing_keywords))}</span>', unsafe_allow_html=True)
        else:
            st.success("Perfect Match! You have all the keywords.")
            
        st.divider()
        
        # The Money Shot (Call to Action)
        if score < 80:
            st.markdown("### ⚠️ WARNING: Low Match Score")
            st.markdown("Your resume is likely to be rejected by the ATS.")
            st.markdown("🔥 **Fix your resume instantly with The Lazy Engineer's Pack**")
            st.link_button("Get The Pack Now", "https://careeronfire.gumroad.com/l/hiwih") # Placeholder link
        else:
            st.markdown("### ✅ Great job!")
            st.markdown("You are ready to beat the bots.")
            st.markdown("Want to prep for the interview? Check my other tools.")
            st.link_button("Check Other Tools", "https://careeronfire.gumroad.com/") # Placeholder link
