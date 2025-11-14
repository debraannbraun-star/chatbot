# UbiMinds AI Adoption Challenge Assessment Chatbot
# Powered by UbiMinds - Your Consulting, Advisory and Staff Augmentation LATAM Partner
# This version uses Streamlit to make it accessible via a browser page.
# To run: pip install streamlit
# Then: streamlit run this_file.py
# Open the provided URL (e.g., http://localhost:8501) in your browser.

import streamlit as st
import os

# Load OpenAI API key from Streamlit secrets (Streamlit Cloud) or environment variable (local)
try:
    openai_api_key = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
except Exception:
    openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("⚠️ OpenAI API key not found. Set it via:\n"
               "- Local: `export OPENAI_API_KEY='sk-...'`\n"
               "- Streamlit Cloud: Settings → Secrets → add `openai_api_key = 'sk-...'`")

# Custom CSS for branding (Orange: #FF6E3D)
st.markdown("""
<style>
    .orange { color: #FF6E3D; }
    .stButton > button { background-color: #FF6E3D; color: white; }
</style>
""", unsafe_allow_html=True)

def calculate_points(responses):
    """Compute points based on responses."""
    points = {}
    
    # Organizational
    q3_map = {"Yes, fully documented and implemented": 3, "Partial (e.g., in planning)": 2, "No, but we're exploring": 1, "No": 0}
    points['q3'] = q3_map.get(responses.get('q3'), 0)
    points['q4'] = {1:1, 2:1.5, 3:2, 4:2.5, 5:3}.get(responses.get('q4'), 0)  # Reversed
    q5_map = {"Rarely": 3, "Sometimes": 2, "Often": 1, "Always": 0}
    points['q5'] = q5_map.get(responses.get('q5'), 0)
    org_sum = sum([points['q3'], points['q4'], points['q5']])
    org_norm = (org_sum / 9) * 10
    
    # Talent
    q6_map = {"None": 0, "1-10": 1, "11-50": 2, "More than 50": 3, "Unsure": 0}
    points['q6'] = q6_map.get(responses.get('q6'), 0)
    q7_map = {"Yes, major issue": 1, "Somewhat": 2, "No": 3}
    points['q7'] = q7_map.get(responses.get('q7'), 0)
    q8_map = {"Less than 5%": 1, "5-10%": 2, "Over 10%": 3, "None": 0, "Unsure": 0}
    points['q8'] = q8_map.get(responses.get('q8'), 0)
    talent_sum = sum([points['q6'], points['q7'], points['q8']])
    talent_norm = (talent_sum / 9) * 10
    
    # Technical
    q9_map = {"Yes, frequently": 1, "Occasionally": 2, "No, not yet": 3, "Haven't piloted": 0}
    points['q9'] = q9_map.get(responses.get('q9'), 0)
    points['q10'] = {1:1, 2:1.5, 3:2, 4:2.5, 5:3}.get(responses.get('q10'), 0)
    q11_map = {"Current impact": 1, "Future impact": 2, "Neither": 3, "Both": 1}
    points['q11'] = q11_map.get(responses.get('q11'), 0)
    tech_sum = sum([points['q9'], points['q10'], points['q11']])
    tech_norm = (tech_sum / 9) * 10
    
    # ROI
    q12_map = {"Yes, significant": 3, "Some": 2, "Minimal or none": 1, "Haven't measured": 0}
    points['q12'] = q12_map.get(responses.get('q12'), 0)
    q13_map = {"Very well": 3, "Adequately": 2, "Poorly": 1, "Not sure": 0}
    points['q13'] = q13_map.get(responses.get('q13'), 0)
    roi_sum = sum([points['q12'], points['q13']])
    roi_norm = (roi_sum / 6) * 10
    
    overall = (org_norm + talent_norm + tech_norm + roi_norm) / 4
    risk_level = "High Risk (Low Maturity)" if overall <= 3 else "Medium Risk (Moderate Maturity)" if overall <= 6 else "Low Risk (High Maturity)"
    
    return {
        "Organizational": org_norm,
        "Talent": talent_norm,
        "Technical": tech_norm,
        "ROI": roi_norm,
        "Overall": overall,
        "Risk Level": risk_level
    }

