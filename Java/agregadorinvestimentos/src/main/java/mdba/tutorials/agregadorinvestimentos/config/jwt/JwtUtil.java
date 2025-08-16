package mdba.tutorials.agregadorinvestimentos.config.jwt;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.auth0.jwt.interfaces.JWTVerifier;

import java.util.Date;

public class JwtUtil {

    private static final String SECRET = "agregadordeinvestimentos782415987";

    // Tempo de expiração em milissegundos (1 hora)
    private static final long EXPIRATION_TIME = 60 * 60 * 1000;

    public static String generateToken(String username) {
        Algorithm algorithm = Algorithm.HMAC256(SECRET);
        return JWT.create()
                .withSubject(username)
                .withIssuer("agregador-investimentos")
                .withExpiresAt(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .sign(algorithm);
    }

    public static DecodedJWT validateToken(String token) {
        Algorithm algorithm = Algorithm.HMAC256(SECRET);
        JWTVerifier verifier = JWT.require(algorithm)
                .withIssuer("agregador-investimentos")
                .build();
        return verifier.verify(token);
    }
}
