
import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

public class VideoCountReduce extends MapReduceBase
        implements Reducer<Text, IntWritable, Text, IntWritable> {


    public void reduce(Text key, Iterator<IntWritable> values,
                       OutputCollector<Text, IntWritable> output,
                       Reporter reporter) throws
            IOException {

        int count = 0;
        while (values.hasNext()) {
            values.next();
            count += 1;
        }
        output.collect(key,
                new IntWritable(count));
    }
}
