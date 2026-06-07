import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_connection import get_connection

st.set_page_config(
    page_title="Supply Chain Risk Intelligence",
    page_icon="📦",
    layout="wide"
)

@st.cache_data(ttl=300)
def load_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=Bebas+Neue&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #14110F;
    color: #F5EBDD;
}

[data-testid="stSidebar"] {
    background: #1B1714;
    border-right: 1px solid #3B3028;
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.hero {
    background: #1F1A17;
    border: 1px solid #B8793E;
    border-radius: 20px;
    padding: 34px;
    margin-bottom: 30px;
    box-shadow: 9px 9px 0px #070605;
}

.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    color: #F5EBDD;
    font-size: 64px;
    letter-spacing: 2px;
    margin-bottom: 4px;
}

.hero p {
    color: #D6C1A8;
    font-size: 16px;
}

.kpi-card, .insight-card {
    background: #211C18;
    border: 1px solid #3B3028;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 6px 6px 0px #070605;
    margin-bottom: 20px;
}

.kpi-title {
    color: #D6C1A8;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin-bottom: 10px;
}

.kpi-value {
    color: #F4A261;
    font-size: 31px;
    font-weight: 800;
}

.sidebar-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 38px;
    color: #F4A261;
    letter-spacing: 1.5px;
}

.sidebar-subtitle {
    color: #D6C1A8;
    font-size: 14px;
    margin-bottom: 18px;
}

h1, h2, h3 {
    color: #F5EBDD;
}

