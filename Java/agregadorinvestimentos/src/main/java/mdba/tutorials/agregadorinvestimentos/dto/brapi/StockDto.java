package mdba.tutorials.agregadorinvestimentos.dto.brapi;

import java.time.Instant;

public record StockDto(
        String currency,
        Long marketCap,
        String shortName,
        String longName,
        Double regularMarketChange,
        Double regularMarketChangePercent,
        Instant regularMarketTime,
        Double regularMarketPrice,
        Double regularMarketDayHigh,
        String regularMarketDayRange,
        Double regularMarketDayLow,
        Long regularMarketVolume,
        Double regularMarketPreviousClose,
        Double regularMarketOpen,
        String fiftyTwoWeekRange,
        Double fiftyTwoWeekLow,
        Double fiftyTwoWeekHigh,
        String symbol,
        String logourl,
        Double priceEarnings,
        Double earningsPerShare
) {
}
