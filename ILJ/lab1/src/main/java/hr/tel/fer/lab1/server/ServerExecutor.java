package hr.tel.fer.lab1.server;

import java.io.*;
import java.net.Socket;
import java.util.List;

import hr.tel.fer.lab1.logger.Entry;
import hr.tel.fer.lab1.logger.LogFilter;
import hr.tel.fer.lab1.logger.LogReader;
import hr.tel.fer.lab1.query.Expression;
import hr.tel.fer.lab1.query.ExpressionExtractor;
import hr.tel.fer.lab1.query.logLexer;
import hr.tel.fer.lab1.query.logParser;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ServerExecutor implements Runnable {
	private static final Logger LOG = LoggerFactory.getLogger(ServerExecutor.class);
	
	private Socket socket;
	private final File dat;

	public ServerExecutor(Socket socket, String dat) {
		this.socket = socket;
		this.dat = new File(dat);
	}

	public void run(){
		try(PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));)
		{
			String strInLine, strOutLine;

			if ((strInLine = in.readLine()) != null) {
				strOutLine = handleQuery(strInLine);
				out.println(strOutLine);
			}

		} catch (IOException ioe) {
			LOG.error("Error handling client.", ioe);
		} catch (Exception e) {
			LOG.error("Query exception", e);
		} finally {
			try {
				socket.close();
			} catch (Exception e) {
			}
		}
	}

	private String handleQuery(String query) throws Exception{
		String quanity = query.substring(query.length() - 2, query.length() -1);
		List<Expression> expressions = parseQuery(query);
		List<Entry> logs = LogReader.readLog(dat);
		List<Entry> filtered = LogFilter.filter(expressions, logs, quanity);

		String logString = "";
		for (Entry e : filtered) {
			logString = logString + e.toString();
		}
		return logString;

	}

	private List<Expression> parseQuery(String query) throws Exception{
		ANTLRInputStream input = new ANTLRInputStream(new StringBufferInputStream(query));

		logLexer lexer = new logLexer(input);
		CommonTokenStream tokens = new CommonTokenStream(lexer);

		logParser parser = new logParser(tokens);
		ParseTree tree = parser.filter();

		ParseTreeWalker walker = new ParseTreeWalker();
		ExpressionExtractor listener = new ExpressionExtractor();
		walker.walk(listener, tree);
		if (listener.getError() != null)
			throw new Exception(listener.getError());

		return listener.getExpressions();
	}
}
