package hr.fer.ilj.lectures.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import hr.fer.ilj.lectures.entities.Course;

public interface CourseRepository extends JpaRepository<Course, Long>{

}
