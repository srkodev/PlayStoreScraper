import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from utils import get_reviews, create_pdf, save_txt
import pandas as pd
from PIL import Image, ImageTk
import os
import re
import threading
from datetime import datetime
import time

class ModernPlayStoreApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("PlayStore Reviews Analyzer")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Couleurs et styles
        self.colors = {
            'primary': '#1f538d',
            'secondary': '#14A44D',
            'accent': '#0EA5E9',
            'success': '#14A44D',
            'warning': '#E4A11B',
            'error': '#DC2626',
            'background': '#1A1B1E',
            'surface': '#2A2B2F',
            'text': '#FFFFFF'
        }
        
        # Configuration du grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_main_content()
        self.create_footer()
        
        # Variables pour les animations
        self.loading = False
        self.progress_value = 0
        
    def create_main_content(self):
        # Container principal
        self.main_container = ctk.CTkFrame(self, fg_color=self.colors['background'])
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        # Section de recherche
        self.create_search_section()
        
        # Section des résultats (initialement cachée)
        self.create_results_section()
        
    def create_search_section(self):
        search_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['surface'],
            corner_radius=15
        )
        search_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        # URL Input avec icône
        url_container = ctk.CTkFrame(search_frame, fg_color="transparent")
        url_container.pack(pady=20, padx=30, fill="x")
        
        url_label = ctk.CTkLabel(
            url_container,
            text="URL de l'application",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        url_label.pack(anchor="w", pady=(0, 5))
        
        self.url_entry = ctk.CTkEntry(
            url_container,
            placeholder_text="https://play.google.com/store/apps/details?id=com.example.app",
            height=45,
            font=ctk.CTkFont(size=13),
            border_color=self.colors['accent']
        )
        self.url_entry.pack(fill="x", pady=(0, 10))
        
        # Bouton de recherche avec animation de chargement
        self.search_button = ctk.CTkButton(
            url_container,
            text="Analyser les avis",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            command=self.start_analysis,
            fg_color=self.colors['accent'],
            hover_color=self.colors['primary']
        )
        self.search_button.pack(pady=10)
        
        # Barre de progression - Correction de l'erreur de transparence
        self.progress_bar = ctk.CTkProgressBar(
            url_container,
            mode="indeterminate",
            height=2,
            fg_color=self.colors['surface'],  # Utilisation d'une couleur au lieu de "transparent"
            progress_color=self.colors['accent']
        )
        self.progress_bar.pack(fill="x", pady=(5, 0))
        self.progress_bar.set(0)
        
    def create_results_section(self):
        self.results_container = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['surface'],
            corner_radius=15
        )
        
        # Stats Cards
        self.stats_frame = ctk.CTkFrame(
            self.results_container,
            fg_color="transparent"
        )
        self.stats_frame.pack(fill="x", padx=20, pady=20)
        self.stats_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Reviews Section
        reviews_frame = ctk.CTkFrame(
            self.results_container,
            fg_color=self.colors['background'],
            corner_radius=10
        )
        reviews_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Titre des avis
        reviews_header = ctk.CTkFrame(reviews_frame, fg_color="transparent")
        reviews_header.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            reviews_header,
            text="Derniers avis",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        # Zone de texte des avis
        self.reviews_text = ctk.CTkTextbox(
            reviews_frame,
            font=ctk.CTkFont(size=13),
            wrap="word",
            fg_color=self.colors['surface'],
            border_color=self.colors['accent'],
            border_width=1
        )
        self.reviews_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Boutons d'export
        self.export_frame = ctk.CTkFrame(reviews_frame, fg_color="transparent")
        self.export_frame.pack(fill="x", padx=15, pady=(0, 15))
        
    def create_stat_card(self, parent, title, value, icon="📊"):
        card = ctk.CTkFrame(parent, fg_color=self.colors['background'], corner_radius=10)
        
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        )
        value_label.pack()
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12)
        )
        title_label.pack(pady=(0, 15))
        
        return card
        
    def create_footer(self):
        footer = ctk.CTkFrame(self, corner_radius=0, fg_color=self.colors['surface'], height=40)
        footer.grid(row=1, column=0, sticky="ew")
        
        footer_text = ctk.CTkLabel(
            footer,
            text=f"© {datetime.now().year} PlayStore Reviews Analyzer - Développé par Loris BALOCCHI & Jules CREVOISIER",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF"
        )
        footer_text.pack(pady=10)
        
    def start_analysis(self):
        if self.loading:
            return
            
        app_url = self.url_entry.get().strip()
        app_id = self.extract_app_id(app_url)
        
        if not app_id:
            self.show_error("URL invalide", "Veuillez entrer une URL valide du Google Play Store.")
            return
            
        self.loading = True
        self.search_button.configure(state="disabled", text="Analyse en cours...")
        self.progress_bar.start()
        
        # Lancer l'analyse dans un thread séparé
        threading.Thread(target=self.fetch_reviews, args=(app_id,), daemon=True).start()
        
    def fetch_reviews(self, app_id):
        try:
            reviews_data, error = get_reviews(app_id)
            
            if error:
                self.after(0, lambda: self.show_error("Erreur", str(error)))
                return
                
            self.after(0, lambda: self.display_results(reviews_data, app_id))
            
        finally:
            self.after(0, self.stop_loading)
            
    def stop_loading(self):
        self.loading = False
        self.search_button.configure(state="normal", text="Analyser les avis")
        self.progress_bar.stop()
        self.progress_bar.set(0)
        
    def display_results(self, reviews_data, app_id):
        # Afficher le conteneur de résultats
        self.results_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Nettoyer les anciennes stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Calculer les statistiques
        df = pd.DataFrame(reviews_data)
        mean_score = df['score'].mean()
        total_reviews = len(df)
        five_stars = len(df[df['score'] == 5])
        
        # Créer les cartes de stats
        stats = [
            ("Note moyenne", f"{mean_score:.1f}/5", "⭐"),
            ("Total des avis", str(total_reviews), "📝"),
            ("Avis 5 étoiles", str(five_stars), "🌟")
        ]
        
        for i, (title, value, icon) in enumerate(stats):
            card = self.create_stat_card(self.stats_frame, title, value, icon)
            card.grid(row=0, column=i, sticky="ew", padx=10)
            
        # Afficher les avis
        self.reviews_text.delete("0.0", "end")
        for review in reviews_data[:10]:
            stars = "⭐" * int(review['score'])
            self.reviews_text.insert("end", f"\n{stars} ({review['score']}/5)\n")
            self.reviews_text.insert("end", f"{review['content']}\n")
            self.reviews_text.insert("end", "─" * 50 + "\n")
            
        # Créer les boutons d'export
        for widget in self.export_frame.winfo_children():
            widget.destroy()
            
        export_buttons = [
            ("PDF", "📑", lambda: self.export_pdf(reviews_data, app_id)),
            ("TXT", "📝", lambda: self.export_txt(reviews_data, app_id)),
            ("Excel", "📊", lambda: self.export_excel(reviews_data, app_id))
        ]
        
        for format_name, icon, command in export_buttons:
            btn = ctk.CTkButton(
                self.export_frame,
                text=f"{icon} Export {format_name}",
                command=command,
                width=120,
                height=35,
                fg_color=self.colors['secondary'],
                hover_color="#0D8A3F"
            )
            btn.pack(side="left", padx=5)
            
    def show_error(self, title, message):
        messagebox.showerror(title, message)
        
    def show_success(self, title, message):
        messagebox.showinfo(title, message)
        
    def extract_app_id(self, url):
        pattern = r"id=([^&]+)"
        match = re.search(pattern, url)
        return match.group(1) if match else None
        
    def export_pdf(self, reviews_data, app_id):
        try:
            initial_dir = os.path.expanduser("~/Documents")  # Dossier Documents par défaut
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf")],
                initialfile=f"avis_{app_id}.pdf",
                initialdir=initial_dir,
                title="Enregistrer le fichier PDF"
            )
            if filename:
                pdf_data = create_pdf(reviews_data)
                with open(filename, 'wb') as f:
                    f.write(pdf_data)
                self.show_success("Succès", f"Export PDF réalisé avec succès!\nFichier: {filename}")
        except Exception as e:
            self.show_error("Erreur", f"Erreur lors de l'export PDF:\n{str(e)}")
            
    def export_txt(self, reviews_data, app_id):
        try:
            initial_dir = os.path.expanduser("~/Documents")
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Fichiers texte", "*.txt")],
                initialfile=f"avis_{app_id}.txt",
                initialdir=initial_dir,
                title="Enregistrer le fichier texte"
            )
            if filename:
                txt_data = save_txt(reviews_data, app_id)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(txt_data)
                self.show_success("Succès", f"Export TXT réalisé avec succès!\nFichier: {filename}")
        except Exception as e:
            self.show_error("Erreur", f"Erreur lors de l'export TXT:\n{str(e)}")
            
    def export_excel(self, reviews_data, app_id):
        try:
            initial_dir = os.path.expanduser("~/Documents")
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Fichiers Excel", "*.xlsx")],
                initialfile=f"avis_{app_id}.xlsx",
                initialdir=initial_dir,
                title="Enregistrer le fichier Excel"
            )
            if filename:
                df = pd.DataFrame(reviews_data)[['score', 'content']]
                df.to_excel(filename, index=False)
                self.show_success("Succès", f"Export Excel réalisé avec succès!\nFichier: {filename}")
        except Exception as e:
            self.show_error("Erreur", f"Erreur lors de l'export Excel:\n{str(e)}")

if __name__ == "__main__":
    app = ModernPlayStoreApp()
    app.mainloop()