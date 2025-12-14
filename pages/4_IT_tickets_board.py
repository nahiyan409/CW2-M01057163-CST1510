import streamlit as st
import pandas as pd

from app.data.tickets import (
    get_all_tickets,
    get_ticket_by_id,
    create_ticket,
    update_ticket,
    delete_ticket,
)

from app.data.ai_assistant_ollama import ai_assistant

# -------------------------------------------------
# 🔐 LOGIN PROTECTION
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "user"

if not st.session_state.logged_in:
    st.error("❌ You must log in first.")
    st.stop()

# -------------------------------------------------
# 🌐 GLOBAL SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.title("🌐 MDIP")
    st.caption("Multi-Domain Intelligence Platform")

    st.divider()

    st.write(f"👤 **User:** {st.session_state.username}")
    st.write(f"🛡️ **Role:** {st.session_state.role}")

    st.divider()

    # 🤖 AI Assistant
    ai_assistant(
        context="IT Service Management Ticket Board",
        username=st.session_state.username
    )

    st.divider()

    # 🚪 Logout
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "user"
        st.success("You have been logged out.")
        st.rerun()

# -------------------------------------------------
# 📝 PAGE INTRO
# -------------------------------------------------
st.caption(
    "Track, manage, and resolve IT support tickets across the organisation."
)

# ---------------------------------------------------------
# 📄 READ — Display All Tickets
# ---------------------------------------------------------
st.subheader("📄 All Tickets")
st.caption("View all IT support tickets currently stored in the system.")

tickets = get_all_tickets()
df = pd.DataFrame(tickets)

# Remove internal SQLite index column if present
df = df.drop(columns=["index"], errors="ignore")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No tickets found in database.")

# ---------------------------------------------------------
# 📊 TICKET ANALYTICS (NEW)
# ---------------------------------------------------------
st.subheader("📊 Ticket Analytics")
st.caption(
    "Visual overview of ticket workload, urgency, and resolution progress."
)

if not df.empty:

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Tickets by Status")
        st.caption("Shows how tickets are distributed across workflow states.")
        status_counts = df["status"].value_counts()
        st.bar_chart(status_counts)

    with col2:
        st.write("### Tickets by Priority")
        st.caption("Highlights urgency levels across all tickets.")
        priority_counts = df["priority"].value_counts()
        st.bar_chart(priority_counts)

else:
    st.info("Charts will appear once tickets are available.")

# ---------------------------------------------------------
# ➕ CREATE — Admin & IT Roles
# ---------------------------------------------------------
st.subheader("➕ Create New Ticket")
st.caption("Create a new IT support ticket with priority and assignment details.")

if st.session_state.role in ("admin", "it_admin", "it_support"):

    with st.form("create_ticket_form"):
        ticket_id = st.number_input("Ticket ID", step=1)
        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Critical"]
        )
        description = st.text_area("Description")
        status = st.selectbox(
            "Status",
            ["Open", "In Progress", "Resolved", "Waiting for User"]
        )
        assigned_to = st.text_input("Assigned To")
        created_at = st.date_input("Created At")
        resolution_hours = st.number_input("Resolution Time (Hours)", step=1)

        create_submit = st.form_submit_button("Create Ticket")

    if create_submit:
        create_ticket(
            ticket_id,
            priority,
            description,
            status,
            assigned_to,
            created_at,
            resolution_hours
        )
        st.success("✅ Ticket created successfully!")
        st.rerun()
else:
    st.info("You do not have permission to create tickets.")

# ---------------------------------------------------------
# ✏️ UPDATE — Admin & IT Roles
# ---------------------------------------------------------
st.subheader("✏️ Update Ticket")
st.caption("Modify ticket priority, status, assignment, or resolution time.")

if len(df) > 0:
    selected_id = st.selectbox(
        "Select Ticket to Update",
        df["ticket_id"]
    )
    ticket = get_ticket_by_id(selected_id)

    with st.form("update_ticket_form"):
        new_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Critical"],
            index=["Low", "Medium", "High", "Critical"].index(ticket["priority"])
        )
        new_description = st.text_area(
            "Description",
            ticket["description"]
        )
        new_status = st.selectbox(
            "Status",
            ["Open", "In Progress", "Resolved", "Waiting for User"],
            index=["Open", "In Progress", "Resolved", "Waiting for User"].index(ticket["status"])
        )
        new_assigned_to = st.text_input(
            "Assigned To",
            ticket["assigned_to"]
        )
        new_resolution = st.number_input(
            "Resolution Time (Hours)",
            value=ticket["resolution_time_hours"],
            step=1
        )

        update_submit = st.form_submit_button("Save Changes")

    if update_submit:
        update_ticket(
            selected_id,
            new_priority,
            new_description,
            new_status,
            new_assigned_to,
            new_resolution
        )
        st.success("🔄 Ticket updated successfully!")
        st.rerun()
else:
    st.info("No tickets available to update.")

# ---------------------------------------------------------
# 🗑️ DELETE — Admin Only
# ---------------------------------------------------------
st.subheader("🗑️ Delete Ticket")
st.caption("Permanently remove tickets that are no longer required.")

if len(df) > 0:
    delete_id = st.selectbox(
        "Select Ticket to Delete",
        df["ticket_id"]
    )

    if st.session_state.role == "admin":
        if st.button("Delete Ticket"):
            delete_ticket(delete_id)
            st.error("❌ Ticket deleted.")
            st.rerun()
    else:
        st.warning("Only administrators can delete tickets.")
else:
    st.info("No tickets available to delete.")
