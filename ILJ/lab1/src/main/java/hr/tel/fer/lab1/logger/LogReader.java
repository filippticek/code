package hr.tel.fer.lab1.logger;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class LogReader {

    public static List<Entry> readLog(File file) throws IOException{
        Scanner sc = new Scanner(new FileInputStream(file));
        List<Entry> log = new ArrayList<>();
        LineParser parser = new LineParser();

        while (sc.hasNextLine()){
            String line = sc.nextLine().trim();
            //System.out.println(line);
            Entry e;

            if((e = parser.parse(line)) != null){
                log.add(e);
            }
        }

        return log;
    }
}
