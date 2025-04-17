%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char *s);
int yylex();
%}

%union {
    int num;
    char* texto;
    char* id;
}

%token <id> IDENTIFICADOR
%token <num> NUMERO
%token <texto> TEXTO

%token GUARDE COMO SE ENTAO SENAO ENQUANTO MOSTRE ESCUTE INFORME
%token ABREPAR FECHAPAR ABRECHAVE FECHACHAVE PONTOVIRG
%token IGUAL DIFERENTE MAIOR MENOR MAIORIGUAL MENORIGUAL
%token MAIS MENOS MULT DIV

%start bloco

%%

bloco:
    ABRECHAVE
    declaracao
    FECHACHAVE
;

declaracao:
    atribuicao
  | condicional
  | repeticao
  | entrada
;

atribuicao:
    GUARDE IDENTIFICADOR COMO expressao PONTOVIRG
;

condicional:
    SE ABREPAR expressao FECHAPAR ENTAO bloco
    [ SENAO bloco ]
;

repeticao:
    ENQUANTO ABREPAR expressao FECHAPAR bloco
;

entrada:
    MOSTRE ABREPAR expressao FECHAPAR PONTOVIRG
;

comparacao:
    expressao IGUAL expressao
  | expressao DIFERENTE expressao
  | expressao NAIORIGUAL expressao
  | expressao MENORIGUAL expressao
  | expressao NAIOR expressao
  | expressao MENOR expressao
  | expressao
;

expressao:
    termo MAIS termo
  | termo MENOS termo
  | termo
;

termo:
    fator MULT fator
  | fator DIV fator
  | fator
;

fator:
    IDENTIFICADOR
  | NUMERO
  | TEXTO
  | MAIS fator
  | MENOS fator
  | ESCUTE ABREPAR FECHAPAR
  | ABREPAR expressao FECHAPAR
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}
