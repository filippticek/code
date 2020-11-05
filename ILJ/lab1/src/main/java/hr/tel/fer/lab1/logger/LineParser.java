package hr.tel.fer.lab1.logger;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LineParser {
    private static final String regex = "((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\\.|)){4})\\s\\[(\\d\\d\\/\\w\\w\\w\\/\\d\\d\\d\\d\\:\\d\\d\\:\\d\\d\\:\\d\\d)\\]\\s" +
            "(GET|PUT|POST|OPTIONS|HEAD)\\s(\\*|\\/.*?)\\s(HTTP\\/1\\.(?:0|1))\\s(\\d\\d\\d)\\s\\\"(.+?)\\\"";
    private static final Pattern pattern = Pattern.compile(regex);

    public Entry parse(String line) {
        Matcher matcher = pattern.matcher(line);
        Entry e = new Entry();
        if (matcher.find()) {
            e.setIp(matcher.group(1));
            e.setDatetime(matcher.group(2));
            e.setMethod((matcher.group(3)));
            e.setPath(matcher.group(4));
            e.setVersion(matcher.group(5));
            e.setStatus(matcher.group(6));
            e.setClient(matcher.group(7));
        }
        return e;
    }
}
