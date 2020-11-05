package hr.fer.ilj.lectures.entities;

import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.OneToMany;

@Entity
public class Person {
	@Id @GeneratedValue
	private Long id;
	
	private String firstName, lastName, phone, room;
	
	@OneToMany(mappedBy = "teacher")
	private List<Course> teaching;

	public Person() {
		this(null, null, null, null);
	}

	public Person(String firstName, String lastName, String phone, String room) {
		this.firstName = firstName;
		this.lastName = lastName;
		this.phone = phone;
		this.room = room;
		teaching = new LinkedList<>();
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getFirstName() {
		return firstName;
	}

	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}

	public String getLastName() {
		return lastName;
	}

	public void setLastName(String lastName) {
		this.lastName = lastName;
	}

	public String getPhone() {
		return phone;
	}

	public void setPhone(String phone) {
		this.phone = phone;
	}

	public String getRoom() {
		return room;
	}

	public void setRoom(String room) {
		this.room = room;
	}

	public List<Course> getTeaching() {
		return teaching;
	}

	public void setTeaching(List<Course> teaching) {
		this.teaching = teaching;
	}

	@Override
	public String toString() {
		return "Person [id=" + id + ", firstName=" + firstName + ", lastName=" + lastName + ", phone=" + phone
				+ ", room=" + room + ", teaching=[" + 
				teaching.stream().map(c -> c.getName()).collect(Collectors.joining(",")) + "]]";
	}
}
