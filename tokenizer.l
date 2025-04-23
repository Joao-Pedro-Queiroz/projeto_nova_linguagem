%{
#include "parser.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%%

"INICIO"            { return INICIO; }
"FIM"               { return FIM; }

"RECEBE"            { return RECEBE; }
"EXIBIR"            { return EXIBIR; }
"GUARDAR"           { return GUARDAR; }
"COMO"              { return COMO; }
"COM"               { return COM; }
"QUANDO"            { return QUANDO; }
"SENAO"             { return SENAO; }
"ENQUANTO"          { return ENQUANTO; }

"OU"                { return OU; }
"E"                 { return E; }

"IGUAL"             { return IGUAL; }
"MAIOR"             { return MAIOR; }
"MENOR"             { return MENOR; }

"MAIS"              { return MAIS; }
"MENOS"             { return MENOS; }
"CONCATENA"         { return CONCATENA; }
"VEZES"             { return MULT; }
"DIVIDIDO"          { return DIV; }
"NAO"               { return NAO; }
"PERGUNTAR"         { return PERGUNTAR; }

"NUMERO"            { return TIPO_NUMERO; }
"BOOLEANO"          { return TIPO_BOOL; }
"TEXTO"             { return TIPO_TEXTO; }

[0-9]+              { yylval.num = atoi(yytext); return NUMERO; }
"VERDADEIRO"        { yylval.booleano = 1; return BOOL; }
"FALSO"             { yylval.booleano = 0; return BOOL; }
\"[^\"]*\"          { yylval.texto = strdup(yytext); return TEXTO; }

[A-Z_][A-Z0-9_]* { yylval.id = strdup(yytext); return IDENTIFICADOR; }

"("                 { return ABREPAR; }
")"                 { return FECHAPAR; }
";"                 { return PONTOVIRG; }

[ \t\r\n]+          { /* Ignorar espaços, tabulações e quebras de linha */ }

.                   { printf("Caractere inválido: %s\n", yytext); }

%% 
