import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="E-Commerce BI Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = os.path.dirname(__file__)

COLORS = {
    "Champions": "#2ecc71",
    "Loyal Customers": "#3498db",
    "Potential Loyalists": "#9b59b6",
    "At Risk": "#e67e22",
    "Hibernating": "#e74c3c",
    "primary": "#4C78A8",
    "accent": "#F58518",
    "on_time": "#2ecc71",
    "late": "#e74c3c",
    "control": "#95a5a6",
    "treatment": "#3498db",
    "treatment_green": "#2ecc71",
}


@st.cache_data
def load_executive_summary():
    df = pd.read_csv(os.path.join(DATA_DIR, "executive_summary.csv"))
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


@st.cache_data
def load_rfm():
    return pd.read_csv(os.path.join(DATA_DIR, "customer_rfm_segments.csv"))


@st.cache_data
def load_cohort():
    return pd.read_csv(os.path.join(DATA_DIR, "cohort_retention_data.csv"))


@st.cache_data
def load_winback_test():
    return pd.read_csv(os.path.join(DATA_DIR, "ab_test_h1_reactivation.csv"))


@st.cache_data
def load_aov_test():
    return pd.read_csv(os.path.join(DATA_DIR, "ab_test_h2_aov.csv"))


@st.cache_data
def load_orders():
    df = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"], errors="coerce"
    )
    df["order_estimated_delivery_date"] = pd.to_datetime(
        df["order_estimated_delivery_date"], errors="coerce"
    )
    df["on_time"] = (
        df["order_delivered_customer_date"] <= df["order_estimated_delivery_date"]
    )
    return df


@st.cache_data
def load_reviews():
    return pd.read_csv(
        os.path.join(DATA_DIR, "olist_order_reviews_dataset.csv"),
        usecols=["order_id", "review_score"],
    )


@st.cache_data
def load_payments():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_order_payments_dataset.csv"))


@st.cache_data
def load_order_items():
    return pd.read_csv(
        os.path.join(DATA_DIR, "olist_order_items_dataset.csv"),
        usecols=["order_id", "seller_id", "price", "freight_value"],
    )


@st.cache_data
def load_sellers():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_sellers_dataset.csv"))


def tableau_js_embed(workbook_name, view_name, height=900):
    html = f"""
    <div class="tableauPlaceholder" style="position:relative; width:100%;">
      <object class="tableauViz" style="display:none;">
        <param name="host_url"           value="https%3A%2F%2Fpublic.tableau.com%2F" />
        <param name="embed_code_version" value="3" />
        <param name="site_root"          value="" />
        <param name="name"               value="{workbook_name}/{view_name}" />
        <param name="tabs"               value="no" />
        <param name="toolbar"            value="yes" />
        <param name="animate_transition" value="yes" />
        <param name="display_static_image" value="yes" />
        <param name="display_spinner"    value="yes" />
        <param name="display_overlay"    value="yes" />
        <param name="display_count"      value="yes" />
        <param name="language"           value="en-US" />
      </object>
    </div>
    <script type="text/javascript">
      var divEl  = document.querySelector(".tableauPlaceholder");
      var vizEl  = divEl.getElementsByTagName("object")[0];
      vizEl.style.width  = "1200px";
      vizEl.style.height = "{height}px";
      var s = document.createElement("script");
      s.src = "https://public.tableau.com/javascripts/api/viz_v1.js";
      divEl.parentNode.insertBefore(s, divEl);
    </script>
    """
    components.html(html, height=height + 20, scrolling=True)


# ── App header ────────────────────────────────────────────────────────────────

st.title("🛒 Brazilian E-Commerce: A Data Story")
st.caption(
    "100,000+ orders from Olist · 2016–2018 · "
    "Built by [Manvi Gawande](https://www.linkedin.com/in/manvi-gawande)"
)
st.divider()

