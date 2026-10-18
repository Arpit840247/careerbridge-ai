import streamlit as st
import pandas as pd
import time
from fpdf import FPDF

# ==========================================
# PAGE CONFIGURATION & LIGHT PROFESSIONAL STYLING
# ==========================================
st.set_page_config(
    page_title="CareerBridge AI - End-to-End Career Acceleration Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Light Theme Styling (Slate White, Border Navy, Electric Blue Accent)
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .light-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }
    
    .badge-verified {
        background-color: #0284c7; color: #ffffff;
        padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
    }
    
    .badge-govt {
        background-color: #d97706; color: #ffffff;
        padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
    }

    .score-badge {
        background-color: #059669; color: #ffffff;
        padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.9rem;
    }

    .pill-match {
        background-color: #dcfce7; color: #15803d;
        border: 1px solid #bbf7d0; padding: 4px 10px; border-radius: 12px; font-size: 0.82rem; font-weight: 600; margin-right: 6px;
    }

    .pill-missing {
        background-color: #fee2e2; color: #b91c1c;
        border: 1px solid #fecaca; padding: 4px 10px; border-radius: 12px; font-size: 0.82rem; font-weight: 600; margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# STATE INITIALIZATION
# ==========================================
if "role" not in st.session_state:
    st.session_state["role"] = "Job Seeker"  # Job Seeker OR Recruiter
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Arpit Srivastav"
if "user_skills" not in st.session_state:
    st.session_state["user_skills"] = ["python", "django", "sql", "react", "javascript"]
if "user_exp" not in st.session_state:
    st.session_state["user_exp"] = 0
if "interview_history" not in st.session_state:
    st.session_state["interview_history"] = []
if "learning_loop" not in st.session_state:
    st.session_state["learning_loop"] = ["Focus on Django REST Framework exception handling", "Practice SQL Window Functions"]

if "jobs_database" not in st.session_state:
    st.session_state["jobs_database"] = [
        {
            "id": 1, "title": "Software Engineer (BCA/BSc Freshers)", "company": "NextGen Technologies",
            "location": "Kanpur / Remote", "required": ["python", "django", "react", "sql"],
            "min_exp": 0, "salary": "₹3.5 - ₹5.5 LPA", "verified": True, "type": "Private",
            "official_url": "", "desc": "Entry-level full stack role for fresh BCA/BSc/BCom graduates."
        },
        {
            "id": 2, "title": "National Apprenticeship Training Scheme (NATS)", "company": "Ministry of Education / Public Sector",
            "location": "Prayagraj / Uttar Pradesh", "required": ["python", "sql", "basics"],
            "min_exp": 0, "salary": "Stipend: ₹12,000/month", "verified": True, "type": "Government",
            "official_url": "https://nats.education.gov.in/", "desc": "Official Government Apprenticeship drive for graduate trainees."
        },
        {
            "id": 3, "title": "Data Analyst Trainee", "company": "Analytics Pulse",
            "location": "Bengaluru / Hybrid", "required": ["python", "sql", "excel", "pandas"],
            "min_exp": 0, "salary": "₹4.0 - ₹6.0 LPA", "verified": True, "type": "Private",
            "official_url": "", "desc": "Analyze data distributions, clean datasets, and build decision dashboards."
        }
    ]

# PDF Resume Generator Utility
def generate_clean_pdf(name, skills_list, exp):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, name, ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Fresher / Experience: {exp} Year(s)", ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Core Competencies", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, ", ".join([s.title() for s in skills_list]))
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Profile Summary", ln=True)
    pdf.set_font("Helvetica", "", 10)
    summary = f"Entry-level technology candidate possessing foundational proficiency in {', '.join([s.title() for s in skills_list[:3]])}. Evaluated objectively via CareerBridge AI."
    pdf.multi_cell(0, 6, summary)
    return bytes(pdf.output())

