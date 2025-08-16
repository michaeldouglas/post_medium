package mdba.tutorials.agregadorinvestimentos.service.user;

import mdba.tutorials.agregadorinvestimentos.dto.user.CreateUserDto;
import mdba.tutorials.agregadorinvestimentos.dto.user.UpdateUserDto;
import mdba.tutorials.agregadorinvestimentos.entity.user.User;
import mdba.tutorials.agregadorinvestimentos.repository.user.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public UUID createUser(CreateUserDto createUserDto) {
        var entity = new User(
                createUserDto.username(),
                createUserDto.email(),
                passwordEncoder.encode(createUserDto.password()),
                Instant.now(),
                null
        );

        var userSave = userRepository.save(entity);
        return userSave.getUserId();
    }

    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    public Optional<User> getUserById(String userId)
    {
        return userRepository.findById(UUID.fromString(userId));
    }

    public Page<User> listUsers(Pageable pageable)
    {
        return userRepository.findAll(pageable);
    }

    public void updateUserById(String userId, UpdateUserDto updateUserDto)
    {
        var id = UUID.fromString(userId);
        var userEntity = userRepository.findById(id);

        if(userEntity.isPresent())
        {
            var user = userEntity.get();
            if (updateUserDto.username() != null) {
                user.setUsername(updateUserDto.username());
            }
            if (updateUserDto.password() != null) {
                user.setPassword(passwordEncoder.encode(updateUserDto.password()));
            }

            userRepository.save(user);
        }
    }

    public void deleteById(String userId)
    {
        var id = UUID.fromString(userId);
        var userExists = userRepository.existsById(id);

        if(userExists) userRepository.deleteById(id);
    }
}
