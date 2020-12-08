import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;


import java.io.IOException;


public class Matrix {

    public static void main(String[] args) throws
            IOException {
        if (args.length != 2) {
            System.err.println("Usage: Matrix <input path> <output path " +
                    ">");
            System.exit(-1);
        }
        JobConf conf = new JobConf(Matrix.class);
        conf.setJobName("Matrix MapReduce1");
        FileInputFormat.addInputPath(conf,
                new Path(args[0]));
        FileOutputFormat.setOutputPath(conf,
                new Path(args[1] + "/tmp"));
        conf.setMapperClass(Map1.class);
        conf.setReducerClass(Reduce1.class);
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);
        JobClient.runJob(conf);

        JobConf conf2 = new JobConf(Matrix.class);
        conf2.setJobName("Matrix MapReduce2");
        FileInputFormat.addInputPath(conf2,
                new Path(args[1] + "/tmp"));
        FileOutputFormat.setOutputPath(conf2,
                new Path(args[1] + "/final"));
        conf2.setMapperClass(Map2.class);
        conf2.setReducerClass(Reduce2.class);
        conf2.setOutputKeyClass(Text.class);
        conf2.setOutputValueClass(Text.class);
        JobClient.runJob(conf2);
    }
}
