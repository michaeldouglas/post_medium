package mdba.tutorials.agregadorinvestimentos.service.user;

import mdba.tutorials.agregadorinvestimentos.entity.user.User;
import mdba.tutorials.agregadorinvestimentos.repository.user.UserRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.doReturn;

@ExtendWith(MockitoExtension.class)
class CustomUserDetailsServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private CustomUserDetailsService customUserDetailsService;

    private User buildUser() {
        var user = new User("username", "email@email.com", "encodedPass", Instant.now(), null);
        user.setUserId(UUID.randomUUID());
        return user;
    }

    @Nested
    class LoadUserByUsername {

        @Test
        @DisplayName("Should load user when exists")
        void shouldLoadUserWhenExists() {
            // Arrange
            var user = buildUser();
            doReturn(Optional.of(user)).when(userRepository).findByUsername("username");

            // Act
            UserDetails result = customUserDetailsService.loadUserByUsername("username");

            // Assert
            assertNotNull(result);
            assertEquals("username", result.getUsername());
            assertEquals("encodedPass", result.getPassword());
            assertTrue(result.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals("ROLE_USER")));
        }

        @Test
        @DisplayName("Should throw exception when user does not exist")
        void shouldThrowWhenUserNotFound() {
            // Arrange
            doReturn(Optional.empty()).when(userRepository).findByUsername("unknown");

            // Act & Assert
            assertThrows(UsernameNotFoundException.class,
                    () -> customUserDetailsService.loadUserByUsername("unknown"));
        }
    }
}
