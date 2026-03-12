"""
Marketplace Product Dossier Analyzer
------------------------------------

Sistema para análise estratégica de anúncios de marketplaces.

Funcionalidades:
- Coleta dados de anúncios a partir de URLs
- Analisa preços de concorrentes
- Extrai palavras-chave dominantes
- Analisa objeções de clientes
- Gera dossiê estratégico do produto

Requisitos:
pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup
from collections import Counter
import statistics
import re


# ============================================
# SCRAPER
# ============================================

class MarketplaceScraper:

    def __init__(self, url):
        self.url = url
        self.html = self.fetch_page()

    def fetch_page(self):
        try:
            response = requests.get(
                self.url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            return response.text
        except:
            return ""

    def parse_html(self):
        return BeautifulSoup(self.html, "html.parser")

    def extract_title(self):
        soup = self.parse_html()
        title = soup.find("h1")
        return title.text.strip() if title else ""

    def extract_price(self):
        soup = self.parse_html()

        price = soup.find(class_="price-tag-fraction")

        if price:
            try:
                return float(price.text.replace(".", "").replace(",", "."))
            except:
                return None

        return None

    def extract_images(self):
        soup = self.parse_html()
        imgs = soup.find_all("img")

        images = []
        for img in imgs:
            src = img.get("src")
            if src:
                images.append(src)

        return images

    def extract_description(self):
        soup = self.parse_html()

        desc = soup.find(id="description")

        if desc:
            return desc.text.strip()

        return ""

    def extract_questions(self):
        soup = self.parse_html()

        questions = []

        q_elements = soup.find_all("p")

        for q in q_elements:
            text = q.text.strip()

            if "?" in text:
                questions.append(text)

        return questions


# ============================================
# KEYWORD ANALYZER
# ============================================

class KeywordAnalyzer:

    def __init__(self, texts):
        self.texts = texts

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def extract_keywords(self, top_n=20):

        words = []

        for text in self.texts:
            cleaned = self.clean_text(text)
            words.extend(cleaned.split())

        counter = Counter(words)

        return counter.most_common(top_n)


# ============================================
# QUESTION ANALYZER
# ============================================

class QuestionAnalyzer:

    def __init__(self, questions):
        self.questions = questions

    def cluster_questions(self):

        clusters = {
            "originalidade": [],
            "entrega": [],
            "funciona": [],
            "uso": []
        }

        for q in self.questions:

            q_lower = q.lower()

            if "original" in q_lower:
                clusters["originalidade"].append(q)

            elif "entrega" in q_lower or "prazo" in q_lower:
                clusters["entrega"].append(q)

            elif "funciona" in q_lower or "resultado" in q_lower:
                clusters["funciona"].append(q)

            else:
                clusters["uso"].append(q)

        return clusters


# ============================================
# MARKET ANALYZER
# ============================================

class MarketAnalyzer:

    def __init__(self, products):
        self.products = products

    def price_analysis(self):

        prices = []

        for p in self.products:
            if p["price"]:
                prices.append(p["price"])

        if not prices:
            return {}

        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(statistics.mean(prices), 2),
            "median_price": round(statistics.median(prices), 2),
            "total_products": len(self.products)
        }

    def collect_titles(self):
        return [p["title"] for p in self.products if p["title"]]


# ============================================
# DOSSIER GENERATOR
# ============================================

class ProductDossier:

    def __init__(self, product_data, keyword_data, market_data, question_data):
        self.product_data = product_data
        self.keyword_data = keyword_data
        self.market_data = market_data
        self.question_data = question_data

    def identify_opportunities(self):

        opportunities = []

        questions_text = str(self.question_data).lower()

        if "original" in questions_text:
            opportunities.append(
                "Adicionar prova de autenticidade do produto"
            )

        if "funciona" in questions_text:
            opportunities.append(
                "Inserir provas de eficácia (antes/depois ou tecnologia)"
            )

        if "entrega" in questions_text:
            opportunities.append(
                "Destacar prazo de envio e logística"
            )

        return opportunities

    def generate_report(self):

        report = {
            "produto": self.product_data["title"],

            "analise_mercado": self.market_data,

            "palavras_chave_dominantes": self.keyword_data,

            "principais_objecoes": self.question_data,

            "oportunidades": self.identify_opportunities()
        }

        return report


# ============================================
# PIPELINE PRINCIPAL
# ============================================

class MarketplaceDossierEngine:

    def __init__(self, urls):
        self.urls = urls

    def run(self):

        products = []
        all_questions = []

        for url in self.urls:

            print(f"Analisando: {url}")

            scraper = MarketplaceScraper(url)

            product = {
                "url": url,
                "title": scraper.extract_title(),
                "price": scraper.extract_price(),
                "description": scraper.extract_description(),
                "images": scraper.extract_images()
            }

            questions = scraper.extract_questions()

            all_questions.extend(questions)

            products.append(product)

        # análise de mercado
        market_analyzer = MarketAnalyzer(products)
        market_data = market_analyzer.price_analysis()

        # análise de palavras-chave
        texts = []

        for p in products:
            texts.append(p["title"])
            texts.append(p["description"])

        keyword_analyzer = KeywordAnalyzer(texts)
        keywords = keyword_analyzer.extract_keywords()

        # análise de perguntas
        question_analyzer = QuestionAnalyzer(all_questions)
        question_clusters = question_analyzer.cluster_questions()

        # gerar dossiê
        dossier = ProductDossier(
            products[0],
            keywords,
            market_data,
            question_clusters
        )

        report = dossier.generate_report()

        return report


# ============================================
# EXECUÇÃO
# ============================================

if __name__ == "__main__":

    urls = [
        "URL_ANUNCIO_1",
        "URL_ANUNCIO_2",
        "URL_ANUNCIO_3"
    ]

    engine = MarketplaceDossierEngine(urls)

    report = engine.run()

    print("\n===== DOSSIÊ DO PRODUTO =====\n")

    for k, v in report.items():
        print(k, ":", v)