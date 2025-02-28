import streamlit as st
import pandas as pd
from utils import get_reviews, create_pdf, create_download_link, save_txt
from styles import apply_custom_styles

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Google Play Store Review Scraper",
    page_icon="📱",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

# Header
st.markdown("""
    <div class="app-header">
        <h1>📱 Google Play Store Scraper d'Avis</h1>
        <p>Extrayez et analysez les avis de n'importe quelle application du Google Play Store</p>
    </div>
""", unsafe_allow_html=True)

# Input section
with st.container():
    st.markdown("### 📝 Entrez l'ID de l'application")

    col1, col2 = st.columns([3, 1])
    with col1:
        app_id = st.text_input(
            "",
            placeholder="Exemple: fr.haruni.frigomagic",
            help="L'ID se trouve dans l'URL de l'application (ex: play.google.com/store/apps/details?id=fr.haruni.frigomagic)"
        )
    with col2:
        fetch_button = st.button("Récupérer les avis", use_container_width=True)

# Main content
if fetch_button and app_id:
    with st.spinner("Récupération des avis en cours..."):
        reviews_data, error = get_reviews(app_id)

        if error:
            st.markdown(f"""
                <div class="error-message">
                    ❌ Erreur: {error}
                </div>
            """, unsafe_allow_html=True)
        else:
            # Success message
            st.markdown(f"""
                <div class="success-message">
                    ✅ {len(reviews_data)} avis récupérés avec succès!
                </div>
            """, unsafe_allow_html=True)

            # Display reviews
            st.markdown("### 📊 Aperçu des avis")
            df = pd.DataFrame(reviews_data)
            st.dataframe(
                df[['score', 'content']].style.format({'score': '{:.1f}'}),
                use_container_width=True
            )

            # Export options
            st.markdown("### 💾 Exporter les résultats")
            col1, col2 = st.columns(2)

            with col1:
                # PDF export
                pdf_data = create_pdf(reviews_data)
                st.markdown(
                    create_download_link(pdf_data, f"avis_{app_id}.pdf", "📥 Télécharger en PDF"),
                    unsafe_allow_html=True
                )

            with col2:
                # TXT export
                txt_data = save_txt(reviews_data, app_id)
                st.download_button(
                    label="📥 Télécharger en TXT",
                    data=txt_data,
                    file_name=f"avis_{app_id}.txt",
                    mime="text/plain"
                )

# Footer
st.markdown("""
    ---
    <div style='text-align: center; color: #666;'>
        Développé par Loris BALOCCHI | Version 1.0
    </div>
""", unsafe_allow_html=True)