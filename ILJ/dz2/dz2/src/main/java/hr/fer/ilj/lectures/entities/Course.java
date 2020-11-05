package hr.fer.ilj.lectures.entities;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.ManyToOne;

@Entity
public class Course {

	@Id @GeneratedValue
	private Long id;
	
	private String name, description;
	
	@ManyToOne
	private Person teacher;
	
	public Course() {
	}

	public Course(String name, String description, Person teacher) {
		this.name = name;
		this.description = description;
		this.teacher = teacher;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public Person getTeacher() {
		return teacher;
	}

	public void setTeacher(Person teacher) {
		this.teacher = teacher;
	}

	@Override
	public String toString() {
		return "Course [id=" + id + ", name=" + name + ", description=" + description + ", teacher=" + 
				teacher.getFirstName() + " " + teacher.getLastName() + "]";
	}
}
