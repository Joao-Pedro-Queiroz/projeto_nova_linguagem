/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    IDENTIFICADOR = 258,           /* IDENTIFICADOR  */
    NUMERO = 259,                  /* NUMERO  */
    TEXTO = 260,                   /* TEXTO  */
    BOOL = 261,                    /* BOOL  */
    INICIO = 262,                  /* INICIO  */
    FIM = 263,                     /* FIM  */
    GUARDAR = 264,                 /* GUARDAR  */
    COMO = 265,                    /* COMO  */
    COM = 266,                     /* COM  */
    EXIBIR = 267,                  /* EXIBIR  */
    PERGUNTAR = 268,               /* PERGUNTAR  */
    FALAR = 269,                   /* FALAR  */
    QUANDO = 270,                  /* QUANDO  */
    SENAO = 271,                   /* SENAO  */
    ENQUANTO = 272,                /* ENQUANTO  */
    MAIS = 273,                    /* MAIS  */
    MENOS = 274,                   /* MENOS  */
    CONCATENA = 275,               /* CONCATENA  */
    MULT = 276,                    /* MULT  */
    DIV = 277,                     /* DIV  */
    NAO = 278,                     /* NAO  */
    RECEBE = 279,                  /* RECEBE  */
    IGUAL = 280,                   /* IGUAL  */
    MAIOR = 281,                   /* MAIOR  */
    MENOR = 282,                   /* MENOR  */
    OU = 283,                      /* OU  */
    E = 284,                       /* E  */
    TIPO_NUMERO = 285,             /* TIPO_NUMERO  */
    TIPO_BOOL = 286,               /* TIPO_BOOL  */
    TIPO_TEXTO = 287,              /* TIPO_TEXTO  */
    ABREPAR = 288,                 /* ABREPAR  */
    FECHAPAR = 289,                /* FECHAPAR  */
    PONTOVIRG = 290                /* PONTOVIRG  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 8 "parser.y"

    int num;
    int booleano;
    char* texto;
    char* id;

#line 106 "parser.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_TAB_H_INCLUDED  */
