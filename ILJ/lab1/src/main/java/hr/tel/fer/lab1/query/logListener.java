// Generated from /home/filip/Programiranje/ILJ/lab1/src/main/java/hr/tel/fer/lab1/query/log.g4 by ANTLR 4.7.2
package hr.tel.fer.lab1.query;


import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link logParser}.
 */
public interface logListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link logParser#filter}.
	 * @param ctx the parse tree
	 */
	void enterFilter(logParser.FilterContext ctx);
	/**
	 * Exit a parse tree produced by {@link logParser#filter}.
	 * @param ctx the parse tree
	 */
	void exitFilter(logParser.FilterContext ctx);
	/**
	 * Enter a parse tree produced by {@link logParser#retur}.
	 * @param ctx the parse tree
	 */
	void enterRetur(logParser.ReturContext ctx);
	/**
	 * Exit a parse tree produced by {@link logParser#retur}.
	 * @param ctx the parse tree
	 */
	void exitRetur(logParser.ReturContext ctx);
	/**
	 * Enter a parse tree produced by {@link logParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(logParser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link logParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(logParser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link logParser#value}.
	 * @param ctx the parse tree
	 */
	void enterValue(logParser.ValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link logParser#value}.
	 * @param ctx the parse tree
	 */
	void exitValue(logParser.ValueContext ctx);
}