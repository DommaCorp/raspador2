import streamlit as st
import google.generativeai as genai
import os

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(page_title="DOMMACORP - Dossiê IA", layout="wide", page_icon="🔥")

# ============================================
# INJEÇÃO DE CSS (TEMA LIGHT DOMMACORP)
# ============================================
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    p, .stMarkdown { color: #333333 !important; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF8C00 0%, #FF5100 100%);
        color: white !important; border: none; border-radius: 8px;
        padding: 10px 24px; font-weight: bold; font-size: 18px;
        transition: all 0.3s ease; box-shadow: 0px 4px 10px rgba(255, 140, 0, 0.3);
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02); box-shadow: 0px 6px 15px rgba(255, 140, 0, 0.6);
    }
    h1, h2, h3 { color: #FF8C00 !important; }
    label { color: #1E1E1E !important; font-weight: 600 !important; }
    .stTextInput > div > div > input {
        background-color: #F8F9FA !important; color: #000000 !important;
        border: 1px solid #FF8C00 !important; border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CABEÇALHO COM LOGO
# ============================================
col_vazia1, col_logo, col_vazia2 = st.columns([2, 1, 2])
with col_logo:
    if os.path.exists("logo.jpg"): st.image("logo.jpg", use_container_width=True)
    elif os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    else: st.markdown("<h1 style='text-align: center; font-size: 50px;'>DOMMACORP</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Dossiê de Mercado com IA e Neuromarketing</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Domine. Converta. Cresça. - Extração de dados de mercado e DNA emocional de vendas.</p>", unsafe_allow_html=True)
st.write("---")

# ============================================
# CONFIGURAÇÃO DA API
# ============================================
try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    modelo_valido = None
    prioridade_modelos = ['gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro']
    modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    for p in prioridade_modelos:
        if f"models/{p}" in modelos_disponiveis:
            modelo_valido = f"models/{p}"
            break
            
    if not modelo_valido:
        for m in modelos_disponiveis:
            if 'gemini' in m.lower():
                modelo_valido = m
                break

    if modelo_valido: model = genai.GenerativeModel(modelo_valido)
    else:
        st.error("❌ Nenhum modelo Gemini válido encontrado.")
        st.stop()
except Exception as e:
    st.error("⚠️ Erro de Autenticação na API do Gemini.")
    st.stop()

# ============================================
# INTERFACE
# ============================================
st.subheader("📋 Informações do Dossiê")
nome_produto = st.text_input("📦 Nome do Produto (Ex: Kit Aneethun Inside Deep Complex):")
st.write("---")
st.subheader("🔗 Comparativo: Seu Anúncio vs Concorrência")
st.write("Cole o **SEU** anúncio (ou o alvo principal) no Link 1, e os concorrentes nos demais.")

col1, col2 = st.columns(2)
with col1:
    url1 = st.text_input("1️⃣ Link 1 (SEU ANÚNCIO - Obrigatório):")
    url3 = st.text_input("3️⃣ Link 3 (Concorrente - Opcional):")
    url5 = st.text_input("5️⃣ Link 5 (Concorrente - Opcional):")
    url7 = st.text_input("7️⃣ Link 7 (Concorrente - Opcional):")
with col2:
    url2 = st.text_input("2️⃣ Link 2 (Concorrente - Opcional):")
    url4 = st.text_input("4️⃣ Link 4 (Concorrente - Opcional):")
    url6 = st.text_input("6️⃣ Link 6 (Concorrente - Opcional):")
    url8 = st.text_input("8️⃣ Link 8 (Concorrente - Opcional):")
st.write("---")

# ============================================
# MOTOR IA
# ============================================
if st.button("🚀 Gerar Dossiê DOMMACORP", type="primary", use_container_width=True):
    urls_input = [url1, url2, url3, url4, url5, url6, url7, url8]
    urls_validas = [u.strip() for u in urls_input if u.strip() != ""]
    
    if not nome_produto: st.warning("⚠️ Digite o Nome do Produto.")
    elif not urls_validas: st.warning("⚠️ O Link 1 (Seu Anúncio) é obrigatório.")
    else:
        with st.spinner(f"🤖 Cruzando os dados do seu anúncio com a concorrência para '{nome_produto}'..."):
            link_principal = urls_validas[0]
            links_concorrentes = "\n".join(urls_validas[1:]) if len(urls_validas) > 1 else "Nenhum concorrente adicional fornecido."

            prompt = f"""
            Você é um Especialista Sênior em E-commerce, Neuromarketing, SEO e Experiência do Cliente para marketplaces como o Mercado Livre no Brasil.

            Produto Alvo: {nome_produto}
            Link Principal (Meu Anúncio): {link_principal}
            Links dos Concorrentes:
            {links_concorrentes}

            Sua missão é CRUzar os dados do Meu Anúncio com a Concorrência e gerar um relatório estruturado exatamente nas 6 seções abaixo em Markdown.

            ### 📊 1. Análise de Preços e Categorias
            - **Preço:** Estime o Preço Médio, Mínimo e Máximo praticado no mercado. Compare com o Link Principal.
            - **Categorização:** Analise a categoria provável do Link Principal em relação aos Concorrentes. Existe alguma falha na categorização atual ou uma categoria de nicho mais vantajosa sendo usada pela concorrência?

            ### 🔑 2. Palavras-Chave Dominantes (SEO)
            Cruze os dados e liste as 10 melhores palavras-chave que faltam no Link Principal ou que devem ser reforçadas, divididas em:
            - **5 Palavras de Cauda Curta (Short-tail):** (Ex: termos amplos e de alto volume).
            - **5 Palavras de Cauda Longa (Long-tail):** (Ex: termos específicos e de alta conversão).

            ### 🧠 3. O DNA Emocional (O Que Ele REALMENTE Compra)
            Responda com extrema precisão o que o cliente REALMENTE quer comprar ao adquirir "{nome_produto}". (Lembre-se: Ele não compra uma furadeira, compra um buraco na parede. Ele não compra um cosmético, compra juventude/pertencimento).
            1. **O Desejo do Cérebro Primitivo:** (Busca por status, sobrevivência, reprodução, fuga da dor ou aceitação social).
            2. **A Justificativa do Cérebro Límbico:** (Qual a história emocional que ele conta a si mesmo para validar essa compra?).

            ### 🗣️ 4. A Voz do Cliente (Perguntas e Avaliações Reais)
            Mapeie os atritos reais dos compradores desse nicho:
            1. **Dúvidas Frequentes:** O que eles mais perguntam antes de comprar?
            2. **Reclamações Recorrentes nos Concorrentes:** Quais as maiores dores nas avaliações negativas? 

            ### 🛠️ 5. Plano de Melhorias Operacionais e Estruturais
            Com base na Seção 4, liste de 2 a 4 ações TÁTICAS (variações, kits, mudança de embalagem, manuais em PDF) para aplicar no Link Principal e aniquilar os problemas da concorrência na raiz.

            ### 🎯 6. Plano de Produção Visual Estratégico (Carrossel)
            Use os desejos da Seção 3 e as resoluções da Seção 5 para criar o roteiro das fotos.

            **REGRAS GLOBAIS OBRIGATÓRIAS PARA OS PROMPTS:**
            Adicione no final de CADA prompt: "Tamanho 1200x1200px, resolução 241 dpi. Textos, fontes e embalagem RIGOROSAMENTE IDÊNTICOS ao original".

            #### A. Foto 1: A Capa Perfeita (Fundo Branco)
            - **Prompt:** Fundo 100% branco puro. Ângulo imponente.
            - **Texto:** (Sugira apenas se for um selo de originalidade).

            #### B. Fotos de Benefícios (1 a 3 imagens)
            - **Prompt:** Foco em satisfazer o desejo Límbico. Fundo livre.
            - **Texto:** Título curto e Checklist do benefício emocional.

            #### C. Fotos de Quebra de Objeção e Instrução (1 a 3 imagens)
            - **Prompt:** Imagens visuais resolvendo as dores operacionais (ex: tabela, embalagem segura).
            - **Texto:** Garantias e instruções.

            #### D. Foto Ambientada de Conclusão (O "Grand Finale")
            - **Prompt:** A foto do "eu ideal" alcançando o desejo Primitivo realçado na Seção 3.
            - **Texto:** Frase curta de transformação emocional (o que ele REALMENTE comprou).
            """

            try:
                response = model.generate_content(prompt)
                st.success(f"✅ Dossiê DOMMACORP gerado com sucesso para: **{nome_produto.upper()}**!")
                st.divider()
                st.markdown(response.text)
            except Exception as e:
                st.error("❌ Erro na geração do conteúdo.")
                st.write(f"Detalhes: {e}")