# ==========================================
# TOP HEADER & AUTHENTICATION
# ==========================================
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown("<h1 style='margin:0; color:#0284c7;'>🚀 CareerBridge AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; margin:0;'>End-to-End Placement Acceleration Engine for Indian Freshers & Graduates</p>", unsafe_allow_html=True)
with col_h2:
    role_choice = st.selectbox("Switch View", ["Job Seeker", "Verified Recruiter"])
    st.session_state["role"] = role_choice

st.markdown("---")

# ==========================================
# VIEW 1: JOB SEEKER EXPERIENCE
# ==========================================
if st.session_state["role"] == "Job Seeker":
    
    st.sidebar.markdown("## 👤 Candidate Profile")
    st.session_state["user_name"] = st.sidebar.text_input("Full Name", value=st.session_state["user_name"])
    st.session_state["user_exp"] = st.sidebar.slider("Experience Years", 0, 5, st.session_state["user_exp"])
    skills_input = st.sidebar.text_area("Your Skills Stack", value=", ".join([s.title() for s in st.session_state["user_skills"]]))
    if st.sidebar.button("Update Skills"):
        st.session_state["user_skills"] = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
        st.sidebar.success("Profile Updated!")
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔁 Learning Outcome Loop")
    for item in st.session_state["learning_loop"]:
        st.sidebar.info(f"💡 {item}")

    t1, t2, t3, t4 = st.tabs([
        "🌐 1. Verified Opportunities & Govt Vacancies", 
        "🎙️ 2. Ethical AI Mock Interview", 
        "📄 3. ATS Resume & Preparation", 
        "📈 4. Outcome Loop & Progress"
    ])

    # ------------------------------------------
    # TAB 1: OPPORTUNITIES & RESPONSIBLE APPLY
    # ------------------------------------------
    with t1:
        st.subheader("🎯 Verified Freshers & Apprenticeships Feed")
        search_kw = st.text_input("🔍 Search by role, skill, or company...", "")
        
        for job in st.session_state["jobs_database"]:
            if search_kw:
                skw = search_kw.lower()
                if not (skw in job["title"].lower() or skw in job["company"].lower() or any(skw in s for s in job["required"])):
                    continue
            
            job_req = set(job["required"])
            user_s = set(st.session_state["user_skills"])
            matched = job_req.intersection(user_s)
            missing = job_req.difference(user_s)
            
            score = round((len(matched) / max(1, len(job_req))) * 70 + (30 if st.session_state["user_exp"] >= job["min_exp"] else 15))
            
            badge_html = "<span class='badge-govt'>🏛️ Official Govt Listing</span>" if job["type"] == "Government" else "<span class='badge-verified'>✓ Employer Verified</span>"
            
            st.markdown(f"""
            <div class="light-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin:0; color:#0f172a;">{job['title']} {badge_html}</h3>
                        <p style="color:#64748b; margin:4px 0;">🏢 {job['company']} &nbsp;|&nbsp; 📍 {job['location']} &nbsp;|&nbsp; 💰 {job['salary']}</p>
                    </div>
                    <div><span class="score-badge">{score}% MATCH</span></div>
                </div>
                <p style="color:#334155; margin-top:10px;">{job['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c_left, c_right = st.columns([3, 1])
            with c_left:
                m_pills = " ".join([f"<span class='pill-match'>✓ {s.title()}</span>" for s in matched])
                g_pills = " ".join([f"<span class='pill-missing'>⚠ {s.title()}</span>" for s in missing])
                st.markdown(f"**Matched Skills:** {m_pills if m_pills else 'None'}", unsafe_allow_html=True)
                st.markdown(f"**Skill Gap:** {g_pills if g_pills else 'None - Fully Qualified!'}", unsafe_allow_html=True)
            with c_right:
                if job["type"] == "Government":
                    st.markdown(f"[🔗 Apply on Official Portal]({job['official_url']})")
                    st.caption("Preserves official government portal requirements.")
                else:
                    if st.button(f"Review & Apply", key=f"job_{job['id']}", type="primary"):
                        st.info("ℹ️ Final Confirmation: CareerBridge never bypasses portal consent or CAPTCHAs without explicit candidate authorization.")
                        st.success(f"Application payload submitted to {job['company']}!")
            st.markdown("<hr style='border: 0.5px solid #e2e8f0;'>", unsafe_allow_html=True)

    # ------------------------------------------
    # TAB 2: ETHICAL AI MOCK INTERVIEW
    # ------------------------------------------
    with t2:
        st.subheader("🎙️ Ethical AI Technical Interview Simulator")
        st.info("🛡️ **Fairness Commitment:** Evaluation is strictly focused on **answer relevance, structural clarity, and technical correctness**. CareerBridge AI does NOT use pseudo-scientific eye-tracking, facial expression analysis, or accent profiling.")
        
        target_role = st.selectbox("Select Target Interview Domain", ["Full Stack Developer", "Data Analyst Trainee"])
        
        q_bank = {
            "Full Stack Developer": "How do you optimize state management in React and handle exceptions in Django ORM endpoints under concurrency?",
            "Data Analyst Trainee": "How do you handle missing values in SQL queries using window functions and imputation in Pandas?"
        }
        
        current_q = q_bank[target_role]
        st.markdown(f"### ❓ Question: {current_q}")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        st.caption("🔊 Question audio player & timer active (2 Minutes recommended).")
        
        user_answer = st.text_area("Type or Paste Response Transcription:", height=140, placeholder="Structure: 1. Core Concept, 2. Implementation Pattern, 3. Optimization...")
        
        if st.button("Submit Response for Objective Evaluation", type="primary"):
            if not user_answer or len(user_answer) < 25:
                st.warning("Please enter a technical response for objective evaluation.")
            else:
                with st.spinner("Evaluating technical correctness and response structure..."):
                    time.sleep(1.2)
                    
                words = set(user_answer.lower().split())
                tech_keywords = {"state", "api", "django", "orm", "database", "sql", "pandas", "async", "react", "python"}
                found = words.intersection(tech_keywords)
                
                rel_score = min(100, len(found) * 20 + 20)
                struct_score = 85 if ("1." in user_answer or "first" in user_answer.lower() or len(user_answer) > 120) else 65
                tech_score = min(95, rel_score + 10)
                overall = round((rel_score + struct_score + tech_score) / 3)
                
                st.markdown("### 📊 Objective Feedback Matrix")
                f1, f2, f3, f4 = st.columns(4)
                f1.metric("Overall Match", f"{overall}%")
                f2.metric("Relevance", f"{rel_score}%")
                f3.metric("Structure", f"{struct_score}%")
                f4.metric("Technical Score", f"{tech_score}%")
                
                st.success("**Strengths Identified:** Clear technical vocabulary and structured problem-solving approach.")
                st.warning(f"**Dynamic Follow-up Question:** You mentioned technical implementation—how do you verify memory efficiency in production?")
                
                # Feedback outcome loop update
                st.session_state["learning_loop"].append(f"Review technical depth for {target_role} (Score: {overall}%)")
                st.session_state["interview_history"].append({
                    "date": time.strftime("%Y-%m-%d %H:%M"), "role": target_role, "score": overall
                })

    # ------------------------------------------
    # TAB 3: ATS RESUME & PREPARATION
    # ------------------------------------------
    with t3:
        st.subheader("📄 ATS Keyword Analyzer & Resume Support")
        
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            res_text = st.text_area("Paste Resume Text", height=160, placeholder="Paste resume contents...")
        with c_r2:
            jd_text = st.text_area("Paste Target Job Description (JD)", height=160, placeholder="Paste JD requirements...")
            
        if st.button("Run ATS Match", type="primary"):
            if res_text and jd_text:
                r_words = set([w.strip(".,!?:;()").lower() for w in res_text.split() if len(w) > 2])
                j_words = set([w.strip(".,!?:;()").lower() for w in jd_text.split() if len(w) > 2])
                matched_kw = j_words.intersection(r_words)
                missing_kw = j_words.difference(r_words)
                ats_score = round((len(matched_kw) / max(1, len(j_words))) * 100)
                
                st.metric("ATS Selection Probability", f"{min(100, ats_score)}%")
                st.write("**Matched Keywords:**", ", ".join(list(matched_kw)[:12]))
                st.write("**Missing Keywords:**", ", ".join(list(missing_kw)[:12]))
                
        st.markdown("---")
        st.subheader("🛠️ Download ATS-Compliant PDF Resume")
        if st.button("Generate Resume PDF"):
            pdf_bytes = generate_clean_pdf(st.session_state["user_name"], st.session_state["user_skills"], st.session_state["user_exp"])
            st.download_button(
                label="📥 Download PDF", data=pdf_bytes, file_name=f"{st.session_state['user_name'].replace(' ', '_')}_Resume.pdf", mime="application/pdf"
            )

    # ------------------------------------------
    # TAB 4: OUTCOME LOOP & HISTORY
    # ------------------------------------------
    with t4:
        st.subheader("📈 Interview Outcomes & Recommendation Tracking")
        if not st.session_state["interview_history"]:
            st.info("No mock interviews completed yet. Complete a session in Tab 2 to activate tracking.")
        else:
            df_hist = pd.DataFrame(st.session_state["interview_history"])
            st.dataframe(df_hist, use_container_width=True)
            st.line_chart(df_hist.set_index("date")["score"])

# ==========================================
# VIEW 2: VERIFIED RECRUITER PORTAL
# ==========================================
else:
    st.subheader("🏢 Verified Employer & Recruiter Control Panel")
    st.info("🛡️ Identity Verification: Recruiter profiles and job listings are moderated to protect candidates from fraudulent offerings.")
    
    rt1, rt2, rt3 = st.tabs(["➕ Post Verified Job", "📋 Candidate Pipeline & Shortlisting", "📊 Recruitment Analytics"])
    
    with rt1:
        st.markdown("### Post a New Opening")
        with st.form("post_job"):
            p_title = st.text_input("Job Title", value="Junior Python Developer")
            p_company = st.text_input("Company Name", value="Tech Innovators Pvt Ltd")
            p_loc = st.text_input("Location", value="Remote / Kanpur")
            p_skills = st.text_input("Required Skills (comma separated)", value="Python, Django, SQL")
            p_sal = st.text_input("Salary / Stipend", value="₹4.0 - ₹6.0 LPA")
            p_submit = st.form_submit_button("Publish Verified Listing")
            
            if p_submit and p_title:
                st.session_state["jobs_database"].append({
                    "id": len(st.session_state["jobs_database"]) + 1,
                    "title": p_title, "company": p_company, "location": p_loc,
                    "required": [s.strip().lower() for s in p_skills.split(",") if s.strip()],
                    "min_exp": 0, "salary": p_sal, "verified": True, "type": "Private",
                    "official_url": "", "desc": "Posted via Recruiter Portal."
                })
                st.success(f"✓ Listing '{p_title}' moderated and published live!")

    with rt2:
        st.markdown("### Candidate Shortlisting Pipeline")
        candidates_data = [
            {"Name": "Arpit Srivastav", "Role": "Full Stack Software Engineer", "Match Score": "88%", "Status": "Shortlisted for Interview"},
            {"Name": "Rohan Verma", "Role": "Data Analyst Trainee", "Match Score": "75%", "Status": "Under Review"},
            {"Name": "Priya Sharma", "Role": "Full Stack Software Engineer", "Match Score": "92%", "Status": "Assessment Completed"}
        ]
        df_cand = pd.DataFrame(candidates_data)
        st.dataframe(df_cand, use_container_width=True)

    with rt3:
        st.markdown("### Recruitment & Platform Analytics")
        st.metric("Total Applicants", "142")
        st.metric("Average Skill Match Score", "81%")
        st.metric("Moderation Safety Rating", "100% Verified")
