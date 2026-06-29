import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import streamlit as st
# It plot a graph on web
import plotly.express as px
import plotly.graph_objects as go 
from config import DATA_FILE
# import splitting function 
from sklearn.model_selection import train_test_split

df = pd.read_csv(DATA_FILE)

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    layout="wide",
)


# styling : 
st.markdown("""
<style>
/* Main Background */
.stApp{background-color: #f0f4f8; color: black;}


/*Style title */  
.dashboard_title{
            color: white;
            background: linear-gradient(155deg, #1e3a5f 0%, #2e6db4 100%);
            padding: 20px 30px;
            text-align: center 
            font-size: 22px
            font-weigth: 700;
            margin-bottom: 24px;

    }
</style>

""", unsafe_allow_html=True)



# Make a Title of dashboard 
st.markdown("""
    <div class="dashboard_title">
    <h2>E-Commerce Sales Analysis &amp Forecasting Dashboard
    </h2>
    </div>
""", unsafe_allow_html=True,)


print(df.info())

df.drop_duplicates(inplace=True)
print(df.isnull().sum())

df["TotalSales"] = df["Quantity"] * df["Price"]

# Extract from orderDate Month 

# Feature Engineering 
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df["Month"] = df['OrderDate'].dt.month_name()

month_order = [
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
]
df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

# print(df.info())

df["year"] = df['OrderDate'].dt.year
print(df['Month'])

# Exploratory Data Analysis : Calculate : Total revenue, Sales by region, Sales by category, Top selling products, Monthly revenue 
# Sales by region
Region_Venue = df.groupby("Region")["TotalSales"].max()


Total_Revenue =  df['TotalSales'].sum()
Top_region = Region_Venue.idxmax()

# Make column for show 1. Total Revenue, Total Orders, Top Region name, Top product : 
# Use KPI card (Key Performance Indicator Card)
k1, k2, k3, k4 = st.columns(4)

