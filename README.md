# 🔆 Projeto Nova Linguagem – LumenScript

Seja bem-vindo ao repositório da **LumenScript**, uma linguagem de programação inclusiva projetada especialmente para **pessoas com baixa visão**. 🌟

---

## 🎯 Objetivo

A **LumenScript** foi criada com o propósito de tornar a programação mais **acessível e legível** para pessoas com baixa visão, utilizando palavras-chave claras, intuitivas e semanticamente significativas, além de uma estrutura visual simplificada e padronizada.

Ela propõe uma nova forma de pensar a programação, focando em clareza, contraste e familiaridade.

---

## 🌐 Conceito

A linguagem substitui elementos técnicos comuns por termos mais acessíveis e fáceis de interpretar visualmente e semanticamente. A proposta da **LumenScript** é que o código seja **autoexplicativo**, com foco em:

- **Alto contraste na interface** (em ambientes gráficos);
- **Palavras-chave amplas, espaçadas e legíveis**;
- **Eliminação de ambiguidade sintática**;
- **Vocabulário em português simples**;
- **Objetividade nas instruções**.

---

## 🧠 Palavras-chave e Significados

| Palavra-chave       | Significado                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `inicio`            | Início do bloco principal do programa.                                      |
| `fim`               | Final de um bloco de código.                                                |
| `exibir(...)`       | Exibe informação na tela. Equivalente ao `print(...)`.                      |
| `perguntar(...)`    | Solicita entrada do usuário. Equivalente ao `reader()` ou `input()`.        |
| `guardar`           | Declara uma variável.                                                       |
| `em`                | Define o tipo da variável (`numero`, `texto`, `verdadeiro`).                |
| `com`               | Opcional: atribui valor inicial à variável.                                 |
| `quando (...)`      | Condicional (if).                                                           |
| `senao`             | Bloco alternativo ao condicional.                                           |
| `enquanto (...)`    | Laço de repetição.                                                          |
| `é igual`, `maior`, `menor` | Operadores relacionais (`==`, `>`, `<`).                            |
| `ou`, `e`           | Operadores lógicos (`||`, `&&`).                                            |
| `mais`, `menos`, `concatena` | Operadores aritméticos (`+`, `-`, `++`).                              |
| `vezes`, `dividido` | Multiplicação e divisão (`*`, `/`).                                         |
| `nao`               | Negação lógica (`!`).                                                       |
| `;`                 | Final da instrução.                                                         |

---

## 🔤 Estrutura Gramatical (EBNF)

A estrutura da **LumenScript** está baseada na EBNF tradicional com nomes acessíveis e semanticamente descritivos:

```ebnf
BlocoPrincipal     = "inicio", { Instrucao }, "fim" ;

Instrucao          = ";"
                   | identificador "é" ExpressaoOu ";"
                   | "exibir" "(" ExpressaoOu ")" ";"
                   | "guardar" identificador "em" tipo [ "com" ExpressaoOu ] ";"
                   | "quando" "(" ExpressaoOu ")" BlocoPrincipal [ "senao" BlocoPrincipal ]
                   | "enquanto" "(" ExpressaoOu ")" BlocoPrincipal ;

ExpressaoOu        = ExpressaoE { "ou" ExpressaoE } ;

ExpressaoE         = ExpressaoRel { "e" ExpressaoRel } ;

ExpressaoRel       = Expressao [ OperadorRelacional Expressao ] ;

Expressao          = Termo { ("mais" | "menos" | "concatena") Termo } ;

Termo              = Fator { ("vezes" | "dividido") Fator } ;

Fator              = numero
                   | texto
                   | booleano
                   | identificador
                   | "mais" Fator
                   | "menos" Fator
                   | "nao" Fator
                   | "(" ExpressaoOu ")"
                   | "perguntar" "(" ")" ;

OperadorRelacional = "é igual" | "maior" | "menor" ;

tipo               = "numero" | "verdadeiro" | "texto" ;

identificador      = letra { letra | digito | "_" } ;
numero             = digito { digito } ;
texto              = '"' { qualquer_caractere_que_nao_seja_aspas } '"' ;
booleano           = "sim" | "nao" ;
```

---

## ✨ Por que LumenScript?

