%{
#include "parser.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%%

"ato"         { return ATO; }
"com"         { return COM; }
"duracao"     { return DURACAO; }

"cena"        { return CENA; }
"se"          { return SE; }
"entao"       { return ENTAO; }
"senao"       { return SENAO; }
"enquanto"    { return ENQUANTO; }

"diretor"     { return DIRETOR; }
"ator"        { return ATOR; }
"como"        { return COMO; }
"fale"        { return FALE; }
"improviso"   { return IMPROVISO; }

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
