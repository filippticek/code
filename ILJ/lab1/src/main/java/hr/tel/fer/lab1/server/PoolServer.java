package hr.tel.fer.lab1.server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.log4j.BasicConfigurator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PoolServer {
	private static final Logger LOG = LoggerFactory.getLogger(PoolServer.class);
	
	public static void main(String[] args) {
		BasicConfigurator.configure();
		try(ServerSocket ssc = new ServerSocket(Integer.parseInt(args[1]));) {
			ExecutorService pool = Executors.newFixedThreadPool(Integer.parseInt(args[0]));
	
			while (true) {
				Socket scClient = ssc.accept();

				ServerExecutor st = new ServerExecutor(scClient, args[2]);
				pool.execute(st);
			}
		} catch (IOException e) {
			LOG.error("Error starting server.", e);
		}
	}
}
