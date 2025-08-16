package mdba.tutorials.agregadorinvestimentos.controller.user;

import com.auth0.jwt.interfaces.DecodedJWT;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import mdba.tutorials.agregadorinvestimentos.config.jwt.JwtUtil;
import mdba.tutorials.agregadorinvestimentos.dto.user.*;
import mdba.tutorials.agregadorinvestimentos.entity.user.User;
import mdba.tutorials.agregadorinvestimentos.service.user.UserService;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.time.Instant;
import java.time.format.DateTimeFormatter;

@RestController
@RequestMapping("/v1/usuarios")
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Usuários", description = "Endpoints para dados do usuário")
public class UserController {

    private final UserService userService;
    private final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss")
                    .withZone(java.time.ZoneId.of("America/Sao_Paulo"));

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @Operation(summary = "Cria um novo usuário", description = "Cria um usuário no sistema com nome e email")
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Usuário criado com sucesso"),
            @ApiResponse(responseCode = "400", description = "Dados inválidos")
    })
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody CreateUserDto createUserDto) {
        var userId = userService.createUser(createUserDto);
        return ResponseEntity.created(URI.create("/v1/usuarios/" + userId)).build();
    }

    @Operation(summary = "Busca dados do usuário autenticado")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Usuário autenticado encontrado"),
            @ApiResponse(responseCode = "401", description = "Token inválido ou expirado")
    })
    @GetMapping("/me")
    public ResponseEntity<AuthUserResponseDto> getAuthenticatedUser(
            @RequestHeader("Authorization") String authorizationHeader) throws Exception {

        String token = authorizationHeader.replace("Bearer ", "");
        DecodedJWT decodedJWT = JwtUtil.validateToken(token);

        TokenExpiryDto tokenInfo = calculateTimeLeft(decodedJWT.getExpiresAt().toInstant());

        String username = decodedJWT.getSubject();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));

        UserResponseDto userDto = UserResponseDto.fromEntity(user, formatter);

        AuthUserResponseDto response = new AuthUserResponseDto(userDto, tokenInfo);

        return ResponseEntity.ok(response);
    }

    private TokenExpiryDto calculateTimeLeft(Instant expiresAt) {
        Instant now = Instant.now();
        long secondsLeft = expiresAt.getEpochSecond() - now.getEpochSecond();

        if (secondsLeft <= 0) {
            return new TokenExpiryDto("Token expirado", 0);
        } else {
            long hours = secondsLeft / 3600;
            long minutes = (secondsLeft % 3600) / 60;
            long seconds = secondsLeft % 60;

            String message;
            if (hours > 0) {
                message = "Faltam " + hours + " hora(s), " + minutes + " minuto(s) e " + seconds + " segundo(s)";
            } else if (minutes > 0) {
                message = "Faltam " + minutes + " minuto(s) e " + seconds + " segundo(s)";
            } else {
                message = "Faltam " + seconds + " segundo(s)";
            }

            return new TokenExpiryDto(message, secondsLeft);
        }
    }

    @GetMapping("/{userId}")
    @Operation(summary = "Busca usuário pelo ID", description = "Retorna os detalhes de um usuário pelo seu ID")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Usuário encontrado"),
            @ApiResponse(responseCode = "401", description = "Token inválido ou não fornecido"),
            @ApiResponse(responseCode = "404", description = "Usuário não encontrado")
    })
    public ResponseEntity<UserResponseDto> getUserById(
            @Parameter(description = "ID do usuário", example = "123e4567-e89b-12d3-a456-426614174000")
            @PathVariable String userId
    ) {
        var userOpt = userService.getUserById(userId);
        return userOpt
                .map(user -> ResponseEntity.ok(UserResponseDto.fromEntity(user, formatter)))
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping
    @Operation(summary = "Lista Usuários", description = "Lista os usuários do sistema com paginação")
    public ResponseEntity<Page<UserResponseDto>> listUsers(
            @Parameter(description = "Número da página (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Tamanho da página", example = "10")
            @RequestParam(defaultValue = "10") int size
    ) {
        Pageable pageable = PageRequest.of(page, size);
        Page<User> usersPage = userService.listUsers(pageable);

        Page<UserResponseDto> dtoPage = usersPage.map(user -> UserResponseDto.fromEntity(user, formatter));

        return ResponseEntity.ok(dtoPage);
    }

    @PutMapping("/{userId}")
    @Operation(summary = "Atualiza Usuário", description = "Atualiza usuário por ID")
    public ResponseEntity<Void> updateUserById(@PathVariable("userId") String userId,
                                               @RequestBody UpdateUserDto updateUserDto)
    {
        userService.updateUserById(userId, updateUserDto);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/{userId}")
    @Operation(summary = "Deleta Usuário", description = "Deleta usuário por ID")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "204", description = "Usuário deletado com sucesso"),
            @ApiResponse(responseCode = "401", description = "Token inválido ou não fornecido"),
            @ApiResponse(responseCode = "500", description = "Erro interno do servidor")
    })
    public ResponseEntity<Void> deleteById(@PathVariable("userId") String userId)
    {
        userService.deleteById(userId);
        return ResponseEntity.noContent().build();
    }
}
