import streamlit as st
import google.generativeai as genai

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(page_title="Dossiê de Mercado IA", layout="wide")

st.title("🧠 Dossiê de Mercado com IA: Analisador de Concorrência")
st.write("Análise avançada usando a inteligência do Gemini para contornar bloqueios de sites e extrair estratégias reais de venda.")

# ============================================
# CONFIGURAÇÃO DA API DO GEMINI E AUTO-DETECÇÃO
# ============================================
try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    # TRUQUE ANTI-ERRO 404: Busca o modelo automaticamente
    modelo_valido = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name.lower():
            modelo_valido = m.name
            break # Pega o primeiro Gemini que estiver liberado para a sua chave
            
    if modelo_valido:
        model = genai.GenerativeModel(modelo_valido)
    else:
        st.error("❌ Nenhum modelo Gemini encontrado para a sua chave de API.")
        st.stop()

except Exception as e:
    st.error("⚠️ Erro de Autenticação: A chave da API do Gemini não foi encontrada ou é inválida.")
    st.info("Verifique no Streamlit Cloud (Settings > Secrets) se a variável GEMINI_API_KEY está correta.")
    st.stop()

# ============================================
# INTERFACE VISUAL (ENTRADAS DO USUÁRIO)
# ============================================
st.subheader("📋 Informações do Dossiê")
nome_produto = st.text_input("📦 Nome do Produto (Ex: Kit Aneethun Inside Deep Complex):", placeholder="Digite o nome completo do produto...")

st.write("---")

st.subheader("🔗 Links dos Concorrentes")
st.write("Cole até 8 links de anúncios. A nossa Inteligência Artificial vai analisar o contexto do mercado com base neles.")

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

# ============================================
# MOTOR DE INTELIGÊNCIA ARTIFICIAL E BOTÃO
# ============================================
if st.button("🚀 Gerar Dossiê com IA", type="primary", use_container_width=True):
    
    urls_input = [url1, url2, url3, url4, url5, url6, url7, url8]
    urls_validas = [u.strip() for u in urls_input if u.strip() != ""]
    
    if not nome_produto:
        st.warning("⚠️ Por favor, digite o Nome do Produto antes de gerar o dossiê.")
    elif not urls_validas:
        st.warning("⚠️ O Link 1 é obrigatório. Insira pelo menos um link para começar a análise.")
    else:
        with st.spinner(f"🤖 IA conectada ao modelo ({modelo_valido}). Analisando o mercado para '{nome_produto}'..."):
            
            links_formatados = "\n".join(urls_validas)

            prompt = f"""
            Você é um Especialista Sênior em E-commerce, Neuromarketing e SEO para marketplaces como o Mercado Livre no Brasil.

            Seu objetivo é criar um "Dossiê Estratégico de Concorrência" para o produto abaixo.

            Produto Alvo: {nome_produto}
            Links dos Concorrentes fornecidos:
            {links_formatados}

            Com base no nome do produto e nas pistas fornecidas pelas URLs dos concorrentes, gere um relatório estruturado nas 4 seções abaixo. 

            Sua resposta DEVE ser formatada em Markdown, usando títulos, bullet points e negritos para facilitar a leitura.

            ### 📊 1. Análise de Preços de Mercado
            Estime de forma realista o Preço Médio, o Preço Mínimo e o Preço Máximo praticado para "{nome_produto}" atualmente no mercado.

            ### 🔑 2. Palavras-Chave Dominantes (SEO)
            Liste as 10 melhores palavras-chave (incluindo cauda longa) que devem ser usadas no Título e nas Tags do anúncio para bater esses concorrentes.

            ### 🗣️ 3. Objeções dos Clientes (Oportunidades)
            Liste as 3 a 5 principais dúvidas, medos ou objeções que os clientes geralmente têm antes de finalizar a compra deste produto específico (ex: originalidade, modo de uso, falsificação, resultados).

            ### 🎯 4. Plano de Ação (Copywriting e Neuromarketing)
            Forneça 3 diretrizes visuais ou textos altamente persuasivos para colocar nas imagens do carrossel (banners) e na descrição do anúncio, visando quebrar exatamente as objeções que você mapeou acima e gerar vendas.
            """

            try:
                response = model.generate_content(prompt)
                
                st.success(f"✅ Dossiê gerado com sucesso para: **{nome_produto.upper()}**!")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error("❌ Ocorreu um erro na geração do conteúdo.")
                st.write(f"Detalhes do erro: {e}")
