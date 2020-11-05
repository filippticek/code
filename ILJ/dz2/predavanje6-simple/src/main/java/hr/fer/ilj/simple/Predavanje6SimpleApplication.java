package hr.fer.ilj.simple;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Predavanje6SimpleApplication implements CommandLineRunner {

	private GreetingService greetingService;

	public static void main(String[] args) {
		SpringApplication.run(Predavanje6SimpleApplication.class, args);
	}
	
	@Autowired
	public void setGreetingService(GreetingService greetingService) {
		this.greetingService = greetingService;
	}

	@Override
	public void run(String... args) throws Exception {
		System.out.println("*************");
		System.out.println(greetingService.hello());
	}
}