# It's for Total Revenue according to region 
with k1:
    st.markdown(f"""
    <div class="Revenu">
        <div class="rev_label">Total Revenue</div>
        <div class="rev_value">₹{Total_Revenue:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
# Total Order : 

print("Total Sales by category")
Category_Sales = df.groupby("Category")["TotalSales"].sum()

Total_Orders = df["OrderID"].nunique()
# Now make Column 2 
with k2:
    st.markdown(f"""
    <div class="Total_Order">
        <div class="Tol_label">Total Order</div>
        <div class="Tol_value">₹{Total_Orders}</div>
    </div>
""", unsafe_allow_html=True )
    
# Top Selling Product 
Top_Sales = df.groupby("Product")['TotalSales'].max()
Top_Product = Top_Sales.idxmax()

with k3:
    st.markdown(f"""
    <div class="Total_Order">
        <div class="Pro_label">Top Product </div>
        <div class="Pro_value">{Top_Product}</div>
    </div>
""", unsafe_allow_html=True )
    


# Top Region
with k4:
    st.markdown(f"""
    <div class="region_Order">
        <div class="reg_label">Top Region </div>
        <div class="reg_value">{Top_region}</div>
    </div>
""", unsafe_allow_html=True )

monthly_revenue = df.groupby(df['Month'])['TotalSales'].sum()
print(monthly_revenue)


# Now Evaluete graph 
# 3 Graphs : 
st.write("")
st.write("")


c1,c2,c3 = st.columns(3)

revenue = Region_Venue.reset_index()
with c1:
    fig_bar = px.bar(
        revenue,
        x="Region",
        y="TotalSales",   
        title="Sales by Region",
        color="Region",
        color_discrete_sequence=["red", "green", "blue", "yellow"]
    )
    fig_bar.update_layout(
        plot_bgcolor="White", paper_bgcolor="white",
        margin=dict(t=50, b=20, l=10, r=10),
        title_font_size=14,
        # Chart title
        title_font=dict(
            size=18,
            color="darkblue"
        ),
          # X-axis labels
        xaxis=dict(
            tickfont=dict(
                size=12,
                color="black"
            ),
            title_font=dict(
                size=14,
                color="blue"
            )
        ),

        # Y-axis labels
        yaxis=dict(
            tickfont=dict(
                size=12,
                color="black"
            ),
            title_font=dict(
                size=14,
                color="blue"
            )
        ),
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)


#Line Chart by Monthly Saled Trend 
monthly_revenue = monthly_revenue.reset_index()
with c2:
    # Create Line Chart
    fig_lin = px.line(
        monthly_revenue,
        x="Month",
        y="TotalSales",
        title="Monthly Sales Trend",
        markers=True
    )

    # Show sales values on each point
    fig_lin.update_traces(
        text=monthly_revenue["TotalSales"],
        textposition="top center"
    )

    # Customize the chart
    fig_lin.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",

        margin=dict(
            t=50,
            b=20,
            l=10,
            r=10
        ),

        title_font=dict(
            size=18,
            color="darkblue"
        ),

        xaxis=dict(
            title="Month",
            title_font=dict(
                size=14,
                color="blue"
            ),
            tickfont=dict(
                size=12,
                color="black"
            )
        ),

        yaxis=dict(
            title="Total Sales",
            title_font=dict(
                size=14,
                color="blue"
            ),
            tickfont=dict(
                size=12,
                color="black"
            )
        ),

        showlegend=False
    )

    # Display chart
    st.plotly_chart(fig_lin, width="stretch")

# Make a Pie plot 
Category_Sales = Category_Sales.reset_index()
with c3:
    fig_pie = px.pie(
    Category_Sales, values="TotalSales", names="Category",
    title="Total Sales by Category",
    color_discrete_sequence=["#2e6db4", "#e07b39", "#27ae60"],
   
    )
    fig_pie.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",

        margin=dict(
            t=50,
            b=20,
            l=10,
            r=10
        ),

        title_font=dict(
            size=18,
            color="darkblue"
        ),

        xaxis=dict(
            title="Month",
            title_font=dict(
                size=14,
                color="blue"
            ),
            tickfont=dict(
                size=12,
                color="black"
            )
        ),

        yaxis=dict(
            title="Total Sales",
            title_font=dict(
                size=14,
                color="blue"
            ),
            tickfont=dict(
                size=12,
                color="black"
            )
        ),
     )

    st.plotly_chart(fig_pie, use_container_width=True)


f1, f2 = st.columns([2,3])
# hEATMAP 
df['Region_encoded'] = df['Region'].astype('category').cat.codes
# Correlation matrix
corr_matrix = df[['TotalSales', 'Price', 'Quantity', 'Region_encoded']].corr()

with f1:
    fig_heat = go.Figure(
    data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale="YlOrRd",
        text=corr_matrix.round(2).values,
        texttemplate="%{text}",
        textfont=dict(size=12)
    )
    
)
    fig_heat.update_layout(
    title="Correlation Heatmap",
    plot_bgcolor="white",
    paper_bgcolor="white"
    )

st.plotly_chart(fig_heat, width="stretch")
    





# Preprocessing Data :
# Convert Month bcz it's a categorical 
# apply Transformation on month, categor, and, 

# Make a object 
le = LabelEncoder()

df['Month_enc'] = le.fit_transform(df['Month'])
df['Category_enc'] = le.fit_transform(df['Category'])
df['Region_enc'] = le.fit_transform(df['Region'])

# Prepare features and split data 

X = df[['Month_enc', 'Region_enc', 'Category_enc',
        'Quantity', 'Price']]

y = df['TotalSales']

# Apply the split 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train rows: {len(X_train)}, Test rows: {len(X_test)}")


# Build and evaluate : train model using X_train and y_train portions, then test its predictive power on X_test and y_test
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

lr_preds = lr_model.predict(X_test)

# Model 2: Random Forest 

rf_model = RandomForestRegressor(
    n_estimators=100, # build 100 trees 
    random_state=42
)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)



# Model Evaluation 
for name, preds in [('Linear Regression', lr_preds),
                    ('Random Forest', rf_preds)]:
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"MAE {mae:.2f} (avg error is )")
    print(f"R^2 : {r2:.4f} (1.0 = perfect)")


future_data = pd.DataFrame({
    'Month_enc':    [0, 1, 2],     # April, May, June
    'Region_enc':   [1, 1, 1],     # North
    'Category_enc': [1, 1, 1],     # Electronics
    'Quantity':     [200, 145, 160],
    'Price':        [23, 27, 23]
})

# Use the better model (Random Forest) to predict
future_preds = rf_model.predict(future_data)

# Show results table
results = pd.DataFrame({
    'Month':           ['April', 'May', 'June'],
    'Predicted Sales': future_preds.astype(int)
})


# Make plot 
# Visualise the predicted trend
months = ["April", "May", "June"]
sales = future_preds.astype(int)

forecast_data = pd.DataFrame({
    "Month": months,
    "Sales": sales
})


with f2:
    fig_lin_pre = px.line(
        monthly_revenue,
        x="Months",
        y="sales",
        title="Monthly Sales Trend",
        markers=True
    )

    # Show sales values on each point
    fig_lin.update_traces(
        text=monthly_revenue["TotalSales"],
        textposition="top center"
    )

    # Customize the chart
    fig_lin.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",

        margin=dict(
            t=50,
            b=20,
            l=10,
            r=10
        ),

        title_font=dict(
            size=18,
            color="darkblue"
        ),

        xaxis=dict(
            title="Month",
            title_font=dict(
                size=14,
                color="blue"
            ),
            tickfont=dict(
                size=12,
                color="black"
            )
        ),

        yaxis=dict(
            title="Total Sales",
            title_font=dict(
                size=14,
                color="blue"
            ),
            tickfont=dict(
                size=12,
                color="black"
            )
        ),

        showlegend=False
    )

    # Display chart
    st.plotly_chart(fig_lin_pre, width="stretch")



"""plt.scatter(y_test, lr_preds, color='red')

plt.title('Actual vs Predicted Sales (Linear Regression)')
plt.xlabel('Actual Sales')
plt.ylabel('Predicted Sales')
plt.grid(True)

plt.show()"""