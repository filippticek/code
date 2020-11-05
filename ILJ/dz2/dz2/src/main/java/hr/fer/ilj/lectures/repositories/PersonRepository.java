package hr.fer.ilj.lectures.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import hr.fer.ilj.lectures.entities.Person;

@RepositoryRestResource(excerptProjection=PersonListProjection.class)
public interface PersonRepository extends JpaRepository<Person, Long>{

}