tab_overview, tab_customers, tab_products, tab_operations, tab_experiments, tab_deep_dive = st.tabs([
    "📊 Overview",
    "👥 Customers",
    "🛍️ Products & Payments",
    "🚚 Operations",
    "🧪 Experiments",
    "🔍 Dashboards & Notebook",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 - Overview
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.header("The Business at a Glance")
    st.markdown(
        "Between 2016 and 2018, Olist connected thousands of Brazilian merchants to customers "
        "across every state in the country. This tab captures the headline numbers: total scale, "
        "growth trajectory, and the geographic footprint of where revenue comes from."
    )

    df = load_executive_summary()

    total_revenue = df["payment_value"].sum()
    total_orders = df["order_id"].nunique()
    unique_customers = df["customer_id"].nunique()
    aov = total_revenue / total_orders

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${total_revenue:,.0f}")
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("Unique Customers", f"{unique_customers:,}")
    c4.metric("Avg Order Value", f"${aov:.2f}")

    st.divider()

    st.subheader("Revenue & Order Volume Over Time")
    st.markdown(
        "Did growth compound steadily, or were there inflection points? "
        "The dual-axis chart below tracks both revenue and order count month by month."
    )

    monthly = (
        df.groupby("year_month")
        .agg(revenue=("payment_value", "sum"), orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("year_month")
    )

    trend_fig = make_subplots(specs=[[{"secondary_y": True}]])
    trend_fig.add_trace(
        go.Bar(
            x=monthly["year_month"], y=monthly["revenue"],
            name="Revenue ($)", marker_color=COLORS["primary"],
        ),
        secondary_y=False,
    )
    trend_fig.add_trace(
        go.Scatter(
            x=monthly["year_month"], y=monthly["orders"],
            name="Orders", mode="lines+markers",
            line=dict(color=COLORS["accent"]),
        ),
        secondary_y=True,
    )
    trend_fig.update_layout(
        title="Monthly Revenue & Order Volume",
        xaxis_tickangle=-45,
        height=420,
        legend=dict(orientation="h"),
    )
    trend_fig.update_yaxes(title_text="Revenue ($)", secondary_y=False)
    trend_fig.update_yaxes(title_text="Orders", secondary_y=True)
    st.plotly_chart(trend_fig, use_container_width=True)

    st.info(
        "**Key Takeaway:** Revenue grew steadily through 2017, with a sharp spike in "
        "November 2017 (Black Friday). The plateau in late 2018 signals a maturing market, and "
        "acquisition alone won't sustain growth. Retention and AOV become the next levers."
    )

    st.divider()

    st.subheader("Where Is the Revenue Coming From?")
    st.markdown(
        "São Paulo dominates by volume, but several southern states punch above their weight "
        "in AOV. The treemap below shows relative revenue share at a glance."
    )

    state_rev = (
        df.groupby("state")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
    )
    state_rev.columns = ["State", "Revenue ($)"]

    col1, col2 = st.columns(2)

    with col1:
        state_bar_fig = px.bar(
            state_rev.head(15),
            x="State", y="Revenue ($)",
            color="Revenue ($)", color_continuous_scale="Blues",
            title="Top 15 States by Revenue", height=400,
        )
        state_bar_fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(state_bar_fig, use_container_width=True)

    with col2:
        treemap_fig = px.treemap(
            state_rev, path=["State"], values="Revenue ($)",
            color="Revenue ($)", color_continuous_scale="Blues",
            title="Revenue Share by State", height=400,
        )
        st.plotly_chart(treemap_fig, use_container_width=True)

    city_rev = (
        df.groupby(["city", "state"])["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
        .head(15)
    )
    city_rev.columns = ["City", "State", "Revenue ($)"]
    city_fig = px.bar(
        city_rev.sort_values("Revenue ($)"),
        x="Revenue ($)", y="City", orientation="h",
        color="Revenue ($)", color_continuous_scale="Blues",
        title="Top 15 Cities by Revenue", height=400,
    )
    city_fig.update_layout(coloraxis_showscale=False, yaxis_title="")
    st.plotly_chart(city_fig, use_container_width=True)

    st.info(
        "**Key Takeaway:** São Paulo state accounts for ~40% of all revenue. "
        "Expansion into underrepresented states like RS and PR offers the clearest "
        "near-term geographic growth opportunity without cannibalizing existing volume."
    )

    st.divider()

    st.subheader("State Deep Dive")
    selected_state = st.selectbox("Select a state", sorted(df["state"].unique()))
    state_cities = (
        df[df["state"] == selected_state]
        .groupby("city")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
        .head(20)
    )
    state_cities.columns = ["City", "Revenue ($)"]
    city_drill_fig = px.bar(
        state_cities,
        x="City", y="Revenue ($)",
        color="Revenue ($)", color_continuous_scale="Blues",
        title=f"Top Cities in {selected_state}", height=360,
    )
    city_drill_fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-35)
    st.plotly_chart(city_drill_fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 - Customers
# ══════════════════════════════════════════════════════════════════════════════
with tab_customers:
    st.header("Who Are Our Customers?")
    st.markdown(
        "Understanding customer behavior is the foundation of sustainable growth. "
        "This section breaks down the customer base by value through RFM segmentation, "
        "then examines loyalty through cohort retention, revealing the biggest opportunity in the business."
    )

    # ── RFM ──────────────────────────────────────────────────────────────────
    st.subheader("Customer Segmentation: RFM")
    st.markdown(
        "96,096 customers were scored on **Recency** (how recently they bought), "
        "**Frequency** (how often), and **Monetary value** (how much they spent), "
        "then grouped into five actionable segments."
    )

    rfm = load_rfm()
    seg_colors = {k: COLORS[k] for k in ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Hibernating"]}

    seg_counts = rfm["Customer_Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]

    col1, col2 = st.columns([1, 1])

    with col1:
        pie_fig = px.pie(
            seg_counts, names="Segment", values="Count",
            color="Segment", color_discrete_map=seg_colors,
            title="Segment Distribution", hole=0.4,
        )
        pie_fig.update_traces(textposition="inside", textinfo="percent+label")
        pie_fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(pie_fig, use_container_width=True)

    with col2:
        seg_metrics = (
            rfm.groupby("Customer_Segment")
            .agg(
                Customers=("Customer_Unique_ID", "count"),
                Avg_Recency=("Recency_Days", "mean"),
                Avg_Frequency=("Frequency", "mean"),
                Avg_Monetary=("Monetary", "mean"),
            )
            .reset_index()
            .round(1)
        )
        seg_metrics.columns = ["Segment", "Customers", "Avg Recency (days)", "Avg Frequency", "Avg Monetary ($)"]
        st.subheader("Metrics by Segment")
        st.dataframe(
            seg_metrics.sort_values("Customers", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

    st.success(
        "**Key Takeaway:** Champions and Loyal Customers form the revenue backbone. "
        "At-Risk customers (those who have purchase history but have gone quiet) are the "
        "highest-leverage reactivation target. Jump to the **Experiments** tab to see what a "
        "20% win-back discount did to their reactivation rate."
    )

    st.divider()

    st.subheader("Recency vs Monetary Value by Segment")
    selected_segs = st.multiselect(
        "Filter Segments",
        options=rfm["Customer_Segment"].unique().tolist(),
        default=rfm["Customer_Segment"].unique().tolist(),
    )
    rfm_filtered = rfm[rfm["Customer_Segment"].isin(selected_segs)]
    sample = rfm_filtered.sample(min(5000, len(rfm_filtered)), random_state=42)

    scatter_fig = px.scatter(
        sample,
        x="Recency_Days", y="Monetary",
        color="Customer_Segment", color_discrete_map=seg_colors,
        opacity=0.5,
        labels={"Recency_Days": "Recency (days)", "Monetary": "Monetary Value ($)"},
        height=420,
    )
    scatter_fig.update_layout(legend_title="Segment")
    st.plotly_chart(scatter_fig, use_container_width=True)

    st.subheader("R Score vs F Score Heatmap")
    rfm_heatmap = rfm.groupby(["R_Score", "F_Score"]).size().reset_index(name="Count")
    pivot_rfm = rfm_heatmap.pivot(index="R_Score", columns="F_Score", values="Count").fillna(0)
    heatmap_fig = px.imshow(
        pivot_rfm,
        color_continuous_scale="Blues", text_auto=True,
        labels={"x": "F Score", "y": "R Score", "color": "Customers"},
        title="Customer Count by R and F Score", height=360,
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)

    st.divider()

    # ── Cohort & Retention ────────────────────────────────────────────────────
    st.subheader("Cohort & Retention Analysis")
    st.markdown(
        "Segmentation tells us who customers are today. Cohort analysis tells us whether they come back. "
        "Each row below is a group of customers who made their first purchase in that month, "
        "and the columns track what percentage returned in subsequent months."
    )

    cohort = load_cohort()
    cohort.columns = ["cohort_month", "month_index", "total_users"]
    cohort = cohort.sort_values(["cohort_month", "month_index"])

    cohort_sizes = cohort[cohort["month_index"] == 0].set_index("cohort_month")["total_users"]
    cohort["cohort_size"] = cohort["cohort_month"].map(cohort_sizes)
    cohort["retention_rate"] = (cohort["total_users"] / cohort["cohort_size"] * 100).round(2)

    pivot_cohort = cohort.pivot(
        index="cohort_month", columns="month_index", values="retention_rate"
    ).sort_index()

    retention_fig = px.imshow(
        pivot_cohort,
        color_continuous_scale="Blues", text_auto=".1f",
        labels={"x": "Months Since First Purchase", "y": "Cohort Month", "color": "Retention %"},
        aspect="auto", height=500,
    )
    retention_fig.update_layout(
        xaxis_title="Months Since First Purchase",
        yaxis_title="Cohort Month",
    )
    st.plotly_chart(retention_fig, use_container_width=True)

    st.subheader("Retention Curves by Cohort")
    available_cohorts = sorted(cohort["cohort_month"].unique().tolist())
    selected_cohorts = st.multiselect(
        "Select Cohorts",
        options=available_cohorts,
        default=available_cohorts[:6],
    )
    cohort_filtered = cohort[cohort["cohort_month"].isin(selected_cohorts)]
    curve_fig = px.line(
        cohort_filtered,
        x="month_index", y="retention_rate",
        color="cohort_month", markers=True,
        labels={
            "month_index": "Months Since First Purchase",
            "retention_rate": "Retention Rate (%)",
            "cohort_month": "Cohort",
        },
        height=420,
    )
    curve_fig.update_layout(yaxis_ticksuffix="%")
    st.plotly_chart(curve_fig, use_container_width=True)

    st.warning(
        "**Key Takeaway:** Only **3.12%** of customers make a repeat purchase. "
        "Retention, not acquisition, is the single biggest untapped growth lever. "
        "Even a 1 percentage point improvement in month-2 retention would meaningfully "
        "shift lifetime value across every cohort."
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 - Products & Payments
# ══════════════════════════════════════════════════════════════════════════════
with tab_products:
    st.header("What Are They Buying and How Are They Paying?")
    st.markdown(
        "Product mix reveals which categories drive the business. Payment behavior reveals "
        "customer trust and price sensitivity, which both inform where pricing or incentive changes "
        "can lift average order value."
    )

    # ── Products ──────────────────────────────────────────────────────────────
    st.subheader("Product & Category Performance")
    st.markdown(
        "Which categories generate the most revenue, and do high-revenue categories also earn "
        "the best reviews? The two charts below tell both sides of that story."
    )

    df = load_executive_summary()
    reviews = load_reviews()
    df_rev = df.merge(reviews, on="order_id", how="left")

    cat_stats = (
        df_rev.groupby("category")
        .agg(
            Revenue=("payment_value", "sum"),
            Orders=("order_id", "nunique"),
            Avg_Review=("review_score", "mean"),
        )
        .reset_index()
        .round(2)
    )
    cat_stats.columns = ["Category", "Revenue ($)", "Orders", "Avg Review Score"]

    top_n = st.slider("Show top N categories", 5, 30, 10)
    top_cats = cat_stats.nlargest(top_n, "Revenue ($)")

    col1, col2 = st.columns(2)

    with col1:
        rev_fig = px.bar(
            top_cats.sort_values("Revenue ($)"),
            x="Revenue ($)", y="Category", orientation="h",
            color="Revenue ($)", color_continuous_scale="Blues",
            title=f"Top {top_n} Categories by Revenue", height=420,
        )
        rev_fig.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(rev_fig, use_container_width=True)

    with col2:
        review_cat_fig = px.bar(
            top_cats.sort_values("Avg Review Score"),
            x="Avg Review Score", y="Category", orientation="h",
            color="Avg Review Score", color_continuous_scale="RdYlGn",
            range_color=[3, 5],
            title=f"Avg Review Score: Top {top_n} Categories", height=420,
        )
        review_cat_fig.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(review_cat_fig, use_container_width=True)

    st.info(
        "**Key Takeaway:** Health & Beauty and Watches lead in both revenue and review scores, "
        "making them ideal candidates for upsell and loyalty campaigns. Categories with high revenue but "
        "below-average reviews signal fulfillment or quality issues worth a deeper investigation."
    )

    st.subheader("Category Deep Dive")
    selected_cat = st.selectbox("Select a category", sorted(cat_stats["Category"].dropna().unique()))
    cat_row = cat_stats[cat_stats["Category"] == selected_cat].iloc[0]

    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Revenue", f"${cat_row['Revenue ($)']:,.2f}")
    cc2.metric("Orders", f"{int(cat_row['Orders']):,}")
    cc3.metric("Avg Review Score", f"{cat_row['Avg Review Score']:.2f} / 5")

    cat_trend = (
        df[df["category"] == selected_cat]
        .groupby("year_month")["payment_value"]
        .sum()
        .reset_index()
    )
    cat_trend.columns = ["Month", "Revenue ($)"]
    cat_trend_fig = px.line(
        cat_trend, x="Month", y="Revenue ($)", markers=True,
        title=f"Monthly Revenue: {selected_cat}",
    )
    cat_trend_fig.update_layout(xaxis_tickangle=-45, height=320)
    st.plotly_chart(cat_trend_fig, use_container_width=True)

    st.divider()

    # ── Payments ──────────────────────────────────────────────────────────────
    st.subheader("Payment Behavior")
    st.markdown(
        "Payment method choice reveals customer trust signals and installment appetite, "
        "both levers for conversion and AOV optimization."
    )

    payments = load_payments()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", f"{len(payments):,}")
    col2.metric("Total Payment Value", f"${payments['payment_value'].sum():,.0f}")
    col3.metric(
        "Avg Installments (Credit)",
        f"{payments[payments['payment_type'] == 'credit_card']['payment_installments'].mean():.1f}",
    )

    col_a, col_b = st.columns(2)

    with col_a:
        pay_type = payments.groupby("payment_type")["payment_value"].sum().reset_index()
        pay_type.columns = ["Payment Type", "Revenue ($)"]
        pay_type["Payment Type"] = pay_type["Payment Type"].str.replace("_", " ").str.title()
        pay_pie_fig = px.pie(
            pay_type, names="Payment Type", values="Revenue ($)", hole=0.45,
            title="Revenue Share by Payment Method", height=360,
        )
        pay_pie_fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(pay_pie_fig, use_container_width=True)

    with col_b:
        pay_count = payments.groupby("payment_type").size().reset_index(name="Transactions")
        pay_count["Payment Type"] = pay_count["payment_type"].str.replace("_", " ").str.title()
        pay_bar_fig = px.bar(
            pay_count.sort_values("Transactions", ascending=False),
            x="Payment Type", y="Transactions",
            color="Transactions", color_continuous_scale="Blues",
            title="Transaction Count by Payment Method", height=360,
        )
        pay_bar_fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(pay_bar_fig, use_container_width=True)

    st.subheader("Installment Distribution (Credit Card)")
    cc_payments = payments[payments["payment_type"] == "credit_card"]
    installment_dist = cc_payments["payment_installments"].value_counts().sort_index().reset_index()
    installment_dist.columns = ["Installments", "Count"]
    installment_fig = px.bar(
        installment_dist, x="Installments", y="Count",
        color="Count", color_continuous_scale="Blues",
        title="Credit Card Installment Choices", height=360,
        labels={"Installments": "Number of Installments", "Count": "Orders"},
    )
    installment_fig.update_layout(coloraxis_showscale=False, xaxis=dict(tickmode="linear"))
    st.plotly_chart(installment_fig, use_container_width=True)

    aov_by_type = payments.groupby("payment_type")["payment_value"].mean().reset_index()
    aov_by_type.columns = ["Payment Type", "Avg Order Value ($)"]
    aov_by_type["Payment Type"] = aov_by_type["Payment Type"].str.replace("_", " ").str.title()
    aov_pay_fig = px.bar(
        aov_by_type.sort_values("Avg Order Value ($)", ascending=False),
        x="Payment Type", y="Avg Order Value ($)",
        color="Avg Order Value ($)", color_continuous_scale="Blues",
        title="Avg Order Value by Payment Method", height=340,
    )
    aov_pay_fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(aov_pay_fig, use_container_width=True)

    st.info(
        "**Key Takeaway:** Credit card dominates both volume and value, with customers averaging "
        "3+ installments, a clear signal of upfront price sensitivity. Boleto has lower AOV but "
        "meaningful volume, indicating a distinct customer segment that may respond differently "
        "to promotions than credit card users."
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 - Operations
# ══════════════════════════════════════════════════════════════════════════════
with tab_operations:
    st.header("How Well Do We Deliver?")
    st.markdown(
        "Operational performance directly shapes review scores and repeat purchase intent. "
        "A late delivery doesn't just fail one customer; it poisons the review that future customers read. "
        "This section examines delivery reliability and the sellers driving marketplace quality."
    )

    # ── Delivery & Reviews ────────────────────────────────────────────────────
    st.subheader("Delivery Performance & Review Quality")

    orders = load_orders()
    reviews = load_reviews()

    delivered = orders[orders["order_status"] == "delivered"].dropna(
        subset=["order_delivered_customer_date", "order_estimated_delivery_date"]
    )
    on_time_pct = delivered["on_time"].mean() * 100
    late_pct = 100 - on_time_pct

    col1, col2, col3 = st.columns(3)
    col1.metric("On-Time Delivery Rate", f"{on_time_pct:.2f}%")
    col2.metric("Late Delivery Rate", f"{late_pct:.2f}%")
    col3.metric("Total Delivered Orders", f"{len(delivered):,}")

    col_a, col_b = st.columns(2)

    with col_a:
        delivery_data = pd.DataFrame({
            "Status": ["On Time", "Late"],
            "Count": [delivered["on_time"].sum(), (~delivered["on_time"]).sum()],
        })
        delivery_fig = px.pie(
            delivery_data, names="Status", values="Count", hole=0.5,
            color="Status",
            color_discrete_map={"On Time": COLORS["on_time"], "Late": COLORS["late"]},
            title="On-Time vs Late Deliveries",
        )
        delivery_fig.update_traces(textposition="inside", textinfo="percent+label")
        delivery_fig.update_layout(showlegend=False, height=360)
        st.plotly_chart(delivery_fig, use_container_width=True)

    with col_b:
        review_dist = reviews["review_score"].value_counts().sort_index().reset_index()
        review_dist.columns = ["Score", "Count"]
        review_dist["Pct"] = (review_dist["Count"] / review_dist["Count"].sum() * 100).round(2)
        score_colors = {1: "#e74c3c", 2: "#e67e22", 3: "#f1c40f", 4: "#3498db", 5: "#2ecc71"}
        review_bar_fig = px.bar(
            review_dist, x="Score", y="Count",
            color="Score", color_discrete_map=score_colors,
            text="Pct", title="Review Score Distribution",
            labels={"Score": "Review Score (1–5)", "Count": "Number of Reviews"},
            height=360,
        )
        review_bar_fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        review_bar_fig.update_layout(showlegend=False, xaxis=dict(tickmode="linear"))
        st.plotly_chart(review_bar_fig, use_container_width=True)

    days_late_series = (
        delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
    ).dt.days
    late_only = delivered[days_late_series > 0].copy()
    late_only["days_late"] = days_late_series[days_late_series > 0]

    late_fig = px.histogram(
        late_only, x="days_late", nbins=40,
        labels={"days_late": "Days Late", "count": "Orders"},
        color_discrete_sequence=[COLORS["late"]],
        title=f"Late Orders: Days Overdue ({len(late_only):,} orders)",
        height=320,
    )
    st.plotly_chart(late_fig, use_container_width=True)

    st.warning(
        "**Key Takeaway:** ~8% of orders arrive late, and late deliveries strongly correlate "
        "with 1-star reviews. Reducing late deliveries by half would meaningfully lift the "
        "platform's average review score and, with it, conversion rates for new visitors."
    )

    st.divider()

    # ── Seller Leaderboard ────────────────────────────────────────────────────
    st.subheader("Seller Performance Leaderboard")
    st.markdown(
        "Not all sellers are equal. The top 10% generate a disproportionate share of revenue "
        "and 5-star reviews. Identifying what they do differently is the playbook to uplift the long tail."
    )

    items = load_order_items()
    sellers = load_sellers()
    orders_slim = load_orders()[["order_id", "customer_id", "order_status"]]

    merged = items.merge(orders_slim, on="order_id", how="left")
    merged = merged.merge(reviews, on="order_id", how="left")

    seller_stats = (
        merged.groupby("seller_id")
        .agg(
            Items_Sold=("order_id", "count"),
            Revenue=("price", "sum"),
            Unique_Customers=("customer_id", "nunique"),
            Avg_Review=("review_score", "mean"),
            Five_Star_Reviews=("review_score", lambda x: (x == 5).sum()),
        )
        .reset_index()
        .round(2)
    )
    seller_stats = seller_stats.merge(
        sellers[["seller_id", "seller_city", "seller_state"]], on="seller_id", how="left"
    )
    seller_stats.columns = [
        "Seller ID", "Items Sold", "Revenue ($)", "Unique Customers",
        "Avg Review", "5-Star Reviews", "City", "State",
    ]
    seller_stats["Seller ID"] = seller_stats["Seller ID"].str[:8] + "..."

    sort_col = st.selectbox(
        "Sort by",
        ["Revenue ($)", "Items Sold", "Unique Customers", "5-Star Reviews", "Avg Review"],
    )
    top_n_sellers = st.slider("Show top N sellers", 10, 50, 20)
    top_sellers = seller_stats.nlargest(top_n_sellers, sort_col)

    seller_fig = px.bar(
        top_sellers.sort_values(sort_col),
        x=sort_col, y="Seller ID", orientation="h",
        color=sort_col, color_continuous_scale="Blues",
        title=f"Top {top_n_sellers} Sellers by {sort_col}",
        height=max(400, top_n_sellers * 22),
    )
    seller_fig.update_layout(coloraxis_showscale=False, yaxis_title="")
    st.plotly_chart(seller_fig, use_container_width=True)

    st.subheader("Full Leaderboard Table")
    st.dataframe(
        top_sellers.sort_values(sort_col, ascending=False).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "**Key Takeaway:** Top sellers consistently outperform on both revenue and review scores. "
        "A seller success program sharing fulfillment best practices from top performers "
        "could lift the marketplace's overall rating without adding new inventory."
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 - Experiments
# ══════════════════════════════════════════════════════════════════════════════
with tab_experiments:
    st.header("What Did We Test?")
    st.markdown(
        "Hypotheses are only worth acting on when tested rigorously. Two A/B tests were run "
        "to validate specific growth levers: one targeting customer reactivation, the other "
        "testing whether a free shipping threshold lifts order value. Both produced statistically "
        "significant results that translate directly into product and marketing decisions."
    )

    ab1 = load_winback_test()
    ab2 = load_aov_test()

    # ── Hypothesis 1 ──────────────────────────────────────────────────────────
    st.subheader("Hypothesis 1: Win-Back Discount for At-Risk Customers")
    st.markdown(
        "**The Question:** If we offer At-Risk customers (inactive for 90–180 days) a 20% discount, "
        "will a meaningful share reactivate compared to a control group that receives nothing?"
    )

    h1_reactivated = ab1[ab1["Outcome"] == "Reactivated"].set_index("Group")["Count"]
    h1_total = ab1.groupby("Group")["Count"].sum()
    h1_rate = (h1_reactivated / h1_total * 100).reset_index()
    h1_rate.columns = ["Group", "Reactivation Rate (%)"]

    ctrl_rate = h1_rate.loc[h1_rate["Group"] == "Control", "Reactivation Rate (%)"].values[0]
    trt_rate = h1_rate.loc[h1_rate["Group"] == "Treatment", "Reactivation Rate (%)"].values[0]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Control Reactivation Rate", f"{ctrl_rate:.2f}%")
        st.metric("Treatment Reactivation Rate", f"{trt_rate:.2f}%", delta=f"+{trt_rate - ctrl_rate:.2f}pp")

    with col2:
        h1_fig = px.bar(
            h1_rate, x="Group", y="Reactivation Rate (%)",
            color="Group",
            color_discrete_map={"Control": COLORS["control"], "Treatment": COLORS["treatment_green"]},
            text="Reactivation Rate (%)",
            title="Reactivation Rate by Group", height=350,
        )
        h1_fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        h1_fig.update_layout(showlegend=False, yaxis_range=[0, 12])
        st.plotly_chart(h1_fig, use_container_width=True)

    st.success(
        "**Result: Statistically Significant (p = 0.0003).** The win-back discount meaningfully "
        "improves reactivation of At-Risk customers. **Recommendation:** Roll out to the full "
        "At-Risk segment. The ROI on discount cost vs. recovered lifetime value is strongly positive."
    )

    st.divider()

    # ── Hypothesis 2 ──────────────────────────────────────────────────────────
    st.subheader("Hypothesis 2: Free Shipping Threshold on 2nd-Order AOV")
    st.markdown(
        "**The Question:** If we offer free shipping on orders over $150, will customers placing "
        "their second order spend more to cross the threshold, lifting average order value?"
    )

    h2_aov = ab2.groupby("Group")["Order_Value"].mean().reset_index()
    h2_aov.columns = ["Group", "Avg Order Value ($)"]

    ctrl_aov = h2_aov.loc[h2_aov["Group"] == "Control", "Avg Order Value ($)"].values[0]
    trt_aov = h2_aov.loc[h2_aov["Group"] == "Treatment", "Avg Order Value ($)"].values[0]
    uplift = (trt_aov - ctrl_aov) / ctrl_aov * 100

    col3, col4 = st.columns([1, 2])
    with col3:
        st.metric("Control AOV", f"${ctrl_aov:.2f}")
        st.metric("Treatment AOV", f"${trt_aov:.2f}", delta=f"+{uplift:.1f}% uplift")

    with col4:
        box_fig = px.box(
            ab2, x="Group", y="Order_Value",
            color="Group",
            color_discrete_map={"Control": COLORS["control"], "Treatment": COLORS["treatment"]},
            title="Order Value Distribution by Group", height=380,
            labels={"Order_Value": "Order Value ($)"},
        )
        box_fig.update_layout(showlegend=False)
        st.plotly_chart(box_fig, use_container_width=True)

    st.subheader("Order Value Distribution Overlay")
    dist_fig = px.histogram(
        ab2, x="Order_Value", color="Group", barmode="overlay",
        color_discrete_map={"Control": COLORS["control"], "Treatment": COLORS["treatment"]},
        opacity=0.7, nbins=60,
        labels={"Order_Value": "Order Value ($)", "count": "Frequency"},
        height=360,
    )
    dist_fig.update_layout(bargap=0.05)
    st.plotly_chart(dist_fig, use_container_width=True)

    st.success(
        "**Result: Highly Significant (p < 0.00001).** Free shipping for orders >$150 drives a "
        "~10% lift in second-order AOV. **Recommendation:** Make this a permanent feature for "
        "repeat customers. The shipping cost is more than offset by the revenue uplift."
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 - Dashboards & Notebook
# ══════════════════════════════════════════════════════════════════════════════
with tab_deep_dive:
    st.header("Dig Deeper")
    st.markdown(
        "The charts above tell the headline story. For those who want to explore the underlying "
        "data interactively or trace the full analytical pipeline, the Tableau dashboards and "
        "analysis notebook are available below."
    )

    notebook_tab, tableau_tab = st.tabs(["📓 Analysis Notebook", "📈 Tableau Dashboards"])

    with tableau_tab:
        st.caption("Interactive dashboards published on Tableau Public")

        dash1, dash2 = st.tabs([
            "E-Commerce Revenue & Geographic Distribution",
            "Customer Lifecycle & Revenue Optimization",
        ])

        with dash1:
            st.markdown(
                "Explores **revenue dynamics across Brazilian states and cities**, including "
                "geographic heatmaps, top-performing regions, and revenue trends over time."
            )
            tableau_js_embed(
                "E-commerceRevenueDynamicGeographicDistribution", "Dashboard1", height=900
            )

        with dash2:
            st.markdown(
                "Covers the **customer lifecycle**: RFM segmentation, cohort retention curves, "
                "and revenue optimization opportunities."
            )
            components.html(
                """
                <div class='tableauPlaceholder' id='viz1777522052277' style='position: relative'>
                  <noscript>
                    <a href='#'>
                      <img alt='Dashboard 1'
                        src='https://public.tableau.com/static/images/Cu/CustomerLifecycleRevenueOptimization/Dashboard1/1_rss.png'
                        style='border: none' />
                    </a>
                  </noscript>
                  <object class='tableauViz' style='display:none;'>
                    <param name='host_url'           value='https%3A%2F%2Fpublic.tableau.com%2F' />
                    <param name='embed_code_version' value='3' />
                    <param name='site_root'          value='' />
                    <param name='name'               value='CustomerLifecycleRevenueOptimization/Dashboard1' />
                    <param name='tabs'               value='no' />
                    <param name='toolbar'            value='yes' />
                    <param name='static_image'
                      value='https://public.tableau.com/static/images/Cu/CustomerLifecycleRevenueOptimization/Dashboard1/1.png' />
                    <param name='animate_transition'   value='yes' />
                    <param name='display_static_image' value='yes' />
                    <param name='display_spinner'      value='yes' />
                    <param name='display_overlay'      value='yes' />
                    <param name='display_count'        value='yes' />
                    <param name='language'             value='en-US' />
                    <param name='filter'               value='publish=yes' />
                  </object>
                </div>
                <script type='text/javascript'>
                  var divElement = document.getElementById('viz1777522052277');
                  var vizElement = divElement.getElementsByTagName('object')[0];
                  vizElement.style.width  = '1200px';
                  vizElement.style.height = '827px';
                  var scriptElement = document.createElement('script');
                  scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                  vizElement.parentNode.insertBefore(scriptElement, vizElement);
                </script>
                """,
                height=870,
                scrolling=True,
            )

    with notebook_tab:
        st.caption(
            "Full SQL & Python pipeline covering 89 cells: data ingestion, 12 SQL queries, "
            "customer lifecycle analysis, RFM segmentation, cohort retention, and A/B testing."
        )
        notebook_html_path = os.path.join(DATA_DIR, "notebook_rendered.html")
        if os.path.exists(notebook_html_path):
            with open(notebook_html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            components.html(html_content, height=900, scrolling=True)
        else:
            st.error("Rendered notebook not found. Please run the pre-render script first.")
            st.code(
                'JUPYTER_DATA_DIR=/opt/homebrew/share/jupyter python3.11 -c "\n'
                "import nbformat\n"
                "from nbconvert import HTMLExporter\n"
                "nb = nbformat.read('Scalable_BI_Pipeline_SQL_&_Tableau_Executive_Intelligence_System.ipynb', as_version=4)\n"
                "exporter = HTMLExporter(template_name='classic')\n"
                "html_body, _ = exporter.from_notebook_node(nb)\n"
                'open(\'notebook_rendered.html\', \'w\').write(html_body)\n"'
            )
