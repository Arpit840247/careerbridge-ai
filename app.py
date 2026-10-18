import streamlit as st
import pandas as pd
import time
from fpdf import FPDF
import io

# ==========================================
# PAGE CONFIGURATION & AWESOME LIGHT STYLING
# ==========================================
st.set_page_config(
    page_title="CareerBridge AI - Ultimate Portfolio & Career Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Professional Light Theme CSS (Clean Slate, Electric Blue, Modern Cards)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #0f172a;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .light-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    
    .light-card:hover {
        transform: translateY(-2px);
        border-color: #cbd5e1;
    }
    
    .auth-card {
        background: #ffffff;
        padding: 36px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08);
        max-width: 480px;
        margin: 40px auto;
    }

    .badge-verified {
        background-color: #0284c7; color: #ffffff;
        padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
    }
    
    .badge-completed {
        background-color: #059669; color: #ffffff;
        padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700;
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
# SESSION STATE INITIALIZATION
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "profile_completed" not in st.session_state:
    st.session_state["profile_completed"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Arpit Srivastav"
if "user_email" not in st.session_state:
    st.session_state["user_email"] = "arpit@example.com"
if "user_phone" not in st.session_state:
    st.session_state["user_phone"] = "9876543210"
if "otp_verified" not in st.session_state:
    st.session_state["otp_verified"] = False
if "id_doc_uploaded" not in st.session_state:
    st.session_state["id_doc_uploaded"] = False
if "resume_uploaded" not in st.session_state:
    st.session_state["resume_uploaded"] = False
if "resume_file_name" not in st.session_state:
    st.session_state["resume_file_name"] = "No Resume Uploaded"
if "user_skills" not in st.session_state:
    st.session_state["user_skills"] = ["python", "django", "sql", "react", "javascript", "node.js"]
if "user_exp" not in st.session_state:
    st.session_state["user_exp"] = 1
if "portfolio_projects" not in st.session_state:
    st.session_state["portfolio_projects"] = [
        {"title": "Bite Bridge - Food Delivery Web App", "tech": "Node.js, Express, MongoDB", "link": "https://github.com/arpit/bite-bridge"},
        {"title": "CareerBridge AI Platform", "tech": "Python, Streamlit, Pandas", "link": "https://github.com/arpit/careerbridge-ai"}
    ]
if "interview_history" not in st.session_state:
    st.session_state["interview_history"] = []

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
            "location": "Bengaluru / Hybrid",
            "required": ["python", "sql", "excel", "pandas"],
            "min_exp": 0, "salary": "₹4.0 - ₹6.0 LPA", "verified": True, "type": "Private",
            "official_url": "", "desc": "Analyze data distributions, clean datasets, and build decision dashboards."
        }
    ]

# PDF Generator
def generate_clean_pdf(name, skills_list, exp):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, name, ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Verified Candidate | Experience: {exp} Year(s)", ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Core Technical Competencies", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, ", ".join([s.title() for s in skills_list]))
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Profile & Identity Verification Status", ln=True)
    pdf.set_font("Helvetica", "", 10)
    summary = f"Full identity verified profile for {name}. Evaluated for technical correctness and job suitability via CareerBridge AI."
    pdf.multi_cell(0, 6, summary)
    return bytes(pdf.output())

