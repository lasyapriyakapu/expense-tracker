import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import date
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* -------------------------------------------------------
   IMPORT FONT
------------------------------------------------------- */

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');


/* -------------------------------------------------------
   GLOBAL
------------------------------------------------------- */

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.18), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(236,72,153,0.16), transparent 25%),
        radial-gradient(circle at 50% 95%, rgba(16,185,129,0.13), transparent 25%),
        #f8fafc;

    min-height: 100vh;
}


/* -------------------------------------------------------
   ANIMATED BACKGROUND ORBS
------------------------------------------------------- */

.stApp::before {
    content: "";
    position: fixed;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: rgba(129,140,248,0.15);
    top: 15%;
    left: -60px;
    animation: floatOne 8s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: rgba(244,114,182,0.12);
    right: -80px;
    bottom: 10%;
    animation: floatTwo 10s ease-in-out infinite;
    z-index: 0;
    pointer-events: none;
}


/* -------------------------------------------------------
   SIDEBAR
------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #312e81 0%,
            #4f46e5 45%,
            #7c3aed 100%
        );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,0.28);
    transform: translateY(-2px);
}


/* -------------------------------------------------------
   HERO HEADER
------------------------------------------------------- */

.hero {
    position: relative;
    overflow: hidden;

    padding: 42px 35px;
    margin-bottom: 28px;

    border-radius: 30px;

    background:
        linear-gradient(
            135deg,
            #4338ca 0%,
            #6366f1 35%,
            #9333ea 65%,
            #ec4899 100%
        );

    box-shadow:
        0 20px 45px rgba(79,70,229,0.28);

    animation: heroAppear 0.9s ease-out;
}


/* Decorative circle inside hero */

.hero::before {
    content: "";
    position: absolute;

    width: 190px;
    height: 190px;

    border-radius: 50%;

    background: rgba(255,255,255,0.10);

    right: 8%;
    top: -80px;

    animation: heroCircle 6s ease-in-out infinite;
}

.hero::after {
    content: "";
    position: absolute;

    width: 100px;
    height: 100px;

    border-radius: 50%;

    background: rgba(255,255,255,0.08);

    right: 25%;
    bottom: -50px;

    animation: heroCircle 8s ease-in-out infinite reverse;
}


/* Main heading */

.hero h1 {
    position: relative;
    z-index: 2;

    margin: 0;

    font-size: 52px;
    line-height: 1.15;

    font-weight: 800;

    letter-spacing: 1px;

    color: white;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #fef3c7,
            #ffffff,
            #ddd6fe
        );

    background-size: 250% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation:
        titleShine 4s linear infinite,
        titleFloat 3s ease-in-out infinite;

    text-shadow:
        0 5px 25px rgba(255,255,255,0.25);
}


/* Subtitle */

.hero p {
    position: relative;
    z-index: 2;

    margin-top: 14px;
    margin-bottom: 0;

    color: rgba(255,255,255,0.92);

    font-size: 17px;
    font-weight: 400;

    letter-spacing: 0.4px;
}


/* Small badge */

.hero-badge {
    position: relative;
    z-index: 2;

    display: inline-block;

    margin-bottom: 15px;

    padding: 7px 14px;

    border-radius: 50px;

    background: rgba(255,255,255,0.16);

    border: 1px solid rgba(255,255,255,0.25);

    color: white;

    font-size: 13px;
    font-weight: 600;

    backdrop-filter: blur(10px);

    animation: badgePulse 2.5s ease-in-out infinite;
}


/* -------------------------------------------------------
   METRIC CARDS
------------------------------------------------------- */

.metric-card {
    position: relative;
    overflow: hidden;

    min-height: 145px;

    padding: 22px;

    border-radius: 22px;

    background: rgba(255,255,255,0.82);

    backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.8);

    box-shadow:
        0 10px 30px rgba(15,23,42,0.07);

    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease;

    animation: cardAppear 0.8s ease;
}


.metric-card:hover {
    transform: translateY(-8px) scale(1.02);

    box-shadow:
        0 20px 40px rgba(15,23,42,0.13);
}


/* Card decorative circle */

.metric-card::after {
    content: "";

    position: absolute;

    width: 90px;
    height: 90px;

    border-radius: 50%;

    right: -35px;
    bottom: -35px;

    background: rgba(99,102,241,0.07);

    transition: transform 0.4s ease;
}

.metric-card:hover::after {
    transform: scale(1.5);
}


.metric-title {
    color: #64748b;

    font-size: 14px;

    font-weight: 500;

    margin-bottom: 8px;
}


.metric-value {
    font-size: 29px;

    font-weight: 800;

    letter-spacing: 0.3px;
}


.purple {
    color: #6366f1;
}

.blue {
    color: #0ea5e9;
}

.green {
    color: #10b981;
}

.red {
    color: #ef4444;
}


