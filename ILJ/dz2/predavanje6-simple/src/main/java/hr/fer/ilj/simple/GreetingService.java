package hr.fer.ilj.simple;

import org.springframework.stereotype.Service;

@Service
public class GreetingService {
	public String hello() {
		return "Bok!";
	}
}
