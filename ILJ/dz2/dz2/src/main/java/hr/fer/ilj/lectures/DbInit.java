package hr.fer.ilj.lectures;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import hr.fer.ilj.lectures.entities.Course;
import hr.fer.ilj.lectures.entities.Person;
import hr.fer.ilj.lectures.repositories.CourseRepository;
import hr.fer.ilj.lectures.repositories.PersonRepository;

@Component
public class DbInit implements CommandLineRunner {
	@Autowired PersonRepository personRepo;
	@Autowired CourseRepository courseRepo;

	@Override
	public void run(String... args) throws Exception {
		Person person1 = new Person("Bruno", "Blašković", "274", "C06-18");
		personRepo.save(person1);

		Person person2 = new Person("Mario", "Kušek", "301", "C08-12");
		personRepo.save(person2);
		
		Course courseIlj = new Course("ILJ", "Informacija, logika i jezici", person1);
		courseRepo.save(courseIlj);
		person1.getTeaching().add(courseIlj);
		personRepo.save(person1);
		
		Person person3 = new Person("Dragan", "Jevtić", "319", "C08-07");
		personRepo.save(person3);
		
		Course courseKM = new Course("KM", "Komunikacijske mreže", person3 );
		courseRepo.save(courseKM);
		person3.getTeaching().add(courseKM);
		personRepo.save(person3);
	}
	
}
