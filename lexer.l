%{
#include "parser.tab.h"
#include <stdio.h>
%}

%%

"guarde"      { return GUARDE; }
"como"        { return COMO; }
"se"          { return SE; }
"entao"       { return ENTAO; }
"senão"       { return SENAO; }
"enquanto"    { return ENQUANTO; }
"mostre"      { return MOSTRE; }
"escute"      { return ESCUTE; }

[0-9]+        { yylval.num = atoi(yytext); return NUMERO; }
\"[^\"]*\"    { yylval.texto = strdup(yytext); return TEXTO; }

[a-zA-Z_][a-zA-Z0-9_]* { yylval.id = strdup(yytext); return IDENTIFICADOR; }

"("           { return ABREPAR; }
")"           { return FECHAPAR; }
"{"           { return ABRECHAVE; }
"}"           { return FECHACHAVE; }
";"           { return PONTOVIRG; }
"=="          { return IGUAL; }
"!="          { return DIFERENTE; }
">="          { return MAIORIGUAL; }
"<="          { return MENORIGUAL; }
">"           { return MAIOR; }
"<"           { return MENOR; }
"+"           { return MAIS; }
"-"           { return MENOS; }
"*"           { return MULT; }
"/"           { return DIV; }

[ \t\n]+      { /* Ignorar espaços e quebras de linha */ }

.             { printf("Caractere inválido: %s\n", yytext); }

%%