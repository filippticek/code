package hr.tel.fer.lab1.query;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link logParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface logVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link logParser#filter}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFilter(logParser.FilterContext ctx);
	/**
	 * Visit a parse tree produced by {@link logParser#retur}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRet(logParser.ReturContext ctx);
	/**
	 * Visit a parse tree produced by {@link logParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpr(logParser.ExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link logParser#value}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitValue(logParser.ValueContext ctx);
}