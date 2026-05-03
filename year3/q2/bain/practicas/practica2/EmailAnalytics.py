import re

import networkx as nx
import nltk
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from textblob import TextBlob


class Email:
    REQUIRED_COLUMNS = ["email_id", "date", "sender", "recipients", "cc", "subject", "body"]

    def __init__(self, csv_path: str):
        nltk.download("stopwords", quiet=True)
        self.csv_path = csv_path
        self.df = None
        self.graph = None
        self.dictionary = None
        self.corpus = None
        self.lda_model = None
        self.stop_words = set(stopwords.words("english"))

    def _ensure_dataframe(self) -> None:
        if self.df is None:
            self.load_data()

    def _split_emails(self, value: str) -> list[str]:
        if not value:
            return []
        return [email.strip() for email in str(value).split(";") if email.strip()]

    def _sentiment_label(self, polarity: float) -> str:
        if polarity > 0.1:
            return "positive"
        if polarity < -0.1:
            return "negative"
        return "neutral"

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)

        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Faltan columnas obligatorias: {missing_columns}")

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        for col in ["sender", "recipients", "cc", "subject", "body"]:
            df[col] = df[col].fillna("")

        df["text"] = df["subject"].str.strip() + " " + df["body"].str.strip()

        self.df = df
        return self.df.copy()

    def build_interaction_graph(self, include_cc: bool = True) -> nx.DiGraph:
        self._ensure_dataframe()
        graph = nx.DiGraph()

        for _, row in self.df.iterrows():
            sender = str(row["sender"]).strip()
            if not sender:
                continue

            recipients = self._split_emails(row["recipients"])
            cc_list = self._split_emails(row["cc"]) if include_cc else []
            targets = recipients + cc_list

            for target in targets:
                if not target or target == sender:
                    continue
                if graph.has_edge(sender, target):
                    graph[sender][target]["weight"] += 1
                else:
                    graph.add_edge(sender, target, weight=1)

        self.graph = graph
        return self.graph

    def analyze_sentiment(self, text_column: str = "text") -> pd.DataFrame:
        self._ensure_dataframe()

        if text_column not in self.df.columns:
            raise ValueError(f"La columna '{text_column}' no existe en el DataFrame.")

        texts = self.df[text_column]
        polarities = []
        subjectivities = []
        labels = []

        for text in texts:
            sentiment = TextBlob(text).sentiment
            polarity, subjectivity = sentiment
            polarities.append(polarity)
            subjectivities.append(subjectivity)
            labels.append(self._sentiment_label(polarity))

        self.df["polarity"] = polarities
        self.df["subjectivity"] = subjectivities
        self.df["sentiment_label"] = labels

        return self.df.copy()

    def preprocess_text_for_lda(self, text: str) -> list[str]:
        if text is None:
            return []
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", str(text).lower())
        tokens = simple_preprocess(text, deacc=True)
        cleaned_tokens = [tok for tok in tokens if tok not in self.stop_words]

        return cleaned_tokens

    def train_topic_model(self, num_topics: int = 3, passes: int = 15, random_state: int = 42) -> tuple[LdaModel, Dictionary, list[list[tuple]]]:
        self._ensure_dataframe()

        processed_docs = [self.preprocess_text_for_lda(text) for text in self.df["text"]]
        processed_docs = [doc if doc else ["empty"] for doc in processed_docs]

        dictionary = Dictionary(processed_docs)
        corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

        effective_topics = max(1, min(num_topics, len(processed_docs), max(1, len(dictionary))))

        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=effective_topics, passes=passes, random_state=random_state)

        self.dictionary = dictionary
        self.corpus = corpus
        self.lda_model = lda_model

        return self.lda_model, self.dictionary, self.corpus

    def assign_topics(self) -> pd.DataFrame:
        if self.lda_model is None or self.corpus is None:
            self.train_topic_model()

        dominant_topics = []
        topic_keywords = []

        for bow in self.corpus:
            topic_distribution = self.lda_model.get_document_topics(bow, minimum_probability=0)
            best_topic = max(topic_distribution, key=lambda x: x[1])[0] if topic_distribution else 0
            dominant_topics.append(int(best_topic))
            topic_keywords.append(", ".join(word for word, _ in self.lda_model.show_topic(best_topic, topn=5)))

        self.df["dominant_topic"] = dominant_topics
        self.df["topic_keywords"] = topic_keywords

        return self.df.copy()

    def get_topic_report(self, topn_words: int = 5) -> pd.DataFrame:
        if self.lda_model is None:
            self.train_topic_model()
        if "dominant_topic" not in self.df.columns:
            self.assign_topics()
        if "polarity" not in self.df.columns:
            self.analyze_sentiment()

        rows = []
        for topic_id in range(self.lda_model.num_topics):
            subset = self.df[self.df["dominant_topic"] == topic_id]
            keywords = ", ".join(word for word, _ in self.lda_model.show_topic(topic_id, topn=topn_words))
            rows.append({
                "topic_id": int(topic_id),
                "keywords": keywords,
                "num_emails": int(len(subset)),
                "mean_polarity": (float(subset["polarity"].mean()) if len(subset) > 0 else 0.0)
            })

        return pd.DataFrame(rows).sort_values("topic_id").reset_index(drop=True)

    def get_emails_by_sender(self, sender: str) -> pd.DataFrame:
        self._ensure_dataframe()
        return self.df[self.df["sender"] == sender].copy()

    def get_emails_by_topic(self, topic_id: int) -> pd.DataFrame:
        if "dominant_topic" not in self.df.columns:
            self.assign_topics()
        return self.df[self.df["dominant_topic"] == topic_id].copy()

    def graph_metrics(self) -> dict[str, float]:
        if self.graph is None:
            self.build_interaction_graph()

        return {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": float(nx.density(self.graph))
        }
