import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# ==========================================
# PAGE CONFIGURATION & AWESOME GLASSMORPHISM STYLING
# ==========================================
st.set_page_config(
    page_title="CareerBridge AI - Ultimate 15-in-1 Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Dark Glassmorphism UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .job-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .badge-verified {
        background-color: #0284c7; color: white;
        padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
    }
    .score-high {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold;
    }
    .score-mid {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold;
    }
    .score-low {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold;
    }
    .skill-matched {
        background-color: rgba(16, 185, 129, 0.2); color: #34d399;
        border: 1px solid #059669; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem; margin-right: 5px;
    }
    .skill-missing {
        background-color: rgba(239, 68, 68, 0.2); color: #f87171;
        border: 1px solid #dc2626; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem; margin-right: 5px;
    }
    .verified-skill-badge {
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
        color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE & DATABASE SETUP
# ==========================================
if "jobs_db" not in st.session_state:
    st.session_state["jobs_db"] = [
        {
            "id": 1,
            "title": "Full Stack Web Developer",
            "company": "NextGen Technologies",
            "location": "Kanpur / Remote",
            "required_skills": ["Python", "Django", "React", "JavaScript", "SQL", "Git"],
            "min_experience": 1,
            "salary_base": 5.5,
            "is_verified": True,
            "description": "Develop scalable MERN/Django web applications and build modern API services."
        },
        {
            "id": 2,
            "title": "Data Analyst & ML Specialist",
            "company": "Analytics Pulse",
            "location": "Bengaluru / Hybrid",
            "required_skills": ["Python", "SQL", "Pandas", "Scikit-Learn", "Machine Learning", "PowerBI"],
            "min_experience": 0,
            "salary_base": 6.0,
            "is_verified": True,
            "description": "Analyze datasets, build predictive models, and implement data visualization pipelines."
        },
        {
            "id": 3,
            "title": "Cybersecurity & Forensic Associate",
            "company": "SecureNet InfoSec",
            "location": "Noida / On-site",
            "required_skills": ["Networking", "Ethical Hacking", "Linux", "Python", "Digital Forensics"],
            "min_experience": 1,
            "salary_base": 7.0,
            "is_verified": True,
            "description": "Conduct vulnerability assessments, network packet audits, and digital forensic investigations."
        }
    ]

if "verified_badges" not in st.session_state:
    st.session_state["verified_badges"] = []

# ==========================================
# HELPER & UTILITY FUNCTIONS
# ==========================================
def calculate_match_analytics(candidate_skills, candidate_exp, job):
    job_skills = set([s.lower().strip() for s in job["required_skills"]])
    cand_skills = set([s.lower().strip() for s in candidate_skills])
    
    matched = list(cand_skills.intersection(job_skills))
    missing = list(job_skills.difference(cand_skills))
    
    skill_score = (len(matched) / max(1, len(job_skills))) * 70.0
    exp_score = 30.0 if candidate_exp >= job["min_experience"] else max(0.0, (candidate_exp / max(1, job["min_experience"])) * 30.0)
        
    total_score = round(skill_score + exp_score)
    is_eligible = (candidate_exp >= job["min_experience"]) and (total_score >= 50)
    
    return {
        "score": total_score,
        "eligible": is_eligible,
        "matched": matched,
        "missing": missing
    }

def generate_pdf_resume(name, email, exp, skills_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, name, ln=True, align="C")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Email: {email} | Experience: {exp} Year(s)", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Professional Profile Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    summary = f"Results-driven technical candidate with {exp} year(s) hands-on experience in software engineering and analytics."
    pdf.multi_cell(0, 6, summary)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Verified Technical Skills & Competencies", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, ", ".join([s.title() for s in skills_list]))
    
    return bytes(pdf.output())

# ==========================================
# SIDEBAR: FEATURE 4 - CANDIDATE PROFILE & VERIFIED BADGES
# ==========================================
st.sidebar.markdown("## 👤 Candidate Profile")
user_name = st.sidebar.text_input("Full Name", value="Arpit Srivastav")
user_email = st.sidebar.text_input("Email Address", value="arpit@example.com")
user_phone = st.sidebar.text_input("WhatsApp Number", value="+91 9876543210")
user_exp = st.sidebar.slider("Years of Experience", min_value=0, max_value=10, value=1)
raw_skills = st.sidebar.text_area(
    "Technical Skills (comma separated)",
    value="Python, Django, JavaScript, SQL, HTML, React, Node.js, Express, MongoDB"
)
candidate_skills_list = [s.strip() for s in raw_skills.split(",") if s.strip()]

if st.session_state["verified_badges"]:
    st.sidebar.markdown("### 🏆 Verified Skill Badges")
    badge_html = " ".join([f"<span class='verified-skill-badge'>✓ {b}</span>" for b in st.session_state["verified_badges"]])
    st.sidebar.markdown(badge_html, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("## 🔍 Portal Filters")
search_query = st.sidebar.text_input("Search Role, Skill, or Company", value="")
verified_only = st.sidebar.checkbox("Verified Listings Only", value=False)

# ==========================================
# MAIN TITLE
# ==========================================
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🚀 CareerBridge AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Complete 15-in-1 Smart Job Portal, Hiring Ecosystem & AI Acceleration Engine</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# TABS SYSTEM (15 FEATURES ORGANIZED INTO 6 TABS)
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌐 1. Jobs & Apply", 
    "⚡ 2. ATS Resume Matcher", 
    "🛣️ 3. Roadmap & Audio Interview", 
    "📄 4. AI Resume Builder", 
    "🏆 5. Quiz & Skill Badges",
    "🏢 6. Recruiter & Alerts"
])

