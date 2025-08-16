package mdba.tutorials.agregadorinvestimentos.dto.user;

import mdba.tutorials.agregadorinvestimentos.entity.user.User;

import java.time.format.DateTimeFormatter;

public class UserResponseDto {
    private final String userId;
    private final String username;
    private final String email;
    private final String createdAt;
    private final String updatedAt;

    public UserResponseDto(String userId, String username, String email, String createdAt, String updatedAt) {
        this.userId = userId;
        this.username = username;
        this.email = email;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public static UserResponseDto fromEntity(User user, DateTimeFormatter formatter) {
        return new UserResponseDto(
                user.getUserId().toString(),
                user.getUsername(),
                user.getEmail(),
                formatter.format(user.getCreated_at()),
                formatter.format(user.getUpdated_at())
        );
    }

    public String getUserId() { return userId; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public String getCreatedAt() { return createdAt; }
    public String getUpdatedAt() { return updatedAt; }
}