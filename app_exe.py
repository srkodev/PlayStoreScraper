import sys
from google_play_scraper import reviews_all
import os
from datetime import datetime

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════════════╗
    ║  📱 Google Play Store Scraper d'Avis - par Loris BALOCCHI 📱               ─ □ ✕  ║
    ╠═══════════════════════════════════════════════════════════════════════════════════╣
    ║  Entrez l'ID de l'application :                                                   ║
    ║  ───────────────────────────────────────────────────────────────────────────────  ║
    ║  Exemple :                                                                        ║
    ║   🔹 Pour https://play.google.com/store/apps/details?id=fr.haruni.frigomagic      ║
    ║   🔹 Entrez seulement : fr.haruni.frigomagic                                      ║
    ╚═══════════════════════════════════════════════════════════════════════════════════╝
    """)

    app_id = input("\nEntrez l'ID de l'application : ").strip()
    
    try:
        print("\nRécupération des avis en cours...")
        reviews = reviews_all(app_id, lang="fr", country="fr")
        
        # Créer le dossier de sortie
        output_dir = "avis_exports"
        os.makedirs(output_dir, exist_ok=True)
        
        # Générer le nom de fichier avec la date
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/avis_{app_id}_{timestamp}.txt"
        
        # Sauvegarder les avis
        with open(filename, "w", encoding="utf-8") as file:
            for review in reviews:
                if review["content"]:
                    file.write(f"Note: {review['score']}/5\n")
                    file.write(f"{review['content']}\n")
                    file.write("-" * 80 + "\n\n")
        
        print(f"\n✅ {len(reviews)} avis ont été récupérés avec succès!")
        print(f"📂 Les avis ont été sauvegardés dans : {filename}")
        
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {str(e)}")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
