grammar log;

@header {
package hr.tel.fer.lab1.query;
}

filter : 'FILTER' expr* retur;
retur : 'RETURN' value;
expr: KEY OP value;
value: STRING ;

KEY: 'IP' | 'DATETIME' | 'METHOD' | 'VERSION' | 'STATUS';
OP: '==' | '!=';
STRING: '"' (ESC|.)*? '"';
NUMBER: [0-9]+;
WS: [ \t\r\n]+ -> skip;
ESC: '\\"' | '\\\\';