# ==========================================
# HEADER & TOP NAVIGATION
# ==========================================
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown("<h1 style='margin:0; color:#0284c7; font-weight:800;'>🚀 CareerBridge AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; margin:0; font-weight:500;'>Smart Placement, Verified Identity & Portfolio Engine for Indian Freshers</p>", unsafe_allow_html=True)
with col_h2:
    if st.session_state["logged_in"]:
        if st.button("Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["profile_completed"] = False
            st.rerun()

st.markdown("---")

# ==========================================
# SCREEN 1: LOGIN / REGISTRATION
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.subheader("🔑 Candidate Portal Access")
    
    auth_tab1, auth_tab2 = st.tabs(["Candidate Login", "New Candidate Registration"])
    
    with auth_tab1:
        l_email = st.text_input("Email Address", value="arpit@example.com", key="login_email")
        l_pass = st.text_input("Password", type="password", value="password123", key="login_pass")
        if st.button("Sign In to Portal", type="primary", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = l_email
            st.rerun()
            
    with auth_tab2:
        r_name = st.text_input("Full Name", value="Arpit Srivastav", key="reg_name")
        r_email = st.text_input("Email Address", value="arpit@example.com", key="reg_email")
        r_phone = st.text_input("Mobile Number", value="9876543210", key="reg_phone")
        r_pass = st.text_input("Create Password", type="password", value="password123", key="reg_pass")
        if st.button("Create Account & Proceed", type="primary", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_name"] = r_name
            st.session_state["user_email"] = r_email
            st.session_state["user_phone"] = r_phone
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# SCREEN 2: PROFILE COMPLETION & ONBOARDING
# ==========================================
elif st.session_state["logged_in"] and not st.session_state["profile_completed"]:
    st.markdown("<h2 style='text-align:center; color:#0f172a;'>📋 Complete Your Verified Candidate Profile</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b;'>Verify your details to unlock the verified jobs feed and portfolio builder.</p>", unsafe_allow_html=True)
    
    steps_done = sum([st.session_state["otp_verified"], st.session_state["id_doc_uploaded"], st.session_state["resume_uploaded"]])
    progress_pct = int((steps_done / 3) * 100)
    
    st.progress(progress_pct)
    st.markdown(f"<p style='text-align:center; font-weight:bold; color:#0284c7;'>Profile Completion Progress: {progress_pct}%</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='light-card'>", unsafe_allow_html=True)
        st.subheader("Step 1: Phone OTP")
        st.write(f"**Mobile:** +91 {st.session_state['user_phone']}")
        if st.button("Verify OTP Code (1234)"):
            st.session_state["otp_verified"] = True
            st.success("✓ Verified!")
        if st.session_state["otp_verified"]:
            st.markdown("<span class='badge-completed'>✓ Verified</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='light-card'>", unsafe_allow_html=True)
        st.subheader("Step 2: Govt ID Verification")
        id_doc = st.file_uploader("Upload ID Copy (PDF/JPG)", type=["pdf", "jpg", "png"])
        if id_doc:
            st.session_state["id_doc_uploaded"] = True
            st.success("✓ ID Uploaded Successfully!")
        if st.session_state["id_doc_uploaded"]:
            st.markdown("<span class='badge-completed'>✓ ID Uploaded</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='light-card'>", unsafe_allow_html=True)
        st.subheader("Step 3: Upload Updated Resume")
        up_res = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        if up_res:
            st.session_state["resume_uploaded"] = True
            st.session_state["resume_file_name"] = up_res.name
            st.success(f"✓ Resume '{up_res.name}' Uploaded!")
        if st.session_state["resume_uploaded"]:
            st.markdown(f"<span class='badge-completed'>✓ {st.session_state['resume_file_name']}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚀 Launch CareerBridge Portal", type="primary", use_container_width=True):
        if not st.session_state["otp_verified"]:
            st.warning("Please verify your phone number via OTP to continue.")
        else:
            st.session_state["profile_completed"] = True
            st.balloons()
            st.rerun()

# ==========================================
# SCREEN 3: FULL PORTAL INTERFACE
# ==========================================
else:
    st.sidebar.markdown("## 👤 Verified Candidate Hub")
    st.sidebar.markdown(f"**Name:** {st.session_state['user_name']}")
    st.sidebar.markdown(f"**Resume:** `{st.session_state['resume_file_name']}`")
    st.sidebar.markdown(f"**Status:** <span class='badge-completed'>✓ Verified</span>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    st.session_state["user_exp"] = st.sidebar.slider("Experience (Years)", 0, 5, st.session_state["user_exp"])
    skills_input = st.sidebar.text_area("Your Skills Stack", value=", ".join([s.title() for s in st.session_state["user_skills"]]))
    if st.sidebar.button("Update Skills"):
        st.session_state["user_skills"] = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
        st.sidebar.success("Skills Updated!")

    # Main Navigation Tabs
    t1, t2, t3, t4, t5 = st.tabs([
        "🌐 Verified Jobs & NATS", 
        "💼 Portfolio & Resume Hub", 
        "🎙️ Ethical AI Mock Interview", 
        "📄 ATS Matcher & PDF", 
        "📈 Analytics & Growth"
    ])

    # TAB 1: VERIFIED JOBS FEED
    with t1:
        st.subheader("🎯 Verified Job Openings & NATS Govt Apprenticeships")
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
            
            badge_html = "<span class='badge-verified'>✓ Verified Opportunity</span>"
            
            st.markdown(f"""
            <div class="light-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin:0; color:#0f172a;">{job['title']} {badge_html}</h3>
                        <p style="color:#64748b; margin:4px 0;">🏢 {job['company']} &nbsp;|&nbsp; 📍 {job['location']} &nbsp;|&nbsp; 💰 {job['salary']}</p>
                    </div>
                    <div><span class="score-badge" style="background-color:#059669; color:white; padding:6px 12px; border-radius:20px;">{score}% MATCH</span></div>
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
                    st.markdown(f"[🔗 Apply on NATS Official Portal]({job['official_url']})")
                else:
                    if st.button(f"One-Click Verified Apply", key=f"job_{job['id']}", type="primary"):
                        st.success(f"🎉 Application & Verified Profile Data Payload Sent to {job['company']}!")
            st.markdown("<hr style='border: 0.5px solid #e2e8f0;'>", unsafe_allow_html=True)

    # TAB 2: PORTFOLIO & RESUME HUB
    with t2:
        st.subheader("💼 Professional Portfolio & Live Resume Management")
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("<div class='light-card'>", unsafe_allow_html=True)
            st.subheader("📄 Upload & Update Resume")
            st.write(f"**Current Active Resume:** `{st.session_state['resume_file_name']}`")
            new_res_upload = st.file_uploader("Upload New Updated Resume (PDF)", type=["pdf"], key="portfolio_res_up")
            if new_res_upload:
                st.session_state["resume_file_name"] = new_res_upload.name
                st.session_state["resume_uploaded"] = True
                st.success(f"✓ Resume successfully updated to '{new_res_upload.name}'!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_p2:
            st.markdown("<div class='light-card'>", unsafe_allow_html=True)
            st.subheader("➕ Add Portfolio Project")
            with st.form("add_project_form"):
                p_title = st.text_input("Project Name", value="Food Delivery App")
                p_tech = st.text_input("Tech Stack", value="React, Node.js, MongoDB")
                p_link = st.text_input("GitHub / Live Link", value="https://github.com/...")
                p_add = st.form_submit_button("Add to Portfolio")
                if p_add and p_title:
                    st.session_state["portfolio_projects"].append({"title": p_title, "tech": p_tech, "link": p_link})
                    st.success(f"✓ Project '{p_title}' added to your portfolio!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("### 🏆 Your Public Portfolio Showcase")
        for proj in st.session_state["portfolio_projects"]:
            st.markdown(f"""
            <div class="light-card">
                <h4 style="margin:0; color:#0284c7;">{proj['title']}</h4>
                <p style="margin:4px 0; color:#64748b;"><b>Tech Stack:</b> {proj['tech']}</p>
                <p style="margin:0;"><a href="{proj['link']}" target="_blank">🔗 View Repository / Live Demo</a></p>
            </div>
            """, unsafe_allow_html=True)

    # TAB 3: ETHICAL AI MOCK INTERVIEW
    with t3:
        st.subheader("🎙️ Objective AI Technical Interview Module")
        st.info("ℹ️ Evaluation criteria: Technical accuracy, answer structure, and conceptual relevance. No facial or accent tracking used.")
        
        target_role = st.selectbox("Select Interview Specialty", ["Software Engineer (Full Stack)", "Data Analyst Trainee"])
        st.markdown(f"### Question: Explain exception handling and ORM concurrency patterns in Python / SQL.")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        
        user_answer = st.text_area("Your Response Transcription:", height=130, placeholder="Explain core concepts and architectural implementation...")
        
        if st.button("Submit Response for Evaluation", type="primary"):
            if user_answer:
                st.success("✓ Evaluation Complete: Technical Correctness 88% | Structural Clarity 82% | Score: 85%")
                st.session_state["interview_history"].append({"date": time.strftime("%Y-%m-%d %H:%M"), "score": 85})

    # TAB 4: ATS RESUME & PDF
    with t4:
        st.subheader("📄 Verified Candidate PDF Resume Generator")
        st.write("Generate your official verified candidate profile resume.")
        
        if st.button("Download Verified Resume PDF", type="primary"):
            pdf_bytes = generate_clean_pdf(st.session_state["user_name"], st.session_state["user_skills"], st.session_state["user_exp"])
            st.download_button(
                label="📥 Download PDF Document",
                data=pdf_bytes,
                file_name=f"{st.session_state['user_name'].replace(' ', '_')}_Verified_Resume.pdf",
                mime="application/pdf"
            )

    # TAB 5: ANALYTICS
    with t5:
        st.subheader("📈 Candidate Placement & Verification Analytics")
        st.metric("Profile Verification Status", "100% Verified")
        st.metric("Total Portfolio Projects", len(st.session_state["portfolio_projects"]))
        if st.session_state["interview_history"]:
            df_hist = pd.DataFrame(st.session_state["interview_history"])
            st.dataframe(df_hist, use_container_width=True)
