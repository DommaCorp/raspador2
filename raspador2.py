import streamlit as st
import google.generativeai as genai

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(page_title="Dossiê de Mercado IA - Neuromarketing", layout="wide")

st.title("🧠 Dossiê de Mercado com IA e Neuromarketing")
st.write("Análise avançada usando a inteligência do Gemini para extrair dados de mercado e o DNA emocional da venda.")

# ============================================
# CONFIGURAÇÃO DA API DO GEMINI E AUTO-DETECÇÃO
# ============================================
try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    
    modelo_valido = None
    prioridade_modelos = ['gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro']
    modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    for p in prioridade_modelos:
        full_name = f"models/{p}"
        if full_name in modelos_disponiveis:
            modelo_valido = full_name
            break
            
    if not modelo_valido and modelos_disponiveis:
        for m in modelos_disponiveis:
            if 'gemini' in m.lower():
                modelo_valido = m
                break

    if modelo_valido:
        model = genai.GenerativeModel(modelo_valido)
    else:
        st.error("❌ Nenhum modelo Gemini válido encontrado para a sua chave de API.")
        st.stop()

except Exception as e:
    st.error("⚠️ Erro de Autenticação: A chave da API do Gemini não foi encontrada ou é inválida.")
    st.info("Verifique no Streamlit Cloud (Settings > Secrets) se a variável GEMINI_API_KEY está correta.")
    st.stop()

# ============================================
# INTERFACE VISUAL (ENTRADAS DO USUÁRIO)
# ============================================
st.subheader("📋 Informações do Dossiê")
nome_produto = st.text_input("📦 Nome do Produto (Ex: Kit Aneethun Inside Deep Complex):", placeholder="Digite o nome completo do produto que estamos analisando...")

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
if st.button("🚀 Gerar Dossiê Estratégico Completo", type="primary", use_container_width=True):
    
    urls_input = [url1, url2, url3, url4, url5, url6, url7, url8]
    urls_validas = [u.strip() for u in urls_input if u.strip() != ""]
    
    if not nome_produto:
        st.warning("⚠️ Por favor, digite o Nome do Produto antes de gerar o dossiê.")
    elif not urls_validas:
        st.warning("⚠️ O Link 1 é obrigatório. Insira pelo menos um link para começar a análise.")
    else:
        with st.spinner(f"🤖 IA conectada ({modelo_valido}). Analisando mercado e criando roteiro visual para '{nome_produto}'..."):
            
            links_formatados = "\n".join(urls_validas)

            # --- PROMPT MESTRE COM A NOVA SEÇÃO 5 ---
            prompt = f"""
            Você é um Especialista Sênior em E-commerce, Neuromarketing, SEO e Direção de Arte Visual para marketplaces como o Mercado Livre no Brasil.

            Seu objetivo é criar um "Dossiê Estratégico de Concorrência e Criação Visual" para o produto abaixo.

            Produto Alvo: {nome_produto}
            Links dos Concorrentes fornecidos:
            {links_formatados}

            Com base no nome do produto e nas pistas fornecidas pelas URLs dos concorrentes, gere um relatório estruturado exatamente nas 5 seções abaixo. 

            Sua resposta DEVE ser formatada em Markdown, usando títulos (#), bullet points (-) e negritos (**) para facilitar a leitura.

            ### 📊 1. Análise de Preços de Mercado
            Estime de forma realista o Preço Médio, o Preço Mínimo e o Preço Máximo praticado para "{nome_produto}" atualmente no mercado.

            ### 🔑 2. Palavras-Chave Dominantes (SEO)
            Liste as 10 melhores palavras-chave (incluindo cauda longa) que devem ser usadas no Título e nas Tags do anúncio para bater esses concorrentes.

            ### 🧠 3. O DNA Emocional da Compra (Análise de Neuromarketing)
            Analise o que o comprador de "{nome_produto}" realmente quer comprar. Responda usando a técnica do cérebro triúno:
            1.  O que o **Cérebro Primitivo** (Reptiliano) está buscando? (Focado em status, segurança, prazer imediato, aceitação social).
            2.  Como o **Cérebro Límbico** (Emocional) justifica essa compra e racionaliza esse desejo? Descreva qual é o **objetivo emocional** final da compra.

            ### 🗣️ 4. Objeções dos Clientes (Oportunidades)
            Liste as 3 a 5 principais dúvidas, medos ou objeções que os clientes geralmente têm antes de finalizar a compra deste produto específico.

            ### 🎯 5. Plano de Produção Visual e Redação (Carrossel de Imagens)
            Com base nas análises das Seções 3 e 4, crie um roteiro detalhado para um carrossel de imagens visando converter a venda.

            **REGRAS GLOBAIS OBRIGATÓRIAS PARA OS PROMPTS DE IMAGEM:**
            - Adicione no final de CADA prompt o seguinte comando exato: "Tamanho 1200x1200px, resolução 241 dpi. Os textos, fontes e design da embalagem devem ser RIGOROSAMENTE IDÊNTICOS ao produto original".

            Estruture esta seção rigorosamente nas seguintes categorias, fornecendo sempre o PROMPT DE IMAGEM e o TEXTO OVERLAY (COPY):

            #### A. Foto 1: A Capa Perfeita (Obrigatório Fundo Branco)
            A primeira imagem é a vitrine do anúncio. 
            - **Regra da Capa:** Esta é a ÚNICA foto que deve ter o fundo 100% branco (as demais têm fundo livre).
            - **Prompt:** Crie um prompt focado no produto com fundo branco puro. Descreva um ângulo estratégico (ex: low angle para imponência) e uma iluminação (ex: reflexos brilhantes controlados) que tornem o produto extremamente atrativo. Inclua as regras globais de tamanho e embalagem.
            - **Texto na Foto:** (Geralmente a capa não tem texto para não perder exposição, mas sugira caso aplique).

            #### B. Fotos de Benefícios (1 a 3 imagens)
            Sugira imagens com fundo livre que materializam os principais benefícios técnicos e emocionais.
            - **Prompt:** Cena, iluminação, ângulo e regras globais de tamanho/embalagem.
            - **Texto na Foto:** Título curto e Checklist de benefícios.

            #### C. Fotos de Quebra de Objeção (1 a 3 imagens)
            Imagens para quebrar os medos mapeados na Seção 4 (ex: originalidade, modo de uso, tamanho). Fundo livre.
            - **Prompt:** Cena, iluminação, ângulo e regras globais de tamanho/embalagem.
            - **Texto na Foto:** Títulos e textos de garantia ou prova social.

            #### D. Foto Ambientada de Conclusão (1 imagem - O "Grand Finale")
            A foto de fechamento de venda. Fundo livre. Mostre o resultado final desejado pelo cérebro Límbico e Primitivo.
            - **Prompt:** Cena com modelo ou ambiente altamente sofisticado, iluminação, ângulo e regras globais de tamanho/embalagem.
            - **Texto na Foto:** Frase curta final resumindo a transformação emocional.
            """

            try:
                response = model.generate_content(prompt)
                
                st.success(f"✅ Dossiê gerado com sucesso para: **{nome_produto.upper()}**!")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error("❌ Ocorreu um erro na geração do conteúdo pela IA.")
                st.write(f"Detalhes do erro: {e}")