def tool_matching(responses):
    """Simple matching logic for AI tools."""
    core = responses.get('q14', [])
    tools = responses.get('q15', [])
    goals = responses.get('q16', [])
    
    matches = []
    if "Microsoft 365 (Office, Teams)" in core and "Automate repetitive tasks (e.g., code gen, workflows)" in goals and "Microsoft Copilot" in tools:
        matches.append("High fit for Copilot: Integrate with Teams for workflows.")
    if "Google Workspace (Docs, Sheets)" in core and "Enhance data analysis/insights" in goals and "Google Gemini" in tools:
        matches.append("High fit for Gemini: Use with Sheets for insights.")
    if "ChatGPT/OpenAI" in tools and "Custom app development" in goals:
        matches.append("Medium fit for ChatGPT: Great for prototyping via API.")
    # Add more rules as needed
    
    return matches or ["No strong matches found. Consider exploring more tools."]

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'start'
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Branded header
st.markdown('<pre style="color:#FF6E3D;">   _    \n  / \\   \n /   \\  </pre>UbiMinds', unsafe_allow_html=True)
st.write("Your Consulting, Advisory and Staff Augmentation LATAM Partner")

# Welcome
if st.session_state.current_step == 'start':
    st.markdown("<span class='orange'>Welcome to the UbiMinds AI Adoption Challenge Assessment Chatbot!</span>", unsafe_allow_html=True)
    st.write("This tool helps mid-market companies (up to 7,000 employees) evaluate AI integration challenges.")
    st.write("Answer the questions honestly. Let's begin!")
    if st.button("Start"):
        st.session_state.current_step = 'q1'
        st.rerun()

# Q1
elif st.session_state.current_step == 'q1':
    q1 = st.selectbox("Q1: How many employees does your organization have?", options=["Under 500", "500-2,000", "2,001-7,000", "Over 7,000"])
    if st.button("Submit"):
        st.session_state.responses['q1'] = q1
        if q1 == "Over 7,000":
            st.session_state.show_q1_note = True
        st.session_state.current_step = 'q2'
        st.rerun()

# Q2
elif st.session_state.current_step == 'q2':
    if 'show_q1_note' in st.session_state:
        st.write("Note: This tool is optimized for mid-market; results may vary for larger firms.")
        del st.session_state.show_q1_note
    q2 = st.selectbox("Q2: What industry best describes your organization?", options=["Tech/Software", "Manufacturing", "Healthcare", "Finance", "Retail", "Professional Services", "Other (specify)"])
    if st.button("Submit"):
        st.session_state.responses['q2'] = q2
        st.session_state.current_step = 'q3'
        st.rerun()

# Q3
elif st.session_state.current_step == 'q3':
    q3 = st.selectbox("Q3: Does your company have a formal AI strategy or roadmap?", options=["Yes, fully documented and implemented", "Partial (e.g., in planning)", "No, but we're exploring", "No"])
    if st.button("Submit"):
        st.session_state.responses['q3'] = q3
        if q3 in ["No, but we're exploring", "No"]:
            st.session_state.current_step = 'q3_follow'
        else:
            st.session_state.current_step = 'q4'
        st.rerun()

# Q3 Follow
elif st.session_state.current_step == 'q3_follow':
    q3_follow = st.selectbox("Follow-up: Is this a current barrier or one you expect in the next 1-2 years?", options=["Current", "Future", "Neither"])
    if st.button("Submit"):
        st.session_state.responses['q3_follow'] = q3_follow
        st.session_state.current_step = 'q4'
        st.rerun()

