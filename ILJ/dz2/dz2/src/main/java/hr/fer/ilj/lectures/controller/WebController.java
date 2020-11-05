package hr.fer.ilj.lectures.controller;

import hr.fer.ilj.lectures.repositories.CourseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.stream.Collectors;

@Controller
public class WebController {

    @GetMapping(value="/")
    public String homepage(){
        return "index.html";
    }

    @GetMapping(value="/asd")
    public String teachers(){
        return "teachers.html";
    }

}
