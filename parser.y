%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char *s);
int yylex();
%}

%union {
    int num;
    int booleano;
    char* texto;
    char* id;
}

%token <id> IDENTIFICADOR
%token <num> NUMERO
%token <texto> TEXTO
%token <booleano> BOOL

%token INICIO FIM
%token GUARDAR COMO COM
%token EXIBIR PERGUNTAR
%token QUANDO ENTAO SENAO
%token ENQUANTO
%token MAIS MENOS CONCATENA MULT DIV
%token NAO
%token É
%token IGUAL MAIOR MENOR
%token OU E

%token TIPO_NUMERO TIPO_BOOL TIPO_TEXTO

%token ABREPAR FECHAPAR PONTOVIRG

%start programa

%%

programa:
    INICIO lista_instrucao FIM
;

lista_instrucao:
    /* vazio */
  | lista_instrucao instrucao
;

instrucao:
    PONTOVIRG
  | IDENTIFICADOR É expressao_ou PONTOVIRG
  | EXIBIR ABREPAR expressao_ou FECHAPAR PONTOVIRG
  | GUARDAR IDENTIFICADOR COMO tipo opcional_com PONTOVIRG
  | QUANDO ABREPAR expressao_ou FECHAPAR bloco opcional_senao
  | ENQUANTO ABREPAR expressao_ou FECHAPAR bloco
;

opcional_com:
    /* vazio */
  | COM expressao_ou
;

opcional_senao:
    /* vazio */
  | SENAO bloco
;

bloco:
    INICIO lista_instrucao FIM
;

tipo:
    TIPO_NUMERO
  | TIPO_BOOL
  | TIPO_TEXTO
;

expressao_ou:
    expressao_e expressao_ou_sufixo
;

expressao_ou_sufixo:
    /* vazio */
  | OU expressao_e expressao_ou_sufixo
;

expressao_e:
    expressao_rel expressao_e_sufixo
;

expressao_e_sufixo:
    /* vazio */
  | E expressao_rel expressao_e_sufixo
;

expressao_rel:
    expressao comparacao_sufixo
;

comparacao_sufixo:
    /* vazio */
  | operador_relacional expressao comparacao_sufixo
;

operador_relacional:
    IGUAL
  | MAIOR
  | MENOR
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
  | CONCATENA
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
    NUMERO
  | TEXTO
  | BOOL
  | IDENTIFICADOR
  | MAIS fator
  | MENOS fator
  | NAO fator
  | ABREPAR expressao_ou FECHAPAR
  | PERGUNTAR ABREPAR FECHAPAR
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}
