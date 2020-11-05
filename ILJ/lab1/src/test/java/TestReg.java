import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TestReg {

    public static void main(String[] args) {
        final String regex = "((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\\.|)){4})\\s\\[(\\d\\d\\/\\w\\w\\w\\/\\d\\d\\d\\d\\:\\d\\d\\:\\d\\d\\:\\d\\d)\\]\\s" +
                "(GET|PUT|POST|OPTIONS|HEAD)\\s(\\*|\\/.*?)\\s(HTTP\\/1\\.(?:0|1))\\s(\\d\\d\\d)\\s\\\"(.+?)\\\"";
        final Pattern pattern = Pattern.compile(regex);

        String asd = "127.0.0.1 [11/Feb/2014:10:45:02] OPTIONS * HTTP/1.0 200 \"Apache/2.2.22 (Debian) (internal dummy connection)\"";
        Matcher matcher = pattern.matcher(asd);
        if (matcher.find()) {
           System.out.println(matcher.group(3));
        }

    }
}
