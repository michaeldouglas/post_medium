package mdba.tutorials.agregadorinvestimentos.config;

import mdba.tutorials.agregadorinvestimentos.entity.user.User;
import mdba.tutorials.agregadorinvestimentos.repository.user.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.Instant;

@Configuration
public class DataInitializer {

    @Bean
    public CommandLineRunner initUsers(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        return args -> {
            System.out.println("DataInitializer rodando...");

            String adminEmail = "admin@email.com";

            if (userRepository.findByEmail(adminEmail).isEmpty()) {
                User admin = new User(
                        "admin",
                        adminEmail,
                        passwordEncoder.encode("admin123"),
                        Instant.now(),
                        Instant.now()
                );

                userRepository.saveAndFlush(admin);

                System.out.println("Usuário padrão criado: admin / admin123");
            } else {
                System.out.println("Usuário padrão já existe.");
            }
        };
    }
}
