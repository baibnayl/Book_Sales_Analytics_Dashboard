import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def render_dashboard(page_title: str, page_subtitle: str, data: dict):
    st.title(page_title)
    st.markdown(
        f"<div style='color:#6b7280; margin-top:-10px; margin-bottom:20px;'>{page_subtitle}</div>",
        unsafe_allow_html=True
    )

    unique_users = data["unique_users"]
    unique_author_sets = data["unique_author_sets"]
    most_popular_authors = data["most_popular_authors"]
    best_buyer_ids = data["best_buyer_ids"]
    top_5_days_data = data["top_5_days_data"]
    daily_revenue_data = data["daily_revenue_data"]

    top_5_days_df = pd.DataFrame(top_5_days_data)

    daily_revenue_df = pd.DataFrame(daily_revenue_data)
    daily_revenue_df["date"] = pd.to_datetime(daily_revenue_df["date"])
    daily_revenue_df = daily_revenue_df.sort_values("date")

    top_5_days_display = top_5_days_df.copy()
    top_5_days_display["Revenue"] = top_5_days_display["Revenue"].map(lambda x: f"${x:,.2f}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Unique Users", f"{unique_users:,}")

    with col2:
        st.metric("Unique Author Sets", f"{unique_author_sets:,}")

    with col3:
        st.metric("Most Popular Author(s)", most_popular_authors)

    with col4:
        st.metric("Best Buyer IDs", ", ".join(map(str, best_buyer_ids)))

    st.divider()

    st.subheader("Daily Revenue")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(daily_revenue_df["date"], daily_revenue_df["daily_revenue"])
    ax.set_title("Daily Revenue Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    st.divider()

    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.subheader("Top 5 Days by Revenue")
        st.dataframe(
            top_5_days_display,
            use_container_width=True,
            hide_index=True
        )

    with right_col:
        st.subheader("Notes")
        st.markdown("""
        <div style="
            background-color:#f8fafc;
            border:1px solid #e5e7eb;
            border-radius:12px;
            padding:16px;
            color:#374151;
        ">
            <b>Methodology</b><br><br>
            • Top 5 revenue days are shown in <code>YYYY-MM-dd</code> format.<br>
            • Unique users were reconciled assuming only one field may change.<br>
            • Author sets were normalized as unordered sets.<br>
            • Revenue values are shown in USD.
        </div>
        """, unsafe_allow_html=True)