A **LumenScript** foi criada com um objetivo claro: tornar a programação **acessível, legível e inclusiva**, especialmente para pessoas com baixa visão. Ao repensar não apenas a sintaxe, mas também os conceitos da linguagem, buscamos construir uma ponte entre tecnologia e acessibilidade real.

### 🌟 Nossos princípios fundamentais:

- **Acessibilidade Visual**: A linguagem foi projetada com foco em contraste, simplicidade e clareza. As palavras-chave são intuitivas e os blocos de código seguem uma estrutura limpa, facilitando o uso com leitores de tela e lupas digitais.

- **Sintaxe Natural e Sem Ambiguidades**: Termos como `exibir`, `guardar`, `perguntar`, `quando`, `enquanto` e `senao` foram escolhidos por sua carga semântica clara e relação direta com ações e conceitos do cotidiano. Isso reduz a curva de aprendizado e torna a experiência de programar mais intuitiva.

- **Inclusão como valor central**: Ao contrário de linguagens tradicionais que muitas vezes afastam iniciantes, a **LumenScript** foi construída para acolher. Seja você um desenvolvedor experiente com deficiência visual ou alguém dando os primeiros passos, encontrará aqui um espaço acessível.

- **Educação centrada no humano**: A LumenScript também visa ser uma ferramenta poderosa em ambientes educacionais inclusivos, onde alunos com necessidades visuais específicas possam acompanhar e participar de atividades de lógica e programação com autonomia.

- **Linguagem pensada para todos os sentidos**: O nome **LumenScript** vem de “lumen”, unidade de luz, simbolizando clareza, foco e visibilidade. A linguagem busca iluminar o caminho para a inclusão digital por meio da escrita de código acessível.

A **LumenScript** é, acima de tudo, um convite para **programar com empatia, clareza e propósito** — onde a luz da acessibilidade guia cada linha de código.

---

## 🌱 Boas Práticas
Aqui estão algumas boas práticas que podem ajudá-lo a escrever código limpo, legível e acessível usando a LumenScript:

1. Seja Descritivo nas Variáveis e Funções
Ao nomear suas variáveis e funções, prefira nomes descritivos e claros. Evite abreviações e prefira palavras completas. Por exemplo:

- Use nome em vez de n.

- Use idade em vez de i.

2. Comentários no Código
Mesmo com uma sintaxe simples e clara, adicionar comentários pode ajudar a explicar partes mais complexas do código, facilitando a leitura para outras pessoas (ou para você mesmo no futuro). Em LumenScript, você pode usar o formato:

```
informe: Este código calcula a idade de uma pessoa.
```

3. Evite Linhas de Código Longas
Se uma linha de código se tornar muito longa ou complexa, quebre-a em várias linhas para facilitar a leitura. Isso é especialmente importante quando você está usando ferramentas como leitores de tela, que podem ter dificuldade com longas sequências de texto.

4. Organize Seu Código
Mantenha seu código organizado em blocos e faça uso de indentação consistente. Cada vez que você inicia um novo bloco, use uma identação clara para mostrar visualmente a estrutura do código.

5. Use Alto Contraste
Se você está escrevendo código em um editor ou IDE, utilize temas com alto contraste, como o modo escuro ou temas específicos para pessoas com baixa visão. Isso pode tornar a experiência de codificação muito mais confortável.

6. Teste com Ferramentas de Acessibilidade
Sempre que possível, teste seu código com leitores de tela ou outras ferramentas de acessibilidade. Isso pode ajudar a identificar pontos que podem ser melhorados para garantir que o código seja acessível a todos.

---

## 🧩 Extensões Futuras

A LumenScript está em constante evolução. Algumas ideias e possibilidades para versões futuras incluem:

- **Compatibilidade com leitores de tela:**  
  Fornecer suporte nativo a leitores de tela, com descrições semânticas e alertas verbais que auxiliem na navegação e interpretação do código.

- **Sistema de alertas sonoros:**  
  Implementação de sons diferenciados para indicar eventos como erro de sintaxe, início de execução ou término bem-sucedido, facilitando o acompanhamento auditivo.

- **Modo braille:**  
  Geração de arquivos `.brf` compatíveis com dispositivos de leitura tátil, permitindo que o código seja lido em displays braille.

- **Modo alto contraste (em IDEs e editores):**  
  Sugestão de temas com alto contraste e legibilidade para utilização da linguagem em ambientes como VS Code ou plataformas online.

