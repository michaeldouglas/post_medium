package mdba.tutorials.agregadorinvestimentos.service.user;

import mdba.tutorials.agregadorinvestimentos.dto.user.CreateUserDto;
import mdba.tutorials.agregadorinvestimentos.dto.user.UpdateUserDto;
import mdba.tutorials.agregadorinvestimentos.entity.user.User;
import mdba.tutorials.agregadorinvestimentos.repository.user.UserRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Captor
    private ArgumentCaptor<User> userCaptor;

    private User buildUser() {
        var user = new User("username", "email@email.com", "encodedPassword", Instant.now(), null);
        user.setUserId(UUID.randomUUID());
        return user;
    }

    @Nested
    class CreateUser {
        @Test
        @DisplayName("Should create a user with success")
        void shouldCreateUser() {
            // Arrange
            var input = new CreateUserDto("username", "email@email.com", "123456");
            var savedUser = buildUser();

            doReturn("encodedPassword").when(passwordEncoder).encode(any());
            doReturn(savedUser).when(userRepository).save(userCaptor.capture());

            // Act
            var output = userService.createUser(input);

            // Assert
            assertNotNull(output);
            assertEquals(savedUser.getUserId(), output);

            var captured = userCaptor.getValue();
            assertEquals("username", captured.getUsername());
            assertEquals("email@email.com", captured.getEmail());
            assertEquals("encodedPassword", captured.getPassword());

            verify(passwordEncoder).encode(input.password());
            verify(userRepository).save(any());
        }

        @Test
        @DisplayName("Should throw exception when repository fails")
        void shouldThrowWhenRepositoryFails() {
            var input = new CreateUserDto("username", "email@email.com", "123456");
            doThrow(new RuntimeException("DB error")).when(userRepository).save(any());

            assertThrows(RuntimeException.class, () -> userService.createUser(input));
        }
    }

    @Nested
    class FindByUsername {
        @Test
        @DisplayName("Should return user when found")
        void shouldReturnUser() {
            var user = buildUser();
            doReturn(Optional.of(user)).when(userRepository).findByUsername("username");

            var result = userService.findByUsername("username");

            assertTrue(result.isPresent());
            assertEquals(user.getUserId(), result.get().getUserId());
        }

        @Test
        @DisplayName("Should return empty when not found")
        void shouldReturnEmpty() {
            doReturn(Optional.empty()).when(userRepository).findByUsername("unknown");

            var result = userService.findByUsername("unknown");

            assertTrue(result.isEmpty());
        }
    }

    @Nested
    class GetUserById {
        @Test
        @DisplayName("Should return user by ID")
        void shouldReturnUserById() {
            var user = buildUser();
            doReturn(Optional.of(user)).when(userRepository).findById(user.getUserId());

            var result = userService.getUserById(user.getUserId().toString());

            assertTrue(result.isPresent());
            assertEquals(user.getUserId(), result.get().getUserId());
        }

        @Test
        @DisplayName("Should return empty when not exists")
        void shouldReturnEmpty() {
            doReturn(Optional.empty()).when(userRepository).findById(any());

            var result = userService.getUserById(UUID.randomUUID().toString());

            assertTrue(result.isEmpty());
        }
    }

    @Nested
    class ListUsers {
        @Test
        @DisplayName("Should return paged list of users")
        void shouldReturnPagedUsers() {
            var users = List.of(buildUser(), buildUser());
            var page = new PageImpl<>(users);
            doReturn(page).when(userRepository).findAll(any(PageRequest.class));

            var result = userService.listUsers(PageRequest.of(0, 10));

            assertEquals(2, result.getContent().size());
        }
    }

    @Nested
    class UpdateUser {
        @Test
        @DisplayName("Should update username and password")
        void shouldUpdateUser() {
            var user = buildUser();
            doReturn(Optional.of(user)).when(userRepository).findById(user.getUserId());
            doReturn("encodedNewPassword").when(passwordEncoder).encode("newPass");
            doReturn(user).when(userRepository).save(userCaptor.capture());

            var input = new UpdateUserDto("newUsername", "newPass");
            userService.updateUserById(user.getUserId().toString(), input);

            var captured = userCaptor.getValue();
            assertEquals("newUsername", captured.getUsername());
            assertEquals("encodedNewPassword", captured.getPassword());

            verify(userRepository).save(any(User.class));
        }

        @Test
        @DisplayName("Should do nothing if user not found")
        void shouldDoNothingWhenUserNotFound() {
            doReturn(Optional.empty()).when(userRepository).findById(any());

            userService.updateUserById(UUID.randomUUID().toString(), new UpdateUserDto("name", "pass"));

            verify(userRepository, never()).save(any());
        }
    }

    @Nested
    class DeleteUser {
        @Test
        @DisplayName("Should delete user when exists")
        void shouldDeleteWhenExists() {
            var id = UUID.randomUUID();
            doReturn(true).when(userRepository).existsById(id);

            userService.deleteById(id.toString());

            verify(userRepository).deleteById(id);
        }

        @Test
        @DisplayName("Should not delete when user does not exist")
        void shouldNotDeleteWhenNotExists() {
            var id = UUID.randomUUID();
            doReturn(false).when(userRepository).existsById(id);

            userService.deleteById(id.toString());

            verify(userRepository, never()).deleteById(any());
        }
    }
}
