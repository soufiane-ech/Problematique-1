import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from time import time


class ModelInterface:

    def __init__(self):
        # =============================
        # Chargement base RH
        # =============================
        self.rh_data = pd.read_excel(
            "RH_Infos_Quest_Réponses.xlsx",
            sheet_name="QA"
        )

        self.rh_data["profil"] = self.rh_data["profil"].str.lower().str.strip()
        self.rh_data["langue"] = self.rh_data["langue"].str.lower().str.strip()
        self.rh_data["question"] = self.rh_data["question"].str.lower()

        self.model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.rh_data["embedding"] = self.rh_data["question"].apply(
            lambda q: self.model.encode(q)
        )

        # =============================
        # STATISTIQUES KPI
        # =============================
        self.stats = {
            "total": 0,
            "understood": 0,
            "correct": 0,
            "escalated": 0,
            "response_times": [],
            "profiles_connected": set(),
            "domain_count": {}
        }

    # =============================
    # AUTHENTIFICATION
    # =============================
    def authenticate_user(self, identifiant, mdp):
        users = pd.read_excel(
            "RH_Infos_Quest_Réponses.xlsx",
            sheet_name="logging"
        )

        user = users[
            (users["identifiant"] == identifiant) &
            (users["mdp"] == mdp)
        ]

        if not user.empty:
            return user.iloc[0]["profil"]

        return None

    # =============================
    # NLP UTILITAIRES
    # =============================
    def detect_language(self, text):
        if any(c in text for c in "أبتثجحخدذرزسشصضطظعغ"):
            return "ar"
        if text.isascii():
            return "en"
        return "fr"

    def normalize(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        stopwords = [
            "je","suis","un","une","le","la","les","de","des",
            "comment","que","quoi","est","ce","pour",
            "how","do","i","am","is","the","to"
        ]
        return " ".join([w for w in text.split() if w not in stopwords])

    # =============================
    # RÉCUPÉRATION RÉPONSE
    # =============================
    def retrieve_answer(self, question, profil):
        profil = profil.lower()
        langue = self.detect_language(question)
        question = self.normalize(question)

        df = self.rh_data[
            (self.rh_data["profil"] == profil) &
            (self.rh_data["langue"] == langue)
        ]

        if df.empty:
            return None, None

        q_emb = self.model.encode(question)

        scores = df["embedding"].apply(
            lambda e: cosine_similarity([q_emb], [e])[0][0]
        )

        best_score = scores.max()
        best_idx = scores.idxmax()

        if best_score >= 0.45:
            return (
                df.loc[best_idx, "reponse"],
                df.loc[best_idx, "domaine"]
            )

        return None, None

    # =============================
    # PIPELINE PRINCIPAL + KPI
    # =============================
    def get_message_response(self, question, profil):
        start = time()
        self.stats["total"] += 1

        self.stats["profiles_connected"].add(profil.lower())

        answer, domain = self.retrieve_answer(question, profil)

        response_time = round(time() - start, 2)
        self.stats["response_times"].append(response_time)

        if answer:
            self.stats["understood"] += 1
            self.stats["correct"] += 1

            if domain:
                self.stats["domain_count"][domain] = (
                    self.stats["domain_count"].get(domain, 0) + 1
                )

            return answer

        self.stats["escalated"] += 1
        return "Je ne peux pas répondre à cette question. Veuillez contacter le service RH."

    # =============================
    # KPIs POUR RH
    # =============================
    def get_kpis(self):
        total = self.stats["total"]

        if total == 0:
            return {}

        avg_time = round(
            sum(self.stats["response_times"]) / len(self.stats["response_times"]), 2
        )

        domain_percent = {
            d: round((c / total) * 100, 2)
            for d, c in self.stats["domain_count"].items()
        }

        domain_ranking = sorted(
            self.stats["domain_count"].items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "Taux de compréhension (%)": round((self.stats["understood"] / total) * 100, 2),
            "Taux de réponse correcte (%)": round((self.stats["correct"] / total) * 100, 2),
            "Taux d’escalade (%)": round((self.stats["escalated"] / total) * 100, 2),
            "Temps moyen de réponse (s)": avg_time,
            "Profils connectés": len(self.stats["profiles_connected"]),
            "Répartition des domaines (%)": domain_percent,
            "Classement des domaines": domain_ranking
        }
