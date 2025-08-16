package mdba.tutorials.agregadorinvestimentos.controller.brapi;

import mdba.tutorials.agregadorinvestimentos.client.BrapiClient;
import mdba.tutorials.agregadorinvestimentos.dto.brapi.BrapiResponseDto;
import mdba.tutorials.agregadorinvestimentos.dto.brapi.StockDto;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/v1/stocks")
public class ListQuotesController {

    private final BrapiClient brapiClient;

    @Value("#{environment.TOKEN}")
    private String TOKEN;

    public ListQuotesController(BrapiClient brapiClient) {
        this.brapiClient = brapiClient;
    }

    @GetMapping
    public BrapiResponseDto listStocks(@RequestParam(required = false) String quote) {
        List<StockDto> stocks;
        if (quote != null && !quote.isBlank()) {
            stocks = brapiClient.getQuote(TOKEN, quote).results();
        } else {
            String[] quotes = {"PETR4", "VALE3", "ITUB4"};
            stocks = Arrays.stream(quotes)
                    .map(s -> brapiClient.getQuote(TOKEN, s).results())
                    .flatMap(List::stream)
                    .toList();
        }
        return new BrapiResponseDto(stocks);
    }
}
