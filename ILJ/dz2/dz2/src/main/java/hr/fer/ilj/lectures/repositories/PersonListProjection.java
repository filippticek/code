package hr.fer.ilj.lectures.repositories;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.rest.core.config.Projection;

import hr.fer.ilj.lectures.entities.Person;

@Projection(name="short", types = { Person.class })
public interface PersonListProjection {
  @Value("#{target.firstName}")
  String getFirstName();

  @Value("#{target.lastName}")
  String getLastName();

  @Value("#{target.phone}")
  String getPhone();

  @Value("#{target.room}")
  String getRoom();

  Long getId();
}
