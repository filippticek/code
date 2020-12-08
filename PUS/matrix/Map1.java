import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

public class Map1 extends MapReduceBase
        implements Mapper<LongWritable, Text, Text, Text> {


    public void map(LongWritable longWritable, Text value,
                    OutputCollector<Text, Text> output,
                    Reporter reporter) throws
            IOException {

        String[] parts = (value.toString()).split(" ");
        String matrix = parts[0];
        String i = parts[1];
        String j = parts[2];
        String v = parts[3];
        if (matrix.equals("a")) {
            output.collect(new Text(j), new Text(matrix + "," + i + "," + v));
        } else if (matrix.equals("b")) {
            output.collect(new Text(i), new Text(matrix + "," + j + "," + v));
        }

    }
}
