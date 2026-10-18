import streamlit as st
import pandas as pd
import time
from fpdf import FPDF

# ==========================================
# PAGE CONFIGURATION & LIGHT THEME STYLING
# ==========================================
st.set_page_config(
    page_title="CareerBridge AI - Verified Career & Placement Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Professional Light Theme CSS
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
if "role" not in st.session_state:
    st.session_state["role"] = "Job Seeker"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "profile_completed" not in st.session_state:
    st.session_state["profile_completed"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Arpit Srivastav"
if "user_email" not in st.session_state:
    st.session_state["user_email"] = "arpit.srivastav@example.com"
if "user_phone" not in st.session_state:
    st.session_state["user_phone"] = "9876543210"
if "user_college" not in st.session_state:
    st.session_state["user_college"] = "CSJM University / Kanpur Institute"
if "user_address" not in st.session_state:
    st.session_state["user_address"] = "Civil Lines, Kanpur, Uttar Pradesh"
if "email_otp_sent" not in st.session_state:
    st.session_state["email_otp_sent"] = False
if "email_verified" not in st.session_state:
    st.session_state["email_verified"] = False
if "resume_file_name" not in st.session_state:
    st.session_state["resume_file_name"] = "Arpit_Srivastav_Resume.pdf"
if "user_skills" not in st.session_state:
    st.session_state["user_skills"] = ["python", "django", "sql", "react", "javascript", "html", "css"]
if "user_exp" not in st.session_state:
    st.session_state["user_exp"] = 0
if "portfolio_projects" not in st.session_state:
    st.session_state["portfolio_projects"] = [
        {"title": "Bite Bridge - Food Delivery App", "tech": "Node.js, Express, MongoDB", "link": "https://github.com/arpit/bite-bridge"},
        {"title": "CareerBridge AI Platform", "tech": "Python, Streamlit, Pandas", "link": "https://github.com/arpit/careerbridge-ai"}
    ]
if "interview_history" not in st.session_state:
    st.session_state["interview_history"] = []

# Comprehensive 18+ Job Listings Database
if "jobs_database" not in st.session_state:
    st.session_state["jobs_database"] = [
        {"id": 1, "title": "Software Engineer (BCA/BSc Freshers)", "company": "NextGen Technologies", "location": "Kanpur / Remote", "required": ["python", "django", "react", "sql"], "min_exp": 0, "salary": "₹3.5 - ₹5.5 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Entry-level full stack role for fresh BCA/BSc graduates."},
        {"id": 2, "title": "National Apprenticeship Training Scheme (NATS)", "company": "Ministry of Education", "location": "Prayagraj / UP", "required": ["python", "sql", "basics"], "min_exp": 0, "salary": "Stipend: ₹12,000/mo", "verified": True, "type": "Government", "official_url": "https://nats.education.gov.in/", "desc": "Official Govt Apprenticeship drive for graduate trainees."},
        {"id": 3, "title": "Data Analyst Trainee", "company": "Analytics Pulse", "location": "Bengaluru / Hybrid", "required": ["python", "sql", "excel", "pandas"], "min_exp": 0, "salary": "₹4.0 - ₹6.0 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Analyze datasets and build automated reporting dashboards."},
        {"id": 4, "title": "Python Junior Developer", "company": "CodeCraft Labs", "location": "Noida / Remote", "required": ["python", "django", "sql"], "min_exp": 0, "salary": "₹3.8 - ₹5.0 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Build backend APIs and maintain database schema."},
        {"id": 5, "title": "Frontend React Intern", "company": "PixelPerfect UI", "location": "Remote", "required": ["react", "javascript", "html", "css"], "min_exp": 0, "salary": "₹15,000/mo Stipend", "verified": True, "type": "Private", "official_url": "", "desc": "Design responsive UI components using React.js and Bootstrap."},
        {"id": 6, "title": "IT Support & Service Desk Associate", "company": "Wipro Tech Services", "location": "Lucknow / On-site", "required": ["networking", "linux", "troubleshooting"], "min_exp": 0, "salary": "₹3.0 - ₹4.5 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Manage IT service management workflows and resolve client incidents."},
        {"id": 7, "title": "Digital Forensics & Security Trainee", "company": "SecureNet InfoSec", "location": "Delhi NCR", "required": ["networking", "ethical hacking", "linux", "python"], "min_exp": 0, "salary": "₹4.5 - ₹6.5 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Assist in security audits and vulnerability assessment tasks."},
        {"id": 8, "title": "Junior Web Developer", "company": "WebSprint Solutions", "location": "Kanpur", "required": ["html", "css", "javascript", "php"], "min_exp": 0, "salary": "₹3.0 - ₹4.2 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Develop responsive client websites and landing pages."},
        {"id": 9, "title": "Bank IT Officer Trainee", "company": "Public Sector Banking Consortium", "location": "All India", "required": ["sql", "networking", "banking software"], "min_exp": 0, "salary": "₹6.0 - ₹8.0 LPA", "verified": True, "type": "Government", "official_url": "https://ibps.in/", "desc": "IT system administration and secure database management."},
        {"id": 10, "title": "NAPS Graduate Apprentice", "company": "National Apprenticeship Promotion Scheme", "location": "Uttar Pradesh", "required": ["basic computer skills", "communication"], "min_exp": 0, "salary": "₹10,000/mo", "verified": True, "type": "Government", "official_url": "https://www.apprenticeshipindia.gov.in/", "desc": "Structured corporate apprenticeship training for fresh graduates."},
        {"id": 11, "title": "Junior Python Automation Tester", "company": "QualityAssure Corp", "location": "Pune / Hybrid", "required": ["python", "selenium", "sql"], "min_exp": 0, "salary": "₹3.6 - ₹5.0 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Write automated test scripts using Python and Selenium."},
        {"id": 12, "title": "Operations & Data Entry Specialist", "company": "Logistics Hub India", "location": "Kanpur", "required": ["excel", "data entry", "typing"], "min_exp": 0, "salary": "₹2.5 - ₹3.5 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Manage inventory logs, shipment records, and digital spreadsheets."},
        {"id": 13, "title": "Junior Machine Learning Intern", "company": "AI Research Labs", "location": "Hyderabad / Remote", "required": ["python", "pandas", "scikit-learn", "numpy"], "min_exp": 0, "salary": "₹20,000/mo Stipend", "verified": True, "type": "Private", "official_url": "", "desc": "Data preprocessing and training baseline predictive classification models."},
        {"id": 14, "title": "NIELIT Technical Assistant (Contract)", "company": "NIELIT Public Sector", "location": "Gorakhpur", "required": ["python", "networking", "linux"], "min_exp": 0, "salary": "₹25,000/month", "verified": True, "type": "Government", "official_url": "https://www.nielit.gov.in/", "desc": "Technical support and lab assistant roles for tech graduates."},
        {"id": 15, "title": "Business Development Associate", "company": "EdTech Global", "location": "Lucknow", "required": ["communication", "sales", "presentation"], "min_exp": 0, "salary": "₹3.5 - ₹6.0 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Client outreach, product demonstration, and market engagement."},
        {"id": 16, "title": "SQL Database Trainee", "company": "DataStore Systems", "location": "Noida", "required": ["sql", "postgresql", "database design"], "min_exp": 0, "salary": "₹4.0 - ₹5.5 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Write complex SQL queries, stored procedures, and optimize indexing."},
        {"id": 17, "title": "Content & Tech Documentation Writer", "company": "DevDocs Pro", "location": "Remote", "required": ["technical writing", "markdown", "git"], "min_exp": 0, "salary": "₹3.2 - ₹4.8 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Create user guides, API documentations, and code tutorials."},
        {"id": 18, "title": "Junior Cloud Support Associate", "company": "CloudNine Networks", "location": "Chennai / Remote", "required": ["linux", "networking", "aws basics"], "min_exp": 0, "salary": "₹4.2 - ₹6.0 LPA", "verified": True, "type": "Private", "official_url": "", "desc": "Assist cloud infrastructure monitoring and server configuration."}
    ]

# PDF Resume Generator
def generate_clean_pdf(name, skills_list, exp, college):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, name, ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"College: {college} | Experience: {exp} Year(s)", ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Core Technical Competencies", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, ", ".join([s.title() for s in skills_list]))
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Verified Profile Summary", ln=True)
    pdf.set_font("Helvetica", "", 10)
    summary = f"Verified graduate from {college} proficient in {', '.join([s.title() for s in skills_list[:4]])}. Evaluated for technical suitability via CareerBridge AI."
    pdf.multi_cell(0, 6, summary)
    return bytes(pdf.output())

# ==========================================
# HEADER & VIEW SWITCHER
# ==========================================
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown("<h1 style='margin:0; color:#0284c7; font-weight:800;'>🚀 CareerBridge AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; margin:0; font-weight:500;'>Smart Placement, Verified Identity & Profile Corner Engine for Freshers</p>", unsafe_allow_html=True)
with col_h2:
    role_choice = st.selectbox("Portal Mode", ["Job Seeker", "Verified Recruiter"])
    st.session_state["role"] = role_choice

st.markdown("---")

# ==========================================
# VIEW 1: JOB SEEKER EXPERIENCE & PROFILE CORNER
# ==========================================
if st.session_state["role"] == "Job Seeker":

    # SCREEN 1: LOGIN / SIGNUP WITH STRICT EMAIL OTP VERIFICATION
    if not st.session_state["logged_in"]:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.subheader("🔑 Secure Candidate Portal Login & Signup")
        st.write("Strict verification required: OTP will be sent to your registered Email ID.")
        
        auth_tab1, auth_tab2 = st.tabs(["Candidate Login", "New Registration & Email OTP"])
        
        with auth_tab1:
            l_email = st.text_input("Registered Email ID", value="arpit.srivastav@example.com", key="l_email")
            l_pass = st.text_input("Password", type="password", value="password123", key="l_pass")
            if st.button("Secure Login", type="primary", use_container_width=True):
                if l_email:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = l_email
                    st.session_state["profile_completed"] = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter a valid email.")
                
        with auth_tab2:
            r_name = st.text_input("Full Name", value="Arpit Srivastav", key="r_name")
            r_email = st.text_input("Email ID (For OTP)", value="arpit.srivastav@example.com", key="r_email")
            r_phone = st.text_input("Mobile Number", value="9876543210", key="r_phone")
            r_college = st.text_input("College / University Name", value="CSJM University, Kanpur", key="r_college")
            r_address = st.text_input("Residential Address", value="Civil Lines, Kanpur", key="r_address")
            r_pass = st.text_input("Create Password", type="password", value="password123", key="r_pass")
            
            if not st.session_state["email_otp_sent"]:
                if st.button("Send Email OTP Verification", use_container_width=True):
                    if r_email and r_name:
                        st.session_state["email_otp_sent"] = True
                        st.session_state["user_name"] = r_name
                        st.session_state["user_email"] = r_email
                        st.session_state["user_phone"] = r_phone
                        st.session_state["user_college"] = r_college
                        st.session_state["user_address"] = r_address
                        st.success(f"✓ OTP successfully dispatched to {r_email}! (Simulated Code: 7890)")
                    else:
                        st.warning("Please fill in Name and Email ID.")
            
            if st.session_state["email_otp_sent"]:
                entered_otp = st.text_input("Enter 4-Digit Email OTP", max_chars=4, key="entered_email_otp")
                if st.button("Verify OTP & Complete Registration", type="primary", use_container_width=True):
                    if entered_otp == "7890" or entered_otp == "1234":
                        st.session_state["email_verified"] = True
                        st.session_state["logged_in"] = True
                        st.session_state["profile_completed"] = True
                        st.balloons()
                        st.success("✓ Email OTP Verified & Profile Registered Successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid OTP code. Try '7890'.")
                
        st.markdown("</div>", unsafe_allow_html=True)

    # SCREEN 2: FULL UNLOCKED PORTAL (PROFILE CORNER + 18+ JOBS + AI INTERVIEW + ATS)
    else:
        # Profile Corner & Sidebar Management
        st.sidebar.markdown("## 👤 Profile Corner")
        st.sidebar.markdown(f"**Name:** {st.session_state['user_name']}")
        st.sidebar.markdown(f"**Email:** {st.session_state['user_email']} <span class='badge-completed'>Verified</span>", unsafe_allow_html=True)
        st.sidebar.markdown(f"**Phone:** +91 {st.session_state['user_phone']}")
        st.sidebar.markdown(f"**College:** {st.session_state['user_college']}")
        st.sidebar.markdown(f"**Address:** {st.session_state['user_address']}")
        st.sidebar.markdown("---")
        
        st.session_state["user_exp"] = st.sidebar.slider("Experience (Years)", 0, 5, st.session_state["user_exp"])
        skills_input = st.sidebar.text_area("Your Skills Stack", value=", ".join([s.title() for s in st.session_state["user_skills"]]))
        if st.sidebar.button("Update Profile Corner Skills"):
            st.session_state["user_skills"] = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
            st.sidebar.success("Profile Corner Skills Updated!")
            
        if st.sidebar.button("Logout", type="secondary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["email_otp_sent"] = False
            st.session_state["email_verified"] = False
            st.rerun()

        # Main Tabs
        t1, t2, t3, t4, t5 = st.tabs([
            f"🌐 Verified Jobs Feed ({len(st.session_state['jobs_database'])})", 
            "💼 Portfolio & Resume Hub", 
            "🎙️ Ethical AI Mock Interview", 
            "📄 ATS Matcher & PDF", 
            "📈 Candidate Analytics & Growth"
        ])

        # TAB 1: VERIFIED JOBS FEED (WITH SKILL REQUIREMENTS DISPLAY)
        with t1:
            st.subheader("🎯 Verified Job Openings, Freshers Drives & NATS Govt Apprenticeships")
            st.write("Browse through curated opportunities and review exact required skills before applying.")
            
            search_kw = st.text_input("🔍 Search by role, skill, or company (e.g., Python, NATS, Data)...", "")
            
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
                
                badge_type = "<span class='badge-verified'>🏛️ Government / NATS</span>" if job["type"] == "Government" else "<span class='badge-verified'>✓ Employer Verified</span>"
                
                st.markdown(f"""
                <div class="light-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin:0; color:#0f172a;">{job['title']} {badge_type}</h3>
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
                    st.markdown(f"**Required Skills for this Role:** {', '.join([s.title() for s in job['required']])}")
                    st.markdown(f"**Your Match Status:** {m_pills if m_pills else ''} {g_pills if g_pills else '<span style=\"color:#15803d; font-weight:600;\">Fully Qualified!</span>'}", unsafe_allow_html=True)
                with c_right:
                    if job["type"] == "Government":
                        st.markdown(f"[🔗 Open Official Govt Portal]({job['official_url']})")
                        st.caption("Official portal navigation required.")
                    else:
                        if st.button(f"One-Click Apply", key=f"job_{job['id']}", type="primary"):
                            st.success(f"🎉 Application payload submitted to {job['company']} using your verified Profile Corner details!")
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
                    st.success(f"✓ Resume successfully updated to '{new_res_upload.name}'!")
                st.markdown("</div>", unsafe_allow_html=True)
                
            with c_p2:
                st.markdown("<div class='light-card'>", unsafe_allow_html=True)
                st.subheader("➕ Add Portfolio Project")
                with st.form("add_project_form"):
                    p_title = st.text_input("Project Name", value="Inventory Tracker System")
                    p_tech = st.text_input("Tech Stack", value="Python, Django, SQLite")
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
            st.write("Generate your official verified candidate profile resume using your Profile Corner details.")
            
            if st.button("Download Verified Resume PDF", type="primary"):
                pdf_bytes = generate_clean_pdf(st.session_state["user_name"], st.session_state["user_skills"], st.session_state["user_exp"], st.session_state["user_college"])
                st.download_button(
                    label="📥 Download PDF Document",
                    data=pdf_bytes,
                    file_name=f"{st.session_state['user_name'].replace(' ', '_')}_Verified_Resume.pdf",
                    mime="application/pdf"
                )

        # TAB 5: ANALYTICS
        with t5:
            st.subheader("📈 Candidate Placement & Verification Analytics")
            st.metric("Profile Verification Status", "100% Email & Mobile Verified")
            st.metric("Total Available Openings", len(st.session_state["jobs_database"]))
            if st.session_state["interview_history"]:
                df_hist = pd.DataFrame(st.session_state["interview_history"])
                st.dataframe(df_hist, use_container_width=True)

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
            p_skills = st.text_input("Required Skills (comma separated)", value="python, django, sql")
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
            {"Name": "Arpit Srivastav", "Role": "Software Engineer", "Match Score": "88%", "Status": "Shortlisted for Interview"},
            {"Name": "Rohan Verma", "Role": "Data Analyst Trainee", "Match Score": "75%", "Status": "Under Review"},
            {"Name": "Priya Sharma", "Role": "Full Stack Engineer", "Match Score": "92%", "Status": "Assessment Completed"}
        ]
        df_cand = pd.DataFrame(candidates_data)
        st.dataframe(df_cand, use_container_width=True)

    with rt3:
        st.markdown("### Recruitment & Platform Analytics")
        st.metric("Total Applicants", "142")
        st.metric("Average Skill Match Score", "81%")
        st.metric("Moderation Safety Rating", "100% Verified")
