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

%token ATO CENA
%token DIRETOR ATOR COMO
%token SE ENTAO SENAO ENQUANTO
%token FALE IMPROVISO
%token COM DURACAO
%token ABREPAR FECHAPAR ABRECHAVE FECHACHAVE PONTOVIRG
%token IGUAL DIFERENTE MAIOR MENOR MAIORIGUAL MENORIGUAL
%token MAIS MENOS MULT DIV

%start programa

%%

programa:
    ATO IDENTIFICADOR COM DURACAO NUMERO bloco
;

bloco:
    ABRECHAVE lista_declaracoes FECHACHAVE
;

lista_declaracoes:
    /* vazio */
  | lista_declaracoes declaracao
;

declaracao:
    atribuicao
  | condicional
  | repeticao
  | fala
  | entrada
;

atribuicao:
    DIRETOR IDENTIFICADOR COMO comparacao PONTOVIRG
;

condicional:
    SE ABREPAR comparacao FECHAPAR ENTAO cena
    [ SENAO cena ]
;

repeticao:
    ENQUANTO ABREPAR comparacao FECHAPAR cena
;

fala:
    FALE ABREPAR comparacao FECHAPAR PONTOVIRG
;

entrada:
    ATOR IDENTIFICADOR COMO IMPROVISO ABREPAR FECHAPAR PONTOVIRG
;

cena:
    CENA bloco
;

comparacao:
    expressao comparacao_sufixo
;

comparacao_sufixo:
    /* vazio */ 
  | operador_comparacao expressao comparacao_sufixo
;

operador_comparacao:
    IGUAL
  | DIFERENTE
  | MAIOR
  | MENOR
  | MAIORIGUAL
  | MENORIGUAL
;

expressao:
    termo expressao_sufixo
;

expressao_sufixo:
    /* vazio */ 
  | operador_expressao termo expressao_sufixo
;

operador_expressao:
    MAIS
  | MENOS
;

termo:
    fator termo_sufixo
;

termo_sufixo:
    /* vazio */ 
  | operador_termo fator termo_sufixo
;

operador_termo:
    MULT
  | DIV
;

fator:
    IDENTIFICADOR
  | NUMERO
  | TEXTO
  | MAIS fator
  | MENOS fator
  | ABREPAR comparacao FECHAPAR
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}
