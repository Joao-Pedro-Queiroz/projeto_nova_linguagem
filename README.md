# 🌱 Projeto Nova Linguagem – AfetoLang

Bem-vindo ao repositório do **Projeto Nova Linguagem**, parte da disciplina de Linguagens e Paradígmas.

Aqui desenvolvemos a **AfetoLang**, uma linguagem de programação inclusiva, acolhedora e com foco em facilitar o aprendizado para qualquer pessoa, independentemente de sua bagagem técnica ou social.

---

## 💡 Motivação

Queremos quebrar as barreiras da linguagem tradicional de programação, que muitas vezes é construída com termos técnicos, em inglês e com uma estrutura pouco intuitiva.

A **AfetoLang** busca:

- Promover **inclusividade linguística**, usando palavras em português acessível.
- Reduzir o medo de quem está começando a programar.
- Estimular uma relação mais humana e empática com o código.

---

## 🧠 Características

- **Palavras-chave** em português, simples e fáceis de lembrar.
- Sintaxe inspirada na fala cotidiana.
- Suporte às estruturas básicas:
  - Declaração de variáveis com `guarde`
  - Condicionais com `se`, `entao` e `senão`
  - Loops com `enquanto`
  - Entrada e saída com `escute` e `mostre`

---

## 🔤 Estrutura da Linguagem (EBNF)

A gramática da AfetoLang foi especificada segundo o padrão **EBNF** e pode ser consultada no arquivo:

📄 [`gramatica.ebnf`](./gramatica.ebnf)

---

## 📚 Exemplo de Código

```afeto
{
    guarde nome como "Maria" ;
    guarde idade como 21 ;

    se (idade > 18) entao {
        mostre("Você é maior de idade.") ;
    } senão {
        mostre("Você é menor de idade.") ;
    }

    enquanto (idade < 25) {
        idade = idade + 1 ;
        mostre(idade) ;
    }

    mostre("Qual é o seu filme favorito?") ;
    guarde filme como escute() ;

    mostre("Você escolheu:") ;
    mostre(filme) ;
}