# Q4
elif st.session_state.current_step == 'q4':
    q4 = st.slider("Q4: On a scale of 1-5, how resistant is your team to adopting new AI tools (1=No resistance, 5=High resistance)?", min_value=1, max_value=5, value=3)
    if st.button("Submit"):
        st.session_state.responses['q4'] = q4
        st.session_state.current_step = 'q5'
        st.rerun()

# Q5
elif st.session_state.current_step == 'q5':
    q5 = st.selectbox("Q5: How often does bureaucracy or approval processes delay tech experiments?", options=["Rarely", "Sometimes", "Often", "Always"])
    if st.button("Submit"):
        st.session_state.responses['q5'] = q5
        st.session_state.current_step = 'q6'
        st.rerun()

# Q6
elif st.session_state.current_step == 'q6':
    q6 = st.selectbox("Q6: How many team members are trained or experienced in using AI tools?", options=["None", "1-10", "11-50", "More than 50", "Unsure"])
    if st.button("Submit"):
        st.session_state.responses['q6'] = q6
        if q6 in ["None", "1-10"]:
            st.session_state.current_step = 'q6_follow'
        else:
            st.session_state.current_step = 'q7'
        st.rerun()

# Q6 Follow
elif st.session_state.current_step == 'q6_follow':
    q6_follow = st.selectbox("Follow-up: Do you plan to hire or upskill in the next year?", options=["Yes", "No", "Maybe"])
    if st.button("Submit"):
        st.session_state.responses['q6_follow'] = q6_follow
        st.session_state.current_step = 'q7'
        st.rerun()

# Q7
elif st.session_state.current_step == 'q7':
    q7 = st.selectbox("Q7: Is finding AI-skilled talent a challenge for your organization today?", options=["Yes, major issue", "Somewhat", "No"])
    if st.button("Submit"):
        st.session_state.responses['q7'] = q7
        st.session_state.current_step = 'q8'
        st.rerun()

# Q8
elif st.session_state.current_step == 'q8':
    q8 = st.selectbox("Q8: What budget do you allocate annually for AI training/upskilling (as a % of total IT budget)?", options=["Less than 5%", "5-10%", "Over 10%", "None", "Unsure"])
    if st.button("Submit"):
        st.session_state.responses['q8'] = q8
        st.session_state.current_step = 'q9'
        st.rerun()

# Q9
elif st.session_state.current_step == 'q9':
    q9 = st.selectbox("Q9: Have you piloted AI tools and encountered issues like inaccurate outputs?", options=["Yes, frequently", "Occasionally", "No, not yet", "Haven't piloted"])
    if st.button("Submit"):
        st.session_state.responses['q9'] = q9
        if q9 == "Yes, frequently":
            st.session_state.current_step = 'q9_follow'
        else:
            st.session_state.current_step = 'q10'
        st.rerun()

# Q9 Follow
elif st.session_state.current_step == 'q9_follow':
    q9_follow = st.text_input("Follow-up: Briefly describe an example (optional):")
    if st.button("Submit"):
        st.session_state.responses['q9_follow'] = q9_follow
        st.session_state.current_step = 'q10'
        st.rerun()

# Q10
elif st.session_state.current_step == 'q10':
    q10 = st.slider("Q10: On a scale of 1-5, how prepared is your infrastructure for AI scaling (1=Not prepared, 5=Fully)?", min_value=1, max_value=5, value=3)
    if st.button("Submit"):
        st.session_state.responses['q10'] = q10
        st.session_state.current_step = 'q11'
        st.rerun()

# Q11
elif st.session_state.current_step == 'q11':
    q11 = st.selectbox("Q11: Do ethical concerns (e.g., bias in AI) impact your adoption today or in the future?", options=["Current impact", "Future impact", "Neither", "Both"])
    if st.button("Submit"):
        st.session_state.responses['q11'] = q11
        st.session_state.current_step = 'q12'
        st.rerun()

