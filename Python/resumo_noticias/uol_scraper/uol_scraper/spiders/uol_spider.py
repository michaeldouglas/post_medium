import scrapy


class UOLSpider(scrapy.Spider):
    name = "uol_vivabem"
    start_urls = [
        "https://www.uol.com.br/vivabem/noticias/redacao/2025/10/08/por-que-as-mulheres-vivem-mais-as-razoes-por-tras-da-longevidade-feminina.htm"
    ]

    def parse(self, response):
        # Extrair o título da notícia
        titulo = response.css("h1::text").get(default="").strip()

        # Selecionar todos elementos de conteúdo relevantes (parágrafos e subtítulos)
        conteudo_selecionado = response.css("p.bullet, h2.bullet")

        conteudo_final = []

        for elem in conteudo_selecionado:
            texto = elem.xpath("string()").get().strip()
            if texto:
                conteudo_final.append(texto)

        yield {
            "titulo": titulo,
            "url": response.url,
            "conteudo": " ".join(conteudo_final)
        }