.stDataFrame {
    border: 1px solid #3B3028;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight_card(title, text):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="kpi-title">{title}</div>
            <div style="color:#F5EBDD;font-size:15px;line-height:1.6;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def retro_chart(fig):
    fig.update_layout(
        paper_bgcolor="#1F1A17",
        plot_bgcolor="#1F1A17",
        font=dict(color="#F5EBDD", family="DM Sans"),
        title_font=dict(color="#F4A261", size=21, family="DM Sans"),
        xaxis=dict(color="#D6C1A8", gridcolor="#3B3028"),
        yaxis=dict(color="#D6C1A8", gridcolor="#3B3028"),
        legend=dict(font=dict(color="#F5EBDD")),
        margin=dict(l=35, r=35, t=65, b=35)
    )
    return fig


def gauge_chart(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": "Overall Supply Chain Risk Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#F4A261"},
            "bgcolor": "#1F1A17",
            "borderwidth": 1,
            "bordercolor": "#3B3028",
            "steps": [
                {"range": [0, 35], "color": "#2F3A2F"},
                {"range": [35, 70], "color": "#5A432C"},
                {"range": [70, 100], "color": "#5A2C2C"}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor="#1F1A17",
        font=dict(color="#F5EBDD", family="DM Sans"),
        height=320,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


st.sidebar.markdown('<div class="sidebar-title">SUPPLY CHAIN</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-subtitle">Optimization & Risk Intelligence</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Inventory Intelligence",
        "Supplier Performance",
        "Shipment Analysis",
        "Warehouse Utilization",
        "Demand Forecasting",
        "Reorder Recommendations",
        "Risk Dashboard"
    ]
)

try:
    if page == "Executive Overview":
        hero(
            "SUPPLY CHAIN RISK INTELLIGENCE",
            "Executive command center for inventory risk, supplier exposure, shipment delays, reorder intelligence, and operational decision support."
        )

        kpi = load_data("""
            SELECT
                (SELECT COUNT(*) FROM products) AS total_products,
                (SELECT COUNT(*) FROM suppliers) AS total_suppliers,
                (SELECT COUNT(*) FROM orders) AS total_orders,
                (SELECT COUNT(*) FROM shipments) AS total_shipments,
                (SELECT ROUND(SUM(inventory_value),2)
                 FROM vw_inventory_intelligence) AS total_inventory_value;
        """)

        risk = load_data("""
            SELECT
                (SELECT COUNT(*) FROM vw_inventory_intelligence 
                 WHERE stock_status = 'Critical Stockout Risk') AS critical_stockouts,
                (SELECT COUNT(*) FROM vw_supplier_scorecard 
                 WHERE risk_level = 'High') AS high_risk_suppliers,
                (SELECT COUNT(*) FROM vw_shipment_analysis 
                 WHERE delivery_status = 'Delayed') AS delayed_shipments,
                (SELECT COUNT(*) FROM vw_reorder_intelligence 
                 WHERE reorder_priority = 'High Priority') AS high_priority_reorders;
        """)

        total_products = int(kpi.loc[0, "total_products"])
        total_suppliers = int(kpi.loc[0, "total_suppliers"])
        total_shipments = int(kpi.loc[0, "total_shipments"])

        critical_stockouts = int(risk.loc[0, "critical_stockouts"])
        high_risk_suppliers = int(risk.loc[0, "high_risk_suppliers"])
        delayed_shipments = int(risk.loc[0, "delayed_shipments"])
        high_priority_reorders = int(risk.loc[0, "high_priority_reorders"])

        inventory_risk_pct = critical_stockouts / max(total_products, 1) * 100
        supplier_risk_pct = high_risk_suppliers / max(total_suppliers, 1) * 100
        shipment_risk_pct = delayed_shipments / max(total_shipments, 1) * 100

        overall_risk_score = round(
            (inventory_risk_pct * 0.4) +
            (supplier_risk_pct * 0.3) +
            (shipment_risk_pct * 0.3),
            2
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            kpi_card("Products", f"{total_products:,}")
        with c2:
            kpi_card("Suppliers", f"{total_suppliers:,}")
        with c3:
            kpi_card("Orders", f"{int(kpi.loc[0, 'total_orders']):,}")
        with c4:
            kpi_card("Shipments", f"{total_shipments:,}")
        with c5:
            kpi_card("Inventory Value", f"₹{float(kpi.loc[0, 'total_inventory_value']):,.0f}")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.plotly_chart(gauge_chart(overall_risk_score), use_container_width=True)

        with col2:
            insight_card(
                "Executive Risk Summary",
                f"""
                Critical stockout items: <b>{critical_stockouts:,}</b><br>
                High-risk suppliers: <b>{high_risk_suppliers:,}</b><br>
                Delayed shipments: <b>{delayed_shipments:,}</b><br>
                High-priority reorder alerts: <b>{high_priority_reorders:,}</b><br><br>
                Overall risk score is <b>{overall_risk_score}/100</b>.
                """
            )

        col3, col4 = st.columns(2)

        inv_value = load_data("""
            SELECT category, SUM(inventory_value) AS total_value
            FROM vw_inventory_intelligence
            GROUP BY category
            ORDER BY total_value DESC;
        """)

        stock = load_data("""
            SELECT stock_status, COUNT(*) AS count
            FROM vw_inventory_intelligence
            GROUP BY stock_status;
        """)

        fig1 = px.bar(
            inv_value,
            x="category",
            y="total_value",
            title="Inventory Value by Category",
            text_auto=".2s",
            template="plotly_white",
            color_discrete_sequence=["#F4A261"]
        )

        fig2 = px.pie(
            stock,
            names="stock_status",
            values="count",
            title="Inventory Health Distribution",
            hole=0.55,
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34"]
        )

        with col3:
            st.plotly_chart(retro_chart(fig1), use_container_width=True)

        with col4:
            st.plotly_chart(retro_chart(fig2), use_container_width=True)

        st.subheader("Top 10 Actionable Risk Items")

        top_risk_products = load_data("""
            SELECT 
                product_name,
                category,
                warehouse_name,
                available_stock,
                reorder_level,
                safety_stock,
                stock_status,
                inventory_value
            FROM vw_inventory_intelligence
            WHERE stock_status <> 'Healthy Stock'
            ORDER BY 
                CASE 
                    WHEN stock_status = 'Critical Stockout Risk' THEN 1
                    WHEN stock_status = 'Reorder Required' THEN 2
                    ELSE 3
                END,
                available_stock ASC
            LIMIT 10;
        """)

        st.dataframe(top_risk_products, use_container_width=True)

    elif page == "Inventory Intelligence":
        hero("INVENTORY INTELLIGENCE", "Track stockout risk, reorder status, available stock, and total inventory value.")

        df = load_data("SELECT * FROM vw_inventory_intelligence;")

        status = st.multiselect(
            "Filter by stock status",
            options=df["stock_status"].unique(),
            default=df["stock_status"].unique()
        )

        filtered = df[df["stock_status"].isin(status)]

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            kpi_card("Inventory Records", f"{len(filtered):,}")
        with c2:
            kpi_card("Critical Risk", f"{len(filtered[filtered['stock_status'] == 'Critical Stockout Risk']):,}")
        with c3:
            kpi_card("Reorder Required", f"{len(filtered[filtered['stock_status'] == 'Reorder Required']):,}")
        with c4:
            kpi_card("Total Value", f"₹{filtered['inventory_value'].sum():,.0f}")

        chart_df = filtered.groupby("category", as_index=False)["inventory_value"].sum()

        fig = px.bar(
            chart_df,
            x="category",
            y="inventory_value",
            title="Inventory Value by Category",
            text_auto=".2s",
            template="plotly_white",
            color_discrete_sequence=["#F4A261"]
        )

        st.plotly_chart(retro_chart(fig), use_container_width=True)
        st.dataframe(filtered, use_container_width=True)

    elif page == "Supplier Performance":
        hero("SUPPLIER PERFORMANCE", "Analyze reliability, defect rate, supplier status, and supplier risk exposure.")

        df = load_data("SELECT * FROM vw_supplier_scorecard;")

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card("Suppliers", f"{len(df):,}")
        with c2:
            kpi_card("High Risk", f"{len(df[df['risk_level'] == 'High']):,}")
        with c3:
            kpi_card("Avg Reliability", f"{df['reliability_score'].mean():.2f}%")

        col1, col2 = st.columns(2)

        fig1 = px.scatter(
            df,
            x="reliability_score",
            y="risk_score",
            size="defect_rate",
            color="supplier_status",
            hover_name="supplier_name",
            title="Supplier Reliability vs Risk",
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34"]
        )

        risk_count = df[df["risk_level"].notna()].groupby("risk_level", as_index=False)["supplier_id"].count()

        fig2 = px.bar(
            risk_count,
            x="risk_level",
            y="supplier_id",
            title="Supplier Risk Distribution",
            text_auto=True,
            template="plotly_white",
            color_discrete_sequence=["#F4A261"]
        )

        with col1:
            st.plotly_chart(retro_chart(fig1), use_container_width=True)

        with col2:
            st.plotly_chart(retro_chart(fig2), use_container_width=True)

        st.subheader("Supplier Risk Leaderboard")
        st.dataframe(df.sort_values("risk_score", ascending=False), use_container_width=True)

    elif page == "Shipment Analysis":
        hero("SHIPMENT ANALYSIS", "Monitor logistics delays, carrier performance, and shipping cost efficiency.")

        df = load_data("SELECT * FROM vw_shipment_analysis;")

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card("Shipments", f"{len(df):,}")
        with c2:
            kpi_card("Delayed", f"{len(df[df['delivery_status'] == 'Delayed']):,}")
        with c3:
            kpi_card("Avg Delay", f"{df['delay_days'].mean():.2f} days")

        carrier = df.groupby("carrier", as_index=False).agg(
            total_shipments=("shipment_id", "count"),
            avg_delay=("delay_days", "mean"),
            avg_shipping_cost=("shipping_cost", "mean")
        )

        col1, col2 = st.columns(2)

        fig1 = px.bar(
            carrier,
            x="carrier",
            y="avg_delay",
            title="Average Delay by Carrier",
            text_auto=".2f",
            template="plotly_white",
            color_discrete_sequence=["#F4A261"]
        )

        fig2 = px.bar(
            carrier,
            x="carrier",
            y="avg_shipping_cost",
            title="Average Shipping Cost by Carrier",
            text_auto=".2f",
            template="plotly_white",
            color_discrete_sequence=["#D6C1A8"]
        )

        with col1:
            st.plotly_chart(retro_chart(fig1), use_container_width=True)

        with col2:
            st.plotly_chart(retro_chart(fig2), use_container_width=True)

        st.subheader("Delayed Shipment Records")
        st.dataframe(df.sort_values("delay_days", ascending=False), use_container_width=True)

    elif page == "Warehouse Utilization":
        hero("WAREHOUSE UTILIZATION", "Track capacity usage, warehouse load, stock concentration, and inventory value.")

        df = load_data("SELECT * FROM vw_warehouse_utilization;")

        fig1 = px.bar(
            df.sort_values("utilization_percentage", ascending=False),
            x="warehouse_name",
            y="utilization_percentage",
            color="utilization_status",
            title="Warehouse Utilization Percentage",
            text_auto=".2f",
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34", "#6B4B32"]
        )

        fig2 = px.scatter(
            df,
            x="utilization_percentage",
            y="warehouse_inventory_value",
            size="total_stock",
            color="utilization_status",
            hover_name="warehouse_name",
            title="Warehouse Utilization vs Inventory Value",
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34", "#6B4B32"]
        )

        st.plotly_chart(retro_chart(fig1), use_container_width=True)
        st.plotly_chart(retro_chart(fig2), use_container_width=True)

        st.dataframe(df, use_container_width=True)

    elif page == "Demand Forecasting":
        hero("DEMAND FORECASTING", "Compare predicted demand with actual demand and evaluate forecast quality.")

        df = load_data("SELECT * FROM vw_demand_forecast_accuracy;")

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card("Forecast Records", f"{len(df):,}")
        with c2:
            kpi_card("Avg Accuracy", f"{df['forecast_accuracy'].mean():.2f}%")
        with c3:
            kpi_card("Avg Demand Gap", f"{df['demand_gap'].mean():.2f}")

        fig1 = px.histogram(
            df,
            x="forecast_accuracy",
            color="forecast_quality",
            title="Forecast Accuracy Distribution",
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34"]
        )

        fig2 = px.bar(
            df.groupby("category", as_index=False)["forecast_accuracy"].mean(),
            x="category",
            y="forecast_accuracy",
            title="Average Forecast Accuracy by Category",
            text_auto=".2f",
            template="plotly_white",
            color_discrete_sequence=["#F4A261"]
        )

        st.plotly_chart(retro_chart(fig1), use_container_width=True)
        st.plotly_chart(retro_chart(fig2), use_container_width=True)

        st.dataframe(df, use_container_width=True)

    elif page == "Reorder Recommendations":
        hero("REORDER RECOMMENDATIONS", "Identify urgent restocking needs based on safety stock and reorder thresholds.")

        df = load_data("SELECT * FROM vw_reorder_intelligence;")
        reorder_df = df[df["reorder_priority"] != "No Reorder Needed"]

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card("Need Reorder", f"{len(reorder_df):,}")
        with c2:
            kpi_card("High Priority", f"{len(reorder_df[reorder_df['reorder_priority'] == 'High Priority']):,}")
        with c3:
            kpi_card("Recommended Units", f"{reorder_df['recommended_reorder_quantity'].sum():,}")

        fig = px.bar(
            reorder_df.groupby("reorder_priority", as_index=False)["recommended_reorder_quantity"].sum(),
            x="reorder_priority",
            y="recommended_reorder_quantity",
            title="Recommended Quantity by Priority",
            text_auto=True,
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8"]
        )

        st.plotly_chart(retro_chart(fig), use_container_width=True)
        st.dataframe(reorder_df.sort_values("recommended_reorder_quantity", ascending=False), use_container_width=True)

    elif page == "Risk Dashboard":
        hero("RISK DASHBOARD", "A consolidated view of inventory risk, supplier risk, and shipment risk exposure.")

        inventory = load_data("""
            SELECT stock_status, COUNT(*) AS count
            FROM vw_inventory_intelligence
            GROUP BY stock_status;
        """)

        suppliers = load_data("""
            SELECT risk_level, COUNT(*) AS count
            FROM vw_supplier_scorecard
            WHERE risk_level IS NOT NULL
            GROUP BY risk_level;
        """)

        shipments = load_data("""
            SELECT delivery_status, COUNT(*) AS count
            FROM vw_shipment_analysis
            GROUP BY delivery_status;
        """)

        col1, col2, col3 = st.columns(3)

        fig1 = px.pie(
            inventory,
            names="stock_status",
            values="count",
            title="Inventory Risk",
            hole=0.55,
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34"]
        )

        fig2 = px.pie(
            suppliers,
            names="risk_level",
            values="count",
            title="Supplier Risk",
            hole=0.55,
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34"]
        )

        fig3 = px.pie(
            shipments,
            names="delivery_status",
            values="count",
            title="Shipment Risk",
            hole=0.55,
            template="plotly_white",
            color_discrete_sequence=["#F4A261", "#D6C1A8", "#8C5A34"]
        )

        with col1:
            st.plotly_chart(retro_chart(fig1), use_container_width=True)

        with col2:
            st.plotly_chart(retro_chart(fig2), use_container_width=True)

        with col3:
            st.plotly_chart(retro_chart(fig3), use_container_width=True)

except Exception as e:
    st.error("Dashboard error occurred.")
    st.exception(e)