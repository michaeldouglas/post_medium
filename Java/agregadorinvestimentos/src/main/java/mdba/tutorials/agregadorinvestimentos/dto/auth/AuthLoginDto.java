package mdba.tutorials.agregadorinvestimentos.dto.auth;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public record AuthLoginDto(
        @NotBlank(message = "O username é obrigatório")
        @Schema(description = "Nome de usuário para login", example = "usuario")
        String username,

        @NotBlank(message = "A senha é obrigatória")
        @Schema(description = "Senha do usuário", example = "senha")
        String password
) {}
