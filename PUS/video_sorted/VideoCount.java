import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;


import java.io.IOException;


public class VideoCount {

    public static void main(String[] args) throws
            IOException {
        if (args.length != 2) {
            System.err.println("Usage: VideoCount <input path> <output path " +
                    ">");
            System.exit(-1);
        }
        JobConf conf = new JobConf(VideoCount.class);
        conf.setJobName("Video count");
        FileInputFormat.addInputPath(conf,
                new Path(args[0]));
        FileOutputFormat.setOutputPath(conf,
                new Path(args[1] + "/tmp"));
        conf.setMapperClass(VideoCountMap.class);
        conf.setReducerClass(VideoCountReduce.class);
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(IntWritable.class);
        JobClient.runJob(conf);

        JobConf conf2 = new JobConf(VideoCount.class);
        conf2.setJobName("Video count sort");
        FileInputFormat.addInputPath(conf2,
                new Path(args[1] + "/tmp"));
        FileOutputFormat.setOutputPath(conf2,
                new Path(args[1] + "/final"));
        conf2.setMapperClass(VideoCountMap2.class);
        conf2.setReducerClass(VideoCountReduce2.class);
        conf2.setOutputKeyClass(IntWritable.class);
        conf2.setOutputValueClass(Text.class);
        conf2.setKeyFieldComparatorOptions("-r");
        JobClient.runJob(conf2);
    }
}
