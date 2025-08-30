package mdba.tutorials.agregadorinvestimentos.controller.auth;

import mdba.tutorials.agregadorinvestimentos.dto.auth.AuthLoginDto;
import mdba.tutorials.agregadorinvestimentos.entity.user.User;
import mdba.tutorials.agregadorinvestimentos.repository.user.UserRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.Instant;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.doReturn;

@ExtendWith(MockitoExtension.class)
class AuthControllerTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private AuthController authController;

    private User buildUser() {
        var user = new User("michael", "michael" + "@mail.com", "encodedPassword", Instant.now(), null);
        user.setUserId(UUID.randomUUID());
        return user;
    }

    @Nested
    class Login {

        @Test
        @DisplayName("Should return 401 when username or password is null")
        void shouldReturn401WhenNullFields() throws Exception {
            var dto = new AuthLoginDto(null, null);

            ResponseEntity<Map<String, Object>> response = authController.login(dto);

            assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
            assertEquals("Usuário e senha são obrigatórios", response.getBody().get("error"));
        }

        @Test
        @DisplayName("Should return 401 when user not found")
        void shouldReturn401WhenUserNotFound() throws Exception {
            var dto = new AuthLoginDto("michael", "123456");
            doReturn(Optional.empty()).when(userRepository).findByUsername("michael");

            ResponseEntity<Map<String, Object>> response = authController.login(dto);

            assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
            assertEquals("Usuário ou senha inválidos", response.getBody().get("error"));
        }

        @Test
        @DisplayName("Should return 401 when password does not match")
        void shouldReturn401WhenPasswordInvalid() throws Exception {
            var dto = new AuthLoginDto("michael", "wrongPass");
            var user = buildUser();

            doReturn(Optional.of(user)).when(userRepository).findByUsername("michael");
            doReturn(false).when(passwordEncoder).matches(dto.password(), user.getPassword());

            ResponseEntity<Map<String, Object>> response = authController.login(dto);

            assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
            assertEquals("Usuário ou senha inválidos", response.getBody().get("error"));
        }

        @Test
        @DisplayName("Should return 200 and token when login success")
        void shouldReturn200WhenLoginSuccess() throws Exception {
            var dto = new AuthLoginDto("michael", "123456");
            var user = buildUser();

            doReturn(Optional.of(user)).when(userRepository).findByUsername("michael");
            doReturn(true).when(passwordEncoder).matches(dto.password(), user.getPassword());

            ResponseEntity<Map<String, Object>> response = authController.login(dto);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNotNull(response.getBody().get("token"));
            assertEquals("michael", response.getBody().get("username"));
            assertEquals(3600, response.getBody().get("expires_in"));
        }
    }

    @Nested
    class HandleRuntimeException {

        @Test
        @DisplayName("Should return 401 when runtime exception occurs")
        void shouldReturn401OnRuntimeException() {
            var ex = new RuntimeException("Erro inesperado");

            ResponseEntity<Map<String, Object>> response = authController.handleRuntimeException(ex);

            assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
            assertEquals("Erro inesperado", response.getBody().get("error"));
        }
    }
}
