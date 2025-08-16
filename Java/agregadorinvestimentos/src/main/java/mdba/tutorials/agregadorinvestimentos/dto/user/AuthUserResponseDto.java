package mdba.tutorials.agregadorinvestimentos.dto.user;

public class AuthUserResponseDto {
    private UserResponseDto user;
    private TokenExpiryDto tokenExpiresIn;

    public AuthUserResponseDto(UserResponseDto user, TokenExpiryDto tokenExpiresIn) {
        this.user = user;
        this.tokenExpiresIn = tokenExpiresIn;
    }

    public UserResponseDto getUser() {
        return user;
    }

    public TokenExpiryDto getTokenExpiresIn() {
        return tokenExpiresIn;
    }
}