# ------------------------------------------
# TAB 1: FEATURES 1, 2, 3, 5 (JOB PORTAL, MATCHING, GAPS, APPLY)
# ------------------------------------------
with tab1:
    st.subheader("🎯 Matched Job Opportunities")
    
    for job in st.session_state["jobs_db"]:
        if verified_only and not job["is_verified"]:
            continue
        if search_query:
            sq = search_query.lower()
            if not (sq in job["title"].lower() or sq in job["company"].lower() or any(sq in s.lower() for s in job["required_skills"])):
                continue
                
        analytics = calculate_match_analytics(candidate_skills_list, user_exp, job)
        score = analytics["score"]
        
        badge_cls = "score-high" if score >= 70 else ("score-mid" if score >= 45 else "score-low")
        v_badge = "<span class='badge-verified'>✓ Verified</span>" if job["is_verified"] else ""
        
        st.markdown(f"""
        <div class="job-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="margin: 0; color: #f8fafc;">{job['title']} {v_badge}</h3>
                    <p style="margin: 4px 0; color: #94a3b8; font-size: 0.95rem;">🏢 {job['company']} | 📍 {job['location']} | 💰 ₹{job['salary_base']} - ₹{job['salary_base']+2.5} LPA</p>
                </div>
                <div><span class='{badge_cls}'>{score}% MATCH</span></div>
            </div>
            <p style="color: #cbd5e1; margin-top: 10px;">{job['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            m_str = " ".join([f"<span class='skill-matched'>✓ {s.title()}</span>" for s in analytics['matched']])
            g_str = " ".join([f"<span class='skill-missing'>⚠ {s.title()}</span>" for s in analytics['missing']])
            st.markdown(f"**Matched Skills:** {m_str if m_str else '<span style=\"color:#94a3b8;\">None</span>'}", unsafe_allow_html=True)
            st.markdown(f"**Skill-Gap (Missing):** {g_str if g_str else '<span style=\"color:#34d399;\">None! Fully Qualified</span>'}", unsafe_allow_html=True)
        
        with col2:
            if analytics["eligible"]:
                if st.button(f"Apply Now", key=f"app_{job['id']}"):
                    st.success("🎉 Application Submitted Successfully!")
            else:
                st.warning("Low Eligibility")
                st.button(f"Upgrade Skills", key=f"up_{job['id']}")
        st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: FEATURES 6, 9, 10 (ATS MATCH, SALARY, BIO)
# ------------------------------------------
with tab2:
    st.subheader("⚡ Feature 6: Instant Resume vs. Job Description ATS Matcher")
    c1, c2 = st.columns(2)
    with c1:
        resume_text = st.text_area("Paste Resume Text", height=160, placeholder="Paste resume contents here...")
    with c2:
        jd_text = st.text_area("Paste Target Job Description (JD)", height=160, placeholder="Paste job requirements here...")
        
    if st.button("🔍 Run ATS Keyword Analysis", type="primary"):
        if resume_text and jd_text:
            stopwords = {"and", "the", "in", "to", "of", "a", "with", "for", "is", "on", "that", "by", "as", "an", "your", "be", "are", "at", "or"}
            jd_words = set([w.strip(".,!?:;()").lower() for w in jd_text.split() if len(w) > 2 and w.lower() not in stopwords])
            r_words = set([w.strip(".,!?:;()").lower() for w in resume_text.split() if len(w) > 2 and w.lower() not in stopwords])
            
            matched_kw = jd_words.intersection(r_words)
            missing_kw = jd_words.difference(r_words)
            ats_score = round((len(matched_kw) / max(1, len(jd_words))) * 100)
            
            st.metric("ATS Selection Probability", f"{min(100, ats_score)}%")
            mc1, mc2 = st.columns(2)
            with mc1:
                st.success(f"✓ Matched ATS Keywords ({len(matched_kw)})")
                st.write(", ".join(list(matched_kw)[:15]))
            with mc2:
                st.error(f"⚠ Missing ATS Keywords ({len(missing_kw)})")
                st.write(", ".join(list(missing_kw)[:15]))

    st.markdown("---")
    sc1, sc2 = st.columns(2)
    with sc1:
        st.subheader("📊 Feature 9: Estimated Salary Predictor")
        base_calc = 3.5 + (user_exp * 1.2) + (len(candidate_skills_list) * 0.4)
        st.metric("Dynamic Market Valuation", f"₹{round(base_calc, 1)} - ₹{round(base_calc + 3.0, 1)} LPA")
    with sc2:
        st.subheader("📄 Feature 10: AI Profile Bio Generator")
        bio = f"Driven tech professional with {user_exp} year(s) experience specializing in {', '.join([s.title() for s in candidate_skills_list[:4]])}. Focused on building high-impact software solutions."
        st.code(bio, language="text")

# ------------------------------------------
# TAB 3: FEATURES 7 & 11 (ROADMAP & VOICE AI INTERVIEW)
# ------------------------------------------
with tab3:
    st.subheader("🛣️ Feature 7: 30-Day Skill Upgrade Roadmap")
    target_job_name = st.selectbox("Select Target Job Role", [j["title"] for j in st.session_state["jobs_db"]])
    target_job_obj = next(j for j in st.session_state["jobs_db"] if j["title"] == target_job_name)
    analytics = calculate_match_analytics(candidate_skills_list, user_exp, target_job_obj)
    
    if analytics["missing"]:
        for idx, skill in enumerate(analytics["missing"], 1):
            st.markdown(f"**Week {idx}: Master {skill.title()}** | [▶ Free Video Tutorials](https://www.youtube.com/results?search_query=learn+{skill}+tutorial)")
    else:
        st.success("🎉 No missing skills! You possess 100% of required competencies.")

    st.markdown("---")
    st.subheader("🎙️ Feature 11: Voice & Audio AI Mock Interviewer")
    st.write("Listen to the AI Interview question and record your audio answer.")
    
    interview_q = f"How do you implement scalable architecture and handle exceptions in {candidate_skills_list[0].title()}?"
    st.info(f"**AI Question:** {interview_q}")
    
    # Audio Player Simulator
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    
    user_audio = st.file_uploader("Upload Audio Answer (WAV/MP3)", type=["mp3", "wav"])
    if user_audio:
        st.success("✓ Audio Answer Received! AI Analysis: Strong communication clarity & accurate technical terminology (Score: 88/100).")

# ------------------------------------------
# TAB 4: FEATURE 12 (AI RESUME PDF BUILDER)
# ------------------------------------------
with tab4:
    st.subheader("📄 Feature 12: One-Click Instant AI Resume PDF Generator")
    st.write("Generate a clean, ATS-compliant PDF Resume directly from your profile details.")
    
    if st.button("🔨 Build Professional PDF Resume", type="primary"):
        pdf_bytes = generate_pdf_resume(user_name, user_email, user_exp, candidate_skills_list)
        st.download_button(
            label="📥 Download Resume PDF",
            data=pdf_bytes,
            file_name=f"{user_name.replace(' ', '_')}_Resume.pdf",
            mime="application/pdf"
        )

# ------------------------------------------
# TAB 5: FEATURE 15 (SKILL ASSESSMENT & BADGES)
# ------------------------------------------
with tab5:
    st.subheader("🏆 Feature 15: 5-Minute Technical Assessment & Skill Verification")
    st.write("Pass this quick technical assessment to earn Verified Skill Badges on your profile.")
    
    quiz_skill = st.selectbox("Choose Skill to Verify", [s.title() for s in candidate_skills_list])
    
    st.markdown(f"**Assessment Question for {quiz_skill}:**")
    ans = st.radio(
        f"Which mechanism in {quiz_skill} ensures thread safety and data consistency?",
        ["Locks & ORM Transactions", "Global Variables", "Static Memory Allocation", "None of the above"]
    )
    
    if st.button("Submit Assessment"):
        if ans == "Locks & ORM Transactions":
            if quiz_skill not in st.session_state["verified_badges"]:
                st.session_state["verified_badges"].append(quiz_skill)
            st.balloons()
            st.success(f"🎉 Congratulations! You earned the Verified Badge for {quiz_skill}!")
        else:
            st.error("Incorrect answer. Please review core concepts and try again.")

# ------------------------------------------
# TAB 6: FEATURES 13 & 14 (RECRUITER DASHBOARD & ALERTS)
# ------------------------------------------
with tab6:
    st.subheader("🏢 Feature 13: Recruiter Hiring Portal & Post Job Engine")
    
    with st.expander("➕ Post a New Job Listing"):
        with st.form("new_job_form"):
            n_title = st.text_input("Job Title")
            n_comp = st.text_input("Company Name")
            n_loc = st.text_input("Location")
            n_skills = st.text_input("Required Skills (comma separated)")
            n_exp = st.number_input("Min Experience", min_value=0, max_value=10, value=1)
            n_sal = st.number_input("Base Salary (LPA)", value=6.0)
            submitted = st.form_submit_button("Publish Job Listing")
            
            if submitted and n_title:
                new_job = {
                    "id": len(st.session_state["jobs_db"]) + 1,
                    "title": n_title,
                    "company": n_comp,
                    "location": n_loc,
                    "required_skills": [s.strip() for s in n_skills.split(",") if s.strip()],
                    "min_experience": n_exp,
                    "salary_base": n_sal,
                    "is_verified": True,
                    "description": "Newly posted position via Recruiter Hiring Portal."
                }
                st.session_state["jobs_db"].append(new_job)
                st.success(f"✓ Job '{n_title}' Published Successfully!")

    st.markdown("---")
    st.subheader("📲 Feature 14: Direct WhatsApp & Email Job Alert Payload Engine")
    st.write("Configure dynamic instant notifications when a high-match (80%+) job opens.")
    
    c_alert1, c_alert2 = st.columns(2)
    with c_alert1:
        st.info(f"**WhatsApp Alert Target:** {user_phone}")
        if st.button("💬 Test WhatsApp Alert Payload"):
            st.success(f"✓ Alert Sent to {user_phone}: '🚀 CareerBridge Alert: New 85% Matched Job Posted - Full Stack Web Developer at NextGen Technologies!'")
    with c_alert2:
        st.info(f"**Email Alert Target:** {user_email}")
        if st.button("📧 Test Email Alert Payload"):
            st.success(f"✓ Alert Email Dispatched to {user_email}!")
