package mdba.tutorials.agregadorinvestimentos.controller.auth;

import io.swagger.v3.oas.annotations.tags.Tag;
import mdba.tutorials.agregadorinvestimentos.config.jwt.JwtUtil;
import mdba.tutorials.agregadorinvestimentos.dto.auth.AuthLoginDto;
import mdba.tutorials.agregadorinvestimentos.repository.user.UserRepository;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/v1/auth")
@Tag(name = "Autenticação", description = "Endpoints para login e geração de tokens")
public class AuthController {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthController(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Operation(summary = "Login do usuário", description = "Autentica o usuário e retorna um token JWT válido por 1 hora")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Login realizado com sucesso",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(example = "{\"token\":\"<jwt>\",\"username\":\"michael\",\"expires_in\":3600}"))),
            @ApiResponse(responseCode = "401", description = "Usuário ou senha inválidos",
                    content = @Content(mediaType = "application/json",
                            schema = @Schema(example = "{\"error\":\"Usuário ou senha inválidos\",\"status\":401,\"suggestion\":\"Verifique se o usuário e a senha estão corretos e tente novamente.\"}")))
    })
    @PostMapping
    public ResponseEntity<Map<String, Object>> login(@RequestBody AuthLoginDto authLoginDto) throws Exception {
        if(authLoginDto.username() == null || authLoginDto.password() == null) {
            return errorResponse("Usuário e senha são obrigatórios");
        }

        var userOpt = userRepository.findByUsername(authLoginDto.username());
        if (userOpt.isEmpty() || !passwordEncoder.matches(authLoginDto.password(), userOpt.get().getPassword())) {
            return errorResponse("Usuário ou senha inválidos");
        }

        var user = userOpt.get();
        String token = JwtUtil.generateToken(user.getUsername());
        Map<String, Object> response = new HashMap<>();
        response.put("token", token);
        response.put("username", user.getUsername());
        response.put("expires_in", 3600);
        return ResponseEntity.ok(response);
    }

    private ResponseEntity<Map<String, Object>> errorResponse(String message) {
        Map<String, Object> error = new HashMap<>();
        error.put("error", message);
        error.put("status", HttpStatus.UNAUTHORIZED.value());
        error.put("suggestion", "Verifique se o usuário e a senha estão corretos e tente novamente.");
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, Object>> handleRuntimeException(RuntimeException ex) {
        return errorResponse(ex.getMessage());
    }
}