- **Suporte a narração de código:**  
  Ferramenta de leitura em voz alta que interpreta os comandos da LumenScript como frases naturais para fácil compreensão.

- **Blocos visuais acessíveis:**  
  Implementação futura de um modo visual alternativo baseado em blocos grandes, com texto ampliado e contrastado para uso educacional.

Essas propostas têm como objetivo ampliar ainda mais a acessibilidade e tornar a experiência de programar mais confortável, intuitiva e inclusiva.

---

## 🙌 Contribuindo

A comunidade é essencial para o crescimento da **LumenScript**. Se você acredita na importância da acessibilidade na programação e deseja colaborar com o projeto, aqui estão algumas formas de contribuir:

### 💡 Sugestões e Ideias

- Proponha novas funcionalidades ou melhorias através de issues.
- Sugira adaptações para públicos com necessidades específicas.
- Compartilhe feedback de pessoas com baixa visão que utilizarem a linguagem.

### 🐞 Relato de Bugs

Encontrou algum erro na linguagem, na gramática ou no comportamento do compilador/interprete? Abra uma issue detalhando:

- O trecho de código utilizado.
- O comportamento esperado.
- O erro apresentado.

### 🧱 Contribuições de Código

1. Fork este repositório.
2. Crie uma branch com sua feature ou correção:  
   `git checkout -b minha-melhoria`
3. Faça suas alterações e dê commit:  
   `git commit -m "feat: adicionei suporte a tema escuro"`
4. Envie seu código:  
   `git push origin minha-melhoria`
5. Abra um pull request com uma descrição clara do que foi feito.

### 📚 Melhoria na Documentação

- Correções gramaticais.
- Explicações mais acessíveis.
- Exemplos adicionais de código com foco em inclusão.

---

A LumenScript é um projeto aberto e coletivo. Toda contribuição é bem-vinda — seja código, ideia, revisão ou teste!

Vamos juntos tornar a programação mais acessível para todos. 💙

---

## 📁 Arquivo da Gramática

A estrutura formal da **LumenScript** foi definida utilizando a notação **EBNF (Extended Backus-Naur Form)**. Essa gramática descreve precisamente como a linguagem é construída, permitindo a implementação de analisadores léxicos e sintáticos robustos.

A gramática completa está disponível no arquivo:

📄 [`gramatica_lumen.ebnf`](./gramatica_lumen.ebnf)

### 🎯 Destaques da Gramática

- Utilização de palavras-chave acessíveis e simbólicas, como `clarear`, `ecoar`, `sentir` e `ver`.
- Suporte para variáveis de diferentes tipos (`luz`, `forma`, `estado`), que correspondem a `número`, `texto` e `booleano`.
- Entrada e saída amigáveis: `sentir()` para ler dados e `ecoar(...)` para exibir informações.
- Blocos de controle intuitivos com `se`, `senao`, `enquanto`, e `visao`.
- Estrutura de instruções clara e legível mesmo para leitores com baixa visão, com pontuação mínima e sintaxe fluida.

---

## 🌟 Conclusão

A **LumenScript** é mais do que uma linguagem de programação — é uma iniciativa para aproximar o desenvolvimento de software de pessoas que enfrentam desafios visuais, tornando esse universo mais inclusivo, compreensível e acessível. 

Inspirada por princípios de legibilidade, contraste e simplicidade, a LumenScript quer ser uma ponte entre tecnologia e empatia, onde todos possam criar, inovar e se expressar através do código, sem barreiras.

Se você acredita que tecnologia deve ser para todos, a LumenScript te convida a escrever com luz, propósito e acessibilidade.

💡 **Programe com clareza. Programe com Lumen.**

---

## 📚 Exemplo de Código

```
inicio

    guardar nome em texto com "Carlos" ;
    guardar idade em numero com 17 ;

    exibir("Verificando idade...") ;

    quando (idade maior 18) 
    inicio
        exibir("Maior de idade.") ;
    fim
    senao 
    inicio
        exibir("Menor de idade.") ;
    fim

    enquanto (idade menor 18)
    inicio
        idade é idade mais 1 ;
        exibir(idade) ;
    fim

    exibir("Qual seu nome?") ;
    nome é perguntar() ;

    exibir("Olá,") ;
    exibir(nome) ;

fim
```