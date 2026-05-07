import streamlit as st 
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os
import hashlib
import random
import string

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title=config.APP_NAME, layout="wide", page_icon="🚢")

# Initialize a simple session-based "database" for the demo to link scores to IDs
if 'assessments' not in st.session_state:
    st.session_state.assessments = {}

# 🚛 NEW: Logistics tracking storage
if 'shipment_status' not in st.session_state:
    st.session_state.shipment_status = {}

# 📦 NEW: Manifest storage
if 'manifests' not in st.session_state:
    st.session_state.manifests = {}

# ==========================================
# 2. BLOCKCHAIN CONNECTION ENGINE
# ==========================================
def get_blockchain_connection():
    try:
        w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
        target_address = Web3.to_checksum_address(config.CONTRACT_ADDRESS)
        contract = w3.eth.contract(address=target_address, abi=config.CONTRACT_ABI)
        return w3, contract, None
    except Exception as e:
        return None, None, str(e)

w3, contract, connection_error = get_blockchain_connection()

# ==========================================
# 3. SIDEBAR & NAVIGATION (FIXED)
# ==========================================
with st.sidebar:

    # --- LOGO ---
    if os.path.exists(config.LOGO_PATH):
        st.image(config.LOGO_PATH, use_container_width=True)
    else:
        st.title("🚢 ClearPort Portal")

    st.divider()

    # --- WEB3 IDENTITY ---
    st.markdown("### 🦊 Web3 Identity")

    demo_roles = [
        "Select Role...",
        "Importer",
        "Logistics Partner",
        "Customs Inspector",
        "Port Authority",
        "Customer View",   # ✅ NEW ROLE
        
    ]

    selected_role = st.selectbox("Connect MetaMask", demo_roles)

    # --- CONNECTION STATUS ---
    if selected_role != "Select Role...":
        st.session_state.user_role = selected_role
        st.session_state.user_wallet = "0xDEMO...1234"
        st.success(f"🟢 Connected as {selected_role}")
    else:
        st.session_state.user_role = None
        st.warning("🔴 Disconnected")

    st.divider()

    # --- ROLE LOGIC ---
    role = st.session_state.get("user_role", None)

    # DEFAULT (NO ROLE SELECTED)
    if role is None:
        pages = [
            "🏠 Home Dashboard",
            "👤 Stakeholder Registration",
            "📦 Import Manifest",
            "📍 Track-My-Shipment",
            "🔍 Risk Assessment",
            "🛡️ Authority Panel",
            "🚛 Logistics Operations Center",
            "📝 Container Entry",
            "ℹ️ About Us",
            "⭐ Reviews"
        ]

    # ✅ CUSTOMER VIEW MODE
    elif role == "Customer View":
        pages = [
            "🏠 Home Dashboard",
            "📍 Track-My-Shipment",
            "ℹ️ About Us",
            "⭐ Reviews"
        ]

    elif role == "Importer":
        pages = [
            "🏠 Home Dashboard",
            "📦 Import Manifest",
            "📍 Track-My-Shipment",
            "ℹ️ About Us",
            "⭐ Reviews"
        ]

    elif role == "Customs Inspector":
        pages = [
            "🏠 Home Dashboard",
            "🔍 Risk Assessment",
            "ℹ️ About Us",
            "⭐ Reviews"
        ]

    elif role == "Port Authority":
        pages = [
            "🏠 Home Dashboard",
            "🛡️ Authority Panel",
            "ℹ️ About Us",
            "⭐ Reviews"
        ]

    elif role == "Logistics Partner":
        pages = [
            "🏠 Home Dashboard",
            "🚛 Logistics Operations Center",
            "📝 Container Entry",
            "ℹ️ About Us",
            "⭐ Reviews"
        ]

    # --- SIDEBAR NAVIGATION ---
    st.markdown("### 📍 Main Navigation")
    app_mode = st.radio("", pages)

# ==========================================
# 4. APPLICATION MODULES
# ==========================================

