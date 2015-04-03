grammar ModelDef;

// Model is Run _task_ with _model_ on _portfolio_
modeldef 
      : task model pfset report
      ;

task  : RUN tasktype;

tasktype : SIMULATE | BACKTEST ;

model : ID;

pfset : ON pf+;

pf    : ID;

report : REPORTING ID;

// Keywords
RUN : [Rr][Uu][Nn];

ON  : [Oo][Nn]; 

SIMULATE : [Ss][Ii][Mm][Uu][Ll][Aa][Tt][Ee];

BACKTEST : [Bb][Aa][Cc][Kk][Tt][Ee][Ss][Tt];

REPORTING : [Rr][Ee][Pp][Oo][Rr][Tt][Ii][Nn][Gg];

INT   : [0-9]+ ;
ID    : [a-zA-Z]+ ;
NEWLINE : [\r\n]+;
WS    : [ \t]+ -> skip;
