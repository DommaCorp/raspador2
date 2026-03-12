import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import statistics
import re

# ============================================
# 1. LISTA DE PALAVRAS A IGNORAR (STOP WORDS PT-BR)
# ============================================
STOP_WORDS = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não",
    "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi",
    "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito",
    "há", "nos", "já", "está", "eu", "também", "só", "pelo", "pela", "até", "isso",
    "ela", "entre", "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem",
    "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", "num",
    "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia",
    "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas",
    "este", "fosse", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas",
    "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas"
}

# ============================================
# 2. MOTOR DE EXTRAÇÃO (SCRAPER)
# ============================================
class MarketplaceScraper:
    def __init__(self, url):
        self.url = url
        self.html = self.fetch_page()

    def fetch_page(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                return ""
        except Exception as e:
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

    def extract_description(self):
        soup = self.parse_html()
        desc = soup.find(class_="ui-pdp-description__content")
        if not desc:
            desc = soup.find(id="description")
        return desc.text.strip() if desc else ""

    def extract_questions(self):
        soup = self.parse_html()
        questions = []
        q_elements = soup.find_all("span", class_="ui-pdp-questions__questions-list__question__message")
        if not q_elements:
            q_elements = soup.find_all("p")
            
        for q in q_elements:
            text = q.text.strip()
            if "?" in text:
                questions.append(text)
        return questions

# ============================================
# 3. ANÁLISE DE DADOS
# ============================================
class KeywordAnalyzer:
    def __init__(self, texts):
        self.texts = texts

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def extract_keywords(self, top_n=15):
        words = []
        for text in self.texts:
            cleaned = self.clean_text(text)
            for word in cleaned.split():
                if word not in STOP_WORDS and len(word) > 2:
                    words.append(word)
        counter = Counter(words)
        return counter.most_common(top_n)

class QuestionAnalyzer:
    def __init__(self, questions):
        self.questions = questions

    def cluster_questions(self):
        clusters = {"originalidade": [], "entrega": [], "funciona": [], "uso": []}
        for q in self.questions:
            q_lower = q.lower()
            if "original" in q_lower or "falso" in q_lower:
                clusters["originalidade"].append(q)
            elif "entrega" in q_lower or "prazo" in q_lower or "chega" in q_lower:
                clusters["entrega"].append(q)
            elif "funciona" in q_lower or "resultado" in q_lower:
                clusters["funciona"].append(q)
            else:
                clusters["uso"].append(q)
        return clusters

class MarketAnalyzer:
    def __init__(self, products):
        self.products = products

    def price_analysis(self):
        prices = [p["price"] for p in self.products if p["price"]]
        if not prices:
            return {"min_price": 0, "max_price": 0, "avg_price": 0, "total_products": len(self.products)}
        
        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(statistics.mean(prices), 2),
            "total_products": len(self.products)
        }

# ============================================
# 4. INTERFACE VISUAL (STREAMLIT)
# ============================================
st.set_page_config(page_title="Dossiê do Produto", layout="wide")

st.title("🕵️‍♂️ Dossiê de Mercado: Analisador de Concorrência")
st.write("Analise seus concorrentes para extrair estratégias de venda, preços médios e objeções de clientes.")

# Campo para o Nome do Produto
st.subheader("📋 Informações do Dossiê")
nome_produto = st.text_input("📦 Nome do Produto (Ex: Kit Aneethun Inside):", placeholder="Digite o nome do produto que estamos analisando...")

st.write("---")

# Campos de entrada de URL organizados em 2 colunas
st.subheader("🔗 Links dos Concorrentes")
st.write("Cole até 8 links de anúncios (focado no Mercado Livre). O **Link 1 é obrigatório**.")

col1, col2 = st.columns(2)

with col1:
    url1 = st.text_input("1️⃣ Link 1 (Obrigatório):")
    url3 = st.text_input("3️⃣ Link 3 (Opcional):")
    url5 = st.text_input("5️⃣ Link 5 (Opcional):")
    url7 = st.text_input("7️⃣ Link 7 (Opcional):")

with col2:
    url2 = st.text_input("2️⃣ Link 2 (Opcional):")
    url4 = st.text_input("4️⃣ Link 4 (Opcional):")
    url6 = st.text_input("6️⃣ Link 6 (Opcional):")
    url8 = st.text_input("8️⃣ Link 8 (Opcional):")

