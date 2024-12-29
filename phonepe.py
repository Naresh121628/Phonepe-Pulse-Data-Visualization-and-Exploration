# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

# Setting up page configuration
icon = Image.open("ICN.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Naresh Rajamanickam",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Naresh Rajamanickam*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :green[**Hello! Welcome to the dashboard**]")

# #To clone the Github Pulse repository use the following code
# Reference Syntax - Repo.clone_from("Clone Url", "Your working directory")
# Repo.clone_from("https://github.com/PhonePe/pulse.git", "Project_3_PhonepePulse/Phonepe_data/data")

# Creating connection with mysql workbench
mydb = sql.connect(host="localhost",
                   user="admin",
                   password="12345",
                   database= "phonepe_pulse"
                  )
mycursor = mydb.cursor(buffered=True)


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Dashboard","Analytics","Data Explore"], 
                icons=["house","graph-up","search", "info-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#36AD6F"},
                        "nav-link-selected": {"background-color": "#36AD6F"}})
# MENU 1 - HOME
if selected == "Dashboard":
    st.image("img2.png")
    st.markdown("# :green[Data Visualization and Exploration]")
    st.markdown("## :green[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :green[Domain :] Fintech")
        st.markdown("### :green[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :green[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("home.png")
        

# MENU 2 - TOP CHARTS
if selected == "Analytics":
    st.markdown("## :green[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        #st.info("Transaction Count")
        st.markdown("### :green[Transaction Count Analysis]")
        col1,col2,col3 = st.columns([1,1,1],gap="small")        
        
        with col1:
            st.markdown("### :green[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total_Transactions_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count'])
            fig = px.pie(df, values='Transactions_Count',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :green[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count'])

            fig = px.pie(df, values='Transactions_Count',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :green[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total_Transactions_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count'])
            fig = px.pie(df, values='Transactions_Count',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        #st.info("Transaction Amount")
        st.markdown("### :green[Transaction Amount Analysis]")
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        with col1:
            st.markdown("### :green[State]")
            mycursor.execute(f"select state, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Amount'],
                             labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :green[District]")
            mycursor.execute(f"select district , sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Amount'],
                             labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :green[Pincode]")
            mycursor.execute(f"select pincode,sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Amount'],
                             labels={'Total_Amount':'Total_Amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        #st.info("Transaction Amount")
        #col1 = st.columns([2],gap="small")   
        #with col1:
        #    mycursor.execute(f"select distinct brands as brands from agg_user")
        #    df = pd.DataFrame(mycursor.fetchall(), columns=['Brands']) 
        #    Brand = st.sidebar.selectbox("**Brand**", df)   
        #st.info("Brand Analysis")
        col1 = st.columns([1], gap="small")

        # Get unique brands
        mycursor.execute(f"select distinct brands as brands from agg_user")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Brands'])
        #Brand = st.sidebar.selectbox("**Brand**", df['Brands'].tolist())

        col1 = st.columns(1)[0]
        with col1:
            st.markdown("### :green[Brand wise Analysis]")
            Brand = st.selectbox("Select Brand", df['Brands'].tolist())
        
        col1, col2, col3 = st.columns([1,1,1], gap="small")

        with col1:
            st.markdown("### :green[State]")
            mycursor.execute(f"""
                SELECT state, sum(count) as Total_Users, avg(percentage)*100 as Percentage 
                FROM agg_user 
                WHERE year = {Year} and quarter = {Quarter} 
                AND brands = '{Brand}'
                GROUP BY state 
                ORDER BY Total_Users DESC 
                LIMIT 10
            """)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Percentage'])
            
            fig = px.pie(df, 
                        values='Total_Users',
                        names='State',
                        title=f'Top 10 States - {Brand} Users',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Percentage'])
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :green[District]")
            mycursor.execute(f"""
                SELECT district, sum(count) as Total_Users 
                FROM map_user mu
                JOIN agg_user au ON mu.state = au.state 
                AND mu.year = au.year 
                AND mu.quarter = au.quarter
                WHERE mu.year = {Year} 
                AND mu.quarter = {Quarter} 
                AND au.brands = '{Brand}'
                GROUP BY district 
                ORDER BY Total_Users DESC 
                LIMIT 10
            """)
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users'])
            
            fig = px.pie(df, 
                        values='Total_Users',
                        names='District',
                        title=f'Top 10 Districts - {Brand} Users',
                        color_discrete_sequence=px.colors.sequential.Agsunset)
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :green[Pincode]")
            mycursor.execute(f"""
                SELECT pincode, sum(registered_users) as Total_Users 
                FROM top_user tu
                JOIN agg_user au ON tu.state = au.state 
                AND tu.year = au.year 
                AND tu.quarter = au.quarter
                WHERE tu.year = {Year} 
                AND tu.quarter = {Quarter} 
                AND au.brands = '{Brand}'
                GROUP BY pincode 
                ORDER BY Total_Users DESC 
                LIMIT 10
            """)
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            
            fig = px.pie(df, 
                        values='Total_Users',
                        names='Pincode',
                        title=f'Top 10 Pincodes - {Brand} Users',
                        color_discrete_sequence=px.colors.sequential.Agsunset)
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        # Additional Summary Statistics
        st.info(f"{Brand} Usage Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            mycursor.execute(f"""
                SELECT 
                    COUNT(DISTINCT state) as Total_States,
                    SUM(count) as Total_Users,
                    ROUND(AVG(percentage)*100, 2) as Avg_Percentage
                FROM agg_user 
                WHERE year = {Year} 
                AND quarter = {Quarter} 
                AND brands = '{Brand}'
            """)
            stats = mycursor.fetchone()
            st.metric("Total States", stats[0])
            st.metric("Total Users", format(stats[1], ","))
            st.metric("Average Usage %", f"{stats[2]}%")

        with col2:
            # Market Share Trend
            mycursor.execute(f"""
                SELECT year, quarter, 
                       ROUND(AVG(percentage)*100, 2) as Market_Share
                FROM agg_user 
                WHERE brands = '{Brand}'
                GROUP BY year, quarter
                ORDER BY year, quarter
            """)
            trend_data = pd.DataFrame(mycursor.fetchall(), 
                                    columns=['Year', 'Quarter', 'Market_Share'])
            
            fig = px.line(trend_data, 
                         x='Quarter', 
                         y='Market_Share',
                         color='Year',
                         title=f'{Brand} Market Share Trend',
                         labels={'Market_Share': 'Market Share %'})
            st.plotly_chart(fig, use_container_width=True)
   

# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :green[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :green[District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :green[Pincode]")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :green[State]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    
    
         
            
# MENU 3 - EXPLORE DATA
if selected == "Data Explore":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :green[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :green[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :green[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :green[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :green[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :green[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        st.markdown("### :green[District wise Analysis]")

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

        mycursor.execute(f"select State,year,quarter,brands as Brands,count as Total_Users from agg_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' order by state")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'Brands', 'Total_Users'])
        df.Total_Users = df.Total_Users.astype(int)
        
        st.markdown("### :green[Brand wise Analysis]")

        fig = px.bar(df,
                     title=selected_state,
                     x="Brands",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)        

    
