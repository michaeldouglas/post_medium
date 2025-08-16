package mdba.tutorials.agregadorinvestimentos.dto.user;

public class TokenExpiryDto {
    private String message;
    private long ttl;

    public TokenExpiryDto(String message, long ttl) {
        this.message = message;
        this.ttl = ttl;
    }

    public String getMessage() {
        return message;
    }

    public long getTtl() {
        return ttl;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public void setTtl(long ttl) {
        this.ttl = ttl;
    }
}
