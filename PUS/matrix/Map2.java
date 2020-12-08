import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

public class Map2 extends MapReduceBase
        implements Mapper<LongWritable, Text, Text, Text> {


    public void map(LongWritable longWritable, Text value,
                    OutputCollector<Text, Text> output,
                    Reporter reporter) throws IOException {

        String[] parts = (value.toString()).split("\\s+");
        output.collect(new Text(parts[0]), new Text(parts[1]));

    }
}