st.write("---")

# Botão de Ação
if st.button("🚀 Gerar Dossiê Estratégico", type="primary", use_container_width=True):
    
    # Coleta todos os links preenchidos
    urls_input = [url1, url2, url3, url4, url5, url6, url7, url8]
    urls = [u.strip() for u in urls_input if u.strip() != ""]
    
    # Validações antes de rodar
    if not nome_produto:
        st.warning("⚠️ Por favor, digite o Nome do Produto antes de gerar o dossiê.")
    elif not url1.strip():
        st.warning("⚠️ O Link 1 é obrigatório. Insira pelo menos um link para começar a análise.")
    else:
        with st.spinner(f"A raspar dados, analisar preços e a ler objeções para '{nome_produto}'..."):
            products = []
            all_questions = []

            # Processamento
            for url in urls:
                scraper = MarketplaceScraper(url)
                product = {
                    "title": scraper.extract_title(),
                    "price": scraper.extract_price(),
                    "description": scraper.extract_description(),
                }
                questions = scraper.extract_questions()
                all_questions.extend(questions)
                products.append(product)

            # Análises
            market_data = MarketAnalyzer(products).price_analysis()
            
            texts = [p["title"] + " " + p["description"] for p in products]
            keywords = KeywordAnalyzer(texts).extract_keywords()
            
            question_clusters = QuestionAnalyzer(all_questions).cluster_questions()

            st.success(f"✅ Dossiê gerado com sucesso para: **{nome_produto.upper()}**!")
            
            st.divider()

            # --- APRESENTAÇÃO DOS RESULTADOS ---
            
            st.subheader(f"📊 1. Análise de Preços de Mercado ({market_data['total_products']} anúncios lidos)")
            if market_data["avg_price"] > 0:
                m1, m2, m3 = st.columns(3)
                m1.metric("Preço Médio", f"R$ {market_data['avg_price']:.2f}")
                m2.metric("Preço Mais Baixo", f"R$ {market_data['min_price']:.2f}")
                m3.metric("Preço Mais Alto", f"R$ {market_data['max_price']:.2f}")
            else:
                st.info("Não foi possível extrair preços. Verifica se o layout do marketplace mudou ou se há bloqueios.")

            col_a, col_b = st.columns(2)
            
            with col_a:
                st.subheader("🔑 2. Palavras-Chave Dominantes (SEO)")
                st.write("Estes são os termos mais repetidos pelos teus concorrentes (ideais para os teus títulos e tags):")
                if keywords:
                    for word, count in keywords:
                        st.markdown(f"- **{word.upper()}** (usada {count} vezes)")
                else:
                    st.write("Nenhum texto descritivo suficiente encontrado.")

            with col_b:
                st.subheader("🗣️ 3. Objeções dos Clientes (Oportunidades)")
                st.write("O que os clientes estão a perguntar antes de comprar?")
                
                tem_perguntas = False
                for categoria, perguntas in question_clusters.items():
                    if perguntas:
                        tem_perguntas = True
                        with st.expander(f"Dúvidas sobre: {categoria.upper()} ({len(perguntas)})"):
                            for p in perguntas:
                                st.write(f"- {p}")
                
                if not tem_perguntas:
                    st.info("Nenhuma pergunta foi encontrada nestes anúncios.")
                    
            st.subheader("🎯 4. Plano de Ação (Copywriting)")
            st.write("Com base nas objeções detetadas, adicione isso aos seus banners e descrições:")
            if len(question_clusters["originalidade"]) > 0:
                st.warning("👉 **Alerta de Falsificação:** Muitos clientes perguntam se é original. Coloque um selo de '100% Original' nas suas fotos.")
            if len(question_clusters["funciona"]) > 0:
                st.info("👉 **Falta de Prova Social:** Clientes duvidam do resultado. Adicione fotos de Antes/Depois no carrossel da imagem.")
            if len(question_clusters["entrega"]) > 0:
                st.success("👉 **Ansiedade de Envio:** Destaque 'Envio Imediato' ou 'Pronta Entrega' na sua primeira foto.")
        print(k, ":", v)
