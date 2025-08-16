package mdba.tutorials.agregadorinvestimentos;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
@OpenAPIDefinition(
        info = @Info(
                title = "Agregador de Investimentos API",
                version = "1.0.0",
                description = "API para consulta e agregação de investimentos",
                contact = @Contact(
                        name = "Michael Douglas Barbosa Araujo",
                        email = "michaeldouglas010790@gmail.com",
                        url = "https://medium.com/@mdbaraujo"
                ),
                license = @License(
                        name = "Apache 2.0",
                        url = "https://www.apache.org/licenses/LICENSE-2.0"
                )
        )
)
public class AgregadorinvestimentosApplication {

	public static void main(String[] args) {
		SpringApplication.run(AgregadorinvestimentosApplication.class, args);
	}

}
