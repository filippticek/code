package hr.tel.fer.lab1.logger;

import hr.tel.fer.lab1.query.Expression;

import java.util.ArrayList;
import java.util.List;

public class LogFilter {
    public static List<Entry> filter(List<Expression> expressions, List<Entry> logs, String quantity) {
        List<Entry> filtered = logs;

        for (Expression exp : expressions) {
            List<Entry> temp = new ArrayList<>();

            switch (exp.getOperator()) {
                case "==":
                    switch (exp.getKey()) {
                        case "IP":
                            for (Entry ent : filtered)
                                if (ent.getIp().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                        case "DATETIME":
                            for (Entry ent : filtered)
                                if (ent.getDatetime().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                        case "METHOD":
                            for (Entry ent : filtered)
                                if (ent.getMethod().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                        case "VERSION":
                            for (Entry ent : filtered)
                                if (ent.getVersion().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                        case "STATUS":
                            for (Entry ent : filtered)
                                if (ent.getStatus().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                    }
                    break;
                case "!=":
                    switch (exp.getKey()) {
                        case "IP":
                            for (Entry ent : filtered)
                                if (!ent.getIp().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                        case "DATETIME":
                            for (Entry ent : filtered)
                                if (!ent.getDatetime().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                        case "METHOD":
                            for (Entry ent : filtered) {
                                if (!ent.getMethod().equals(exp.getValue()))
                                    temp.add(ent);
                            }
                            break;
                        case "VERSION":
                            for (Entry ent : filtered)
                                if (!ent.getVersion().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                        case "STATUS":
                            for (Entry ent : filtered)
                                if (!ent.getStatus().equals(exp.getValue()))
                                    temp.add(ent);
                            break;
                    }
                    break;
            }
            filtered = temp;


        }

    if (quantity.equals("*")) {
        return filtered;
    } else {
        return filtered.subList(0, Integer.parseInt(quantity));
    }
    }
}
