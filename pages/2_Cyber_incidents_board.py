import streamlit as st
import pandas as pd
from app.data.cyber_incidents import *

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
# 🔓 GLOBAL SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.title("🌐 MDIP")
    st.caption("Multi-Domain Intelligence Platform")

    st.divider()

    st.write(f"👤 **User:** {st.session_state.username}")
    st.write(f"🛡️ **Role:** {st.session_state.role}")

    st.divider()

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = "user"
        st.success("You have been logged out.")
        st.rerun()


st.caption("Monitor, analyse, and manage reported cybersecurity incidents across the organisation.")

# -------------------------------------------------
# 📥 LOAD DATA
# -------------------------------------------------
rows, cols = load_cyber_incidents()
df = pd.DataFrame(rows, columns=cols)

st.subheader("🛡️ Cyber Incidents Dataset")
st.write(
    "This table displays all recorded cybersecurity incidents. "
    "You can search, filter, analyse trends, and manage incident records below."
)

# -------------------------------------------------
# 🔍 SEARCH + FILTERS
# -------------------------------------------------
with st.expander("🔍 Search & Filters", expanded=True):
    st.caption("Use the search box or filters to quickly find specific incidents.")

    search = st.text_input("Search incidents (description, category, or status):")

    col1, col2, col3 = st.columns(3)

    with col1:
        severity_filter = st.multiselect(
            "Severity",
            options=sorted(df['severity'].unique()),
            default=sorted(df['severity'].unique()),
            help="Filter incidents by severity level"
        )

    with col2:
        category_filter = st.multiselect(
            "Category",
            options=sorted(df['category'].unique()),
            default=sorted(df['category'].unique()),
            help="Filter incidents by incident category"
        )

    with col3:
        status_filter = st.multiselect(
            "Status",
            options=sorted(df['status'].unique()),
            default=sorted(df['status'].unique()),
            help="Filter incidents by current status"
        )

# Apply filters
filtered_df = df[
    (df["severity"].isin(severity_filter)) &
    (df["category"].isin(category_filter)) &
    (df["status"].isin(status_filter))
]

# Apply search
if search:
    search_lower = search.lower()
    filtered_df = filtered_df[
        df.apply(
            lambda row:
                search_lower in str(row["description"]).lower()
                or search_lower in str(row["category"]).lower()
                or search_lower in str(row["status"]).lower(),
            axis=1
        )
    ]

# -------------------------------------------------
# 📊 DATA TABLE
# -------------------------------------------------
st.write("### 📊 Incident Records")
st.caption("View, filter, and manage cybersecurity incident records in the table below.")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------------------------
# 📈 INTERACTIVE CHARTS
# -------------------------------------------------
st.subheader("📈 Interactive Analytics")
st.caption("Visual insights based on the filtered incident data.")

st.write("#### Incidents by Severity")
st.caption("Shows how incidents are distributed across severity levels.")
severity_counts = filtered_df["severity"].value_counts()
st.bar_chart(severity_counts)

st.write("#### Incidents by Category")
st.caption("Displays the number of incidents per category.")
category_counts = filtered_df["category"].value_counts()
st.bar_chart(category_counts)

if "timestamp" in df.columns:
    st.write("#### Incidents Over Time")
    st.caption("Tracks how incidents occur over time.")

    time_df = filtered_df.copy()
    time_df["timestamp"] = pd.to_datetime(time_df["timestamp"], errors="coerce")
    time_df = time_df.dropna(subset=["timestamp"])

    time_df["date"] = time_df["timestamp"].dt.date
    incidents_per_day = time_df.groupby("date").size()

    st.line_chart(incidents_per_day)

# -------------------------------------------------
# ➕ CREATE INCIDENT
# -------------------------------------------------
st.subheader("➕ Create New Incident")
st.caption("Add a new cybersecurity incident record to the system.")

with st.form("create_form"):
    c1, c2 = st.columns(2)

    with c1:
        incident_id = st.number_input("Incident ID", step=1)
        timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")

    with c2:
        severity = st.text_input("Severity")
        category = st.text_input("Category")

    status = st.text_input("Status")
    description = st.text_area("Description")

    create_submit = st.form_submit_button("Create Incident")

if create_submit:
    create_incident(
        (incident_id, timestamp, severity, category, status, description)
    )
    st.success("✅ New incident created successfully.")
    st.rerun()

# -------------------------------------------------
# ✏️ UPDATE / DELETE INCIDENTS
# -------------------------------------------------
st.subheader("✏️ Update or Delete Records")
st.caption(
    "Modify existing incident details or remove records that are no longer required."
)

for idx, row in filtered_df.iterrows():
    with st.expander(f"Incident Record ID {row['index']}"):

        u1, u2 = st.columns(2)

        with u1:
            new_incident_id = st.number_input(
                f"Incident ID ({row['index']})",
                value=row["incident_id"],
                step=1,
                key=f"incident_id_{row['index']}"
            )

            new_timestamp = st.text_input(
                "Timestamp",
                value=row["timestamp"],
                key=f"timestamp_{row['index']}"
            )

            new_severity = st.text_input(
                "Severity",
                value=row["severity"],
                key=f"severity_{row['index']}"
            )

        with u2:
            new_category = st.text_input(
                "Category",
                value=row["category"],
                key=f"category_{row['index']}"
            )

            new_status = st.text_input(
                "Status",
                value=row["status"],
                key=f"status_{row['index']}"
            )

        new_description = st.text_area(
            "Description",
            value=row["description"],
            key=f"description_{row['index']}"
        )

        colA, colB = st.columns(2)

        with colA:
            if st.button("Update", key=f"update_btn_{row['index']}"):
                update_incident(
                    row["index"],
                    (
                        new_incident_id,
                        new_timestamp,
                        new_severity,
                        new_category,
                        new_status,
                        new_description
                    )
                )
                st.success("✅ Record updated successfully.")
                st.rerun()

        with colB:
            if st.button("Delete", key=f"delete_btn_{row['index']}"):
                delete_incident(row["index"])
                st.error("❌ Record deleted.")
                st.rerun()
