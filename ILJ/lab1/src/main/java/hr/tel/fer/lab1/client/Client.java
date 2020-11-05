package hr.tel.fer.lab1.client;

import java.net.*;

import org.apache.log4j.BasicConfigurator;

import java.io.*;




public class Client
{
  public static void main( String[] args ) throws Exception
  {
	  BasicConfigurator.configure();
    Socket sc = new Socket( args[0], Integer.parseInt(args[1]) );
    PrintWriter pwOut = new PrintWriter( sc.getOutputStream(), true );
    BufferedReader brIn = new BufferedReader( new InputStreamReader( sc
            .getInputStream() ) );

    String strUserInput = "";

    for (int i = 2; i < args.length; i++) {
      strUserInput = strUserInput + " " + args[i];
    }

    pwOut.println( strUserInput );
    String strFromServer;
    while ( (strFromServer = brIn.readLine()) != null) {
      System.out.println( strFromServer );
    }

    pwOut.close();
    brIn.close();
    sc.close();
    System.out.println( "Kraj!" );
  }
}
