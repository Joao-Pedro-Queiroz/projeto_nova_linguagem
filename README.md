# 🎭 Projeto Nova Linguagem – TeatroLang

Bem-vindo ao repositório da **TeatroLang**, uma linguagem de programação que transforma a lógica de programação em uma verdadeira peça teatral! 🎬✨

---

## 🎯 Objetivo

A **TeatroLang** nasce com a proposta de transformar o processo de programação em uma experiência criativa e envolvente, utilizando a metáfora do teatro para estruturar o código. 

Cada programa é como uma peça: dividido em atos, cenas e falas — com atores desempenhando ações em um palco digital.

---

## 🎭 Conceito

Inspirada em roteiros teatrais, **TeatroLang** substitui termos técnicos por expressões artísticas, tornando o código mais narrativo e lúdico. Aqui, programar é escrever uma peça!

- **Ato** representa o bloco principal do programa.
- **Cena** representa um bloco de ações (como condicionais e laços).
- **Atores** são os identificadores/variáveis.
- **Fala** representa a saída no console.
- **Improviso** representa entrada de dados.
- **Diretor** faz atribuições.
- **Palco** é o local de execução (blocos de código).
- **Script** é a lógica, expressões e comparações.

---

## 🧠 Principais Palavras-Chave

| Palavra-chave    | Significado                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `ato`            | Define o início de uma peça/programa. É o ponto de entrada do código.       |
| `cena`           | Representa o bloco de ações que acontece dentro de uma estrutura de controle. |
| `se (...) entao` | Define uma condição. Se for verdadeira, executa a `cena` correspondente.    |
| `senao`          | Bloco alternativo, executado quando a condição do `se` for falsa.           |
| `enquanto (...)` | Define uma repetição, executando a `cena` enquanto a condição for verdadeira.|
| `diretor`        | Declara uma variável e atribui seu valor inicial — como o papel de um ator. |
| `como`           | Palavra que faz a atribuição de valor.                                     |
| `ator`           | Declara um novo ator (variável) e captura um valor com `improviso()`.       |
| `improviso()`    | Entrada de dados — o ator responde espontaneamente no palco.                |
| `fale(...)`      | Exibe uma fala no console, como uma linha de um roteiro.                    |
| `;`              | Delimita o fim de uma instrução.                                            |
| `{ ... }`        | Define um bloco de execução, ou seja, o que acontece no palco.              |


---

## 🔤 Estrutura Gramatical (EBNF)

A linguagem **TeatroLang** foi definida formalmente utilizando a **Extended Backus-Naur Form (EBNF)**, garantindo clareza e consistência na sua estrutura sintática.

A gramática completa está disponível no arquivo:

📄 [`gramatica_teatro.ebnf`](./gramatica_teatro.ebnf)

Essa gramática define as regras formais da linguagem, com destaque para:

- O uso de `"ato"` como ponto de partida do programa.
- A estrutura de blocos teatrais delimitados por `{}`.
- Elementos dramáticos como `cena`, `fala`, `ator`, `improviso`, e `diretor`.
- Expressões condicionais e matemáticas com sintaxe acessível.

A estrutura foi pensada para ser interpretável como um roteiro, tornando o código mais expressivo e convidativo, especialmente para iniciantes ou pessoas com afinidade com artes e comunicação.

---

## 🚀 Por que TeatroLang?

A **TeatroLang** foi criada com a intenção de oferecer uma linguagem de programação que seja tanto acessível quanto criativa. Ao invés de seguir a tradição de linguagens de programação tecnicamente complexas e distantes da realidade de muitas pessoas, a **TeatroLang** adota uma abordagem mais humanizada, focada na expressão e na narrativa. Algumas das razões para criar esta linguagem incluem:

- **Acessibilidade**: A sintaxe foi desenvolvida para ser próxima da linguagem natural e fácil de entender, permitindo que qualquer pessoa, mesmo sem conhecimento prévio em programação, consiga compreender e criar código.
  
- **Criatividade e Arte**: Inspirada no universo do teatro, a **TeatroLang** permite que programadores criem scripts de maneira artística, utilizando elementos como `ator`, `cena`, `fala`, e `improviso`. A ideia é transformar a programação em um processo criativo, onde a narrativa é um componente central.
  
- **Educação e Inclusão**: O design da linguagem busca quebrar as barreiras do ensino de programação, tornando-o mais acessível e convidativo para iniciantes, especialmente aqueles com pouca experiência com linguagens de programação convencionais.

- **Promoção de Diversidade**: A linguagem visa ser inclusiva, utilizando palavras e conceitos familiares a todos, independentemente da área de conhecimento técnico. Além disso, ela tem um foco na promoção da expressão pessoal dentro do mundo da programação.

Com a **TeatroLang**, a programação se transforma em um ato criativo e colaborativo, onde o código é uma peça de teatro e cada programador é um artista construindo cenas de um grande espetáculo.

---

## 📚 Exemplo de Código

```teatro
ato principal {
    diretor nome como "Julieta" ;
    diretor idade como 16 ;

    fale("Verificando idade da personagem...") ;

    cena (idade >= 18) entao {
        fale("Você já pode sair de casa.") ;
    } senao {
        fale("Você ainda é menor de idade.") ;
    }

    cena enquanto (idade < 18) {
        diretor idade como idade + 1;
        fale(idade) ;
    }

    fale("Qual é o nome do próximo ator?") ;
    ator novo_ator como improviso() ;

    fale("Bem-vindo ao palco,") ;
    fale(novo_ator) ;
}