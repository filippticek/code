
import java.io.IOException;
import java.util.Iterator;
import java.util.Map;
import java.util.HashMap;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

public class Reduce1 extends MapReduceBase
        implements Reducer<Text, Text, Text, Text> {


    public void reduce(Text key, Iterator<Text> values,
                       OutputCollector<Text, Text> output,
                       Reporter reporter) throws IOException {

        Map<String, Integer> hashA = new HashMap<String, Integer>();
        Map<String, Integer> hashB = new HashMap<String, Integer>();

        while(values.hasNext()) {
            String[] parts = ((values.next()).toString()).split(",");
            if (parts[0].equals("a")) {
                hashA.put(parts[1], Integer.parseInt(parts[2]));
            } else if (parts[0].equals("b")) {
                hashB.put(parts[1], Integer.parseInt(parts[2]));
            }
        }

        for (Map.Entry<String, Integer> a : hashA.entrySet()) {
            for (Map.Entry<String, Integer> b : hashB.entrySet()) {
                output.collect(new Text(a.getKey() + "," + b.getKey()),
                        new Text(Integer.toString(a.getValue() * b.getValue())));
            }
        }
    }
}
