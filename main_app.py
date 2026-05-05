import streamlit as st
import base64

# -----------------------------
# MUST BE FIRST Streamlit call
# -----------------------------
st.set_page_config(page_title="91 Care Helpdesk", page_icon="🏥")

# -----------------------------
# Background & Styles
# -----------------------------
def get_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

img = get_base64("bg.jpeg")

if img:
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                    url("data:image/jpeg;base64,{img}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
div.stButton > button {
    background-color: #f0f2f6;
    color: black;
    border-radius: 8px;
    height: 45px;
}
div.stButton > button:hover {
    background-color: #007BFF;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Logo Header
# -----------------------------
col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    colA, colB = st.columns([1, 3])
    with colA:
        try:
            st.image("loginlogo.jpg", width=70)
        except Exception:
            st.markdown("🏥")
    with colB:
        st.markdown("<h2 style='margin-top:15px;'>91 Care</h2>", unsafe_allow_html=True)

# -----------------------------
# Session State Initialization
# -----------------------------
defaults = {
    "module": None,
    "role": None,
    "step": "module",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# UNIVERSAL BACK FUNCTIONS
# -----------------------------
def back(target_step, reset_role=False, reset_module=False, key="back"):
    if st.button("⬅ Back", key=key):
        if reset_role:
            st.session_state.role = None
        if reset_module:
            st.session_state.module = None
        st.session_state.step = target_step
        st.rerun()

def back_to_main(key):
    if st.button("⬅ Back", key=key):
        st.session_state.step = "main"
        st.rerun()

def back_to_admin_main(key):
    if st.button("⬅ Back", key=key):
        st.session_state.step = "admin_main"
        st.rerun()

# =============================================
# MODULE SELECTION
# =============================================
def module_selection():
    st.title("🏥 91 Care Helpdesk")
    st.subheader("Select Module")

    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("🩺 OPD", use_container_width=True):
        st.session_state.module = "OPD"
        st.session_state.step = "role"

    if col2.button("🧪 LAB", use_container_width=True):
        st.session_state.module = "LAB"
        st.session_state.step = "role"

    if col3.button("🛏️ IPD", use_container_width=True):
        st.session_state.module = "IPD"
        st.session_state.step = "role"

    if col4.button("💊 Pharmacy", use_container_width=True):
        st.session_state.module = "pharmacy"
        st.session_state.step = "role"

    if col5.button("🧑‍💻 Admin", use_container_width=True):
        st.session_state.module = "Admin"
        st.session_state.step = "admin_main"

# =============================================
# ADMIN MAIN MENU
# =============================================
def admin_main():
    col_back, col_logout = st.columns([6, 1])
    with col_back:
        if st.button("⬅ Back to Modules", key="back_admin_main"):
            st.session_state.module = None
            st.session_state.step = "module"
            st.rerun()

    st.subheader("🧑‍💻 Admin Panel")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏥 Clinics"):
            st.session_state.step = "admin_Clinics"
    with col2:
        if st.button("👤 Users"):
            st.session_state.step = "admin_Users"
    with col3:
        if st.button("💬 Messages"):
            st.session_state.step = "admin_Messages"

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Prescription Template"):
            st.session_state.step = "admin_PT"
    with col2:
        if st.button("📄 PDF Template"):
            st.session_state.step = "admin_PDFT"
    with col3:
        if st.button("🧾 Template"):
            st.session_state.step = "admin_Temp"

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👨‍⚕️ Referral Doctor"):
            st.session_state.step = "admin_RD"
    with col2:
        if st.button("🔳 QR Code"):
            st.session_state.step = "admin_QR"
    with col3:
        if st.button("📋 Patient Info"):
            st.session_state.step = "admin_UPI"

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏥 OT Creation"):
            st.session_state.step = "admin_OT"
    with col2:
        if st.button("📊 Reports"):
            st.session_state.step = "admin_Reports"
    with col3:
        if st.button("📋 IPD"):
            st.session_state.step = "admin_IPD"

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🆔 UHID Configuration"):
            st.session_state.step = "admin_UHID"

# =============================================
# ROLE SELECTION
# =============================================
def role_selection():
    back("module", reset_role=True, reset_module=True, key="back_module")

    st.subheader(f"{st.session_state.module} → Select Role")

    cols = st.columns(4)

    module_roles = {
        "OPD": ["🩺Doctor", "💉Nurse", "📞Receptionist", "🧑‍💻Admin"],
        "LAB": ["🩺Doctor", "💉Nurse", "📞Receptionist", "🧑‍💻Admin", "🧪Phlebotomist", "🔬Pathologist"],
        "IPD": ["🩺Doctor", "💉Nurse", "📞Receptionist", "🧑‍💻Admin"],
        "pharmacy": ["👨‍⚕️pharmacist ", "🧑‍💻Admin"]
    }

    roles = module_roles.get(st.session_state.module, [])

    for i, role in enumerate(roles):
        if cols[i % 3].button(role, use_container_width=True):
            st.session_state.role = role
            st.session_state.step = "main"

# =============================================
# MAIN MENU (OPD / LAB / IPD / Pharmacy)
# =============================================
def main_menu():
    if st.button("⬅ Back", key="back_role"):
        st.session_state.role = None
        st.session_state.step = "role"
        st.rerun()

    module = st.session_state.module
    role = st.session_state.role

    st.subheader(f"{module} | {role}")

    # -------- OPD --------
    if module == "OPD":

        if role == "🩺Doctor":
            if st.button("🧾 Download Report", key="dr_1"):
                st.session_state.step = "Report"
            if st.button("📅 Availability", key="av_1"):
                st.session_state.step = "Availability"
            if st.button("💊 Prescription", key="pr_1"):
                st.session_state.step = "prescription"

        elif role == "📞Receptionist":
            if st.button("📅 Book Appointment", key="ba_1"):
                st.session_state.step = "appointment"
            if st.button("🔢 Token", key="tk_1"):
                st.session_state.step = "Token"
            if st.button("💳 Payment Status", key="ps_1"):
                st.session_state.step = "Payment_Status"
            if st.button("👨‍⚕️ Doctors list", key="dl_1"):
                st.session_state.step = "doctors_list"
            if st.button("⚙️ Edit details", key="editing_1"):
                st.session_state.step = "Editing"

        elif role == "🧑‍💻Admin":
            if st.button("🧾 Download Report", key="dr_2"):
                st.session_state.step = "Report"
            if st.button("📅 Availability", key="av_2"):
                st.session_state.step = "Availability"
            if st.button("💊 Prescription", key="pr_2"):
                st.session_state.step = "prescription"
            if st.button("📅 Book Appointment", key="ba_2"):
                st.session_state.step = "appointment"
            if st.button("🔢 Token", key="tk_2"):
                st.session_state.step = "Token"
            if st.button("💳 Payment Status", key="ps_2"):
                st.session_state.step = "Payment_Status"
            if st.button("👨‍⚕️ Doctors list", key="dl_2"):
                st.session_state.step = "doctors_list"
            if st.button("⚙️ Edit details", key="editing_2"):
                st.session_state.step = "Editing"
            if st.button("🛠️ Check Service", key="service_2"):
                st.session_state.step = "service"
            if st.button("🧾 Invoice", key="invoice_2"):
                st.session_state.step = "invoice"
            if st.button("🧾 Vitals", key="vitals_2"):
                st.session_state.step = "vitals"

        elif role == "💉Nurse":
            if st.button("📅 Appointment", key="ap_3"):
                st.session_state.step = "appointment"
            if st.button("💊 Prescription", key="pr_3"):
                st.session_state.step = "prescription"
            if st.button("💳 Payment Status", key="ps_3"):
                st.session_state.step = "Payment_Status"
            if st.button("🛠️ Check Service", key="service_3"):
                st.session_state.step = "service"
            if st.button("🧾 Invoice", key="invoice_3"):
                st.session_state.step = "invoice"
            if st.button("🧾 Vitals", key="vitals_3"):
                st.session_state.step = "vitals"

    # -------- LAB --------
    elif module == "LAB":

        if role == "🧑‍💻Admin":
            if st.button("💳 Billing", key="billing_1"):
                st.session_state.step = "billing"
            if st.button("👤 Add patient", key="add_patient_1"):
                st.session_state.step = "add_patient"
            if st.button("📋 Download Reports", key="dr_lab_1"):
                st.session_state.step = "DR"
            if st.button("📋 Update Reports", key="ur_1"):
                st.session_state.step = "UR"
            if st.button("👤 Search Patient", key="sp_1"):
                st.session_state.step = "sp"
            if st.button("👁️ Transaction History", key="th_1"):
                st.session_state.step = "TH"
            if st.button("🧪 Add Test", key="at_1"):
                st.session_state.step = "AT"
            if st.button("📝 Test List", key="tl_1"):
                st.session_state.step = "TL"

        elif role == "🧪Phlebotomist":
            if st.button("💳 Billing", key="billing_2"):
                st.session_state.step = "billing"
            if st.button("👤 Add patient", key="add_patient_2"):
                st.session_state.step = "add_patient"
            if st.button("📋 Download Reports", key="dr_lab_2"):
                st.session_state.step = "DR"
            if st.button("📋 Update Reports", key="ur_2"):
                st.session_state.step = "UR"
            if st.button("👤 Search Patient", key="sp_2"):
                st.session_state.step = "sp"
            if st.button("👁️ Transaction History", key="th_2"):
                st.session_state.step = "TH"
            if st.button("🧪 Add Test", key="at_2"):
                st.session_state.step = "AT"
            if st.button("📝 Test List", key="tl_2"):
                st.session_state.step = "TL"

        elif role == "🩺Doctor":
            if st.button("👤 Add patient", key="add_patient_3"):
                st.session_state.step = "add_patient"
            if st.button("📋 Download Reports", key="dr_lab_3"):
                st.session_state.step = "DR"
            if st.button("📋 Update Reports", key="ur_3"):
                st.session_state.step = "UR"
            if st.button("👤 Search Patient", key="sp_3"):
                st.session_state.step = "sp"

        elif role == "💉Nurse":
            if st.button("💳 Billing", key="billing_4"):
                st.session_state.step = "billing"
            if st.button("👤 Add patient", key="add_patient_4"):
                st.session_state.step = "add_patient"
            if st.button("📋 Download Reports", key="dr_lab_4"):
                st.session_state.step = "DR"
            if st.button("📋 Update Reports", key="ur_4"):
                st.session_state.step = "UR"
            if st.button("👤 Search Patient", key="sp_4"):
                st.session_state.step = "sp"
            if st.button("👁️ Transaction History", key="th_4"):
                st.session_state.step = "TH"
            if st.button("🧪 Add Test", key="at_4"):
                st.session_state.step = "AT"
            if st.button("📝 Test List", key="tl_4"):
                st.session_state.step = "TL"

        elif role == "📞Receptionist":
            if st.button("💳 Billing", key="billing_5"):
                st.session_state.step = "billing"

        elif role == "🔬Pathologist":
            if st.button("📋 Download Reports", key="dr_lab_5"):
                st.session_state.step = "DR"
            if st.button("📋 Update Reports", key="ur_5"):
                st.session_state.step = "UR"
            if st.button("✅ Report Approval", key="ra_5"):
                st.session_state.step = "RA"

    # -------- IPD --------
    elif module == "IPD":

        if role == "🩺Doctor":
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎟️ Book OT", key="ipd_ot_1"):
                    st.session_state.step = "OT"
            with col2:
                if st.button("🧾 Prescription", key="ipd_prescription_1"):
                    st.session_state.step = "Prescription"
            with col3:
                if st.button("📝 Assign Doctor", key="ipd_assign_1"):
                    st.session_state.step = "assign_doctor"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Transfer Patient", key="ipd_transfer_1"):
                    st.session_state.step = "Transfer"
            with col2:
                if st.button("🏠 Discharge Patient", key="ipd_discharge_1"):
                    st.session_state.step = "Discharge"

        elif role == "💉Nurse":
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🛏️ Admit Patient", key="ipd_admit_2"):
                    st.session_state.step = "Admit"
            with col2:
                if st.button("🔄 Reschedule OT", key="ipd_reschedule_2"):
                    st.session_state.step = "Reschedule"
            with col3:
                if st.button("📋 Registration Form", key="ipd_reg_2"):
                    st.session_state.step = "Registration_form"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📁 Upload Files", key="ipd_upload_2"):
                    st.session_state.step = "Upload"
            with col2:
                if st.button("📝 Assign Doctor", key="ipd_assign_2"):
                    st.session_state.step = "assign_doctor"
            with col3:
                if st.button("🔄 Transfer Patient", key="ipd_transfer_2"):
                    st.session_state.step = "Transfer"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("❌ Cancel Appointment", key="ipd_cancel_2"):
                    st.session_state.step = "cancel_appointment"
            with col2:
                if st.button("✍️ Consent Form", key="ipd_consent_2"):
                    st.session_state.step = "consent_form"
            with col3:
                if st.button("📅 Schedule Consultation", key="ipd_schedule_2"):
                    st.session_state.step = "schedule_consultation"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🪪 Visitor ID", key="ipd_visitor_2"):
                    st.session_state.step = "visitor_id"
            with col2:
                if st.button("🧾 Billing History", key="ipd_billing_2"):
                    st.session_state.step = "billing_history"
            with col3:
                if st.button("📜 Download Invoice", key="ipd_invoice_2"):
                    st.session_state.step = "Download_invoice"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👁️ View Certificate", key="ipd_certificate_2"):
                    st.session_state.step = "View_certificate"
            with col2:
                if st.button("♻️ Old Patient Linking", key="ipd_old_2"):
                    st.session_state.step = "old_patient_linking"
            with col3:
                if st.button("⬆️ Update Admission", key="ipd_update_2"):
                    st.session_state.step = "Update_Admission"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👩 Nurse Notes", key="ipd_notes_2"):
                    st.session_state.step = "Nurse_notes"
            with col2:
                if st.button("💊 Prescription", key="ipd_prescription_2"):
                    st.session_state.step = "Prescription"

        elif role == "📞Receptionist":
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🛏️ Admit Patient", key="ipd_admit_3"):
                    st.session_state.step = "Admit"
            with col2:
                if st.button("🔄 Reschedule OT", key="ipd_reschedule_3"):
                    st.session_state.step = "Reschedule"
            with col3:
                if st.button("📋 Registration Form", key="ipd_reg_3"):
                    st.session_state.step = "Registration_form"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📁 Upload Files", key="ipd_upload_3"):
                    st.session_state.step = "Upload"
            with col2:
                if st.button("🔄 Transfer Patient", key="ipd_transfer_3"):
                    st.session_state.step = "Transfer"
            with col3:
                if st.button("❌ Cancel Appointment", key="ipd_cancel_3"):
                    st.session_state.step = "cancel_appointment"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🏠 Discharge Patient", key="ipd_discharge_3"):
                    st.session_state.step = "Discharge"
            with col2:
                if st.button("📁 Consent Form", key="ipd_consent_3"):
                    st.session_state.step = "consent_form"
            with col3:
                if st.button("📅 Schedule Consultation", key="ipd_schedule_3"):
                    st.session_state.step = "schedule_consultation"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🪪 Visitor ID", key="ipd_visitor_3"):
                    st.session_state.step = "visitor_id"
            with col2:
                if st.button("➕ Add Service", key="ipd_service_3"):
                    st.session_state.step = "Add_service"
            with col3:
                if st.button("🧾 Billing History", key="ipd_billing_3"):
                    st.session_state.step = "billing_history"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📜 Download Invoice", key="ipd_invoice_3"):
                    st.session_state.step = "Download_invoice"
            with col2:
                if st.button("💳 Pay Final Bill", key="ipd_pay_3"):
                    st.session_state.step = "Pay_Bill"
            with col3:
                if st.button("👁️ View Certificate", key="ipd_certificate_3"):
                    st.session_state.step = "View_certificate"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("♻️ Old Patient Linking", key="ipd_old_3"):
                    st.session_state.step = "old_patient_linking"
            with col2:
                if st.button("⬆️ Update Admission", key="ipd_update_3"):
                    st.session_state.step = "Update_Admission"

        elif role == "🧑‍💻Admin":
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🛏️ Admit Patient", key="ipd_admit_4"):
                    st.session_state.step = "Admit"
            with col2:
                if st.button("🎟️ Book OT", key="ipd_ot_4"):
                    st.session_state.step = "OT"
            with col3:
                if st.button("🔄 Reschedule OT", key="ipd_reschedule_4"):
                    st.session_state.step = "Reschedule"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Registration Form", key="ipd_reg_4"):
                    st.session_state.step = "Registration_form"
            with col2:
                if st.button("📁 Upload Files", key="ipd_upload_4"):
                    st.session_state.step = "Upload"
            with col3:
                if st.button("📝 Assign Doctor", key="ipd_assign_4"):
                    st.session_state.step = "assign_doctor"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Transfer Patient", key="ipd_transfer_4"):
                    st.session_state.step = "Transfer"
            with col2:
                if st.button("🏠 Discharge Patient", key="ipd_discharge_4"):
                    st.session_state.step = "Discharge"
            with col3:
                if st.button("❌ Cancel Appointment", key="ipd_cancel_4"):
                    st.session_state.step = "cancel_appointment"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🧾 Billing History", key="ipd_billing_4"):
                    st.session_state.step = "billing_history"
            with col2:
                if st.button("📜 Download Invoice", key="ipd_invoice_4"):
                    st.session_state.step = "Download_invoice"
            with col3:
                if st.button("💳 Pay Final Bill", key="ipd_pay_4"):
                    st.session_state.step = "Pay_Bill"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👁️ View Certificate", key="ipd_certificate_4"):
                    st.session_state.step = "View_certificate"
            with col2:
                if st.button("⬆️ Update Admission", key="ipd_update_4"):
                    st.session_state.step = "Update_Admission"
            with col3:
                if st.button("✍️ Consent Form", key="ipd_consent_4"):
                    st.session_state.step = "consent_form"

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📅 Schedule Consultation", key="ipd_schedule_5"):
                    st.session_state.step = "schedule_consultation"

    elif module == "pharmacy":

        if role == "👨‍⚕️pharmacist ":
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💵 New Bill"):
                    st.session_state.step = "New_Bill"
            with col2:
                if st.button("📦 Add stock"):
                    st.session_state.step = "Add_stock"
            with col3:
                if st.button("📦 Modify stock"):
                    st.session_state.step = "Modify_stock"
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💳 Billing"):
                    st.session_state.step = "Billing"
            with col2:
                if st.button("📦 Indent Management"):
                    st.session_state.step = "Indent_Management"
            with col3:
                if st.button("↔️ Store Transfer"):
                    st.session_state.step = "Store_Transfer"
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💊 Medicine"):
                    st.session_state.step = "Medicine"
            with col2:
                if st.button("💻 Issue Medication Via Online Rx"):
                    st.session_state.step = "Online_Prescription"

        elif role == "🧑‍💻Admin":
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💵 New Bill"):
                    st.session_state.step = "New_Bill"
            with col2:
                if st.button("📦 Add stock"):
                    st.session_state.step = "Add_stock"
            with col3:
                if st.button("📦 Modify stock"):
                    st.session_state.step = "Modify_stock"
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💳 Billing"):
                    st.session_state.step = "Billing"
            with col2:
                if st.button("📦 Indent Management"):
                    st.session_state.step = "Indent_Management"
            with col3:
                if st.button("↔️ Store Transfer"):
                    st.session_state.step = "Store_Transfer"
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💊 Medicine"):
                    st.session_state.step = "Medicine"
            with col2:
                if st.button("💻 Issue Medication Via Online Rx"):
                    st.session_state.step = "Online_Prescription"


# =============================================
# OPD / LAB FEATURE PAGES
# =============================================
def Report():
    st.markdown("""
### 📥 Steps to Download

🔹 Go to **Dashboard**  
🔹 Click on **Download Report** (top-right)  
🔹 File will download automatically  
""")
    back_to_main("back_main")

def Availability():
    st.markdown("""
### 📅 Steps to Manage Availability

🔹 Go to **Appointment Page**  
🔹 Click on **Doctor's Time Off** (top-right)  
🔹 Fill in the required details  
🔹 Click **Submit** to save  
""")
    back_to_main("back_main2")

def prescription():
    st.markdown("""
### 💊 Steps to View Prescription

🔹 Go to **Appointment Page**  
🔹 Search for the **Patient Name**  
🔹 Locate the patient in the list  
🔹 Click on **Prescription** (at the end of the row)  
🔹 View the prescribed details  
""")
    back_to_main("back_main3")

def appointment():
    st.markdown("""
### 📅 Steps to Book Appointment

🔹 Go to **Appointment Page**  
🔹 Click on **+ Appointment** (top-right)  
🔹 Fill in the **required details**  
🔹 Click on **Submit**  
""")
    back_to_main("back_main4")

def Token():
    st.markdown("""
### 🎟️ Steps to Manage Token

🔹 Go to **Appointment Page**  
🔹 Click on **Token Entry** (top-right)  
🔹 Enter or update the **Token Number**  
🔹 Save the changes  
""")
    back_to_main("back_main5")

def Payment_Status():
    st.markdown("""
### 💳 Steps to Check Payment Status

🔹 Go to **Patients Page**  
🔹 Search for the **Patient Name**  
🔹 Select the patient from the list  
🔹 View the **Payment Status**  
""")
    back_to_main("back_main6")

def doctors_list():
    st.markdown("""
### 👨‍⚕️ Steps to View Doctors List

🔹 Go to **Appointment Page**  
🔹 Click on **Doctor Section** (right side)  
🔹 View the list of **Available Doctors**  
""")
    back_to_main("back_main7")

def Editing():
    st.markdown("""
### ✏️ Steps to Edit Patient Details

🔹 Go to **Appointment Page**  
🔹 Locate the **Patient** in the list  
🔹 Click on the **⋮ (3 vertical dots)** at the end of the row  
🔹 Select **Edit Option**  
🔹 Update the required details and save  
""")
    back_to_main("back_main8")

def service():
    st.markdown("""
### 📋 Steps to Check Patient Services

🔹 Go to **Patients Page**  
🔹 View the list of patients  
🔹 Click on the **(⋮)** at the end of the row → Select **Check Services**  
🔹 View services for the selected patient  
""")
    back_to_main("back_main9")

def invoice():
    st.markdown("""
### 🧾 Steps to Raise an Invoice

🔹 Go to **Appointments Page**  
🔹 View the list of appointments  
🔹 Click on **'Raise Invoice'** at the end of the required row  
🔹 The invoice will be displayed  
""")
    back_to_main("back_main10")

def vitals():
    st.markdown("""
### 🧾 Steps to see Vitals

🔹 Go to **Appointments Page**  
🔹 View the list of appointments  
🔹 Click on the **three vertical dots (⋮)** at the end of the row  
🔹 Click on **'Vitals'** from the list  
🔹 The Vitals will be displayed  
""")
    back_to_main("back_main11")

def billing():
    st.markdown("""
### 🧾 Billing Instructions

🔹 Go to the **Dashboard**  
🔹 Click on **Add Bill** in the top right corner  

🔹 To add to an existing bill:  
   • Select the bill from the list  

🔹 To create a new bill:  
   • Click on **New Bill**  
   • Search and select the **patient name**  
   • Patient details will be **auto-filled**  
   • Add the required **bill details**  

🔹 Finally, you can:  
   • **Save** the bill  
   • Or **Pay** the bill  
""")
    back_to_main("back_main12")

def add_patient():
    st.markdown("""
### 🧾 Patient Instructions

🔹 Go to the **Dashboard**  
🔹 Click on **Add Patient** in the top right corner  
🔹 Fill the form with patient details  
🔹 Save the details  
""")
    back_to_main("back_main13")

def DR():
    st.markdown("""
### 🧾 Download Reports

🔹 Go to the **Billing** section  
🔹 View the list of patients  
🔹 Locate the **Invoice PDF** option at the end of each row  
🔹 Click on it to download the patient report  
""")
    back_to_main("back_main14")

def UR():
    st.markdown("""
### 📋 Update Report Instructions

🔹 Go to the **Dashboard**  
🔹 View the list of patients  
🔹 Locate the **Update Report** option at the end of each row  
🔹 Click on it to update the patient report  
""")
    back_to_main("back_main15")

def sp():
    st.markdown("""
### 🔍 Search Patient Instructions

🔹 Go to the **Dashboard**  
🔹 Use the **Search Box** to enter the patient name  
🔹 View the patient details from the results  
""")
    back_to_main("back_main16")

def TH():
    st.markdown("""
### 👁️ Patient Transaction History Instructions

🔹 Go to the **Patients** section  
🔹 View the list of patients  
🔹 Locate the **👁️ (View)** icon at the end of each row  
🔹 Click on it to view the transaction history of the patient  
""")
    back_to_main("back_main17")

def AT():
    st.markdown("""
### 🧪 Lab Services Instructions

🔹 Go to the **Lab Services** section  
🔹 Click on **Add Test** in the top right corner  
🔹 Fill in the required test details  

🔹 While filling details, you will see a **Type** field with two options:  
   - **One Time**  
   - **Package**  

🔹 If you select **Package**, enter the number of tests.  
   - The total amount will be automatically calculated in the billing section  
   - You can either keep the auto-generated total or modify it manually  

🔹 Click on **Submit** to save  
""")
    back_to_main("back_main18")

def TL():
    st.markdown("""
### 🧪 Lab Services Instructions

🔹 Go to the **Lab Services** section  
🔹 View the list of available tests  
🔹 Check the test details from the list  
""")
    back_to_main("back_main19")

def RA():
    st.markdown("""
### ✅ Report Approval Instructions

🔹 Go to **Dashboard**  
🔹 Click on **Waiting for Approval**  
🔹 Approve the request  
""")
    back_to_main("back_main21")

# =============================================
# IPD FEATURE PAGES
# =============================================
def OT():
    st.markdown("""
### 🎟️ OT Booking Instructions
🔹 Go to the **OT Page**  
🔹 Click on **Book OT** (top right corner)  
🔹 Fill in the required details  
🔹 Submit the form to book the OT  
""")
    back_to_main("back_main22")

def Admit():
    st.markdown("""
### 🛏️ Admit Patient Instructions
🔹 Go to the **Home Page**  
🔹 Click on **Admit Patient** (top right corner)  
🔹 Fill in the required details  
🔹 Submit the form to admit the patient  
""")
    back_to_main("back_main23")

def Reschedule():
    st.markdown("""
### 🧾 OT Reschedule Instructions
🔹 Go to the **OT Page**  
🔹 View the list of all OT bookings  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Reschedule**  
🔹 Choose the new **date and time**  
🔹 Submit the form to reschedule the OT booking  
""")
    back_to_main("back_main24")

def Registration_form():
    st.markdown("""
### 🏠 Patient Registration Form Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 At the end of each patient row, click on the **📄 File icon**  
🔹 The registration form will open  
🔹 View or verify the patient details  
""")
    back_to_main("back_main26")

def Prescription():
    st.markdown("""
### 💊 Prescription View Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Prescription**  
🔹 The prescription details will open in a new page  
""")
    back_to_main("back_main27")

def Upload():
    st.markdown("""
### 📁 File Upload Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Files**  
🔹 Choose the file to upload  
🔹 Submit the form to upload the file  
""")
    back_to_main("back_main28")

def Assign_Doctor():
    st.markdown("""
### 📝 Assign Doctor Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Assign Doctor**  
🔹 Choose the doctor to assign  
🔹 Submit the form to assign the doctor  
""")
    back_to_main("back_main29")

def Transfer():
    st.markdown("""
### 🔄 Transfer Patient Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Transfer**  
🔹 Choose the new department or ward  
🔹 Submit the form to transfer the patient  
""")
    back_to_main("back_main30")

def cancel_appointment():
    st.markdown("""
### ❌ Cancel Appointment Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Cancel Appointment**  
🔹 Confirm the cancellation  
""")
    back_to_main("back_main31")

def Discharge():
    st.markdown("""
### 🏠 Discharge Patient Instructions

🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the patient row  
🔹 Select **Discharge Summary**                  
&nbsp;&nbsp;&nbsp;&nbsp;• Choose the **date and time**  
&nbsp;&nbsp;&nbsp;&nbsp;• Select a **template**  
&nbsp;&nbsp;&nbsp;&nbsp;• Fill in the form with accurate details  
🔹 Click **Submit** to discharge the patient  
🔹 Then Discharge Summary will be generated 
""")
    back_to_main("back_main32")

def consent_form():
    st.markdown("""
### 📁 Consent Form Upload Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Upload Consent Form**  
🔹 Choose the consent form to upload  
🔹 Submit the form to upload the consent form  
""")
    back_to_main("back_main33")

def schedule_consultation():
    st.markdown("""
### 📅 Schedule Consultation Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Schedule Consultation**  
🔹 Choose the date and time for the consultation  
🔹 Submit the form to schedule the consultation  
""")
    back_to_main("back_main34")

def visitor_id():
    st.markdown("""
### 🪪 Visitor ID Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Visitor ID**  
🔹 View, download, or print the Visitor ID  
""")
    back_to_main("back_main35")

def Add_service():
    st.markdown("""
### ➕ Add Service Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Billing History** → then **Add Service**  
🔹 Choose the service to add  
🔹 Submit the form to add the service  
""")
    back_to_main("back_main36")

def billing_history():
    st.markdown("""
### 🧾 Billing History Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Billing History**  
🔹 View the billing history of the patient  
""")
    back_to_main("back_main37")

def Download_invoice():
    st.markdown("""
### 📜 Download Invoice Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Final Billing**  
🔹 Click on the **Invoice** button to download  
""")
    back_to_main("back_main38")

def Pay_Bill():
    st.markdown("""
### 💳 Pay Bill Instructions  
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Final Billing**  
🔹 Click on the **Pay Bill** button to proceed with payment  
""")
    back_to_main("back_main39")

def View_certificate():
    st.markdown("""
### 👁️ View Certificate Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **View Certificate**  
🔹 The certificate will open in a new page  
""")
    back_to_main("back_main40")

def old_patient_linking():
    st.markdown("""
### ♻️ Old Patient Linking Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Old Patient Linking**  
🔹 Verify the **ABHA ID**  
🔹 Submit the form to link the old patient record  
""")
    back_to_main("back_main41")

def Update_Admission():
    st.markdown("""
### ⬆️ Update Admission Instructions
🔹 Go to the **Home Page**  
🔹 View the list of all patients  
🔹 Click on **⋮** at the end of the row  
🔹 Select **Update Admission**  
🔹 Update the required details and submit  
""")
    back_to_main("back_main42")

def Nurse_notes():
    st.markdown("""
### 👩‍⚕️ Nurse Notes Instructions
🔹 Go to the **Home Page**  
🔹 View the list of patients  
🔹 Identify patients in **Admitted Status**  
🔹 Click on **⋮ (three vertical dots)** at the end of the row  
🔹 Select **Nurse Notes**  
🔹 Fill in the required details  
🔹 Click **Submit** to save the nurse notes  
""")
    back_to_main("back_main43")

# =============================================
# PHARMACY PAGES
# =============================================
def New_Bill():
    st.markdown("""
### 💊 Generate Pharmacy Bill Instructions

🔹 Go to the **Pharma Tab**  
🔹 On the **Dashboard Page**, locate the **New Bill** button at the top right  
🔹 Click on **New Bill** to create a new bill  
🔹 Enter the **Medicine Name**, **Quantity**, and **Discount**  
🔹 After entering details, you can:  
&nbsp;&nbsp;&nbsp;&nbsp;✔️ Save the bill  
&nbsp;&nbsp;&nbsp;&nbsp;🗑️ Delete the bill  
&nbsp;&nbsp;&nbsp;&nbsp;💳 Pay the bill  
🔹 Use the buttons available at the bottom of the page to complete the action  
""")
    back_to_main("back_main44")

def Add_stock():
    st.markdown("""
### 📦 Stock Management Instructions

🔹 Go to the **Dashboard**  
🔹 Click on the **Add Stock** button at the top right  

🔹 You will see two options:  
    • **Add Stock** – Use this to update stock for existing items  
    • **Add New Stock** – Use this to add a completely new item  

🔹 Select the required option  
🔹 Fill in all the necessary fields on the page  
🔹 Click **Save** to add or update the stock  
""")
    back_to_main("back_main45")

def Modify_stock():
    st.markdown("""
### 📦 Stock Management Instructions

🔹 Go to the **Dashboard**  
🔹 You will see the list of all stock items  

🔹 At the end of each row, you will find three buttons along with **Expiry date**:   
    • **View Stock** – View detailed information of the stock  
    • **Edit Stock** – Modify the stock details            
    • **Delete Stock** – Remove the stock from the list  

🔹 Click the required button to perform the desired action  
""")
    back_to_main("back_main46")

def Billing():
    st.markdown("""
### 💳 Billing Instructions

🔹 Go to the **Billing** section  
🔹 View the list of bills based on date  
🔹 At the end of each row, you will find the following options:  
 1️⃣ **Pay Invoice**  
    → Used to view or complete payment for the bill  

 2️⃣ **Return Invoice**  
    → Used to generate a return bill  

 3️⃣ **View PDF**  
    → Used to see the bill in PDF format and print it  

 4️⃣ **Prescription**  
    → Used to view the PDF of prescribed medicines and patient details  
""")
    back_to_main("back_main47")

def Indent_Management():
    st.markdown("""
### 📦 Indent Management Instructions  
🔹 Go to the **Pharmacy Indent** Page 
🔹 Fill in all the required details   
🔹 Click on the **Add Item** button    

✅ The indent will be added successfully  
🔹 Go to the **Indent Management** page  
🔹 Select the **Store**  
🔹 Choose the **Date**  

🔹 Based on your selection, you can view:  
    • 📋 **Indent Item Details**  
    • 🕒 **Indent History**  
    • 📍 **Indent Tracking**

🔹 Only Authorised users can  **Approves the Indent**.                

✅ This helps you monitor and manage indent activities efficiently
""")
    back_to_main("back_main48")

def Store_Transfer():
    st.markdown("""
### 🔄 Store Transfer Instructions 
                
🔹 Go to the **Stores** section    
🔹 You can view the list of all available stores    

🔹 At the end of each row:    
    • Click the **Edit (✏️) icon** to modify the store name   

🔹 At the top right corner:    
    • Click on **Add Store** to create a new store    
    • Enter the required details and save              

🔹 Go to the **Store Transfer** page    
🔹 At the top right, you will find **Store Transfer** and **Download** buttons    
🔹 Click on **Store Transfer**    
🔹 Fill in the required details:  
    - From Store   
    - To Store    
    - Select Medicine    

🔹 Click on **Add Store** to complete the transfer    
🔹 Use the **Download** button to download the Store Transfer report   
""")
    back_to_main("back_main49")

def Medicine():
    st.markdown("""
### 💊 Medicine Management Instructions  

🔹 Go to the **Medicine** page    
🔹 You can see the **list of medicines**    
🔹 At the end of each row:  
 • Click the **Edit (✏️) icon** to update medicine details  

🔹 At the top right:  
 • Click the **Add Medicine** button  
 • Fill in the required details  
 • Click **Save/Add** to add a new medicine       
""")
    back_to_main("back_main50")

def Online_Prescription():
    st.markdown("""
### 💊 Issue by Online RX Instructions  

🔹 Go to the **Issue by Online RX** page    
🔹 You will see the **list of prescriptions**      
 • Medicines prescribed by the doctor in OPD will appear here    

🔹 Click on a prescription to view details    
🔹 The pharmacist should:   
 • Enter the **issued quantity**  
 • Click on **Submit** to complete the process  
""")
    back_to_main("back_main51")


# =============================================
# ADMIN FEATURE PAGES
# =============================================
def admin_clinics():
    st.markdown("""
### 🏥 Clinic Management Instructions

🔹 Go to the **Clinic** page  

🔹 At the top right:  
   • Click on **Add Clinic**  

🔹 By clicking on it:  
   • Fill in the required clinic details  
   • Select permissions and services  
   • Click **Submit** to add the clinic  

🔹 You will see a **list of clinics**  

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify clinic details  
   • After making changes, click **Submit** to save updates  
""")
    back_to_admin_main("back_admin_Clinics")

def admin_users():
    st.markdown("""
### 👥 User & Role Management Instructions

🔹 Go to the **Users** page  

🔹 You will see two sections:  
   • **Roles**  
   • **Users**  

🔹 In the **Roles** section:  
   • At the top right, click on **Add Role**  
   • Enter details such as **Role Name**, **Status**, and **Max Discount**  
   • Click **Submit** to create the role  
   • Click **Edit (✏️)** to modify or **Delete (🗑️)** to remove a role  

🔹 In the **Users** section:  
   • At the top right, click on **Add User**  
   • Fill in required fields such as personal details, permissions, and services  
   • Click **Submit** to add the user  
   • Click **Edit (✏️)** to update or **Delete (🗑️)** to remove a user  
""")
    back_to_admin_main("back_admin_Users")

def admin_messages():
    st.markdown("""
### 💬 Message Settings Instructions

🔹 Go to the **Messages** page  

🔹 At the top right:  
   • Click on the **Settings** button  

🔹 By clicking on it:  
   • Enter the **Clinic Name**, **Username**, and **API Key**  
   • Enable or disable **Follow-up**, **Appointment**, and **Prescription** options  
   • Click **Submit** to save the message settings  

🔹 You will see a **list of clinics**  

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify settings  
   • Click **Delete (🗑️)** to remove an entry  

🔹 While editing, you can:  
   • Enable or disable **Follow-up**, **Appointment**, and **Prescription** options  
   • Update the **Username** and **API Key**  

🔹 Click **Submit** to save your changes  
""")
    back_to_admin_main("back_admin_Messages")

def admin_PT():
    st.markdown("""
### 📄 Prescription Template Instructions

🔹 Go to the **Prescription** page

🔹 At the top right:  
• Click **Create Template** to add a new template with your own customization

🔹 You can view the **list of templates**

🔹 At the end of each row:  
• Click **Edit (✏️)** to modify a template  
• Click **Delete (🗑️)** to remove a template
""")
    back_to_admin_main("back_admin_PT")

def admin_PDFT():
    st.markdown("""
### 📄 PDF Template Instructions

🔹 Go to the **PDF** page   
🔹 At the top right:    
    • Click **Create Template** to add a new template by own customization 
                             
🔹 You can view the **list of templates**

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify a template    
   • Click **Delete (🗑️)** to remove a template  
""")
    back_to_admin_main("back_admin_PDFT")

def admin_Temp():
    st.markdown("""
### 🧾 Template Page Instructions

🔹 Go to the **Template** page   

🔹 At the top right:  
   • Click on **New Template**  

🔹 By clicking on it:  
   • You can create a **new template**  

🔹 Fill in the required details and save                   

🔹 You will see a **list of templates**  

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify a template  
   • Click **Delete (🗑️)** to remove a template  
""")
    back_to_admin_main("back_admin_Temp")

def admin_RD():
    st.markdown("""
### 👨‍⚕️ Referral Doctor Page Instructions

🔹 Go to the **Referral Doctor** page  
🔹 At the top right:  
   • Click on **Add Doctor**  

🔹 By clicking on it:  
   • Enter the required details  
   • Click **Submit** to add the doctor to the list  

🔹 You will see a **list of doctors with their details**  

🔹 At the end of each row:  
   • Click **View (👁️)** to see details  
   • Click **Edit (✏️)** to modify doctor information  
   • Click **Delete (🗑️)** to remove the doctor  
""")
    back_to_admin_main("back_admin_RD")

def admin_QR():
    st.markdown("""
### 🔳 QR Code Page Instructions

🔹 Go to the **QR Code** page

🔹 At the top right:  
   • Click **Generate QR**  

🔹 By clicking on it:  
   • You can add a new user and generate a QR code                  

🔹 You will see a **list of users**  

🔹 At the end of each row:  
   • Click **View (👁️)** to see the QR code  
   • Click **Edit (✏️)** to modify user information and update the QR code  
   • Click **Delete (🗑️)** to remove the user from the list  
""")
    back_to_admin_main("back_admin_QR")

def admin_UPI():
    st.markdown("""
### 🧾 Patient Upload Instructions

🔹 Go to the **Patient Upload** page  

🔹 You will see an **Upload button** in the middle of the page  

🔹 By clicking on it:  
   • You can enter patient personal information such as:  
     - Name, Mobile Number, Gender, Email  
     - Occupation, Address, Marital Status  

🔹 You can also upload a **CSV file** containing patient details  

🔹 Click **Upload** to submit and save the patient information  

🔹 To view the list of patients:  
   • Go to the **Patient Data** page  

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify patient details  
   • Click **Delete (🗑️)** to remove the patient  
""")
    back_to_admin_main("back_admin_UPI")

def admin_OT():
    st.markdown("""
### 🏥 OT Creation Instructions

🔹 Go to the **OT Creation** page  
🔹 At the top right:  
   • Click on **OT Creation**  

🔹 By clicking on it:  
   • Enter the **OT Name** and **Cost**  
   • Click **Submit** to create a new OT    

🔹 You will see a **list of OTs with their cost**  

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify OT details  
   • Click **Delete (🗑️)** to remove the OT  
""")
    back_to_admin_main("back_admin_OT")

def admin_Reports():
    st.markdown("""
### 📊 Reports Page Instructions

🔹 Go to the **Reports** page  

🔹 You will see buttons for different modules:  
   • **OPD Reports**  
   • **IPD Reports**  
   • **Pharmacy Reports**  
   • **Lab Reports**  
   • **Clinic Reports**  

🔹 After selecting a module:  
   • You will see different report options related to that module  

🔹 Select a report:  
   • Enter the required fields  

🔹 Based on your selection:  
   • You can view the statistics for the chosen report  
""")
    back_to_admin_main("back_admin_Reports")

def admin_UHID():
    st.markdown("""
### 🆔 UHID Configuration Instructions

🔹 Go to the **UHID Config** page  
               
🔹 At the top right:  
   • Click on **Add UHID**  

🔹 By clicking on it:  
   • Select the **Clinic Name**  
   • Enter the **UHID** and **Starting Number**  
   • Click **Save** to create and store the UHID configuration                 

🔹 You will see a **list of UHIDs**  

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify UHID details  
   • You can update the information provided during creation, such as the **Clinic Name**  
""")
    back_to_admin_main("back_admin_UHID")

def admin_IPD():
    st.markdown("""
### 🏥 IPD Management Instructions

🔹 Go to the **IPD** page  

🔹 You will see options such as:  
   • **Block**  
   • **Floors**  
   • **Department**  
   • **Wards**  

🔹 By clicking on these options:  
   • You can add or edit the respective details  

🔹 Go to the **Beds** section:  
   • You will see a list of beds  

🔹 At the end of each row:  
   • Click **Edit (✏️)** to modify bed details  
   • Click **Delete (🗑️)** to remove the bed  

🔹 At the top right:  
   • Click on **Add Bed**  

🔹 By clicking on it:  
   • Fill in the required fields  
   • Click **Submit** to add the bed to the list  
""")
    back_to_admin_main("back_admin_IPD")


# =============================================
# NAVIGATION CONTROLLER
# =============================================
step = st.session_state.step

# --- Module & Role flow ---
if step == "module":
    module_selection()
elif step == "role":
    role_selection()
elif step == "main":
    main_menu()

# --- Admin flow ---
elif step == "admin_main":
    admin_main()
elif step == "admin_Clinics":
    admin_clinics()
elif step == "admin_Users":
    admin_users()
elif step == "admin_Messages":
    admin_messages()
elif step == "admin_PT":
    admin_PT()
elif step == "admin_PDFT":
    admin_PDFT()
elif step == "admin_Temp":
    admin_Temp()
elif step == "admin_RD":
    admin_RD()
elif step == "admin_QR":
    admin_QR()
elif step == "admin_UPI":
    admin_UPI()
elif step == "admin_OT":
    admin_OT()
elif step == "admin_Reports":
    admin_Reports()
elif step == "admin_UHID":
    admin_UHID()
elif step == "admin_IPD":
    admin_IPD()

# --- OPD / LAB pages ---
elif step == "Report":
    Report()
elif step == "Availability":
    Availability()
elif step == "prescription":
    prescription()
elif step == "appointment":
    appointment()
elif step == "Token":
    Token()
elif step == "Payment_Status":
    Payment_Status()
elif step == "doctors_list":
    doctors_list()
elif step == "Editing":
    Editing()
elif step == "service":
    service()
elif step == "invoice":
    invoice()
elif step == "vitals":
    vitals()
elif step == "billing":
    billing()
elif step == "add_patient":
    add_patient()
elif step == "DR":
    DR()
elif step == "UR":
    UR()
elif step == "sp":
    sp()
elif step == "TH":
    TH()
elif step == "AT":
    AT()
elif step == "TL":
    TL()
elif step == "RA":
    RA()

# --- IPD pages ---
elif step == "OT":
    OT()
elif step == "Admit":
    Admit()
elif step == "Reschedule":
    Reschedule()
elif step == "Registration_form":
    Registration_form()
elif step == "Prescription":
    Prescription()
elif step == "Upload":
    Upload()
elif step == "assign_doctor":
    Assign_Doctor()
elif step == "Transfer":
    Transfer()
elif step == "cancel_appointment":
    cancel_appointment()
elif step == "Discharge":
    Discharge()
elif step == "consent_form":
    consent_form()
elif step == "schedule_consultation":
    schedule_consultation()
elif step == "visitor_id":
    visitor_id()
elif step == "Add_service":
    Add_service()
elif step == "billing_history":
    billing_history()
elif step == "Download_invoice":
    Download_invoice()
elif step == "Pay_Bill":
    Pay_Bill()
elif step == "View_certificate":
    View_certificate()
elif step == "old_patient_linking":
    old_patient_linking()
elif step == "Update_Admission":
    Update_Admission()
elif step == "Nurse_notes":
    Nurse_notes()

# --- Pharmacy pages ---
elif step == "New_Bill":
    New_Bill()
elif step == "Add_stock":
    Add_stock()
elif step == "Modify_stock":
    Modify_stock()
elif step == "Billing":
    Billing()
elif step == "Indent_Management":
    Indent_Management()
elif step == "Store_Transfer":
    Store_Transfer()
elif step == "Medicine":
    Medicine()
elif step == "Online_Prescription":
    Online_Prescription()