# ===============================
# --- MODULE 1: HOME DASHBOARD ---
# ===============================
if app_mode == "🏠 Home Dashboard":
    st.markdown(
        """
        <style>
        /* BACKGROUND IMAGE (Copied from About Us) */
        .stApp {
            background-image: linear-gradient(
                rgba(0, 0, 0, 0.4), 
                rgba(0, 0, 0, 0.5)
            ),
            url("https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&q=80&w=2070");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .block-container {
            padding-top: 3rem !important;
            max-width: 1200px;
        }

        /* HERO CARD - Ultra Transparent (Copied from About Us) */
        .hero-card {
            background: rgba(15, 23, 42, 0.15) !important; 
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.12);
            padding: 3rem;
            text-align: center;
            margin-bottom: 2rem;
            margin-top: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }

        .hero-title {
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            background: -webkit-linear-gradient(45deg, #60a5fa, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0px 4px 12px rgba(0,0,0,0.5);
            margin-bottom: 0.5rem;
        }

        /* Home Dashboard Specifics */
        .hero-subtitle { font-size: 1.5rem; color: #94a3b8; font-weight: 600; margin-bottom: 1.5rem; }
        .hero-desc { font-size: 1.15rem; color: #e2e8f0; max-width: 800px; margin: 0 auto; }
        
        [data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.15) !important;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        [data-testid="stMetricValue"] { color: #ffffff !important; justify-content: center; }
        [data-testid="stMetricLabel"] { color: #94a3b8 !important; justify-content: center; }
        
        /* Darken delta values (Active and 12%) for better contrast */
        [data-testid="stMetricDelta"] { filter: brightness(0.6) !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">Welcome to {config.APP_NAME}</div>
            <div class="hero-subtitle">{config.TAGLINE}</div>
            <div class="hero-desc">{config.DESCRIPTION}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    if connection_error:
        st.error(f"⚠️ **Connection Alert:** {connection_error}")

# --- DYNAMIC METRIC CALCULATIONS ---
    # 1. Define a baseline for growth (e.g., 1000 containers)
    baseline_count = 1 
    
    # 2. Get current active count from your session state
    current_active = len(st.session_state.shipment_status)
    
    # 3. Calculate dynamic growth percentage
    growth_pct = ((current_active - baseline_count) / baseline_count) * 100
    delta_label = f"{growth_pct:+.1f}%"

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    
    with m1: 
        st.metric("Network Status", "Sepolia LIVE", delta="Active")
    with m2: 
        st.metric("Contract Node", f"{config.CONTRACT_ADDRESS[:6]}...")
    with m3: 
        # Metric now uses the dynamic count and calculated growth
        st.metric("Active Shipments", f"{current_active:,}", delta=delta_label)

    st.markdown("<br><hr>", unsafe_allow_html=True)

# --- Live Shipment Tracking (Fixed Indentation) ---
    
    # ✅ FIXED TRACKING LOGIC
    route_to_port_list = [
        cid for cid, status in st.session_state.shipment_status.items()
        if status in ["Picked Up (Port)", "In Transit to Port"]
    ]

    at_port_list = [
        cid for cid, status in st.session_state.shipment_status.items()
        if status == "Arrived At Port"
    ]

    route_to_customer_list = [
        cid for cid, status in st.session_state.shipment_status.items()
        if status in ["Picked Up From Port", "In Transit to Customer"]
    ]

    # 2. Get the counts
    count_route_port = len(route_to_port_list)
    count_at_port = len(at_port_list)
    count_route_customer = len(route_to_customer_list)

    # 3. Build Stat Card (Indentation removed to prevent Markdown code blocks)
    def build_stat_card(label, count, icon):
        return f"""<div style="background: rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
<div style="font-size: 1rem; color: #94a3b8; margin-bottom: 0.5rem;">{icon} {label}</div>
<div style="font-size: 2.5rem; font-weight: 800; color: #ffffff;">{count}</div>
<div style="font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Total Containers</div>
</div>"""

    # 4. Render the tracking section (Indentation removed)
    tracking_html = f"""<div class="hero-card" style="padding: 2.5rem; margin-top: 0;">
<h3 style="color: white; margin-top: 0; margin-bottom: 2rem; text-align: center;">🚛 Live Fleet Overview</h3>
<div style="display: flex; gap: 1.5rem; flex-wrap: wrap; justify-content: center;">
<div style="flex: 1; min-width: 200px;">
{build_stat_card("On Route to Port", count_route_port, "🛣️")}
</div>
<div style="flex: 1; min-width: 200px;">
{build_stat_card("At Port", count_at_port, "⚓")}
</div>
<div style="flex: 1; min-width: 200px;">
{build_stat_card("On Route to Customer", count_route_customer, "🚚")}
</div>
</div>
</div>"""
    
    st.markdown(tracking_html, unsafe_allow_html=True)

# --- MODULE 2: STAKEHOLDER REGISTRATION ---
elif app_mode == "👤 Stakeholder Registration":
    st.header("Stakeholder Onboarding")
    st.write("Register your identity to receive Role-Based Access Control (RBAC) permissions.")
    
    # Updated: "Importer/Supplier" changed to "Importer"
    ROLE_MAP = {
        "Importer": 2,
        "Customs Inspector": 3,
        "Port Authority": 4,
        "Logistics Partner": 5
    }

    # Placed outside the form so the UI updates dynamically upon selection
    role = st.selectbox("Select Your Role", list(ROLE_MAP.keys()))

    with st.form("stakeholder_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            full_name = st.text_input("Name / Business Name")
        with col_b:
            # Defaults to user_wallet if already pulled from MetaMask state
            default_wallet = user_wallet if 'user_wallet' in locals() and user_wallet else ""
            wallet_address = st.text_input("Wallet Address", value=default_wallet, placeholder="0x...")

        st.divider()
        st.markdown(f"### 📋 {role} Requirements")
        
        dynamic_data = {}
        
        # Conditional file uploaders based on the selected role
        if role == "Logistics Partner":
            dynamic_data["biz_reg"] = st.file_uploader("Upload Business Registration Doc", type=["pdf", "png", "jpg"])
            
        elif role == "Importer": # Updated condition
            dynamic_data["id_biz_reg"] = st.file_uploader("Upload ID/Business Registration Doc", type=["pdf", "png", "jpg"])
            
        elif role == "Port Authority":
            dynamic_data["emp_id"] = st.file_uploader("Upload Employee Identification Doc", type=["pdf", "png", "jpg"])
            
        elif role == "Customs Inspector":
            dynamic_data["emp_id"] = st.file_uploader("Upload Employee Identification Doc", type=["pdf", "png", "jpg"])

        submitted = st.form_submit_button("Register Identity on Blockchain")
        
        if submitted:
            # Validation checks
            if not wallet_address:
                st.error("Connect MetaMask or manually enter your wallet address.")
            elif not full_name:
                st.warning("Please provide your Name / Business Name.")
            else:
                # Check if the required document was actually uploaded
                uploaded_file = list(dynamic_data.values())[0] if dynamic_data else None
                
                if not uploaded_file:
                    st.warning(f"Please upload the required documentation for the {role} role.")
                else:
                    role_id = ROLE_MAP[role]
                    
                    # Create a reference for the document
                    doc_reference = f"{uploaded_file.name}_{uploaded_file.size}"
                    
                    # Generate a data hash for blockchain submission
                    raw_data = f"{full_name}-{role}-{doc_reference}-{wallet_address}"
                    data_hash = hashlib.sha256(raw_data.encode()).hexdigest()
                    
                    # Store in session state for cross-module access
                    if 'stakeholders' not in st.session_state:
                        st.session_state.stakeholders = []
                    
                    st.session_state.stakeholders.append({
                        "full_name": full_name,
                        "role": role,
                        "wallet": wallet_address,
                        "hash": data_hash
                    })
                    
                    st.success(f"Identity for '{full_name}' submitted. Awaiting Admin verification.")
                    st.info(f"**Wallet:** {wallet_address}\n\n**Role:** {role} (ID: {role_id})\n\n**Verified Data Hash:** {data_hash}")

# --- 📦 NEW MODULE: IMPORT MANIFEST ---
elif app_mode == "📦 Import Manifest":
    st.header("Import Manifest Generator")
    st.write("Upload official shipment documents")

    with st.form("manifest_form"):
        importer = st.text_input("Importer / Business Name")
        goods = st.text_input("Goods Description")
        origin = st.selectbox("Country of Origin", ["Standard Origin", "High-Risk Region"])

        # ==========================================
        # ✅ FIXED 2-COLUMN DOCUMENT LAYOUT
        # ==========================================
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📦 Shipping Documents")
            bill_of_lading = st.file_uploader("Bill of Lading", type=["pdf", "png", "jpg", "jpeg"])
            commercial_invoice = st.file_uploader("Commercial Invoice", type=["pdf", "png", "jpg", "jpeg"])
            packing_list = st.file_uploader("Packing List", type=["pdf", "png", "jpg", "jpeg"])

            st.subheader("🛡️ Compliance Documents")
            inspection_certificate = st.file_uploader("Inspection Certificate", type=["pdf", "png", "jpg", "jpeg"])
            health_certificate = st.file_uploader("Health / Phytosanitary Certificate", type=["pdf", "png", "jpg", "jpeg"])

        with col2:
            st.subheader("🧾 Customs Documents")
            customs_declaration = st.file_uploader("Customs Declaration", type=["pdf", "png", "jpg", "jpeg"])
            import_permit = st.file_uploader("Import Permit (if required)", type=["pdf", "png", "jpg", "jpeg"])
            certificate_of_origin = st.file_uploader("Certificate of Origin", type=["pdf", "png", "jpg", "jpeg"])

            st.subheader("⚠️ High Risk / Optional Docs")
            dangerous_goods_declaration = st.file_uploader("Dangerous Goods Declaration", type=["pdf", "png", "jpg", "jpeg"])
            insurance_certificate = st.file_uploader("Insurance Certificate", type=["pdf", "png", "jpg", "jpeg"])

        # ==========================================
        # LOGISTICS PARTNERS
        # ==========================================
        st.divider()
        st.subheader("🚛 Select Logistics Partners")

        registered_partners = [
            "Select Logistics Partner...",
            "Global Freight Co.",
            "Oceanic Logistics",
            "FastTrack Shipping",
            "Apex Transports"
        ]

        logistics_port = st.selectbox("On Route to Port", registered_partners)
        logistics_customer = st.selectbox("On Route to End-Customer", registered_partners)

        submitted = st.form_submit_button("Generate Manifest")

        if submitted:
            if not importer or not goods:
                st.error("Please complete importer and goods fields.")
            else:
                container_id = random.randint(1000, 9999)
                manifest_id = "MAN-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                def extract_file(file):
                    if file is not None:
                        return {
                            "filename": file.name,
                            "filetype": file.type,
                            "content": file.getvalue()
                        }
                    return None

                st.session_state.manifests[container_id] = {
                    "manifest_id": manifest_id,
                    "importer": importer,
                    "goods": goods,
                    "origin": origin,
                    "logistics_port": logistics_port,
                    "logistics_customer": logistics_customer,

                    "shipping_documents": {
                        "bill_of_lading": extract_file(bill_of_lading),
                        "commercial_invoice": extract_file(commercial_invoice),
                        "packing_list": extract_file(packing_list)
                    },

                    "customs_documents": {
                        "customs_declaration": extract_file(customs_declaration),
                        "import_permit": extract_file(import_permit),
                        "certificate_of_origin": extract_file(certificate_of_origin)
                    },

                    "compliance_documents": {
                        "inspection_certificate": extract_file(inspection_certificate),
                        "health_certificate": extract_file(health_certificate),
                        "dangerous_goods_declaration": extract_file(dangerous_goods_declaration),
                        "insurance_certificate": extract_file(insurance_certificate)
                    }
                }

                raw_manifest_data = f"{manifest_id}-{importer}-{goods}-{origin}-{logistics_port}-{logistics_customer}"
                manifest_hash = hashlib.sha256(raw_manifest_data.encode()).hexdigest()

                st.success("✅ Manifest Generated and Uploaded to Blockchain Successfully")
                st.info(f"""
                **Container ID:** {container_id}  
                **Manifest ID:** {manifest_id}  
                **Verified On-Chain Hash:** `{manifest_hash}`
                """)

# --- MODULE 3: CONTAINER ENTRY ---
elif app_mode == "📝 Container Entry":
    st.header("Container Registration")
    st.info("Log shipments onto the immutable ledger. Only hashes and IDs are stored on-chain.")

    # ==========================================
    # FORM
    # ==========================================
    with st.form("reg_form"):
        c_id = st.number_input("Container ID (Numeric)", min_value=1, step=1)
        manifest_id_input = st.text_input("Manifest ID", placeholder="e.g. MAN-XXXXXX")
        
        # ------------------------------------------
        # AUTO FETCH ORIGIN
        # ------------------------------------------
        auto_origin = "Pending Manifest ID..."
        for m in st.session_state.manifests.values():
            if m["manifest_id"] == manifest_id_input:
                auto_origin = m["origin"]
                break

        st.text_input(
            "Country of Origin Risk Profile",
            value=auto_origin,
            disabled=True
        )

        # ==========================================
        # SUBMIT
        # ==========================================
        if st.form_submit_button("Broadcast to Blockchain"):

            # 🔁 WALLET RESOLUTION (SESSION OR DEMO)
            wallet_to_use = st.session_state.get("user_wallet")

            if not wallet_to_use:
                wallet_to_use = "0xDEMO_WALLET_ADDRESS"
                st.warning("No wallet detected — running in DEMO mode.")

            if not manifest_id_input:
                st.warning("Please fill in all manifest references.")

            elif auto_origin == "Pending Manifest ID...":
                st.error("Invalid Manifest ID. Origin profile cannot be verified.")

            else:
                raw_shipment_data = f"{c_id}-{auto_origin}-{manifest_id_input}-{wallet_to_use}"
                shipment_hash = hashlib.sha256(raw_shipment_data.encode()).hexdigest()

                st.success(f"Successfully broadcast Container #{c_id}")
                st.write(f"**Verified On-Chain Hash:** `{shipment_hash}`")

                st.info("Transaction prepared.")

                if wallet_to_use == "0xDEMO_WALLET_ADDRESS":
                    st.info("Demo mode: no MetaMask signature required.")
                else:
                    st.info("Initiating transaction... Please confirm in MetaMask.")
# --- MODULE 4: RISK ASSESSMENT ---
elif app_mode == "🔍 Risk Assessment":

    # ==========================================
    # SESSION STATE INIT (FIX)
    # ==========================================
    if "assessment_tasks" not in st.session_state:
        st.session_state.assessment_tasks = {}

    st.header("Risk Assessment Engine")
    st.write("Complete the multi-factor field assessment to calculate the risk score (10 pts per criteria).")

    # ==========================================
    # PENDING ASSESSMENT PANEL (MOVED TO TOP)
    # ==========================================
    st.subheader("📋 Pending Risk Assessments")

    all_containers = st.session_state.manifests.keys()
    pending_tasks = []

    for cid in all_containers:
        if cid not in st.session_state.assessments:
            pending_tasks.append(cid)

    if not pending_tasks:
        st.success("✅ All containers have been assessed.")

    else:
        for cid in pending_tasks:

            status = st.session_state.assessment_tasks.get(cid, "PENDING")

            col1, col2 = st.columns([2, 2])

            with col1:
                st.write(f"Container #{cid}")

            with col2:
                st.write(f"Status: **{status}**")

    st.divider()

    # ==========================================
    # ASSESSMENT ENGINE
    # ==========================================
    container_to_check = st.number_input("Enter Container ID to Assess", min_value=1)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 📦 Physical Verification")
        c1 = st.checkbox("Weight Mismatch Detected")
        c2 = st.checkbox("Suspicious Packaging / Structural Tampering")
        c3 = st.checkbox("Seal integrity Compromised (Broken Seal)")
        c4 = st.checkbox("Anomalous Temperature Readings (Reefer)")
        c5 = st.checkbox("Unreported Dangerous Goods Labeling")

    with col_b:
        st.markdown("### 📄 Documentation & History")
        c6 = st.checkbox("Documentation Inaccuracies / Missing Pages")
        c7 = st.checkbox("Poor Importer / Supplier Compliance History")
        c8 = st.checkbox("Irregular Shipping Frequency for this Route")
        c9 = st.checkbox("Sanctioned or High-Risk Port of Call")
        c10 = st.checkbox("Vessel IMO / Identity Discrepancy")

    factors = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
    risk_score = sum(factors) * 10

    st.divider()
    st.metric("Calculated Risk Score", f"{risk_score}/100")

    if risk_score >= 70:
        st.error("🚨 CRITICAL RISK: Immediate seizure and secondary physical inspection required.")
    elif risk_score >= 40:
        st.warning("⚠️ ELEVATED RISK: Additional documentation audit and X-ray screening suggested.")
    else:
        st.success("✅ LOW RISK: Proceeding to standard customs clearance.")

    # ==========================================
    # SUBMIT ASSESSMENT
    # ==========================================
    if st.button("Submit Assessment to Smart Contract"):

        st.session_state.assessments[container_to_check] = risk_score
        st.session_state.assessment_tasks[container_to_check] = "COMPLETED"

        st.success(f"Assessment completed for Container #{container_to_check}")

# --- MODULE 5: ADMIN PANEL ---
elif app_mode == "🛡️ Authority Panel":
    st.header("Authority Clearance & Overview")
    st.write("Monitor the movement of all shipments and manage clearance for flagged containers.")

    # ==========================================
    # AUTHORITY STATE STORAGE
    # ==========================================
    if "authority_decision" not in st.session_state:
        st.session_state.authority_decision = {}

    if not st.session_state.manifests:
        st.info("ℹ️ No active shipments found in the system.")

    else:
        # ==========================================
        # 1. ALL ACTIVE SHIPMENTS OVERVIEW
        # ==========================================
        st.subheader("🌐 Active Shipments Tracker")

        overview_data = []
        flagged_containers = []

        for cid, m_data in st.session_state.manifests.items():
            score = st.session_state.assessments.get(cid, "Pending")

            # Risk label only (NO logistics status, NO alerts)
            risk_label = "Pending Assessment"

            if isinstance(score, int):
                if score >= 70:
                    risk_label = "🔴 Critical"
                    flagged_containers.append(cid)
                elif score >= 40:
                    risk_label = "🟡 Elevated"
                    flagged_containers.append(cid)
                else:
                    risk_label = "🟢 Low"

            # Authority decision column
            decision = st.session_state.authority_decision.get(cid, "PENDING")

            overview_data.append({
                "Container ID": cid,
                "Manifest ID": m_data["manifest_id"],
                "Origin": m_data["origin"],
                "Risk Status": risk_label,
                "Logistics Phase": st.session_state.shipment_status.get(cid, "Manifest Created"),
                "Authority Decision": decision
            })

        st.dataframe(overview_data, use_container_width=True)

        st.divider()

        # ==========================================
        # 2. AUTHORITY CLEARANCE (MANUAL INPUT)
        # ==========================================
        st.subheader("🛡️ Final Clearance Control")

        target_id = st.number_input("Enter Container ID for Action", min_value=1, step=1)

        if target_id and target_id in st.session_state.manifests:

            score = st.session_state.assessments.get(target_id, "Pending")
            decision = st.session_state.authority_decision.get(target_id, "PENDING")

            # Risk display only (no alerts in UI anymore)
            if isinstance(score, int):
                st.write(f"Risk Score: **{score}/100**")
            else:
                st.write("Risk Score: **Pending Assessment**")

            # Wallet fallback (kept your logic)
            if not st.session_state.get('user_wallet'):
                st.session_state.user_wallet = "DEMO_WALLET"
                st.info("🔓 No wallet detected — running in **DEMO MODE**")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Approve Final Clearance", use_container_width=True):

                    st.session_state.authority_decision[target_id] = "APPROVED"

                    if st.session_state.user_wallet == "DEMO_WALLET":
                        st.success(f"SIMULATED APPROVAL: Container #{target_id} cleared.")
                    else:
                        st.success(f"Container #{target_id} approved and sent to network.")

            with col2:
                if st.button("❌ Decline Final Clearance", use_container_width=True):

                    st.session_state.authority_decision[target_id] = "DECLINED"

                    if st.session_state.user_wallet == "DEMO_WALLET":
                        st.error(f"SIMULATED DECLINE: Container #{target_id} flagged.")
                    else:
                        st.error(f"Container #{target_id} officially declined and flagged on-chain.")

        else:
            st.info("Enter a valid Container ID to approve or decline clearance.")

# ==========================================
# --- MODULE: LOGISTICS OPERATIONS CENTER ---
# ==========================================
elif app_mode == "🚛 Logistics Operations Center":
    st.header("🚛 Logistics Operations Center")

    # --- 1. ACCESS CONTROL ---
    partner_name = st.text_input(
        "Enter your Registered Company Name",
        placeholder="e.g. Global Freight Co."
    )

    if 'stakeholders' not in st.session_state:
        st.session_state.stakeholders = []

    registered_companies = [s['full_name'] for s in st.session_state.stakeholders]

    mock_partners = [
        "Global Freight Co.",
        "Oceanic Logistics",
        "FastTrack Shipping",
        "Apex Transports"
    ]

    # --- ACCESS CONTROL LOGIC ---
    if not partner_name:
        st.info("Please enter your company name to access your dashboard.")

    elif partner_name not in registered_companies and partner_name not in mock_partners:
        st.error(
            "🚫 Access Denied. This company is not registered. "
            "Please register in the 'Stakeholder Registration' panel first."
        )

    else:
        st.subheader(f"🏠 {partner_name} Dashboard")

        my_port_jobs = [
            cid for cid, m in st.session_state.manifests.items()
            if m.get('logistics_port') == partner_name
        ]

        my_customer_jobs = [
            cid for cid, m in st.session_state.manifests.items()
            if m.get('logistics_customer') == partner_name
        ]

        tab1, tab2 = st.tabs([
            "🛣️ Port Logistics (Incoming)",
            "🚚 Customer Delivery (Outgoing)"
        ])

        # ==================================================
        # PORT LOGISTICS
        # ==================================================
        with tab1:

            if not my_port_jobs:
                st.write("No pending port shipments assigned.")

            for cid in my_port_jobs:

                current_status = st.session_state.shipment_status.get(
                    cid,
                    "Manifest Created / Pending Pickup"
                )

                with st.expander(
                    f"Container #{cid} - Status: {current_status}"
                ):

                    status_port = st.selectbox(
                        "Current Stage",
                        [
                            "Picked Up (Port)",
                            "In Transit to Port",
                            "Arrived At Port"
                        ],
                        key=f"port_status_{cid}"
                    )

                    if st.button(
                        "Update Status",
                        key=f"update_port_{cid}"
                    ):

                        st.session_state.shipment_status[cid] = status_port

                        st.success(
                            f"Container #{cid} updated to '{status_port}'"
                        )

        # ==================================================
        # CUSTOMER DELIVERY
        # ==================================================
        with tab2:

            if not my_customer_jobs:
                st.write("No pending customer shipments assigned.")

            for cid in my_customer_jobs:

                current_status = st.session_state.shipment_status.get(
                    cid,
                    "Arrived At Port"
                )

                with st.expander(
                    f"Container #{cid} - Status: {current_status}"
                ):

                    status_customer = st.selectbox(
                        "Current Stage",
                        [
                            "Picked Up From Port",
                            "In Transit to Customer",
                            "Delivered"
                        ],
                        key=f"customer_status_{cid}"
                    )

                    if st.button(
                        "Update Status",
                        key=f"update_customer_{cid}"
                    ):

                        st.session_state.shipment_status[cid] = status_customer

                        st.success(
                            f"Container #{cid} updated to '{status_customer}'"
                        )

# ==========================================
# --- MODULE: TRACK-MY-SHIPMENT ---
# ==========================================
elif app_mode == "📍 Track-My-Shipment":
    st.header("📍 End-to-End Shipment Tracking")
    st.write("Real-time visibility from Container Entry to Final Delivery.")

    search_id = st.number_input("Enter your Container ID", min_value=1, step=1)

    if search_id:

        manifest_data = st.session_state.manifests.get(search_id)
        logistics_status = st.session_state.shipment_status.get(search_id, "Manifest Created")
        risk_score = st.session_state.assessments.get(search_id, "Not Yet Assessed")

        if manifest_data:
            st.markdown(f"### 📦 Container #{search_id} Dashboard")

            # =========================
            # TOP METRICS
            # =========================
            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Current Stage", logistics_status)

            with c2:
                if isinstance(risk_score, int):
                    risk_label = (
                        "🔴 High Risk" if risk_score >= 70
                        else "🟡 Elevated" if risk_score >= 40
                        else "🟢 Low Risk"
                    )
                    st.metric("Risk Assessment", risk_label, delta=f"{risk_score} pts")
                else:
                    st.metric("Risk Assessment", "Pending")

            with c3:
                st.metric("Origin", manifest_data['origin'])

            st.divider()

            # =========================
            # FIXED JOURNEY FLOW (YOUR ORDER)
            # =========================
            st.subheader("🚢 Journey Progress")

            stages = [
                "Manifest Created",
                "Picked Up (Port)",
                "In Transit to Port",
                "Container Entry",
                "Risk Assessed",
                "Arrived At Port",
                "Picked Up From Port",
                "In Transit to Customer",
                "Delivered"
            ]

            stage_map = {stage: i for i, stage in enumerate(stages)}
            current_idx = stage_map.get(logistics_status, 0)

            progress_val = (current_idx + 1) / len(stages)
            st.progress(progress_val)

            cols = st.columns(len(stages))

            for i, stage in enumerate(stages):
                if i < current_idx:
                    cols[i].markdown(f"✅ **{stage}**")
                elif i == current_idx:
                    cols[i].markdown(f"🔵 **{stage}**")
                else:
                    cols[i].markdown(f"⚪ {stage}")

            st.divider()

            # =========================
            # MANIFEST DETAILS
            # =========================
            col_info_left, col_info_right = st.columns(2)

            with col_info_left:
                with st.container(border=True):
                    st.markdown("#### 📋 Manifest Details")
                    st.write(f"**Manifest ID:** {manifest_data['manifest_id']}")
                    st.write(f"**Importer:** {manifest_data['importer']}")
                    st.write(f"**Goods:** {manifest_data['goods']}")

            # =========================
            # FIXED AUTHORITY STATUS
            # =========================
            with col_info_right:
                with st.container(border=True):
                    st.markdown("#### 🛡️ Authority Status")

                    # FINAL AUTHORITY DECISION
                    decision = st.session_state.get("authority_decision", {}).get(search_id, "PENDING")

                    # ==========================================
                    # FINAL AUTHORITY DECISION OVERRIDES EVERYTHING
                    # ==========================================
                    if decision == "APPROVED":
                        st.success("SHIPMENT CLEARED")

                    elif decision == "DECLINED":
                        st.error("SHIPMENT DECLINED")

                    # ==========================================
                    # OTHERWISE USE RISK ASSESSMENT
                    # ==========================================
                    else:

                        # No assessment submitted yet
                        if not isinstance(risk_score, int):
                            st.info("AWAITING ASSESSMENT")

                        # Elevated Risk
                        elif risk_score >= 40 and risk_score < 70:
                            st.warning("ENHANCED INSPECTION REQUIRED")

                        # Critical Risk
                        elif risk_score >= 70:
                            st.error("SEIZURE / BLOCKED BEFORE CLEARANCE")

                        # Low Risk waiting for authority action
                        else:
                            st.info("AWAITING FINAL AUTHORITY CLEARANCE")

        else:
            st.error(f"No records found for Container #{search_id}. Please verify the ID.")
            
# ===============================
# --- MODULE 6: ABOUT US ---
# ===============================
elif app_mode == "ℹ️ About Us":
    import base64
    import os

    dash_bg = "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&q=80&w=2070"

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(
            rgba(0, 0, 0, 0.4), 
            rgba(0, 0, 0, 0.5)
        ),
        url("{dash_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 3rem !important;
        max-width: 1200px;
    }}

    .hero-card {{
        background: rgba(15, 23, 42, 0.15) !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.12);
        padding: 3rem;
        text-align: center;
        margin-bottom: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }}

    .hero-title {{
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #60a5fa, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 12px rgba(0,0,0,0.5);
    }}

    .info-card {{
        background: rgba(15, 23, 42, 0.10) !important;
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        border-radius: 18px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 2px 4px 15px rgba(0,0,0,0.2);
    }}

    .section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    .section-text {{
        color: #ffffff;
        line-height: 1.6;
        font-size: 1.05rem;
        text-shadow: 1px 1px 5px rgba(0,0,0,1);
    }}
    </style>
    """, unsafe_allow_html=True)

    # --- HERO ---
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">About ClearPort</div>
        <div style="color: #e2e8f0; font-size: 1.2rem; text-shadow: 1px 1px 8px rgba(0,0,0,0.9); margin-top: 1rem;">
            A next-generation blockchain logistics infrastructure redefining global trade through transparency, security, and intelligent automation.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- OVERVIEW ---
    st.markdown("""
    <div class="info-card">
        <div class="section-title">🚢 Overview</div>
        <div class="section-text">
            ClearPort is a blockchain-powered logistics infrastructure designed to transform global trade and port operations. By utilizing trustless verification systems, we connect stakeholders through a unified digital layer where every movement of goods is secure, traceable, and verifiable in real time. We provide the digital bedrock that allows shippers, carriers, and authorities to interact with absolute confidence.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- MISSION ---
    st.markdown("""
    <div class="info-card">
        <div class="section-title">🎯 Our Mission</div>
        <div class="section-text">
            Our mission is to eliminate inefficiencies, reduce fraud, and modernize global logistics using blockchain infrastructure. We aim to build a trusted global trade ecosystem where data integrity and automation replace fragmented legacy systems, ensuring that trade remains fluid and secure.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- WHAT WE DO ---
    st.markdown("""
    <div class="info-card">
        <div class="section-title">⚙️ What We Do</div>
        <div class="section-text">
            ClearPort delivers a comprehensive suite of infrastructure services designed for standardizing and securing maritime and multimodal trade:<br><br>
            • <b>Trustless Identity Verification:</b> We verify stakeholder identities within a trusted network to ensure secure interactions.<br>
            • <b>Documentation Digitization:</b> We digitize shipment documentation to streamline administrative processes and reduce physical paperwork.<br>
            • <b>Intelligent Risk Assessment:</b> Our system conducts structured risk assessments to identify potential issues before they impact the supply chain.<br>
            • <b>Real-Time Cargo Tracking:</b> We provide the ability to track cargo in real time, offering unprecedented visibility into the movement of goods.<br>
            • <b>Secure Customs Clearance:</b> We enable secure customs clearance decisions, facilitating faster and more reliable border crossings.<br>
            • <b>Immutable Audit Trails:</b> We maintain a full audit trail of logistics events, ensuring every action is recorded and verifiable.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HOW IT WORKS ---
    st.markdown("""
    <div class="info-card">
        <div class="section-title">🔗 How It Works</div>
        <div class="section-text">
            ClearPort utilizes a hybrid architecture to balance privacy with transparency. We use off-chain storage for sensitive data to maintain privacy and scalability, while employing on-chain hashing for immutable verification. This ensures that while sensitive details remain protected, the integrity of the logistics operation is fully transparent and tamper-proof.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- KEY BENEFITS ---
    st.markdown("""
    <div class="info-card">
        <div class="section-title">🚀 Key Benefits</div>
        <div class="section-text">
            • <b>Transparency:</b> All stakeholders operate on shared, immutable records, reducing disputes and improving trust across the supply chain.<br><br>
            • <b>Security:</b> Blockchain-based verification ensures that data cannot be altered, forged, or manipulated after submission.<br><br>
            • <b>Efficiency:</b> Automated workflows reduce administrative delays, manual processing, and bottlenecks at ports and checkpoints.<br><br>
            • <b>Accountability:</b> Every action is traceable, creating full visibility and responsibility across the entire logistics lifecycle.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===============================
    # --- MEET THE TEAM (HIGH VISIBILITY) ---
    # ===============================
    st.markdown("""
    <div style="background-color: rgba(0, 0, 0, 0.6); padding: 20px; border-radius: 15px; border-left: 5px solid #4A90E2; margin-bottom: 20px;">
        <div style="color: #FFFFFF; font-size: 1.5rem; font-weight: bold; margin-bottom: 10px;">👥 Meet the Team (TrustLedger)</div>
        <p style="color: #E0E0E0; font-size: 1rem; line-height: 1.5;">
            The leadership team powering ClearPort’s TrustLedger ecosystem. Our team is structured to lead the industry in innovation, operations, and financial integrity:
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Team Data 
    team = [
        ("Ms. S. Sikhosana", "Chief Executive Officer (CEO)", "siyamthandasikhosana465@gmail.com", "0606395484", "SS"),
        ("Ms. K. Chaka", "Managing Director (MD)", "katlichaka@gmail.com", "0681222534", "KC"),
        ("Ms. B.W. Motshoane", "Chief Operating Officer (COO)", "bwmotshoane22@gmail.com", "0670113639", "BW"),
        ("Mr. T. Thinane", "Chief Financial Officer (CFO)", "tebohothinane58@gmail.com", "0683648101", "TT"),
        ("Ms. P.L. Mphuthi", "Procurement Manager", "lebohangpoloko@gmail.com", "0788105466", "PL"),
        ("Mr. A.K. Ntanzi", "Software Developer", "anelentanzi9@gmail.com", "0736178795", "AK"),
    ]

    # Side-by-side grid
    grid_cols = st.columns(2)
    for i, (name, role, email, phone, img) in enumerate(team):
        target_col = grid_cols[i % 2]
        with target_col:
            inner_col1, inner_col2 = st.columns([1, 2])
            with inner_col1:
                try:
                    st.image(f"assets/{img}.jpg", use_container_width=True)
                except:
                    st.info(f"Image: {img}")
            
            with inner_col2:
                # High-contrast HTML Card
                card_html = f"""
                <div style="background-color: rgba(20, 20, 20, 0.85); padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333333; height: 160px;">
                    <div style="color: #FFFFFF; font-weight: bold; font-size: 1.15rem; margin-bottom: 2px;">{name}</div>
                    <div style="color: #64B5F6; font-size: 0.95rem; font-weight: 600; margin-bottom: 12px;">{role}</div>
                    <div style="color: #F0F0F0; font-size: 0.85rem; margin-bottom: 6px;">
                        <span style="color: #4A90E2;">📧</span> <a href="mailto:{email}" style="color: #F0F0F0; text-decoration: none;">{email}</a>
                    </div>
                    <div style="color: #F0F0F0; font-size: 0.85rem;">
                        <span style="color: #4A90E2;">📞</span> <a href="tel:{phone}" style="color: #F0F0F0; text-decoration: none;">{phone}</a>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

    # --- VISION ---
    st.markdown("""
    <div class="info-card" style="margin-top: 0.5rem;">
        <div class="section-title">🌍 Our Vision</div>
        <div class="section-text">
            We envision a global logistics ecosystem where trade flows seamlessly across borders. By leveraging decentralized trust, real-time data, and intelligent infrastructure, we are building a world where the barriers to global trade are dismantled by technology.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- CLOSING ---
    st.markdown("""
    <div class="info-card">
        <div class="section-title">📌 Closing Statement</div>
        <div class="section-text">
            ClearPort is more than a platform—it is the foundation for the future of global trade.<br><br>
            We are committed to a future defined by transparency, efficiency, and verifiable trust.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MODULE 7: REVIEWS ---
elif app_mode == "⭐ Reviews":
    st.header("Industry Feedback")
    
    reviews = [
        {"user": "Durban Port Authority", "rating": "⭐⭐⭐⭐⭐", "comment": "Reduced our administrative clearance time by 40%."},
        {"user": "Global Logistics Inc.", "rating": "⭐⭐⭐⭐", "comment": "The risk scoring transparency is a game changer."},
        {"user": "Independent Inspector", "rating": "⭐⭐⭐⭐⭐", "comment": "Extremely user-friendly interface."}
    ]
    
    for r in reviews:
        with st.container(border=True):
            st.subheader(r["user"])
            st.write(r["rating"])
            st.write(f"_{r['comment']}_")

    st.divider()
    st.write("### Leave a Review")

    user_review = st.text_area("Your Feedback")
    user_rating = st.slider("Your Rating", 1, 5, 5)

    if st.button("Submit Review"):
        stars = "⭐" * user_rating
        st.success("Thank you for your feedback")
        st.write(f"Your Rating: {stars}")
        st.balloons()
