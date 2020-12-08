
import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

public class Reduce2 extends MapReduceBase
        implements Reducer<Text, Text, Text, Text> {


    public void reduce(Text key, Iterator<Text> values,
                       OutputCollector<Text, Text> output,
                       Reporter reporter) throws IOException {
        int sum = 0;

        while(values.hasNext()) {
            sum += Integer.parseInt((values.next()).toString());
        }

        String[] parts = (key.toString()).split(",");
        Text key_output = new Text(parts[0] + " " + parts[1]);
        output.collect(key_output, new Text(Integer.toString(sum)));
    }

}
