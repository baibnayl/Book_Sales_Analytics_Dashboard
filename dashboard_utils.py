import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


def _inject_styles():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.3rem;
                padding-bottom: 2rem;
                max-width: 1450px;
            }

            .dashboard-subtitle {
                color: #6b7280;
                font-size: 1rem;
                margin-top: -8px;
                margin-bottom: 1.25rem;
            }

            .section-title {
                font-size: 1.05rem;
                font-weight: 700;
                color: #111827;
                margin-bottom: 0.65rem;
            }

            .card {
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 18px 18px 14px 18px;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
                min-height: 124px;
            }

            .card-label {
                font-size: 0.82rem;
                color: #6b7280;
                font-weight: 600;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 0.03em;
            }

            .card-value {
                font-size: 1.85rem;
                font-weight: 800;
                color: #0f172a;
                line-height: 1.1;
                word-break: break-word;
            }

            .card-value-small {
                font-size: 1rem;
                font-weight: 700;
                color: #0f172a;
                line-height: 1.35;
                word-break: break-word;
            }

            .panel {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 18px;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
            }

            .note-box {
                background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                padding: 16px;
                color: #334155;
                font-size: 0.95rem;
                line-height: 1.55;
            }

            .badge-wrap {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 4px;
            }

            .badge {
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                color: #1d4ed8;
                font-size: 0.88rem;
                font-weight: 700;
            }

            .header-box {
                background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
                border-radius: 22px;
                padding: 24px 24px 18px 24px;
                margin-bottom: 1.1rem;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.18);
            }

            .header-title {
                color: white;
                font-size: 2rem;
                font-weight: 800;
                margin: 0;
                line-height: 1.15;
            }

            .header-subtitle {
                color: rgba(255,255,255,0.82);
                font-size: 1rem;
                margin-top: 8px;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 16px;
                overflow: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _load_daily_revenue_data(daily_revenue_data):
    if isinstance(daily_revenue_data, (str, Path)):
        df = pd.read_csv(daily_revenue_data)
    elif isinstance(daily_revenue_data, list):
        df = pd.DataFrame(daily_revenue_data)
    else:
        raise ValueError(
            "daily_revenue_data must be either a CSV path or a list of dictionaries."
        )

    if "date" not in df.columns or "daily_revenue" not in df.columns:
        raise ValueError(
            "daily_revenue_data must contain 'date' and 'daily_revenue' columns."
        )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["daily_revenue"] = pd.to_numeric(df["daily_revenue"], errors="coerce")
    df = df.dropna(subset=["date", "daily_revenue"]).sort_values("date")

    return df


def _format_top_5_days(top_5_days_data):
    df = pd.DataFrame(top_5_days_data).copy()

    required_cols = {"Rank", "Date", "Revenue"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"top_5_days_data is missing columns: {missing}")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
    df = df.sort_values("Rank")

    display_df = df.copy()
    display_df["Revenue"] = display_df["Revenue"].map(
        lambda x: f"${x:,.2f}" if pd.notna(x) else "-"
    )
    return display_df


def _render_card(label, value, small=False):
    value_class = "card-value-small" if small else "card-value"
    st.markdown(
        f"""
        <div class="card">
            <div class="card-label">{label}</div>
            <div class="{value_class}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_badges(ids):
    if not ids:
        return '<span class="badge">—</span>'

    return "".join([f'<span class="badge">{i}</span>' for i in ids])


def render_dashboard(page_title: str, page_subtitle: str, data: dict):
    _inject_styles()

    unique_users = data["unique_users"]
    unique_author_sets = data["unique_author_sets"]
    most_popular_authors = data["most_popular_authors"]
    best_buyer_ids = data["best_buyer_ids"]
    top_5_days_data = data["top_5_days_data"]
    daily_revenue_data = data["daily_revenue_data"]

    top_5_days_display = _format_top_5_days(top_5_days_data)
    daily_revenue_df = _load_daily_revenue_data(daily_revenue_data)

    st.markdown(
        f"""
        <div class="header-box">
            <div class="header-title">{page_title}</div>
            <div class="header-subtitle">{page_subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        _render_card("Unique Users", f"{unique_users:,}")

    with col2:
        _render_card("Unique Author Sets", f"{unique_author_sets:,}")

    with col3:
        _render_card("Most Popular Author(s)", most_popular_authors, small=True)

    with col4:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-label">Best Buyer IDs</div>
                <div class="badge-wrap">{_render_badges(best_buyer_ids)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown('<div class="section-title">Daily Revenue Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(12, 4.8))

    ax.plot(
        daily_revenue_df["date"],
        daily_revenue_df["daily_revenue"],
        linewidth=2.6,
        marker="o",
        markersize=4.5,
    )
    ax.fill_between(
        daily_revenue_df["date"],
        daily_revenue_df["daily_revenue"],
        alpha=0.10,
    )

    ax.set_title("Daily Revenue Over Time", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Revenue (USD)", fontsize=10)

    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    left_col, right_col = st.columns([1.35, 1])

    with left_col:
        st.markdown('<div class="section-title">Top 5 Days by Revenue</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.dataframe(
            top_5_days_display,
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="note-box">
                <b>Dashboard Notes</b><br><br>
                • Top 5 revenue days are displayed in <code>YYYY-MM-dd</code> format.<br>
                • Unique users were reconciled under the assumption that only one user field may change.<br>
                • Author combinations were treated as unordered sets.<br>
                • Revenue is shown in USD after normalization.<br>
                • Best buyer is represented by all linked alias IDs.
            </div>
            """,
            unsafe_allow_html=True,
        )