/* -------------------------------------------------------
   SECTION TITLE
------------------------------------------------------- */

.section-title {
    margin-top: 30px;
    margin-bottom: 18px;

    font-size: 25px;

    font-weight: 700;

    color: #1e293b;

    animation: sectionAppear 0.7s ease;
}


/* -------------------------------------------------------
   GLASS SECTION
------------------------------------------------------- */

.glass-box {
    padding: 24px;

    border-radius: 22px;

    background: rgba(255,255,255,0.72);

    backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.85);

    box-shadow:
        0 10px 30px rgba(15,23,42,0.06);
}


/* -------------------------------------------------------
   BUTTONS
------------------------------------------------------- */

.stButton > button {
    border-radius: 13px;

    border: none;

    font-weight: 600;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;

    box-shadow:
        0 5px 15px rgba(79,70,229,0.08);
}

.stButton > button:hover {
    transform: translateY(-3px);

    box-shadow:
        0 10px 25px rgba(79,70,229,0.18);
}


/* -------------------------------------------------------
   INPUT BOXES
------------------------------------------------------- */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
}


/* -------------------------------------------------------
   DATAFRAME
------------------------------------------------------- */

[data-testid="stDataFrame"] {
    border-radius: 18px;

    overflow: hidden;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);
}


/* -------------------------------------------------------
   FOOTER
------------------------------------------------------- */

.footer {
    text-align: center;

    padding: 22px;

    margin-top: 35px;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #fdf2f8
        );

    color: #64748b;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);
}


/* -------------------------------------------------------
   ANIMATIONS
------------------------------------------------------- */

@keyframes heroAppear {

    from {
        opacity: 0;
        transform: translateY(-25px) scale(0.98);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }

}


@keyframes titleShine {

    0% {
        background-position: 0% center;
    }

    50% {
        background-position: 100% center;
    }

    100% {
        background-position: 0% center;
    }

}


@keyframes titleFloat {

    0%, 100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-3px);
    }

}


@keyframes heroCircle {

    0%, 100% {
        transform: translate(0,0) rotate(0deg);
    }

    50% {
        transform: translate(-20px,20px) rotate(30deg);
    }

}


@keyframes badgePulse {

    0%, 100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.04);
    }

}


