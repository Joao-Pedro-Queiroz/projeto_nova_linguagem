%{
#include "parser.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%%

"inicio"            { return INICIO; }
"fim"               { return FIM; }

"é"                 { return É; }
"exibir"            { return EXIBIR; }
"guardar"           { return GUARDAR; }
"como"              { return COMO; }
"com"               { return COM; }
"quando"            { return QUANDO; }
"senao"             { return SENAO; }
"enquanto"          { return ENQUANTO; }

"ou"                { return OU; }
"e"                 { return E; }

"igual"             { return IGUAL; }
"maior"             { return MAIOR; }
"menor"             { return MENOR; }

"mais"              { return MAIS; }
"menos"             { return MENOS; }
"concatena"         { return CONCATENA; }
"vezes"             { return MULT; }
"dividido"          { return DIV; }
"nao"               { return NAO; }
"perguntar"         { return PERGUNTAR; }

"numero"            { return TIPO_NUMERO; }
"booleano"          { return TIPO_BOOL; }
"texto"             { return TIPO_TEXTO; }

[0-9]+              { yylval.num = atoi(yytext); return NUMERO; }
"verdadeiro"        { yylval.booleano = 1; return BOOL; }
"falso"             { yylval.booleano = 0; return BOOL; }
\"[^\"]*\"          { yylval.texto = strdup(yytext); return TEXTO; }

[a-zA-Z_][a-zA-Z0-9_]* { yylval.id = strdup(yytext); return IDENTIFICADOR; }

"("                 { return ABREPAR; }
")"                 { return FECHAPAR; }
";"                 { return PONTOVIRG; }

[ \t\r\n]+          { /* Ignorar espaços, tabulações e quebras de linha */ }

.                   { printf("Caractere inválido: %s\n", yytext); }

%% 
