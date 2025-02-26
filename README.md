# 📊 LinkedIn Analytics Dashboard

A **Streamlit-based web application** for analyzing LinkedIn social media performance, including impressions, clicks, engagement rates, and NLP-based post classification.

## 🚀 Features
- **Interactive Dashboard**: View LinkedIn performance metrics in real-time.
- **Filtering Options**: Select date ranges, content types (Organic/Sponsored), and performance categories.
- **Post Classification**: NLP-based clustering of posts to identify key trends.
- **Performance Metrics**: Analyzes Impressions, Clicks, Engagement Rate, and Reactions.
- **Visualization**: Graphs for post performance and category-based trends.

## 🛠️ Installation

### **1️⃣ Clone the Repository**
```bash
 git clone https://github.com/mutonic/marketing_social.git
 cd marketing_social
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Streamlit App**
```bash
streamlit run linkedin_dashboard.py
```

## 📂 Project Structure
```
📦 marketing_social
 ┣ 📂 data                 # Folder containing the LinkedIn dataset (Excel files)
 ┣ 📂 scripts              # Additional utility scripts (if any)
 ┣ 📜 linkedin_dashboard.py  # Main Streamlit application script
 ┣ 📜 requirements.txt      # Python dependencies
 ┣ 📜 runtime.txt          # Defines Python version for Streamlit Cloud
 ┗ 📜 README.md            # Project documentation
```

## 🌍 Deployment

### **1️⃣ Deploy on Streamlit Cloud**
1. Push the repository to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Click **New App**, select the repo, and choose `linkedin_dashboard.py`.
4. Click **Deploy**.

### **2️⃣ Netlify (Frontend Only, Optional)**
For frontend hosting, Netlify can be used to deploy static files.

## 📝 Author
Developed by **Mutonic**.

---

### 🌟 **Like this project? Give it a star ⭐ on GitHub!**
