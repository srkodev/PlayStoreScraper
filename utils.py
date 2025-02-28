import streamlit as st
from google_play_scraper import reviews_all
import pandas as pd
from fpdf import FPDF
import base64
import io

def get_reviews(app_id):
    try:
        reviews = reviews_all(app_id, lang="fr", country="fr")
        return reviews, None
    except Exception as e:
        return None, str(e)

def create_pdf(reviews_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Avis Google Play Store", ln=True, align='C')
    pdf.ln(10)
    
    # Add reviews
    pdf.set_font("Arial", size=12)
    for review in reviews_data:
        if review["content"]:
            pdf.multi_cell(0, 10, txt=f"★ {review['score']}/5\n{review['content']}\n", align='L')
            pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin1')

def create_download_link(data, filename, text):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'
    return href

def save_txt(reviews_data, app_id):
    output = io.StringIO()
    for review in reviews_data:
        if review["content"]:
            output.write(f"★ {review['score']}/5\n{review['content']}\n\n")
    return output.getvalue()