@keyframes cardAppear {

    from {
        opacity: 0;
        transform: translateY(25px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}


@keyframes sectionAppear {

    from {
        opacity: 0;
        transform: translateX(-15px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }

}


@keyframes floatOne {

    0%, 100% {
        transform: translate(0,0);
    }

    50% {
        transform: translate(30px,-40px);
    }

}


@keyframes floatTwo {

    0%, 100% {
        transform: translate(0,0);
    }

    50% {
        transform: translate(-40px,30px);
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# JSON FILE
# =========================================================

FILE_NAME = "expenses.json"


# =========================================================
# LOAD DATA
# =========================================================

def load_expenses():

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except Exception:
        return []


# =========================================================
# SAVE DATA
# =========================================================

def save_expenses(expenses):

    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# =========================================================
# SESSION STATE
# =========================================================

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()


# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-badge">
✨ SMART PERSONAL FINANCE DASHBOARD
</div>

<h1>💰 Expense Tracker</h1>

<p>
Track your spending • Understand your habits • Manage your money smarter
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 💳 Expense Manager")

    st.markdown(
        "### Add your daily expenses"
    )

    st.divider()

    expense_date = st.date_input(
        "📅 Date",
        value=date.today()
    )

    category = st.selectbox(
        "🏷️ Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Education",
            "Entertainment",
            "Health",
            "Other"
        ]
    )

    description = st.text_input(
        "📝 Description",
        placeholder="Example: Lunch"
    )

    amount = st.number_input(
        "💰 Amount (₹)",
        min_value=0.0,
        step=10.0
    )

    st.markdown("")

    add_expense = st.button(
        "✨ Add Expense",
        use_container_width=True
    )

    if add_expense:

        if amount <= 0:

            st.error("⚠️ Please enter an amount greater than ₹0.")

        else:

            new_expense = {
                "id": str(uuid.uuid4())[:8],
                "date": str(expense_date),
                "category": category,
                "description": description if description else "No description",
                "amount": amount
            }

            st.session_state.expenses.append(new_expense)

            save_expenses(st.session_state.expenses)

            st.success("🎉 Expense added successfully!")

            st.balloons()

            st.rerun()

    st.divider()

    st.markdown("### 💡 Quick Tip")

    st.info(
        "Add expenses regularly to understand where your money goes."
    )


# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame(st.session_state.expenses)


# =========================================================
# CALCULATE METRICS
# =========================================================

if not df.empty:

    total_expense = df["amount"].sum()

    average_expense = df["amount"].mean()

    number_expenses = len(df)

    highest_expense = df["amount"].max()

else:

    total_expense = 0

    average_expense = 0

    number_expenses = 0

    highest_expense = 0


# =========================================================
# DASHBOARD CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">💰 Total Spending</div>
<div class="metric-value purple">₹{total_expense:,.2f}</div>
</div>
""", unsafe_allow_html=True)


with col2:

    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">🧾 Transactions</div>
<div class="metric-value blue">{number_expenses}</div>
</div>
""", unsafe_allow_html=True)


with col3:

    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">📊 Average Expense</div>
<div class="metric-value green">₹{average_expense:,.2f}</div>
</div>
""", unsafe_allow_html=True)


with col4:

    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">🔥 Highest Expense</div>
<div class="metric-value red">₹{highest_expense:,.2f}</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# ANALYTICS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Spending Analytics</div>',
    unsafe_allow_html=True
)


if not df.empty:

    chart_col1, chart_col2 = st.columns(2)

    # -----------------------------------------------------
    # PIE CHART
    # -----------------------------------------------------

    with chart_col1:

        category_data = (
            df.groupby("category")["amount"]
            .sum()
            .reset_index()
        )

        fig_pie = px.pie(
            category_data,
            names="category",
            values="amount",
            hole=0.58,
            title="💸 Where Your Money Goes"
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Poppins",
                size=13
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig_pie,
            width="stretch"
        )


    # -----------------------------------------------------
    # BAR CHART
    # -----------------------------------------------------

    with chart_col2:

        fig_bar = px.bar(
            category_data,
            x="category",
            y="amount",
            title="📈 Spending by Category",
            text_auto=".2f"
        )

        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Poppins",
                size=13
            ),
            xaxis_title="Category",
            yaxis_title="Amount (₹)",
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig_bar,
            width="stretch"
        )


else:

    st.markdown("""
<div class="glass-box">

<h3>🚀 Start Tracking Your Money</h3>

<p>
You don't have any expenses yet.
Use the sidebar to add your first expense and your analytics will appear here.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# EXPENSE TABLE
# =========================================================

st.markdown(
    '<div class="section-title">🧾 Your Expenses</div>',
    unsafe_allow_html=True
)


if not df.empty:

    display_df = df[
        [
            "id",
            "date",
            "category",
            "description",
            "amount"
        ]
    ].copy()

    display_df.columns = [
        "ID",
        "Date",
        "Category",
        "Description",
        "Amount (₹)"
    ]

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "📭 No expenses added yet. Add your first expense from the sidebar!"
    )


# =========================================================
# MANAGE EXPENSES
# =========================================================

if not df.empty:

    st.markdown(
        '<div class="section-title">⚙️ Manage Expenses</div>',
        unsafe_allow_html=True
    )

    manage_col1, manage_col2 = st.columns(2)


    # =====================================================
    # UPDATE
    # =====================================================

    with manage_col1:

        st.markdown("""
<div class="glass-box">
<h3>✏️ Update Expense</h3>
</div>
""", unsafe_allow_html=True)

        selected_id = st.selectbox(
            "Select expense to update",
            df["id"].tolist(),
            key="update_select"
        )

        selected_expense = next(
            item
            for item in st.session_state.expenses
            if item["id"] == selected_id
        )

        new_amount = st.number_input(
            "💰 New Amount (₹)",
            min_value=0.0,
            value=float(selected_expense["amount"]),
            step=10.0,
            key="new_amount"
        )

        update_button = st.button(
            "💾 Update Expense",
            use_container_width=True
        )

        if update_button:

            if new_amount <= 0:

                st.error("Amount must be greater than ₹0.")

            else:

                for expense in st.session_state.expenses:

                    if expense["id"] == selected_id:
                        expense["amount"] = new_amount

                save_expenses(st.session_state.expenses)

                st.success("✅ Expense updated successfully!")

                st.rerun()


    # =====================================================
    # DELETE
    # =====================================================

    with manage_col2:

        st.markdown("""
<div class="glass-box">
<h3>🗑️ Delete Expense</h3>
</div>
""", unsafe_allow_html=True)

        delete_id = st.selectbox(
            "Select expense to delete",
            df["id"].tolist(),
            key="delete_select"
        )

        delete_button = st.button(
            "🗑️ Delete Expense",
            use_container_width=True
        )

        if delete_button:

            st.session_state.expenses = [
                expense
                for expense in st.session_state.expenses
                if expense["id"] != delete_id
            ]

            save_expenses(st.session_state.expenses)

            st.success("🗑️ Expense deleted successfully!")

            st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

<h3>💰 Expense Tracker</h3>

<p>
✨ Track smarter &nbsp; • &nbsp;
📊 Analyze better &nbsp; • &nbsp;
💵 Spend wisely
</p>

<small>
Your personal finance dashboard
</small>

</div>
""", unsafe_allow_html=True)