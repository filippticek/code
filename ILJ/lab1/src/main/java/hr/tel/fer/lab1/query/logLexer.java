// Generated from /home/filip/Programiranje/ILJ/lab1/src/main/java/hr/tel/fer/lab1/query/log.g4 by ANTLR 4.7.2
package hr.tel.fer.lab1.query;


import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class logLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.7.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, KEY=3, OP=4, STRING=5, NUMBER=6, WS=7, ESC=8;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "KEY", "OP", "STRING", "NUMBER", "WS", "ESC"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'FILTER'", "'RETURN'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, "KEY", "OP", "STRING", "NUMBER", "WS", "ESC"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public logLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "log.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\nb\b\1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\3\2\3\2\3\2\3\2"+
		"\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3"+
		"\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4"+
		"\3\4\3\4\3\4\3\4\5\4?\n\4\3\5\3\5\3\5\3\5\5\5E\n\5\3\6\3\6\3\6\7\6J\n"+
		"\6\f\6\16\6M\13\6\3\6\3\6\3\7\6\7R\n\7\r\7\16\7S\3\b\6\bW\n\b\r\b\16\b"+
		"X\3\b\3\b\3\t\3\t\3\t\3\t\5\ta\n\t\3K\2\n\3\3\5\4\7\5\t\6\13\7\r\b\17"+
		"\t\21\n\3\2\4\3\2\62;\5\2\13\f\17\17\"\"\2k\2\3\3\2\2\2\2\5\3\2\2\2\2"+
		"\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2"+
		"\2\2\3\23\3\2\2\2\5\32\3\2\2\2\7>\3\2\2\2\tD\3\2\2\2\13F\3\2\2\2\rQ\3"+
		"\2\2\2\17V\3\2\2\2\21`\3\2\2\2\23\24\7H\2\2\24\25\7K\2\2\25\26\7N\2\2"+
		"\26\27\7V\2\2\27\30\7G\2\2\30\31\7T\2\2\31\4\3\2\2\2\32\33\7T\2\2\33\34"+
		"\7G\2\2\34\35\7V\2\2\35\36\7W\2\2\36\37\7T\2\2\37 \7P\2\2 \6\3\2\2\2!"+
		"\"\7K\2\2\"?\7R\2\2#$\7F\2\2$%\7C\2\2%&\7V\2\2&\'\7G\2\2\'(\7V\2\2()\7"+
		"K\2\2)*\7O\2\2*?\7G\2\2+,\7O\2\2,-\7G\2\2-.\7V\2\2./\7J\2\2/\60\7Q\2\2"+
		"\60?\7F\2\2\61\62\7X\2\2\62\63\7G\2\2\63\64\7T\2\2\64\65\7U\2\2\65\66"+
		"\7K\2\2\66\67\7Q\2\2\67?\7P\2\289\7U\2\29:\7V\2\2:;\7C\2\2;<\7V\2\2<="+
		"\7W\2\2=?\7U\2\2>!\3\2\2\2>#\3\2\2\2>+\3\2\2\2>\61\3\2\2\2>8\3\2\2\2?"+
		"\b\3\2\2\2@A\7?\2\2AE\7?\2\2BC\7#\2\2CE\7?\2\2D@\3\2\2\2DB\3\2\2\2E\n"+
		"\3\2\2\2FK\7$\2\2GJ\5\21\t\2HJ\13\2\2\2IG\3\2\2\2IH\3\2\2\2JM\3\2\2\2"+
		"KL\3\2\2\2KI\3\2\2\2LN\3\2\2\2MK\3\2\2\2NO\7$\2\2O\f\3\2\2\2PR\t\2\2\2"+
		"QP\3\2\2\2RS\3\2\2\2SQ\3\2\2\2ST\3\2\2\2T\16\3\2\2\2UW\t\3\2\2VU\3\2\2"+
		"\2WX\3\2\2\2XV\3\2\2\2XY\3\2\2\2YZ\3\2\2\2Z[\b\b\2\2[\20\3\2\2\2\\]\7"+
		"^\2\2]a\7$\2\2^_\7^\2\2_a\7^\2\2`\\\3\2\2\2`^\3\2\2\2a\22\3\2\2\2\n\2"+
		">DIKSX`\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}