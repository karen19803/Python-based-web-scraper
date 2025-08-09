# Python-based-web-scraper
This project is a **web scraping task** completed as part of my **AI/ML Internship at Konecta**.

## 📌 Task Overview
The goal is to build a **Python-based web scraper** that collects structured product data from an e-commerce website.

### **Objective**
- Extract product details for at least 100 items in a specific category.
- Save the results into a clean CSV file or Pandas DataFrame for further analysis.

### **Data Fields**
The scraper collects:
- Product Name / Title
- Price
- Product Rating (if available)
- Number of Reviews (if available)
- Product URL
- Image URL
- Brand (if available)

## 🛠️ Tools & Libraries
- **Python 3**
- **requests** – to fetch HTML pages
- **BeautifulSoup (bs4)** – to parse HTML and extract data
- **pandas** – to store and export data to CSV
- **lxml** – as an HTML parser

## 🚀 How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/python-based-web-scraper.git
   cd python-based-web-scraper
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the scraper:
   ```bash
   python scraper.py
4. The results will be saved as:
    ```bash
   products.csv
## 📂 Project Structure
```bash
python-based-web-scraper/
│
├── scraper.py         # Main Python script for scraping
├── requirements.txt   # List of dependencies
├── README.md          # Project documentation
└── products.csv       # Output file (generated after running)
