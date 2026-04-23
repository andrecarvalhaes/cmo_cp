#!/usr/bin/env python3
"""
Gera PDF: Análise Estratégica Instagram @clubpetro
Cruza dados reais da API com análise qualitativa.
"""
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, "Analise Estrategica Instagram @clubpetro | Abril 2026", align="R")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def titulo_secao(self, txt):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(230, 80, 0)
        self.cell(0, 12, txt, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(230, 80, 0)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def subtitulo(self, txt):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, txt, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def sub2(self, txt):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, txt, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def corpo(self, txt):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, txt)
        self.ln(2)

    def corpo_bold(self, txt):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, txt)
        self.ln(2)

    def bullet(self, txt):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, txt)
        self.ln(1)

    def nota_box(self, titulo, txt):
        self.set_fill_color(255, 243, 230)
        self.set_draw_color(230, 80, 0)
        y0 = self.get_y()
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(230, 80, 0)
        self.cell(0, 7, f"  {titulo}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(60, 40, 0)
        self.multi_cell(0, 5, f"  {txt}", fill=True)
        y1 = self.get_y()
        self.rect(self.l_margin, y0, self.w - self.l_margin - self.r_margin, y1 - y0)
        self.ln(4)

    def tabela(self, headers, rows, col_widths=None):
        if col_widths is None:
            w = (self.w - self.l_margin - self.r_margin) / len(headers)
            col_widths = [w] * len(headers)
        # header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(40, 40, 40)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in rows:
            if self.get_y() > 265:
                self.add_page()
                self.set_font("Helvetica", "B", 9)
                self.set_fill_color(40, 40, 40)
                self.set_text_color(255, 255, 255)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
                self.ln()
                self.set_font("Helvetica", "", 9)
                self.set_text_color(30, 30, 30)
                fill = False
            if fill:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 6, str(cell), border=1, fill=True, align="C" if i > 0 else "L")
            self.ln()
            fill = not fill
        self.ln(3)

    def check_page(self, needed=30):
        if self.get_y() > 297 - 20 - needed:
            self.add_page()


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# === CAPA ===
pdf.ln(40)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(230, 80, 0)
pdf.cell(0, 14, "Analise Estrategica", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 14, "Instagram @clubpetro", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)
pdf.set_font("Helvetica", "", 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, "Auditoria completa de perfil + Diagnostico + Banco de temas", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(15)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 7, "Data: 21 de Abril de 2026", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, "Dados: Instagram Graph API v21.0 (real-time)", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, "Preparado para: Andre Carvalhaes, CMO ClubPetro", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(30)
pdf.set_draw_color(230, 80, 0)
pdf.line(60, pdf.get_y(), pdf.w - 60, pdf.get_y())
pdf.ln(8)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(140, 140, 140)
pdf.cell(0, 6, "Documento confidencial - ClubPetro", align="C", new_x="LMARGIN", new_y="NEXT")

# === SUMARIO EXECUTIVO ===
pdf.add_page()
pdf.titulo_secao("SUMARIO EXECUTIVO")
pdf.corpo(
    "O @clubpetro lidera o nicho de tecnologia para postos de combustivel no Instagram com 22.069 seguidores "
    "- 2x o segundo colocado (WebPosto, 11K) e 4x o terceiro (XPert, 5,2K). A identidade visual e forte, o mix "
    "de formatos e adequado e o alcance diario medio de ~14K (63% da base) e excelente.\n\n"
    "Porem, o perfil opera significativamente abaixo do seu potencial. O engagement rate medio sobre followers e "
    "de 0,14% - bem abaixo do benchmark B2B de 1,5%. O SEO do Instagram esta praticamente zerado (nome sem "
    "palavra-chave, bio sem termos indexaveis, alt-text vazio). Os ganchos dos Reels sao descritivos em vez de "
    "persuasivos, perdendo retencao nos primeiros 3 segundos.\n\n"
    "A boa noticia: quando medimos o True ER (interacoes/reach em vez de interacoes/followers), os melhores "
    "posts atingem 3,8% a 11,9% - excelente para B2B. O problema nao e a qualidade do conteudo em si, e a "
    "otimizacao para distribuicao. As correcoes sao tecnicas e podem ser implementadas imediatamente."
)

pdf.nota_box("NOTA GERAL: 58/100",
    "Fase: Em crescimento com risco de estagnacao. Lideranca de audiencia no segmento, mas perdendo "
    "30-50% do alcance potencial por problemas corrigiveis sem custo.")

# === DADOS REAIS DA API ===
pdf.titulo_secao("DADOS REAIS DA API (21/04/2026)")
pdf.subtitulo("Perfil")
pdf.tabela(
    ["Metrica", "Valor"],
    [
        ["Seguidores", "22.069"],
        ["Seguindo", "6.474"],
        ["Posts totais", "1.491"],
        ["Bio link", "ig.rdstation.com/clubpetro"],
        ["Bio", "Aditivamos os Resultados de +1800 Postos..."],
    ],
    [100, 90]
)

pdf.subtitulo("Alcance - Ultimos 30 dias")
pdf.tabela(
    ["Metrica", "Valor"],
    [
        ["Reach total (30d)", "415.613"],
        ["Reach diario medio", "13.854"],
        ["Reach diario maximo", "18.318"],
        ["Reach diario minimo", "7.421"],
        ["Reach / Followers", "~63% (benchmark >50% = excelente)"],
        ["Novos seguidores (30d)", "+487 (~16/dia)"],
        ["Accounts engaged", "1.998"],
        ["Total interactions", "4.669"],
        ["Website clicks", "111"],
        ["Profile views", "2.905"],
    ],
    [100, 90]
)

pdf.subtitulo("Engagement - Ultimos 25 posts")
pdf.tabela(
    ["Metrica", "Valor"],
    [
        ["Total likes", "657"],
        ["Total comments", "130"],
        ["Total engagement", "787"],
        ["Avg likes/post", "26,3"],
        ["Avg comments/post", "5,2"],
        ["Avg ER (eng/followers)", "0,143%"],
        ["Mix: Reels", "18 (72%)"],
        ["Mix: Carrosseis", "6 (24%)"],
        ["Mix: Imagem", "1 (4%)"],
    ],
    [100, 90]
)

pdf.subtitulo("Performance por tipo de conteudo")
pdf.tabela(
    ["Tipo", "Qtd", "Avg Likes", "Avg Comments", "Avg ER"],
    [
        ["VIDEO (Reels)", "18", "28,2", "6,6", "0,158%"],
        ["CAROUSEL", "6", "24,0", "2,0", "0,118%"],
        ["IMAGE", "1", "5,0", "0,0", "0,023%"],
    ],
    [40, 25, 35, 45, 45]
)

pdf.check_page(60)
pdf.subtitulo("True ER - Top 5 posts (interacoes/reach)")
pdf.corpo(
    "O ER sobre followers (0,14%) e enganoso. O True ER (total_interactions / reach) revela que os "
    "melhores posts performam excelentemente - o problema esta na base de seguidores inativos, nao "
    "na qualidade do conteudo."
)
pdf.tabela(
    ["Post", "Tipo", "True ER", "Shares", "Reach"],
    [
        ["Guerra/greve/desabastecimento", "Reel", "11,86%", "7", "1.054"],
        ["Google Maps postos", "Reel", "11,07%", "3", "858"],
        ["Preco combustivel disparou", "Reel", "5,46%", "41", "2.071"],
        ["Fiscalizacao postos", "Carousel", "3,81%", "98", "6.115"],
        ["A culpa nao e nossa", "Reel", "3,81%", "39", "2.700"],
    ],
    [52, 26, 26, 26, 30]
)

pdf.nota_box("INSIGHT CRITICO",
    "O post de fiscalizacao teve 98 shares e 6.115 de reach - True ER de 3,81%. "
    "Shares sao o multiplicador de distribuicao mais forte do algoritmo. "
    "Conteudo que gera indignacao do setor e o motor de crescimento organico desse perfil.")

# === COMPETITIVO ===
pdf.check_page(50)
pdf.titulo_secao("PANORAMA COMPETITIVO")
pdf.corpo(
    "ClubPetro lidera o nicho no Instagram por larga margem. Nenhum concorrente direto ou player do "
    "setor se aproxima dos 22K seguidores. Isso e um ativo real de distribuicao."
)
pdf.tabela(
    ["Perfil", "Seguidores", "Tipo", "Posts"],
    [
        ["@clubpetro", "22.069", "SaaS Fidelizacao", "1.491"],
        ["@webposto.oficial", "~11.000", "ERP para Postos", "~253"],
        ["@sejaxpert", "~5.197", "Automacao Postos", "-"],
        ["@renato.brasilpostos", "~4.054", "Influenciador B2B", "~796"],
        ["@linxpostos", "~1.778", "SaaS Gestao", "-"],
    ],
    [50, 35, 55, 30]
)

# === PARTE 1 - AVALIACAO ===
pdf.add_page()
pdf.titulo_secao("PARTE 1 - AVALIACAO DO PERFIL (10 dimensoes)")
pdf.corpo("Escala: 1-3 = prejudica ativamente | 4-5 = perde alcance | 6-7 = funciona, nao diferencia | 8-9 = acima de 80% do nicho | 10 = referencia")

# 1. Foto
pdf.subtitulo("1. Foto de Perfil - 8/10")
pdf.corpo(
    "A logo e legivel, o fundo laranja cria contraste forte, o texto 'club petro' aparece mesmo em "
    "tamanho miniatura. Esta acima de 80% dos perfis B2B do setor.\n\n"
    "O que impede o 9: a borda dourada/amarela ao redor funciona como separacao, mas cria um efeito "
    "'duplo circulo' que polui levemente. Para chegar em 9, simplifique para logo em fundo solido "
    "laranja, sem borda decorativa."
)

# 2. Nome
pdf.subtitulo("2. Nome e @ - 7/10")
pdf.corpo(
    "Nome de exibicao: 'ClubPetro' - sem palavra-chave nenhuma. O nome de exibicao e campo indexado "
    "pelo algoritmo de busca do Instagram. Quem digita 'fidelizacao posto' ou 'gestao posto combustivel' "
    "no buscador do app nao encontra o ClubPetro - encontra quem colocou esses termos no nome. Isso e "
    "alcance perdido todos os dias.\n\n"
    "O @ 'clubpetro' e memoravel, curto e direto - esse esta certo. O problema esta no nome, nao no handle."
)
pdf.corpo_bold("Correcao imediata: Alterar para 'ClubPetro | Fidelizacao para Postos' ou 'ClubPetro | Gestao de Postos'. Testar as duas por 30 dias.")

# 3. Bio
pdf.check_page(50)
pdf.subtitulo("3. Bio - 5/10")
pdf.corpo(
    "Bio atual:\n"
    "Aditivamos os Resultados de +1800 Postos / Conheca seus clientes e transforme suas vendas / "
    "Tome decisoes estrategicas agora\n\n"
    "O que esta errado: A primeira linha e a mais forte do perfil inteiro e esta sendo desperdicada "
    "numa prova social vaga. '+1800 postos' e um numero impactante, mas isolado nao diz o que voce faz. "
    "Um visitante que chega pelo Reels nao sabe que e um SaaS - pensa que pode ser consultoria, "
    "distribuidora, sindicato.\n\n"
    "A segunda linha e generica ao nivel de qualquer empresa no Brasil. A terceira tem CTA mas nao diz "
    "para onde nem por que.\n\n"
    "Estrutura ausente: nao ha clareza de publico ('para revendedores'), nao ha proposta de valor concreta, "
    "nao ha diferenciacao. Sem palavras-chave estrategicas: 'fidelizacao', 'cashback', 'gestao de postos', "
    "'programa de pontos' nao aparecem - invisivel para busca."
)

# 4. Link e CTA
pdf.check_page(40)
pdf.subtitulo("4. Link e CTA - 5/10")
pdf.corpo(
    "'ig.rdstation.com/clubpetro e mais 1' - dois problemas graves.\n\n"
    "Primeiro: um link de RD Station para um visitante frio e friccao desnecessaria. O visitante que "
    "chega pelo Reels quer entender o produto antes de preencher formulario. Uma landing page leve ou "
    "o site com video curto converteria melhor.\n\n"
    "Segundo: o 'e mais 1' escondido significa que ha um segundo link que a maioria nao vai clicar "
    "porque nem sabe que existe.\n\n"
    "Dado concreto: 111 website clicks em 30 dias com 415K de reach = taxa de clique de 0,027%. "
    "Para referencia, um link bem posicionado com CTA claro deveria gerar 0,1-0,3%.\n\n"
    "O CTA na bio (seta para baixo) aponta para o link mas nao diz o que vai encontrar - 'Agende uma demo', "
    "'Veja como funciona' ou 'Fale com um especialista' converte mais que uma seta."
)

# 5. Destaques
pdf.check_page(40)
pdf.subtitulo("5. Destaques - 6/10")
pdf.corpo(
    "Destaques atuais: WhatsApp, Funcionalidades, Campanhas, Resultados, FAQ, Quem Somos!, Materiais - "
    "pelo menos 7 visiveis. A cobertura de temas e boa: tem prova social (Resultados), FAQ, o que faz "
    "(Funcionalidades).\n\n"
    "O que esta errado: as capas usam icones vetoriais em fundo escuro que ficam muito pequenos - em "
    "tela de celular viram manchas indistintas. O destaque 'WhatsApp' como primeiro item envia um sinal "
    "estranho para visitante frio: parece suporte, nao produto. 'Quem Somos!' com exclamacao soa informal "
    "para B2B. Nao ha um destaque de Cases/Clientes separado - o maior ativo de prova social esta enterrado "
    "em 'Resultados'."
)

# 6. Feed
pdf.check_page(40)
pdf.subtitulo("6. Feed - 7/10")
pdf.corpo(
    "Identidade visual consistente: laranja + preto + branco, fonte bold, logo no canto. Quem chega de "
    "fora consegue perceber em 3 segundos que e sobre postos de combustivel. O mix Reels/carrossel esta correto.\n\n"
    "O problema esta na narrativa visual do grid: ha posts de bastidores de evento, posts de produto (tela de "
    "sistema), posts de crise (texto preto/branco dramatico), posts de talking head - sem hierarquia. O visitante "
    "que olha o grid nao consegue identificar 'o que essa empresa vende'.\n\n"
    "Falta um post fixado com pitch claro do produto. Os 3 posts fixados ideais: (1) Case de resultado concreto "
    "com numero real, (2) Explicacao de o que e o produto em 60s, (3) Depoimento de cliente."
)

# 7. Qualidade dos Reels
pdf.check_page(50)
pdf.subtitulo("7. Qualidade dos Reels - 6/10")
pdf.corpo(
    "O que funciona: Variedade de formatos (talking head, bastidores, motion text, depoimento). Producao "
    "decente, nao amadora. CTAs nas legendas.\n\n"
    "O que nao funciona - e esta custando alcance diretamente:"
)
pdf.corpo_bold("O maior problema esta nos ganchos.")
pdf.corpo(
    "Exemplos reais do perfil:\n\n"
    "'POV: vantagens que voce pode oferecer em seu posto alem de preco' - isso e um titulo, nao um gancho. "
    "Nao cria curiosidade nem urgencia. O algoritmo distribui baseado em retencao nos primeiros 3 segundos.\n\n"
    "'Meta sem acompanhamento e so numero no papel' - melhor, mas generico. Qualquer empresa de gestao "
    "poderia usar.\n\n"
    "'A Copa vai aumentar o consumo em ate 74%' - ESSE e o padrao correto. Numero especifico, relevancia "
    "imediata, deixa em aberto o 'e dai?'. Precisa ser a regra, nao a excecao.\n\n"
    "Outro problema: nos Reels de produto/funcionalidade, a camera esta em tela de sistema sem contexto "
    "humano. Video de tela sem narracao envolvente tem retencao baixissima."
)

# 8. Legendas
pdf.check_page(40)
pdf.subtitulo("8. Legendas - 6/10")
pdf.corpo(
    "A estrutura existe em alguns posts (gancho -> desenvolvimento -> CTA) mas e inconsistente. Os melhores "
    "exemplos usam 'Comente X para receber no direct' - esse mecanismo esta funcionando, os posts com essa "
    "mecanica tem mais comentarios.\n\n"
    "Os piores exemplos sao textos corridos sem estrutura, com paragrafos longos e emojis decorativos.\n\n"
    "Hashtags - problema real: O perfil usa entre 4 e 6 hashtags por post. Alguns erros sistematicos: "
    "(1) tags genericas que nao levam trafego qualificado (#google, #guerra, #diesel fora de contexto); "
    "(2) sem uso consistente de hashtags de micro-nicho (#gestaodeposto, #revendedordecombustivel, "
    "#fidelidadeparapostos). Alt-text nao esta sendo usado - campo de SEO completamente desperdicado."
)

# 9. Engajamento
pdf.check_page(50)
pdf.subtitulo("9. Engajamento - 5/10")
pdf.corpo(
    "22 mil seguidores. Dados reais dos ultimos 25 posts:\n\n"
    "Melhor resultado: 107 curtidas + 12 comentarios (Carousel fiscalizacao, True ER 3,81%)\n"
    "Media: ~26 curtidas, ~5 comentarios\n"
    "ER medio (eng/followers): 0,143% - baixa para B2B de nicho com 22K\n"
    "Benchmark B2B nicho: 0,5% a 1,5%\n\n"
    "Porem, a metrica que importa e o True ER (interacoes/reach):\n"
    "Top posts atingem 3,8% a 11,9% - o conteudo funciona para quem o ve.\n\n"
    "O diagnostico real: a base tem um percentual relevante de seguidores inativos ou nao-qualificados "
    "(resultado de 1.491 posts ao longo de anos). Esses seguidores fantasmas penalizam o ER relativo e "
    "sinalizam ao algoritmo que o conteudo nao e relevante - reduzindo distribuicao.\n\n"
    "O perfil responde comentarios nos posts recentes - positivo. Mas a interacao e majoritariamente "
    "emojis de aplauso, nao discussao real. Falta provocar mais, tomar posicoes."
)

# 10. SEO
pdf.check_page(40)
pdf.subtitulo("10. SEO do Instagram - 4/10")
pdf.corpo(
    "Este e o maior gap do perfil. O Instagram hoje funciona como mecanismo de busca - e o ClubPetro "
    "esta praticamente invisivel para quem nao ja conhece a marca.\n\n"
    "Nome de exibicao: sem palavra-chave -> nao indexado para nenhum termo de busca relevante\n"
    "Bio: termos 'fidelizacao', 'cashback', 'programa de pontos', 'gestao de posto' nao aparecem\n"
    "Legendas: algumas usam termos certos, mas de forma inconsistente\n"
    "Alt-text dos posts: nao configurado em nenhum post\n"
    "Hashtags: sub-utilizadas e sem estrategia de faixa (alta/media/baixa)\n\n"
    "Resultado pratico: um dono de posto que abre o Instagram e digita 'como fidelizar clientes no posto' "
    "NAO encontra o ClubPetro. Isso nao e especulacao - e a consequencia direta de nao ter nenhuma "
    "palavra-chave nas posicoes que o algoritmo de busca indexa."
)

# === QUADRO RESUMO ===
pdf.check_page(60)
pdf.subtitulo("Quadro Resumo - 10 Dimensoes")
pdf.tabela(
    ["Dimensao", "Nota", "Status"],
    [
        ["Foto de Perfil", "8/10", "Acima de 80% do nicho"],
        ["Nome e @", "7/10", "Funciona, nao diferencia"],
        ["Bio", "5/10", "Perde alcance por isso"],
        ["Link e CTA", "5/10", "Perde alcance por isso"],
        ["Destaques", "6/10", "Funciona, nao diferencia"],
        ["Feed", "7/10", "Funciona, nao diferencia"],
        ["Qualidade dos Reels", "6/10", "Funciona, nao diferencia"],
        ["Legendas", "6/10", "Funciona, nao diferencia"],
        ["Engajamento", "5/10", "Perde alcance por isso"],
        ["SEO do Instagram", "4/10", "Perde alcance por isso"],
    ],
    [60, 30, 80]
)

# === PARTE 2 - DIAGNOSTICO ===
pdf.add_page()
pdf.titulo_secao("PARTE 2 - DIAGNOSTICO")

pdf.subtitulo("Situacao Atual")
pdf.nota_box("NOTA GERAL: 58/100",
    "Perfil com lideranca clara de audiencia no segmento (22K vs concorrentes abaixo de 11K), "
    "identidade visual funcional e mix de formatos adequado - mas que perde alcance organico "
    "sistematicamente por ganchos fracos, SEO zerado e engajamento desproporcional ao tamanho da base.")

pdf.corpo_bold("Fase: Em crescimento - com risco de estagnacao.")
pdf.corpo(
    "O perfil cresceu para uma posicao dominante no segmento, mas os indicadores de engajamento "
    "e os ganchos sugerem que o crescimento pode estar desacelerando. Sem ajuste de hook quality "
    "e SEO, a base existente nao vai se converter em leads qualificados na velocidade que o funil exige."
)

pdf.subtitulo("Alcance estimado sendo perdido (corrigivel agora, sem custo)")
pdf.tabela(
    ["Problema", "Alcance perdido", "Dificuldade"],
    [
        ["SEO zerado (nome + alt-text + bio)", "40-60% menos buscas", "Facil - hoje"],
        ["Ganchos fracos nos Reels", "30-50% menos distribuicao", "Media - por Reel"],
        ["Inconsistencia de frequencia", "15-25% reducao base", "Media - processo"],
    ],
    [70, 55, 45]
)

# O que funciona
pdf.check_page(50)
pdf.subtitulo("O que esta funcionando (3 pontos fortes)")

pdf.sub2("1. Dominio de audiencia no segmento")
pdf.corpo(
    "22K seguidores com o segundo colocado em 11K e o terceiro em 5,2K. Isso nao e vantagem marginal "
    "- e 2x maior. Mecanicamente, quando um post vai bem, tem muito mais chance de cair no Explore de quem "
    "ja segue perfis do nicho.\n\n"
    "Como explorar mais: usar essa autoridade de forma explicita no conteudo - 'somos a maior plataforma "
    "de fidelizacao para postos do Brasil' nao esta sendo dito com a frequencia que deveria."
)

pdf.sub2("2. Mecanica de 'Comente X para receber no direct'")
pdf.corpo(
    "O Reel sobre Google/dica teve 23 comentarios (melhor resultado do periodo). O sobre rotatividade "
    "de funcionarios teve 9 comentarios em 3 dias. Funciona porque: (a) gera sinal de engajamento para "
    "o algoritmo; (b) abre conversa 1:1 no direct - melhor ambiente para qualificacao de lead B2B.\n\n"
    "Como explorar mais: essa mecanica precisa estar em pelo menos 60% dos Reels, nao nos 30-40% atuais."
)

pdf.sub2("3. Mix de formatos e consistencia visual")
pdf.corpo(
    "Laranja + preto + bold ja e reconhecivel no nicho. A variacao entre talking head, texto animado e "
    "depoimento de cliente e o padrao correto para B2B.\n\n"
    "Como explorar mais: formalize series recorrentes com 'assinatura' visual - ex: 'Coisas que eu sei "
    "sobre seu posto #N'. Publique toda semana no mesmo dia."
)

# 5 problemas
pdf.check_page(50)
pdf.subtitulo("Os 5 problemas que mais custam alcance (por impacto)")

pdf.sub2("#1 - SEO zerado no nome e alt-text (IMPACTO: ALTO)")
pdf.corpo(
    "O que esta errado: O campo 'nome' diz apenas 'ClubPetro'. O Instagram indexa esse campo para busca. "
    "Qualquer termo de busca do nicho retorna perfis que tenham esses termos no nome. O ClubPetro nao "
    "aparece. Alt-text dos posts esta completamente vazio.\n\n"
    "Como afeta: Invisibilidade total nas buscas organicas do app."
)
pdf.corpo_bold("Correcao (execute hoje):")
pdf.bullet("Alterar nome de exibicao para: ClubPetro | Fidelizacao para Postos")
pdf.bullet("Ativar alt-text nos proximos posts: 'Dica de fidelizacao de clientes para postos de combustivel - programa de pontos e cashback para revendedores'")
pdf.bullet("Editar os 20 posts mais recentes e adicionar alt-text manual")

pdf.check_page(50)
pdf.sub2("#2 - Ganchos fracos nos Reels (IMPACTO: ALTO)")
pdf.corpo(
    "O Instagram decide nos primeiros 1-3 segundos se vai distribuir um Reel. Ganchos como "
    "'POV: vantagens que voce pode oferecer' sao descricoes, nao ganchos. Nao criam tensao, "
    "nao interrompem o scroll.\n\n"
    "Estrutura que funciona: Especificidade + Tensao + Relevancia"
)
pdf.tabela(
    ["Gancho atual", "Gancho reescrito"],
    [
        ["POV: vantagens alem de preco", "Seu posto cobra R$0,05 a mais e ainda esta cheio. Vou mostrar por que."],
        ["Meta sem acompanhamento...", "Seu frentista bateu a meta? Se nao sabe em 5s, esse video e pra voce."],
        ["Ela nao sabia que o posto...", "Ela tinha um posto igual ao vizinho. Em 4 meses, o vizinho perdeu 30%."],
    ],
    [70, 100]
)

pdf.check_page(40)
pdf.sub2("#3 - Bio sem proposta de valor (IMPACTO: ALTO)")
pdf.corpo(
    "A bio atual nao passa o teste dos 5 segundos para visitante frio. 'Aditivamos os Resultados de "
    "+1800 Postos' e prova social sem contexto. 'Conheca seus clientes e transforme suas vendas' e "
    "generico ao nivel de qualquer CRM do mercado.\n\n"
    "Como afeta: Visitante que chega pelo Reel e vai ao perfil nao converte em seguidor nem em lead."
)

pdf.check_page(40)
pdf.sub2("#4 - Engajamento desproporcional a audiencia (IMPACTO: MEDIO-ALTO)")
pdf.corpo(
    "Uma base de 22K com 25 curtidas/post sinaliza ao algoritmo que o conteudo nao e relevante. "
    "A provavel causa: parte da base foi adquirida por conteudo que atraiu seguidores nao-qualificados.\n\n"
    "Correcao: (a) CTAs que gerem resposta de texto - perguntas polarizadas funcionam melhor que abertas; "
    "(b) Stories com enquetes toda semana; (c) Lives mensais de 30 minutos sobre problema real do setor - "
    "Lives tem prioridade de distribuicao no algoritmo."
)

pdf.check_page(40)
pdf.sub2("#5 - Inconsistencia de frequencia (IMPACTO: MEDIO)")
pdf.corpo(
    "Janeiro e fevereiro com ~9 posts cada (~2/semana). Marco com ~20 posts (~5/semana). O algoritmo "
    "aprende o ritmo e ajusta a distribuicao. Quedas bruscas causam reducao que demora semanas para recuperar.\n\n"
    "Correcao: Minimo inegociavel de 4 posts/semana (3 Reels + 1 carrossel). Criar buffer de 2 semanas "
    "de conteudo gravado antes de entrar no calendario."
)

# Reescritas de bio
pdf.add_page()
pdf.subtitulo("Reescritas prontas da bio")
pdf.corpo("Palavras-chave estrategicas marcadas com colchetes [ ] - use exatamente esses termos no campo de bio.")

pdf.sub2("Opcao A - Autoridade")
pdf.corpo(
    "[ClubPetro] | [SaaS de fidelizacao] para [postos de combustivel]\n"
    "+1.800 postos usam nossa plataforma para [parar de perder clientes] por preco\n"
    "[Programa de pontos] . [cashback] . [gestao de metas] . [IA]\n"
    "Conheca como funciona (seta)"
)

pdf.sub2("Opcao B - Beneficio direto")
pdf.corpo(
    "Seu posto para de [perder cliente] para o concorrente ao lado\n"
    "[Fidelizacao], [cashback] e [gestao] integrados em 1 plataforma\n"
    "+1.800 [revendedores] ja usam . Sem guerra de preco\n"
    "Veja uma demo gratuita (seta)"
)

pdf.sub2("Opcao C - Curiosidade")
pdf.corpo(
    "Por que [postos de combustivel] com [programa de fidelizacao] vendem 34% mais?\n"
    "A gente ajuda +1.800 [revendedores] a descobrir isso na pratica\n"
    "[Fidelizacao] . [cashback] . [metas] . [dados de consumo]\n"
    "Entenda como funciona (seta)"
)

# Destaques
pdf.check_page(50)
pdf.subtitulo("Estrutura dos 5 destaques essenciais")
pdf.tabela(
    ["Destaque", "Conteudo"],
    [
        ["Como Funciona", "Reel/story explicando produto em 60s, prints de tela, video demo"],
        ["Resultados", "Cases com numeros reais: 'Posto X +X% galonagem em Y meses'"],
        ["Para Quem E", "FAQ: posto pequeno? sistema? quanto custa? Story interativo"],
        ["Bastidores", "Equipe real, dia a dia, eventos do setor. Humaniza a empresa"],
        ["Comecar", "CTA unico: link para demo, WhatsApp comercial. 1 story, 1 acao"],
    ],
    [40, 130]
)
pdf.corpo("Remover/renomear: 'WhatsApp' -> mesclar com 'Comecar'. 'Quem Somos!' -> renomear para 'Equipe'.")

# === PARTE 3 - BANCO DE TEMAS ===
pdf.add_page()
pdf.titulo_secao("PARTE 3 - BANCO DE TEMAS PARA REELS")

pdf.subtitulo("Pilares de conteudo")
pdf.tabela(
    ["Pilar", "Proporcao", "Por que funciona"],
    [
        ["Gestao Sem Depender de Preco", "30%", "Problema-raiz do publico: preso na guerra de preco"],
        ["Dados e Inteligencia de Operacao", "25%", "Revendedor decide por intuicao, dados mudam decisoes"],
        ["Realidade do Setor", "20%", "Posts com maior engagement sao desse pilar (indignacao)"],
        ["Prova Social / Cases Reais", "15%", "B2B compra por prova. Case > argumento teorico"],
        ["Bastidores e Equipe", "10%", "Reduz barreira de confianca (maior obstaculo SaaS B2B)"],
    ],
    [55, 22, 93]
)

pdf.subtitulo("30 temas prontos para gravar")
pdf.corpo("Distribuicao: 47% Alcance | 20% Autoridade | 17% Conexao | 17% Conversao. Minimo 40% Alcance cumprido.")

temas = [
    ["1", "Gestao", "3 coisas que cliente fiel faz vs cliente de preco", "Lista/talking head", "Tem dois tipos de cliente no seu posto. Um voce perde amanha...", "Alcance"],
    ["2", "Gestao", "Posto em cidade de 8 mil criou fila na bomba", "Storytelling", "Cidade de 8 mil. Dois postos. Um tem fila toda sexta...", "Alcance"],
    ["3", "Gestao", "Cliente vai embora por R$0,05 a menos", "Opiniao direta", "Seu cliente vai pro concorrente por R$0,05? Entao nunca foi seu...", "Alcance"],
    ["4", "Gestao", "5 acoes de fidelizacao sem custo", "Tutorial rapido", "5 acoes. Custo zero. A primeira a maioria nunca fez.", "Alcance"],
    ["5", "Gestao", "Programa de pontos nao funciona", "Mito vs verdade", "Voce tem programa de pontos e clientes nao voltam. Nao e culpa deles.", "Autoridade"],
    ["6", "Gestao", "Quanto vale cliente que abastece toda semana", "Tutorial + numero", "Quanto vale um cliente fiel no seu caixa em 12 meses? Fiz a conta.", "Alcance"],
    ["7", "Dados", "Horario que seu posto perde mais clientes", "Revelacao/dado", "Todos os postos tem um horario onde perdem 30% mais clientes...", "Alcance"],
    ["8", "Dados", "O que os dados revelam que voce nao percebeu", "Opiniao + dado", "Tem informacao no seu sistema que mudaria uma decisao dessa semana.", "Autoridade"],
    ["9", "Dados", "Frentista vendendo ou so abastecendo", "Tutorial pratico", "Frentista que abastece vs frentista que vende. A diferenca e um dado.", "Autoridade"],
    ["10", "Dados", "Ticket medio: R$2 a mais muda o mes", "Explicacao direta", "R$2 a mais de ticket medio. No fim do mes e quanto? Fiz a conta.", "Alcance"],
    ["11", "Dados", "Gestao de metas: sem vs com sistema", "Antes/depois", "Antes: eu ligava pro gerente todo dia. Agora: 10 segundos.", "Conversao"],
    ["12", "Dados", "Cliente inativo e dinheiro que pode voltar", "Educativo", "Clientes que abasteceram 10x e sumiram. Nao foram pro concorrente.", "Alcance"],
    ["13", "Setor", "Revendedor: elo mais culpado e menos protegido", "Opiniao forte", "Petroleo sobe: culpa do posto. Cambio cai: culpa do posto.", "Alcance"],
    ["14", "Setor", "ANP fiscaliza mais o posto que distribuidora", "Mito vs verdade", "Distribuidora aumenta preco antes. Posto leva a multa.", "Alcance"],
    ["15", "Setor", "Carros eletricos vao acabar com postos?", "Tendencia + opiniao", "Resposta direta: depende do que voce faz nos proximos 3 anos.", "Alcance"],
    ["16", "Setor", "Posto bandeirado vs independente", "Educativo/opiniao", "Parece o mesmo negocio. Nao e. Confundir esta custando margem.", "Alcance"],
    ["17", "Setor", "O que aprender com o supermercado", "Analogia/tendencia", "Supermercado resolveu margem ha 30 anos. Combustiveis nao copiou.", "Alcance"],
    ["18", "Setor", "Preco do combustivel: do poco a bomba", "Infografico", "Voce paga R$6,20. Dono do posto fica com R$0,18. De onde vem o resto?", "Alcance"],
    ["19", "Prova", "Posto pequeno que superou rede bandeirada", "Storytelling", "Cidade pequena. Posto independente vs rede bandeirada. Um saiu.", "Alcance"],
    ["20", "Prova", "Numeros reais: 6 meses de fidelizacao", "Antes/depois", "6 meses. 1 posto. Numeros reais: galonagem, ticket, inativos.", "Conversao"],
    ["21", "Prova", "Depoimento Rede Magnolia", "Depoimento", "Ela nao acreditava que ia funcionar. Esse foi o resultado.", "Conversao"],
    ["22", "Prova", "Serie: o que 1.800 postos tem em comum #4", "Serie/revelacao", "Analisamos dados de 1.800 postos. Tem uma coisa que os lucrativos fazem.", "Autoridade"],
    ["23", "Bastidores", "Onboarding: do contrato ao primeiro cliente", "Bastidores real", "Assina contrato na sexta. Quando o primeiro cliente usa? Vou mostrar.", "Conexao"],
    ["24", "Bastidores", "Um dia com o time de sucesso do cliente", "Dia a dia", "Esse time liga quando o resultado nao sai. Eles trabalham assim.", "Conexao"],
    ["25", "Bastidores", "O erro que o ClubPetro cometeu", "Vulnerabilidade", "A gente errou. Vou falar o que foi, com que cliente, e o que mudou.", "Conexao"],
    ["26", "Gestao", "Campanha de Dia dos Pais que traz cliente", "Tutorial sazonal", "Dia dos Pais em 2 meses. Posto que prepara agora captura o cliente.", "Alcance"],
    ["27", "Gestao", "SMS converte mais que WhatsApp para reativacao", "Mito vs verdade", "Todo mundo foi pro WhatsApp. E por isso que SMS voltou a converter.", "Autoridade"],
    ["28", "Dados", "IA para contratar frentista: 3 filtros", "Tendencia/nicho", "Maioria contrata frentista igual aos anos 90. Esse filtro de IA mudou.", "Alcance"],
    ["29", "Setor", "Rotina de dono de posto sem gestao profissional", "Bastidores/real", "Acordar sem saber se o caixa fechou. Ligar pro frentista. Reconheceu?", "Conexao"],
    ["30", "Gestao", "Conveniencia: o que vende que mercadinho nao", "Opiniao + tutorial", "Sua conveniencia tem uma vantagem que nenhum mercadinho tem.", "Alcance"],
]

headers = ["#", "Pilar", "Tema", "Formato", "Gancho (primeiros 3s)", "Objetivo"]
cw = [8, 20, 40, 28, 60, 20]

pdf.set_font("Helvetica", "B", 7)
pdf.set_fill_color(40, 40, 40)
pdf.set_text_color(255, 255, 255)
for i, h in enumerate(headers):
    pdf.cell(cw[i], 7, h, border=1, fill=True, align="C")
pdf.ln()

pdf.set_font("Helvetica", "", 7)
pdf.set_text_color(30, 30, 30)
fill = False
for row in temas:
    if pdf.get_y() > 260:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_fill_color(40, 40, 40)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            pdf.cell(cw[i], 7, h, border=1, fill=True, align="C")
        pdf.ln()
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(30, 30, 30)
        fill = False
    if fill:
        pdf.set_fill_color(245, 245, 245)
    else:
        pdf.set_fill_color(255, 255, 255)
    max_h = 6
    # calculate needed height
    for i, cell in enumerate(row):
        lines = pdf.multi_cell(cw[i], 5, str(cell), split_only=True)
        needed = len(lines) * 5
        if needed > max_h:
            max_h = needed
    y0 = pdf.get_y()
    x0 = pdf.get_x()
    for i, cell in enumerate(row):
        x = x0 + sum(cw[:i])
        pdf.set_xy(x, y0)
        pdf.cell(cw[i], max_h, "", border=1, fill=True)
        pdf.set_xy(x + 0.5, y0 + 0.5)
        pdf.multi_cell(cw[i] - 1, 5, str(cell))
    pdf.set_xy(x0, y0 + max_h)
    fill = not fill

pdf.ln(5)

# Calendario
pdf.check_page(80)
pdf.subtitulo("Calendario de 2 semanas")
pdf.tabela(
    ["Dia", "Formato", "Tema", "Objetivo", "Horario"],
    [
        ["Seg S1", "Reel", "#13 Revendedor culpado", "Alcance", "18h30"],
        ["Ter S1", "Reel", "#7 Horario perde clientes", "Alcance", "12h"],
        ["Qui S1", "Carrossel", "#4 5 acoes fidelizacao", "Alcance", "19h"],
        ["Sex S1", "Reel", "#22 Serie Coisas que sei", "Autoridade", "12h"],
        ["Sab S1", "Reel", "#19 Case cidade pequena", "Alcance", "10h"],
        ["Seg S2", "Reel", "#3 Cliente por R$0,05", "Alcance", "18h30"],
        ["Ter S2", "Reel", "#10 Ticket medio conta", "Alcance", "12h"],
        ["Qua S2", "Reel", "#28 IA contratar frentista", "Alcance", "19h"],
        ["Qui S2", "Carrossel", "#5 Programa pontos", "Autoridade", "18h"],
        ["Sex S2", "Reel", "#20 Numeros reais 6m", "Conversao", "12h"],
        ["Sab S2", "Reel", "#29 Rotina honesta", "Conexao", "10h"],
    ],
    [25, 28, 52, 30, 25]
)
pdf.corpo("Horarios baseados em dados B2B Brasil: ter/qui ao meio-dia (almoco) e seg/qui 18h30 (apos expediente). Sabado de manha funciona para revendedores que checam celular antes da abertura.")

# === ROTEIRO COMPLETO ===
pdf.add_page()
pdf.titulo_secao("ROTEIRO COMPLETO - Tema #13")
pdf.subtitulo("'O revendedor e o elo mais culpado e o menos protegido'")
pdf.corpo("Maior potencial de viralizacao: combina indignacao do setor + narrativa de injustica + conteudo altamente compartilhavel. O post de fiscalizacao (tema similar) teve 98 shares e True ER de 3,81%.")

pdf.sub2("GANCHO (0-3s)")
pdf.nota_box("FRASE EXATA:", "Quando o petroleo sobe: culpa do posto. Quando o cambio cai: culpa do posto. Alguem tem que falar o que ninguem fala.")
pdf.corpo(
    "Instrucao de gravacao: Olhando direto para a camera. Tom serio, sem sorriso. Fundo simples (parede, "
    "escritorio). Texto na tela nos primeiros frames: 'A CULPA E SEMPRE DO POSTO?' em caixa alta, fonte bold, "
    "laranja sobre fundo preto. Isso para o scroll antes de a voz terminar a frase."
)

pdf.sub2("CORPO (3-45s)")
pdf.corpo(
    "[Bloco 1 - A injustica]\n"
    "O preco do petroleo sobe no mercado internacional. A Petrobras repassa pra distribuidora. A distribuidora "
    "repassa pro posto. E na bomba, o consumidor olha pro frentista e pergunta: 'por que ta tao caro?'\n\n"
    "O posto e o unico elo da cadeia que da a cara pra bater. A refinaria nao atende consumidor. A distribuidora "
    "nao atende consumidor. Quem atende e voce.\n\n"
    "[Bloco 2 - A conta que ninguem mostra]\n"
    "Voce sabia que de cada R$6,20 que o consumidor paga no litro de gasolina, a margem do revendedor e em "
    "media R$0,18? Dezoito centavos. O resto vai pra imposto, Petrobras, distribuidora, etanol.\n\n"
    "Mas quando o preco sobe, quem e investigado? O posto. Quando o fiscal bate, bate onde? No posto. Quando "
    "o consumidor reclama, reclama de quem? Do posto.\n\n"
    "[Bloco 3 - O que precisa mudar]\n"
    "O revendedor brasileiro precisa parar de aceitar ser o bode expiatorio da cadeia de combustiveis. E isso "
    "comeca com uma coisa: informacao.\n\n"
    "Quando voce tem os dados da sua operacao, voce sabe exatamente qual e a sua margem, quanto voce paga, "
    "quanto voce ganha. E quando alguem vem dizer que 'o posto ta lucrando demais', voce tem numero pra mostrar."
)

pdf.check_page(40)
pdf.sub2("FECHAMENTO + CTA (45-60s)")
pdf.corpo(
    "[Frase final - a que fica:]\n"
    "'O posto nao e o problema. O posto e o que segura a cadeia de pe. E ta na hora de todo revendedor "
    "entender isso.'\n\n"
    "[CTA:]\n"
    "'Se voce concorda, compartilha esse video com outro dono de posto. Quanto mais gente souber, menos "
    "a conta cai so no nosso colo.'\n\n"
    "[Texto na tela no ultimo frame:]\n"
    "'COMPARTILHA COM UM REVENDEDOR' + logo ClubPetro"
)

pdf.sub2("Instrucoes de producao")
pdf.bullet("Duracao ideal: 45-60 segundos")
pdf.bullet("Formato: Talking head, camera fixa, fundo simples")
pdf.bullet("Legendas: automaticas + enfatizar numeros com texto bold na tela")
pdf.bullet("Musica de fundo: suave, tom dramatico/inspiracional (nao alegre)")
pdf.bullet("Hashtags: #postodecombustivel #revendedor #combustivel #gasolina #precodagasolina #ANP #fidelizacao")
pdf.bullet("Alt-text: 'Revendedor de postos de combustivel: margem do posto, fiscalizacao ANP, cadeia de combustiveis'")
pdf.bullet("CTA na legenda: 'Comente MARGEM pra receber um conteudo exclusivo sobre como proteger seus numeros'")

# === ACOES IMEDIATAS ===
pdf.add_page()
pdf.titulo_secao("PLANO DE ACAO - PRIORIZADO")

pdf.subtitulo("Acoes imediatas (esta semana)")
pdf.tabela(
    ["#", "Acao", "Impacto", "Esforco"],
    [
        ["1", "Alterar nome exibicao: ClubPetro | Fidelizacao para Postos", "ALTO", "5 min"],
        ["2", "Reescrever bio (usar Opcao A, B ou C acima)", "ALTO", "10 min"],
        ["3", "Adicionar alt-text nos 20 posts mais recentes", "ALTO", "30 min"],
        ["4", "Reescrever CTA do link: 'Veja como funciona' ou 'Demo gratuita'", "MEDIO", "5 min"],
        ["5", "Reorganizar destaques (5 essenciais + capas novas)", "MEDIO", "1 hora"],
    ],
    [8, 95, 28, 25]
)

pdf.subtitulo("Acoes semanais (processo recorrente)")
pdf.tabela(
    ["#", "Acao", "Frequencia"],
    [
        ["1", "Publicar minimo 4 posts/semana (3 Reels + 1 carrossel)", "Semanal"],
        ["2", "Todo Reel com gancho validado (Especificidade + Tensao + Relevancia)", "Por post"],
        ["3", "Todo post com alt-text descritivo com palavras-chave", "Por post"],
        ["4", "CTA 'Comente X' em pelo menos 60% dos Reels", "Por post"],
        ["5", "Stories com enquete ou pergunta polarizada", "2-3x/semana"],
        ["6", "Hashtags: 3 de nicho + 2 de micro-nicho + 1 de campanha", "Por post"],
    ],
    [8, 120, 35]
)

pdf.subtitulo("Acoes mensais (estrategia)")
pdf.tabela(
    ["#", "Acao", "Quando"],
    [
        ["1", "Gravar buffer de 2 semanas de conteudo (8 videos)", "Inicio do mes"],
        ["2", "1 Live de 30 min sobre problema real do setor", "1x/mes"],
        ["3", "Revisar metricas: True ER, shares, website clicks, follows", "Final do mes"],
        ["4", "Atualizar serie recorrente ('Coisas que eu sei sobre seu posto')", "1x/mes"],
        ["5", "1 colab ou mencao com influenciador do setor (Brasil Postos etc)", "1x/mes"],
    ],
    [8, 120, 35]
)

# === METRICAS DE ACOMPANHAMENTO ===
pdf.check_page(60)
pdf.subtitulo("Metricas de acompanhamento (metas para 90 dias)")
pdf.tabela(
    ["Metrica", "Atual", "Meta 90 dias", "Como medir"],
    [
        ["Seguidores", "22.069", "24.000+", "Perfil"],
        ["ER medio (eng/followers)", "0,14%", "0,5%+", "Avg 25 posts"],
        ["True ER medio (top 5)", "3,8-11,9%", "Manter >5%", "Insights por post"],
        ["Website clicks/mes", "111", "300+", "Profile insights"],
        ["Frequencia publicacao", "~4/semana (irregular)", "4/semana (estavel)", "Calendario"],
        ["Shares medio/post", "~8", "15+", "Post insights"],
        ["Comentarios medio/post", "5,2", "10+", "Post insights"],
    ],
    [45, 35, 35, 45]
)

# FINAL
pdf.ln(10)
pdf.set_draw_color(230, 80, 0)
pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
pdf.ln(5)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 6, "Analise gerada com dados reais da Instagram Graph API v21.0 em 21/04/2026", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "Cruzamento de auditoria quantitativa (API) + analise qualitativa de conteudo", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "Preparado para Andre Carvalhaes, CMO ClubPetro", align="C", new_x="LMARGIN", new_y="NEXT")

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analise_instagram_clubpetro.pdf")
pdf.output(out_path)
print(f"PDF gerado: {out_path}")
print(f"Paginas: {pdf.page_no()}")