# Q12
elif st.session_state.current_step == 'q12':
    q12 = st.selectbox("Q12: Has AI integration delivered measurable ROI in your pilots?", options=["Yes, significant", "Some", "Minimal or none", "Haven't measured"])
    if st.button("Submit"):
        st.session_state.responses['q12'] = q12
        st.session_state.current_step = 'q13'
        st.rerun()

# Q13
elif st.session_state.current_step == 'q13':
    q13 = st.selectbox("Q13: How well do generic AI tools fit your specific workflows without customization?", options=["Very well", "Adequately", "Poorly", "Not sure"])
    if st.button("Submit"):
        st.session_state.responses['q13'] = q13
        st.session_state.current_step = 'q14'
        st.rerun()

# Q14
elif st.session_state.current_step == 'q14':
    core_options = ["Microsoft 365 (Office, Teams)", "Google Workspace (Docs, Sheets)", "CRM (e.g., Salesforce, HubSpot)", "ERP (e.g., SAP, Oracle)", "Custom/internal apps", "Cloud platforms (e.g., AWS, Azure)", "None yet", "Other"]
    q14 = st.multiselect("Q14: Which core systems does your tech foundation include? (Select all that apply)", options=core_options)
    if st.button("Submit"):
        st.session_state.responses['q14'] = q14
        st.session_state.current_step = 'q15'
        st.rerun()

# Q15
elif st.session_state.current_step == 'q15':
    tool_options = ["ChatGPT/OpenAI", "Microsoft Copilot", "Google Gemini", "Anthropic Claude", "xAI Grok", "None", "Other"]
    q15 = st.multiselect("Q15: Which AI tools are you already using or considering? (Select all that apply)", options=tool_options)
    if st.button("Submit"):
        st.session_state.responses['q15'] = q15
        st.session_state.current_step = 'q16'
        st.rerun()

# Q16
elif st.session_state.current_step == 'q16':
    goal_options = ["Automate repetitive tasks (e.g., code gen, workflows)", "Enhance data analysis/insights", "Improve customer support/chatbots", "Boost collaboration/productivity", "Custom app development", "Other"]
    q16 = st.multiselect("Q16: What are your primary goals for AI integration? (Select up to 3)", options=goal_options, max_selections=3)
    if st.button("Submit"):
        st.session_state.responses['q16'] = q16
        st.session_state.current_step = 'results'
        st.rerun()

# Results
elif st.session_state.current_step == 'results':
    st.markdown("<span class='orange'>Assessment Complete! Here's your personalized report from UbiMinds:</span>", unsafe_allow_html=True)
    scores = calculate_points(st.session_state.responses)
    matches = tool_matching(st.session_state.responses)
    
    st.write(f"Overall Maturity Score: {scores['Overall']:.1f}/10")
    st.write(f"Risk Level: {scores['Risk Level']}")
    st.write("\nCategory Breakdown:")
    for cat, score in scores.items():
        if cat not in ["Overall", "Risk Level"]:
            st.write(f"- {cat}: {score:.1f}/10")
    
    # Simple text radar chart
    st.write("\nText Radar Chart (Higher = Better Maturity):")
    max_bar = 10
    for cat, score in scores.items():
        if cat not in ["Overall", "Risk Level"]:
            bar = int(score) * '#' + (max_bar - int(score)) * '-'
            st.write(f"{cat.ljust(12)}: [{bar}] {score:.1f}")
    
    st.write("\nAI Tool Matches & Recommendations:")
    for match in matches:
        st.write(f"- {match}")
    
    if scores['Overall'] <= 6:
        st.write("\nTips: Focus on building an AI strategy and upskilling to reduce risks.")
    else:
        st.write("\nTips: You're in a strong position—optimize with advanced integrations.")
    
    st.markdown("<span class='orange'>Powered by UbiMinds - Your Consulting, Advisory and Staff Augmentation LATAM Partner | Visit us at https://ubiminds.com/</span>", unsafe_allow_html=True)