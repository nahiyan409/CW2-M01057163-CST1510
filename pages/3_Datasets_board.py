import streamlit as st
import pandas as pd
from app.data.datasets import (
    get_all_metadata,
    create_dataset,
    update_dataset,
    delete_dataset
)

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


st.caption(
    "Manage dataset metadata including size, structure, ownership, and upload details."
)

# -------------------------------------------------
# 📥 LOAD DATA
# -------------------------------------------------
rows, cols = get_all_metadata()
df = pd.DataFrame(rows, columns=cols)

# -------------------------------------------------
# 🔍 SEARCH AND FILTERS
# -------------------------------------------------
st.subheader("🔍 Search & Filter Datasets")
st.caption(
    "Use the search box or filters to quickly locate datasets by name or uploader."
)

with st.expander("Search & Filter Options", expanded=True):

    search = st.text_input("Search (dataset name or uploader):")

    uploaded_by_filter = st.multiselect(
        "Filter by Uploaded By",
        options=sorted(df['uploaded_by'].unique()),
        default=sorted(df['uploaded_by'].unique()),
        help="Show datasets uploaded by specific users"
    )

filtered_df = df[df["uploaded_by"].isin(uploaded_by_filter)]

if search:
    s = search.lower()
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda r:
                s in str(r["name"]).lower()
                or s in str(r["uploaded_by"]).lower(),
            axis=1
        )
    ]

# -------------------------------------------------
# 📊 DATA TABLE
# -------------------------------------------------
st.subheader("📄 Dataset Records")
st.caption(
    "This table displays metadata for all datasets currently stored in the system."
)
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------------------------
# 📈 VISUAL ANALYTICS
# -------------------------------------------------
st.subheader("📈 Dataset Overview Charts")
st.caption(
    "Quick visual insights into dataset size and structure."
)

st.write("### Number of Rows per Dataset")
st.caption("Shows how large each dataset is in terms of row count.")
st.bar_chart(filtered_df.set_index("name")["rows"])

st.write("### Number of Columns per Dataset")
st.caption("Displays the structural complexity of each dataset.")
st.bar_chart(filtered_df.set_index("name")["columns"])

# -------------------------------------------------
# ➕ CREATE DATASET
# -------------------------------------------------
st.subheader("➕ Add New Dataset")
st.caption(
    "Register a new dataset by providing its structure and upload information."
)

with st.form("create_dataset_form"):
    c1, c2 = st.columns(2)

    with c1:
        dataset_id = st.number_input("Dataset ID", step=1)
        name = st.text_input("Dataset Name")

    with c2:
        rows_val = st.number_input("Number of Rows", step=1)
        cols_val = st.number_input("Number of Columns", step=1)

    uploaded_by = st.text_input("Uploaded By")
    upload_date = st.text_input("Upload Date (YYYY-MM-DD)")

    submit_create = st.form_submit_button("Create Dataset")

if submit_create:
    create_dataset(
        (dataset_id, name, rows_val, cols_val, uploaded_by, upload_date)
    )
    st.success("✅ Dataset created successfully.")
    st.rerun()

# -------------------------------------------------
# ✏️ UPDATE / DELETE DATASETS
# -------------------------------------------------
st.subheader("✏️ Edit or Delete Datasets")
st.caption(
    "Update dataset details or remove datasets that are no longer required."
)

for idx, row in filtered_df.iterrows():
    with st.expander(f"Dataset ID {row['dataset_id']} (Index {row['index']})"):

        c1, c2 = st.columns(2)

        with c1:
            new_dataset_id = st.number_input(
                "Dataset ID",
                value=row["dataset_id"],
                step=1,
                key=f"ds_id_{row['index']}"
            )
            new_name = st.text_input(
                "Dataset Name",
                value=row["name"],
                key=f"name_{row['index']}"
            )
            new_rows = st.number_input(
                "Rows",
                value=row["rows"],
                step=1,
                key=f"rows_{row['index']}"
            )

        with c2:
            new_cols = st.number_input(
                "Columns",
                value=row["columns"],
                step=1,
                key=f"cols_{row['index']}"
            )
            new_uploaded_by = st.text_input(
                "Uploaded By",
                value=row["uploaded_by"],
                key=f"uploadedby_{row['index']}"
            )
            new_upload_date = st.text_input(
                "Upload Date",
                value=row["upload_date"],
                key=f"uploaddate_{row['index']}"
            )

        colA, colB = st.columns(2)

        with colA:
            if st.button("Update", key=f"update_btn_{row['index']}"):
                update_dataset(
                    row["index"],
                    (
                        new_dataset_id,
                        new_name,
                        new_rows,
                        new_cols,
                        new_uploaded_by,
                        new_upload_date,
                    )
                )
                st.success("✅ Dataset updated successfully.")
                st.rerun()

        with colB:
            if st.button("Delete", key=f"delete_btn_{row['index']}"):
                delete_dataset(row["index"])
                st.error("❌ Dataset deleted.")
                st.rerun()

