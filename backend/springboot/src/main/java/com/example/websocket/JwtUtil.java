package com.example.websocket;

import java.util.Date;

import org.springframework.stereotype.Component;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

@Component
public class JwtUtil {

    private final String SECRET_KEY = "super_secret_key_123456789"; // Shared secret key

    public String generateToken(String payload) {
        return Jwts.builder()
                .setSubject(payload)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + 500000)) // 50 secs
                .signWith(SignatureAlgorithm.HS256, SECRET_KEY)
                .compact();
    }
}
