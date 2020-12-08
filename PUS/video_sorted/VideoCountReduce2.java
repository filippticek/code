
import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

public class VideoCountReduce2 extends MapReduceBase
        implements Reducer<IntWritable, Text, Text, IntWritable> {


    public void reduce(IntWritable key, Iterator<Text> value,
                       OutputCollector<Text, IntWritable> output,
                       Reporter reporter) throws
            IOException {

        output.collect(value.next(), key);
    }

}
