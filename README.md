# Government-Tender-Tracker-Bid-Match-Recommender

**Video Link:** https://www.loom.com/share/726df4839cf647f3b9c17a67f9affd4b?sid=f8443f1b-9b7f-4568-8504-e8f737e475ce

**LinkedIn** : https://www.linkedin.com/in/sumaiya-sulthana-906876137 

**Full Technical Plan**: Government Tender Tracker & Recommender

**1. Modules & Responsibilities**
1.**Tender Aggregator**--	Connect to CPPP, GeM, and State portals, fetch tender data (scraping).

2.**Tender Parser**--	Extract fields like EMD, deadlines, scopes using pdfplumber, BeautifulSoup, and regex.

3.**Profile Manager**--	Upload or link a company’s capability document (PDF) and store features.
     **Used Firecrawl**to scrape CompanyProfiles and saved as PDF
     
4.**Matcher	Use**--TF-IDF or Embeddings (Sentence Transformers) to compute similarity score between profile and tender description.

5.**Dashboard** --(Streamlit)	Interactive dashboard: view tenders, upload profile, see matches, apply filters.

6.**Notifier	Optional**-- Send SMS (Twilio) or Email (Gmail SMTP OAuth2) when high-match tenders appear.

7.**Database (Storage)**--	Store tenders, profiles, match scores — recommended: lightweight SQL (SQLite).

**2.Tech Stack**

Web Framework --Streamlit

Scraping/Parsing --	Requests, BeautifulSoup4, pdfplumber, PyMuPDF

scikit-learn TF-IDF

SQLite 

pandas

**3. Key Flows**

a)**Tender Aggregation**--
CPPP XML feed (scraping with BeautifulSoup). Save into database.

b)**Company Parsing**--
Download attached company Capabilities documents (PDF/DOCX).
Use pdfplumber or PyMuPDF to extract

c)**Company Profile Upload**--
Allow .pdf--Extract text.--Store in database.

d)**Matching Engine**
Used **TF-IDF Vectorizer** to embed:

       Profile text--Tender Scope text
       
       Compute cosine similarity.
       
       Apply a match threshold (say 0.19).Achieved

e)**Streamlit Dashboard**

**Home Page**: # Has a slider Bar with Menubar showing  1.View Tenders 2.Upload company profile 3.Match Recommendations

               # Then a selectionbar has 1.CPP 2.GEM 3.State portal   Default used CPP 
               
               # Main page Shows Short Despcrition about Tender and Indian Image followed by all latest tenders.

**Upload Page**: Upload Company name and capability profile.

**Matches Recommendation page**: List tenders sorted by match score in Assending Order.
