import { tool } from "@langchain/core/tools";
import { z } from "zod";

/**
 * Transforma texto de resultados de voo em uma análise detalhada, estatística e comparativa.
 * Calcula menor, maior e preço médio, recomenda a melhor opção e aponta prós e contras básicos.
 */
export const ResultadoEmHTMLTool = tool(
  async ({ input }: { input: string }) => {
    try {
      // Separar blocos de cada voo
      const blocks = input.split(/\d+\.\s*/).filter((b) => b.trim() !== "");

      // Extrair dados das opções de voo
      const flights = blocks.map((block, i) => {
        // Nome da companhia / plataforma
        const platformMatch = /^(.+?):/.exec(block);
        const platform = platformMatch
          ? platformMatch[1].trim()
          : `Opção ${i + 1}`;

        // Captura preço R$ 349 ou R$ 557,52
        const priceMatch = /R\$ (\d+(?:[\.,]\d+)?)/.exec(block);
        const price = priceMatch
          ? parseFloat(priceMatch[1].replace(".", "").replace(",", "."))
          : undefined;

        // Tipo de voo, ida, volta, conforto (se não houver, deixa não especificado)
        return {
          platform,
          price,
          type: "Não especificado",
          departure: "",
          returnDate: "",
          comfort: "Não especificado",
        };
      });

      // Estatísticas
      const prices = flights
        .map((f) => f.price)
        .filter((p) => typeof p === "number") as number[];
      const minPrice = prices.length ? Math.min(...prices) : undefined;
      const maxPrice = prices.length ? Math.max(...prices) : undefined;
      const avgPrice = prices.length
        ? prices.reduce((a, b) => a + b, 0) / prices.length
        : undefined;

      // Melhor opção baseada no menor preço
      const bestOption =
        flights.find((f) => f.price === minPrice)?.platform ?? "Não definido";

      // Montar análise detalhada
      const analysis = flights.map((f) => ({
        Companhia: f.platform,
        Preço:
          f.price !== undefined ? `R$ ${f.price.toFixed(2)}` : "Não disponível",
        Tipo: f.type,
        Conforto: f.comfort,
        Ida: f.departure || "Não informado",
        Volta: f.returnDate || "Não informado",
        Prós: f.price === minPrice ? "Menor preço" : "",
        Contras: f.price === undefined ? "Preço não disponível" : "",
      }));

      return {
        flights: analysis,
        statistics: {
          menorPreco:
            minPrice !== undefined
              ? `R$ ${minPrice.toFixed(2)}`
              : "Não disponível",
          maiorPreco:
            maxPrice !== undefined
              ? `R$ ${maxPrice.toFixed(2)}`
              : "Não disponível",
          precoMedio:
            avgPrice !== undefined
              ? `R$ ${avgPrice.toFixed(2)}`
              : "Não disponível",
        },
        recomendacao: bestOption,
      };
    } catch (err) {
      console.error(err);
      return {
        error: "Erro ao gerar análise de voos.",
      };
    }
  },
  {
    name: "FlightAnalysisTool",
    description:
      "Transforma texto de resultados de voo em uma análise detalhada e estatística, incluindo pros, contras e recomendação baseada em preço.",
    schema: z.object({
      input: z.string(),
    }),
  }
);
