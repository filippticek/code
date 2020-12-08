import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

public class VideoCountMap2 extends MapReduceBase
        implements Mapper<LongWritable, Text, IntWritable, Text> {


    public void map(LongWritable longWritable, Text value,
                    OutputCollector<IntWritable, Text> output,
                    Reporter reporter) throws
            IOException {

        String[] parts = (value.toString()).split("\\s+");

        String id = parts[0];
        int views = Integer.parseInt(parts[1]);
        output.collect(new IntWritable(views), new Text(id));

    }
}
