from google_play_scraper import reviews_all
import pandas as pd
from fpdf import FPDF
import os

def get_reviews(app_id):
    """Récupère les avis depuis Google Play Store de manière sécurisée"""
    try:
        # Limiter le nombre de requêtes
        reviews = reviews_all(
            app_id, 
            lang="fr", 
            country="fr",
            sleep_milliseconds=100  # Ajouter un délai entre les requêtes
        )
        return reviews, None
    except Exception as e:
        return None, str(e)

def create_pdf(reviews_data):
    """Crée un PDF formaté avec les avis"""
    pdf = FPDF()
    pdf.add_page()
    
    # Configuration de la police et des marges
    pdf.set_font("helvetica", size=16)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Titre
    pdf.set_font("helvetica", 'B', 20)
    pdf.cell(0, 20, "Avis Google Play Store", ln=True, align='C')
    pdf.ln(10)
    
    # Statistiques
    df = pd.DataFrame(reviews_data)
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, "Statistiques", ln=True)
    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 8, f"Note moyenne: {df['score'].mean():.1f}/5", ln=True)
    pdf.cell(0, 8, f"Nombre total d'avis: {len(df)}", ln=True)
    pdf.cell(0, 8, f"Avis 5 étoiles: {len(df[df['score'] == 5])}", ln=True)
    pdf.ln(10)
    
    # Avis
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, "Détail des avis", ln=True)
    pdf.ln(5)
    
    for review in reviews_data:
        if review["content"]:
            # Note
            pdf.set_font("helvetica", 'B', 12)
            pdf.cell(0, 8, f"Note: {review['score']}/5", ln=True)
            
            # Contenu
            pdf.set_font("helvetica", size=10)
            try:
                pdf.multi_cell(0, 6, review['content'])
            except Exception:
                cleaned_content = review['content'].encode('ascii', 'ignore').decode()
                pdf.multi_cell(0, 6, cleaned_content)
            pdf.ln(5)
            
            # Ligne de séparation
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(8)
    
    return pdf.output()

def save_txt(reviews_data, app_id):
    """Crée un fichier texte formaté avec les avis"""
    df = pd.DataFrame(reviews_data)
    
    content = [
        f"Avis pour l'application {app_id}",
        "=" * 50,
        "",
        "STATISTIQUES",
        "-" * 12,
        f"Note moyenne: {df['score'].mean():.1f}/5",
        f"Nombre total d'avis: {len(df)}",
        f"Avis 5 étoiles: {len(df[df['score'] == 5])}",
        "",
        "DÉTAIL DES AVIS",
        "-" * 14,
        ""
    ]
    
    for review in reviews_data:
        content.extend([
            f"Note: {review['score']}/5",
            f"Avis: {review['content']}",
            "-" * 50,
            ""
        ])
    
    return "\n".join(content)