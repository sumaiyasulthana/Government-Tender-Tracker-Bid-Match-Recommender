import streamlit as st
from database.db_manager import SessionLocal, Tender, CompanyProfile, Match
from scrapers.scraper import fetch_cppp_tenders
from matchers.matcher import compute_match_score
from utils.text_extractor import extract_text_from_pdf
import pandas as pd
import sqlite3

db = SessionLocal()
# STREAMLIT PART
st.set_page_config(layout="wide")
 
with open(r'C:\Users\Admin\Desktop\TENDER\style1.css') as f:
  st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
st.title("Government Tender Tracker & Bid-Match Recommender ")
menu = ["View Tenders", "Upload Company Profile", "Match Recommendations"]
choice = st.sidebar.selectbox("Menu", menu)

col1,col2 = st.columns(2)
with col1:
    st.write("****e-Publishing System****")
    st.write("****The Central Public Procurement Portal of Government of India facilitates all the Central Government Organisations to publish their Tender Enquiries,Corrigenda and Award of Contract details.The system also enables users to migrate to total electronic procurement mode****")
    
with col2:
    st.image("C:/Users/Admin/Desktop/TENDER/Capture.JPG", caption="****ministry of culture government of India****", 
              width=300,use_container_width=300, clamp=False,
              channels="RGB", output_format="icon")     



if choice == "View Tenders":
    st.subheader("All Tenders 🌍")
    
     # Convert to DataFrame --- 
    data =fetch_cppp_tenders()
    details= pd.DataFrame(data)
    # Connect to SQLite
    conn = sqlite3.connect('tender_tracker.db')
    cursor = conn.cursor()

    details.to_sql('details', con=conn, if_exists='replace', index=False)

    #calling curr dataframes from sqlite
    
    cursor.execute("select * from details")
    conn.commit()
    table1 = cursor.fetchall()
    df1 =pd.DataFrame(table1,columns =["Opening_Date","Closing_Date","e_Published_Date",
                                       "title","Organisation ","source_portal"])
    st.write(df1)
    
elif choice == "Upload Company Profile":
    st.subheader("Upload Profile 🏛️")
    name = st.text_input("Company Name")
    uploaded_file = st.file_uploader("Upload Capability Profile (PDF)", type=["pdf"])

    if st.button("Upload") and uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        profile = CompanyProfile(name=name, profile_text=text)
        db.add(profile)
        db.commit()
        st.success("Profile uploaded successfully.")

elif choice == "Match Recommendations":
    st.subheader("Tender Recommendations📈")
    profiles = db.query(CompanyProfile).all()
    conn = sqlite3.connect('tender_tracker.db')
    cursor = conn.cursor()
    cursor.execute("select * from details")
    tenders = cursor.fetchall()

    if profiles:
        selected_profile = st.selectbox("Select Profile", profiles, format_func=lambda x: x.name)
        matches = []
        for tender in tenders:
            score = compute_match_score(selected_profile.profile_text, tender[3])
            matches.append((tender, score))
        
        matches = sorted(matches, key=lambda x: x[1], reverse=True)
        for tender, score in matches:
            st.write(f"**{tender[3]}** (Match Score: ***{score:.2f}***)")
            st.write(f"***{tender[4]}***")
            st.write("---")
    else:
        st.warning("No profiles found! Upload first.")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")

# Sidebar: Select tender sources
st.sidebar.multiselect(
    "Select Tender Sources",
    ["CPPP", "GeM", "State Portal"],
    default=["CPPP"])
