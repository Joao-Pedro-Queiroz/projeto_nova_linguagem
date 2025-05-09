import sys
import re
from abc import ABC, abstractmethod
import os
import pyttsx3


class Code:
    def __init__(self):
        self.instructions = []

    def append(self, instruction):
        if isinstance(instruction, list):
            self.instructions.extend(instruction)
        else:
            self.instructions.append(instruction)

    def dump(self, input_filename="output.zig"):
        output_name = os.path.splitext(input_filename)[0] + ".ll"

        with open(output_name, "w") as f:
            f.write("; === LLVM IR Module ===\n")

            # === Global Constants ===
            f.write('@.int_print_fmt = private unnamed_addr constant [4 x i8] c"%d\\0A\\00"\n')
            f.write('@.int_read_fmt = private unnamed_addr constant [3 x i8] c"%d\\00"\n')
            f.write('@.str_read_fmt = private unnamed_addr constant [3 x i8] c"%s\\00"\n')
            f.write('@.newline = private unnamed_addr constant [2 x i8] c"\\0A\\00"\n')
            f.write('@.true_str = private constant [5 x i8] c"true\\00"\n')
            f.write('@.false_str = private constant [6 x i8] c"false\\00"\n')
            f.write('@.espeak_prefix = private unnamed_addr constant [9 x i8] c"espeak \\22\\00"\n')
            f.write('@.espeak_suffix = private unnamed_addr constant [2 x i8] c"\\22\\00"\n')
            f.write('\n')

            # === External Function Declarations ===
            f.write('declare i32 @printf(i8*, ...)\n')
            f.write('declare i32 @scanf(i8*, ...)\n')
            f.write('declare i8* @malloc(i64)\n')
            f.write('declare i8* @strcpy(i8*, i8*)\n')
            f.write('declare i8* @strcat(i8*, i8*)\n')
            f.write('declare i32 @system(i8*)\n')
            f.write('\n')

            # === Main Function ===
            f.write('define i32 @main() {\n')

            for instr in self.instructions:
                f.write("  " + instr + "\n")

            f.write("  ret i32 0\n")
            f.write("}\n")

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.tableoffset = {}
        self.offset = 0
        self.expecting_type = None

    def allocate(self, name, var_type):
        self.offset += 4
        self.tableoffset[name] = {"offset": self.offset, "type": var_type}
        return self.offset

    def get_offset(self, name):
        return self.tableoffset[name]["offset"]

    def declare(self, name, var_type):
        if name in self.table:
            raise Exception(f"Variable '{name}' already declared.")
        
        self.table[name] = (None, var_type)

    def set(self, name, value):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared.")
        
        _, expected_type = self.table[name]
        actual_type = value[1]

        if expected_type != actual_type:
            raise TypeError(f"Type mismatch in assignment to '{name}'. Expected '{expected_type}', got '{actual_type}'.")
        
        self.table[name] = value

    def get(self, name):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared.")
        
        value, _ = self.table[name]

        if value is None:
            raise Exception(f"Variable '{name}' used before assignment.")
        
        return self.table[name]  # (value, type)


class Node(ABC):
    current_id = 0

    @staticmethod
    def newId():
        Node.current_id += 1
        return Node.current_id

    def __init__(self, value, children: list):
        self.value = value
        self.children = children
        self.id = Node.newId()

    @abstractmethod
    def Evaluate(self, symbol_table):
        pass

    @abstractmethod
    def Generate(self, symbol_table):
        pass


class BinOp(Node):
    def __init__(self, value, left, right):
        super().__init__(value, [left, right])


    def Evaluate(self, symbol_table):
        left_value, left_type = self.children[0].Evaluate(symbol_table)
        right_value, right_type = self.children[1].Evaluate(symbol_table)

        if self.value in {"MAIS", "MENOS", "VEZES", "DIVIDIDO"}:
            if left_type != "NUMERO" or right_type != "NUMERO":
                raise TypeError(f"Operação aritmética requer operandos 'i32', mas recebeu '{left_type}' e '{right_type}'")
            
            if self.value == "MAIS":
                return (left_value + right_value, "NUMERO")
            elif self.value == "MENOS":
                return (left_value - right_value, "NUMERO")
            elif self.value == "VEZES":
                return (left_value * right_value, "NUMERO")
            elif self.value == "DIVIDIDO":
                if right_value == 0:
                    raise ZeroDivisionError("Erro: divisão por zero.")
                
                return (left_value // right_value, "NUMERO")
        
        elif self.value in {"E", "OU"}:
            if left_type != "BOOLEANO" or right_type != "BOOLEANO":
                raise TypeError(f"Operação lógica requer operandos 'bool', mas recebeu '{left_type}' e '{right_type}'")
            
            if self.value == "E":
                return (1 if left_value and right_value else 0, "BOOLEANO")
            elif self.value == "OU":
                return (1 if left_value or right_value else 0, "BOOLEANO")
        
        elif self.value in {"IGUAL", "MAIOR", "MENOR"}:
            if left_type != right_type:
                raise TypeError(f"Comparação requer operandos do mesmo tipo, mas recebeu '{left_type}' e '{right_type}'")
            
            if self.value == "IGUAL":
                return (1 if left_value == right_value else 0, "BOOLEANO")
            elif self.value == "MAIOR":
                return (1 if left_value > right_value else 0, "BOOLEANO")
            elif self.value == "MENOR":
                return (1 if left_value < right_value else 0, "BOOLEANO")
        
        elif self.value == "CONCATENA":
            if left_type == "BOOLEANO" and right_type == "BOOLEANO":
                return (str("true" if left_value else "false") + str("true" if right_value else "false"), "TEXTO")
            elif left_type == "BOOLEANO" and right_type != "BOOLEANO":
                return (str("true" if left_value else "false") + str(right_value), "TEXTO")
            elif right_type == "BOOLEANO" and left_type != "BOOLEANO":
                return (str(left_value) + str("true" if right_value else "false"), "TEXTO")
            else:
                return (str(left_value) + str(right_value), "TEXTO")

        else:
            raise ValueError(f"Operador binário desconhecido: {self.value}")
        
    def Generate(self, symbol_table):
        code = []

        right_code = self.children[1].Generate(symbol_table)
        left_code = self.children[0].Generate(symbol_table)

        code += right_code
        code += left_code

        left_result = f"%temp_{self.children[0].id}" if not isinstance(self.children[0], Identifier) else f"%{self.children[0].id}"
        right_result = f"%temp_{self.children[1].id}" if not isinstance(self.children[1], Identifier) else f"%{self.children[1].id}"

        result_var = f"%temp_{self.id}"

        if self.value == "MAIS":
            code.append(f"{result_var} = add i32 {left_result}, {right_result}")
        elif self.value == "MENOS":
            code.append(f"{result_var} = sub i32 {left_result}, {right_result}")
        elif self.value == "VEZES":
            code.append(f"{result_var} = mul i32 {left_result}, {right_result}")
        elif self.value == "DIVIDIDO":
            code.append(f"{result_var} = sdiv i32 {left_result}, {right_result}")
        elif self.value == "IGUAL":
            code.append(f"{result_var} = icmp eq i32 {left_result}, {right_result}")
        elif self.value == "MAIOR":
            code.append(f"{result_var} = icmp sgt i32 {left_result}, {right_result}")
        elif self.value == "MENOR":
            code.append(f"{result_var} = icmp slt i32 {left_result}, {right_result}")
        elif self.value == "E":
            code.append(f"{result_var} = and i1 {left_result}, {right_result}")
        elif self.value == "OU":
            code.append(f"{result_var} = or i1 {left_result}, {right_result}")
        elif self.value == "CONCATENA":
            malloc_size = 256
            malloc_var = f"%malloc_{self.id}"
            strcat_1 = f"%strcat1_{self.id}"
            strcat_2 = f"%strcat2_{self.id}"

            code.append(f"{malloc_var} = call i8* @malloc(i64 {malloc_size})")
            code.append(f"{strcat_1} = call i8* @strcat(i8* {malloc_var}, i8* {left_result})")
            code.append(f"{strcat_2} = call i8* @strcat(i8* {strcat_1}, i8* {right_result})")
            code.append(f"{result_var} = bitcast i8* {strcat_2} to i8*")
        else:
            raise Exception(f"Operador binário desconhecido: {self.value}")

        return code


class UnOp(Node):
    def __init__(self, value, child):
        super().__init__(value, [child])


    def Evaluate(self, symbol_table):
        value, val_type = self.children[0].Evaluate(symbol_table)

        if self.value in {"MAIS", "MENOS"}:
            if val_type != "NUMERO":
                raise TypeError(f"Operador unário '{self.value}' requer tipo 'i32', mas recebeu '{val_type}'")
            
            return ((+value if self.value == "MAIS" else -value), "NUMERO")

        elif self.value == "NAO":
            if val_type != "BOOLEANO":
                raise TypeError(f"Operador unário '!' requer tipo 'bool', mas recebeu '{val_type}'")
            
            return (1 if not value else 0, "BOOLEANO")
        
        else:
            raise ValueError(f"Operador unário desconhecido: {self.value}")
    
    def Generate(self, symbol_table):
        code = []

        child_code = self.children[0].Generate(symbol_table)
        code += child_code

        child_result = f"%temp_{self.children[0].id}" if not isinstance(self.children[0], Identifier) else f"%{self.children[0].id}"
        result_var = f"%temp_{self.id}"

        if self.value == "NAO":
            code.append(f"{result_var} = xor i1 {child_result}, true")
        elif self.value == "MENOS":
            code.append(f"{result_var} = sub i32 0, {child_result}")
        elif self.value == "MAIS":
            code.append(f"{result_var} = add i32 0, {child_result}")
        else:
            raise Exception(f"Operador unário desconhecido: {self.value}")

        return code


class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])


    def Evaluate(self, symbol_table):
         return (self.value, "NUMERO")
    
    def Generate(self, symbol_table):
        temp_var = f"temp_{self.id}"
        code = [f"%{temp_var} = add i32 0, {self.value}"]
        return code
    

class BoolVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self, symbol_table):
        return (1 if self.value == "true" else 0, "BOOLEANO")
    
    def Generate(self, symbol_table):
        temp_var = f"temp_{self.id}"
        val = "1" if self.value == "VERDADEIRO" else "0"
        code = [f"%{temp_var} = icmp eq i1 {val}, 1"]
        return code


class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self, symbol_table):
        return (self.value, "TEXTO")
    
    def Generate(self, symbol_table):
        temp_var = f"temp_{self.id}"
        string_constant = f"c\"{self.value}\\00\""
        code = [f"@{self.id} = private constant [{len(self.value) + 1} x i8] {string_constant}"]
        code.append(f"%{temp_var} = getelementptr inbounds [{len(self.value) + 1} x i8], [{len(self.value) + 1} x i8]* @{self.id}, i32 0, i32 0")
        return code


class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, [])


    def Evaluate(self, symbol_table):
        return symbol_table.get(self.value)
    
    def Generate(self, symbol_table):
        if symbol_table.get(self.value)[1] == "NUMERO" or symbol_table.get(self.value)[1] == "BOOLEANO":
            return [f"%{self.id} = load i32, i32* @{self.value}"]
        elif symbol_table.get(self.value)[1] == "TEXTO":
            return [f"%{self.id} = load i8*, i8** @{self.value}"]
        else:
            raise ValueError(f"Tipo de variável desconhecido para {self.value}")
    

class VarDeC(Node):
    def __init__(self, identifier, type, expression=None):
        super().__init__("GUARDAR", [identifier, type] + ([expression] if expression else []))


    def Evaluate(self, symbol_table):
        symbol_table.declare(self.children[0].value, self.children[1])

        if len(self.children) == 3:
            if self.children[1] != self.children[2].Evaluate(symbol_table)[1]:
                raise TypeError(f"Tipo de variável '{self.children[0].value}' não corresponde ao tipo da expressão.")
            
            value, type = self.children[2].Evaluate(symbol_table)
            symbol_table.set(self.children[0].value, (value, type))
            return (value, type)
        
        return (None, None)
    
    def Generate(self, symbol_table):
        identifier = self.children[0].value
        type_ = self.children[1]  # "NUMERO", "BOOLEANO", "TEXTO"
        code = []

        llvm_type = {
            "NUMERO": "i32",
            "BOOLEANO": "i32",
            "TEXTO": "i8*"
        }.get(type_)

        if llvm_type is None:
            raise ValueError(f"Tipo de variável desconhecido: {type_}")

        # Declara a variável globalmente (com valor neutro)
        if type_ == "TEXTO":
            code.append(f"@{identifier} = global {llvm_type} null")
        else:
            code.append(f"@{identifier} = global {llvm_type} 0")

        # Registra no symbol_table
        symbol_table.declare(identifier, type_)

        # Se há expressão de inicialização
        if len(self.children) == 3:
            symbol_table.expecting_type = type_
            expr_code = self.children[2].Generate(symbol_table)
            code += expr_code
            symbol_table.expecting_type = None

            expr_result = f"%temp_{self.children[2].id}" if not isinstance(self.children[2], Identifier) else f"%{self.children[2].id}"

            if type_ == "TEXTO":
                code.append(f"store {llvm_type} {expr_result}, {llvm_type}* @{identifier}")
            else:
                code.append(f"store i32 {expr_result}, i32* @{identifier}")

            symbol_table.set(identifier, ("init", type_))

        return code


class Assignment(Node):
    def __init__(self, identifier, expression):
        super().__init__("RECEBE", [identifier, expression])


    def Evaluate(self, symbol_table):
        value, type = self.children[1].Evaluate(symbol_table)
        symbol_table.set(self.children[0].value, (value, type))
        return (value, type)
    
    def Generate(self, symbol_table):
        code = []

        var_name = self.children[0].value
        var_type = symbol_table.get(var_name)[1]
        symbol_table.expecting_type = var_type

        # Gera o valor da expressão do lado direito
        expr_code = self.children[1].Generate(symbol_table)
        code += expr_code

        symbol_table.expecting_type = None

        # Resultado gerado (LLVM IR variable)
        expr_result = f"%temp_{self.children[1].id}" if not isinstance(self.children[1], Identifier) else f"%{self.children[1].id}"

        # Store adequado ao tipo
        if var_type == "NUMERO" or var_type == "BOOLEANO":
            code.append(f"store i32 {expr_result}, i32* @{var_name}")
        elif var_type == "TEXTO":
            code.append(f"store i8* {expr_result}, i8** @{var_name}")
        else:
            raise ValueError(f"Tipo de variável desconhecido para atribuição: {var_type}")
        
        symbol_table.set(var_name, ("init", var_type))

        return code


class Print(Node):
    def __init__(self, expression):
        super().__init__("EXIBIR", [expression])


    def Evaluate(self, symbol_table):
        value = self.children[0].Evaluate(symbol_table)
        if value[1] == "BOOLEANO":
            print("true" if value[0] else "false")
        else:
            print(value[0])
        return (value, None)
    
    def Generate(self, symbol_table):
        code = self.children[0].Generate(symbol_table)
        
        child = self.children[0]
        result_var = f"%temp_{child.id}" if not isinstance(child, Identifier) else f"%{child.id}"

        # Descobrir tipo
        if isinstance(child, Identifier):
            val_type = symbol_table.get(child.value)[1]
        else:
            _, val_type = child.Evaluate(symbol_table)

        if val_type == "NUMERO":
            format_str = "@.int_print_fmt"
            code.append(f"%call_{self.id} = call i32 (i8*, ...) @printf(i8* {format_str}, i32 {result_var})")
        elif val_type == "BOOLEANO":
            # Converte booleano (i1) em string com ponteiro condicional
            true_str = "@.true_str"
            false_str = "@.false_str"
            bool_ptr = f"%bool_ptr_{self.id}"
            code.append(f"{bool_ptr} = select i1 {result_var}, i8* {true_str}, i8* {false_str}")
            code.append(f"%call_{self.id} = call i32 (i8*, ...) @printf(i8* %bool_ptr_{self.id})")
        elif val_type == "TEXTO":
            code.append(f"%call_{self.id} = call i32 (i8*, ...) @printf(i8* {result_var})")
        else:
            raise Exception(f"Tipo inválido em Print: {val_type}")
        
        return code

class Falar(Node):
    def __init__(self, expression):
        super().__init__("FALAR", [expression])
        self.engine = pyttsx3.init()
        self.engine.setProperty("volume", 0.7)

    def Evaluate(self, symbol_table):
        value = self.children[0].Evaluate(symbol_table)

        if isinstance(value, tuple):
            value = value[0]

        self.engine.say(str(value))
        self.engine.runAndWait()
        
        return (value, None)

    def Generate(self, symbol_table):
        code = []

        expr_code = self.children[0].Generate(symbol_table)
        code += expr_code

        value_ptr = f"%temp_{self.children[0].id}" if not isinstance(self.children[0], Identifier) else f"%{self.children[0].id}"
        casted_ptr = f"%cast_{self.id}"
        cmd_ptr = f"%cmd_{self.id}"
        cmd_concat = f"%cmd_concat_{self.id}"
        system_call = f"%system_call_{self.id}"

        # Alocar string "espeak \""
        prefix = f"@.espeak_prefix = private unnamed_addr constant [9 x i8] c\"espeak \\22\\00\""
        suffix = f"@.espeak_suffix = private unnamed_addr constant [2 x i8] c\"\\22\\00\""

        # Note: essas constantes devem estar no cabeçalho do programa

        code.append(f"{casted_ptr} = bitcast i8* {value_ptr} to i8*")
        
        # Aloca um buffer para montar o comando: "espeak \"<mensagem>\""
        code.append(f"{cmd_ptr} = call i8* @malloc(i64 256)")
        code.append(f"%tmp1_{self.id} = call i8* @strcpy(i8* {cmd_ptr}, i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.espeak_prefix, i32 0, i32 0))")
        code.append(f"%tmp2_{self.id} = call i8* @strcat(i8* %tmp1_{self.id}, i8* {casted_ptr})")
        code.append(f"%tmp3_{self.id} = call i8* @strcat(i8* %tmp2_{self.id}, i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.espeak_suffix, i32 0, i32 0))")

        # system(cmd)
        code.append(f"{system_call} = call i32 @system(i8* {cmd_ptr})")

        return code
    
    
class If(Node):
    def __init__(self, condition, then_branch, else_branch=None):
        super().__init__("QUANDO", [condition, then_branch] + ([else_branch] if else_branch else []))

    def Evaluate(self, symbol_table):
        condition_value, condition_type = self.children[0].Evaluate(symbol_table)
        
        if condition_type != "BOOLEANO":
            raise TypeError(f"Condição do 'QUANDO' deve ser do tipo 'BOOLEANO', mas recebeu '{condition_type}'")
        
        if condition_value:
            return self.children[1].Evaluate(symbol_table)
        elif len(self.children) > 2:
            return self.children[2].Evaluate(symbol_table)
        
    def Generate(self, symbol_table):
        code = []

        cond_code = self.children[0].Generate(symbol_table)
        code += cond_code

        cond_result = f"%temp_{self.children[0].id}"
        then_label = f"then_{self.id}"
        else_label = f"else_{self.id}"
        end_label = f"endif_{self.id}"

        # Branch condicional
        if len(self.children) == 3:
            code.append(f"br i1 {cond_result}, label %{then_label}, label %{else_label}")

            # THEN branch
            code.append(f"{then_label}:")
            then_code = self.children[1].Generate(symbol_table)
            code += then_code
            code.append(f"br label %{end_label}")

            # ELSE branch
            code.append(f"{else_label}:")
            else_code = self.children[2].Generate(symbol_table)
            code += else_code
            code.append(f"br label %{end_label}")
        else:
            code.append(f"br i1 {cond_result}, label %{then_label}, label %{end_label}")

            # THEN only
            code.append(f"{then_label}:")
            then_code = self.children[1].Generate(symbol_table)
            code += then_code
            code.append(f"br label %{end_label}")

        # Fim
        code.append(f"{end_label}:")

        return code
    

class While(Node):
    def __init__(self, condition, block):
        super().__init__("ENQUANTO", [condition, block])

    def Evaluate(self, symbol_table):
        condition_value, condition_type = self.children[0].Evaluate(symbol_table)

        if condition_type != "BOOLEANO":
            raise TypeError(f"Condição do 'ENQUANTO' deve ser do tipo 'BOOLEANO', mas recebeu '{condition_type}'")
        
        result = None

        while condition_value:
            result = self.children[1].Evaluate(symbol_table)
            condition_value, _ = self.children[0].Evaluate(symbol_table)

        return result
    
    def Generate(self, symbol_table):
        code = []

        loop_id = self.id
        cond_label = f"loop_cond_{loop_id}"
        body_label = f"loop_body_{loop_id}"
        end_label = f"loop_end_{loop_id}"

        # Começo com o salto para a verificação da condição
        code.append(f"br label %{cond_label}")

        # Bloco da condição
        code.append(f"{cond_label}:")
        cond_code = self.children[0].Generate(symbol_table)
        code += cond_code
        cond_result = f"%temp_{self.children[0].id}"
        code.append(f"br i1 {cond_result}, label %{body_label}, label %{end_label}")

        # Bloco do corpo do laço
        code.append(f"{body_label}:")
        body_code = self.children[1].Generate(symbol_table)
        code += body_code
        code.append(f"br label %{cond_label}")  # volta para verificar a condição

        # Fim do laço
        code.append(f"{end_label}:")

        return code


class Block(Node):
    def __init__(self, statements):
        super().__init__("block", statements)


    def Evaluate(self, symbol_table):
        for statement in self.children:
            statement.Evaluate(symbol_table)

        return (None, None)
    
    def Generate(self, symbol_table):
        code = []

        for stmt in self.children:
            code += stmt.Generate(symbol_table)

        return code


class Read(Node):
    def __init__(self):
        super().__init__("PERGUNTAR", [])

    def Evaluate(self, symbol_table):
        value = input()

        try:
            if value.isdigit():
                return (int(value), "NUMERO")
            else:
                return (value, "TEXTO")
        except ValueError:
            raise ValueError(f"Entrada inválida: {value}. Esperado um número inteiro.")
        
    def Generate(self, symbol_table):
        code = []
        temp_var = f"%temp_{self.id}"

        # Buffer para leitura de string (estático, tamanho fixo para simplificação)
        buffer_name = f"%buf_{self.id}"
        str_format = "@.str_read_fmt"   # definido no cabeçalho como: `@.str_read_fmt = private constant [3 x i8] c\"%s\\00\"`
        int_format = "@.int_read_fmt"   # definido no cabeçalho como: `@.int_read_fmt = private constant [3 x i8] c\"%d\\00\"`

        # Tentativa de inferência de tipo, como no Evaluate (assumiremos sempre texto se for usado de forma independente)
        read_type = symbol_table.expecting_type if hasattr(symbol_table, "expecting_type") else "TEXTO"

        if read_type == "NUMERO":
            code.append(f"{temp_var}_ptr = alloca i32")
            code.append(f"%call_scanf_{self.id} = call i32 (i8*, ...) @scanf(i8* {int_format}, i32* {temp_var}_ptr)")
            code.append(f"{temp_var} = load i32, i32* {temp_var}_ptr")
        elif read_type == "TEXTO":
            code.append(f"{buffer_name} = alloca [256 x i8]")
            code.append(f"%gep_{self.id} = getelementptr inbounds [256 x i8], [256 x i8]* {buffer_name}, i32 0, i32 0")
            code.append(f"%call_scanf_{self.id} = call i32 (i8*, ...) @scanf(i8* {str_format}, i8* %gep_{self.id})")
            code.append(f"{temp_var} = add i8* %gep_{self.id}, 0")  # só alias para retorno
        else:
            raise Exception("Tipo de leitura não suportado")

        return code


class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])


    def Evaluate(self, symbol_table):
        return (None, None)
    
    def Generate(self, symbol_table):
        return []


class PrePro:
    @staticmethod
    def filter(code: str):
        return re.sub(r'INFORME:.*', '', code).strip()


class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, source: str, position: int, next: Token):
        self.source = source
        self.position = position
        self.next = next
        self.keywords = {
            "INICIO": "INICIO", "FIM": "FIM", "RECEBE": "RECEBE", "EXIBIR": "EXIBIR", "FALAR": "FALAR", 
            "GUARDAR": "GUARDAR","COMO": "COMO", "COM": "COM", "QUANDO": "QUANDO", "SENAO": "SENAO",
            "ENQUANTO": "ENQUANTO", "OU": "OU", "E": "E", "IGUAL": "IGUAL", "MAIOR": "MAIOR", "MENOR": "MENOR",
            "MAIS": "MAIS", "MENOS": "MENOS", "CONCATENA": "CONCATENA", "VEZES": "VEZES", "DIVIDIDO": "DIVIDIDO",
            "NAO": "NAO", "PERGUNTAR": "PERGUNTAR", "VERDADEIRO": "BOOL", "FALSO": "BOOL", "NUMERO": "TYPE_NUMERO",
            "BOOLEANO": "TYPE_BOOL", "TEXTO": "TYPE_TEXTO"
            }
    
    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] in {' ', '\n', '\r', '\t'}:
            self.position += 1

        if self.position < len(self.source):
            char = self.source[self.position]

            if char.isdigit():
                num = ''
                
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    num += self.source[self.position]
                    self.position += 1
                
                if self.position < len(self.source) and self.source[self.position].isalpha():
                    raise ValueError(f"Erro de sintaxe: número seguido de letra sem separação: {num}{self.source[self.position]}")

                self.next = Token("NUMERO", int(num))
                return
            elif char.isalpha():
                ident = ''

                while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                    ident += self.source[self.position]
                    self.position += 1

                token_type = self.keywords.get(ident, "IDENTIFICADOR")
                
                self.next = Token(token_type, ident)
                return
            elif char == '"':
                self.position += 1
                string_val = ''

                while self.position < len(self.source) and self.source[self.position] != '"':
                    string_val += self.source[self.position]
                    self.position += 1

                if self.position >= len(self.source) or self.source[self.position] != '"':
                    raise ValueError("String não fechada corretamente com aspas.")

                self.position += 1
                self.next = Token("TEXTO", string_val)
                return
            elif char == '(': 
                self.next = Token("ABREPAR", char)
            elif char == ')':
                self.next = Token("FECHAPAR", char)
            elif char == ';': 
                self.next = Token("PONTOVIRG", char)
            else:
                raise ValueError("Caractere inválido")
            
            self.position += 1
        else:
            self.next = Token("EOF", None)


class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer


    def parseFactor(self):
        token = self.tokenizer.next

        if token.type == "NUMERO":
            self.tokenizer.selectNext()
            return IntVal(token.value)
        elif token.type == "IDENTIFICADOR":
            self.tokenizer.selectNext()
            return Identifier(token.value)
        elif token.type == "TEXTO":
            self.tokenizer.selectNext()
            return StrVal(token.value)
        elif token.type == "BOOL":
            self.tokenizer.selectNext()
            return BoolVal(token.value)
        elif token.type == "MAIS":
            self.tokenizer.selectNext()
            return UnOp("MAIS", self.parseFactor())
        elif token.type == "MENOS":
            self.tokenizer.selectNext()
            return UnOp("MENOS", self.parseFactor())
        elif token.type == "NAO":
            self.tokenizer.selectNext()
            return UnOp("NAO", self.parseFactor())
        elif token.type == "ABREPAR":
            self.tokenizer.selectNext()
            result = self.parseOrExpression()

            if self.tokenizer.next.type != "FECHAPAR":
                raise ValueError("Parênteses desbalanceados")
            
            self.tokenizer.selectNext()
            return result
        elif self.tokenizer.next.type == "PERGUNTAR":
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type != "ABREPAR":
                raise ValueError("Parênteses esperados após 'reader'")
            
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type != "FECHAPAR":
                raise ValueError("Parênteses de fechamento esperados após 'reader()'")
            
            self.tokenizer.selectNext()
            return Read()
        else:
            raise ValueError(f"Token inesperado: {token.type}")

    
    def parseTerm(self):
        left = self.parseFactor()

        while self.tokenizer.next.type in ("VEZES", "DIVIDIDO"):
            operador = self.tokenizer.next.type
            self.tokenizer.selectNext()

            right = self.parseFactor()

            if operador == "VEZES":
                left = BinOp("VEZES", left, right)
            elif operador == "DIVIDIDO":
                left = BinOp("DIVIDIDO", left, right)

        return left  

    
    def parseExpression(self):
        left = self.parseTerm()

        while self.tokenizer.next.type in ("MAIS", "MENOS", "CONCATENA"):
            operador = self.tokenizer.next.type
            self.tokenizer.selectNext()

            right = self.parseTerm()

            if operador == "MAIS":
                left = BinOp("MAIS", left, right)
            elif operador == "MENOS":
                left = BinOp("MENOS", left, right)
            elif operador == "CONCATENA":
                left = BinOp("CONCATENA", left, right)

        return left
    
    
    def parseRelationalExpression(self):
        left = self.parseExpression()

        while self.tokenizer.next.type in ("IGUAL", "MAIOR", "MENOR"):
            operador = self.tokenizer.next.type
            self.tokenizer.selectNext()

            right = self.parseExpression()

            if operador == "IGUAL":
                left = BinOp("IGUAL", left, right)
            elif operador == "MAIOR":
                left = BinOp("MENOR", left, right)
            elif operador == "MENOR":
                left = BinOp("MENOR", left, right)

        return left
    

    def parseAndExpression(self):
        left = self.parseRelationalExpression()

        while self.tokenizer.next.type == "E":
            self.tokenizer.selectNext()

            right = self.parseRelationalExpression()

            left = BinOp("E", left, right)

        return left
    

    def parseOrExpression(self):
        left = self.parseAndExpression()

        while self.tokenizer.next.type == "OU":
            self.tokenizer.selectNext()
            right = self.parseAndExpression()

            left = BinOp("OU", left, right)

        return left      
    

    def parseStatement(self):
        if self.tokenizer.next.type == "PONTOVIRG":
            self.tokenizer.selectNext() 
            return NoOp()
    
        if self.tokenizer.next.type == "IDENTIFICADOR":
            identifier = Identifier(self.tokenizer.next.value)
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "RECEBE":
                self.tokenizer.selectNext()
                expr = self.parseOrExpression()

                if self.tokenizer.next.type != "PONTOVIRG":
                    raise ValueError("Ponto e vírgula esperado")
                
                self.tokenizer.selectNext()
                return Assignment(identifier, expr)
        elif self.tokenizer.next.type == "EXIBIR":
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type != "ABREPAR":
                raise ValueError("Parênteses esperados após 'print'")
            
            self.tokenizer.selectNext()
            expr = self.parseOrExpression()
            
            if self.tokenizer.next.type != "FECHAPAR":
                raise ValueError("Parênteses fechando esperados após condição de 'print'")
            
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "PONTOVIRG":
                raise ValueError("Ponto e vírgula esperado")

            self.tokenizer.selectNext()
            return Print(expr)
        elif self.tokenizer.next.type == "FALAR":
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type != "ABREPAR":
                raise ValueError("Parênteses esperados após 'print'")
            
            self.tokenizer.selectNext()
            expr = self.parseOrExpression()
            
            if self.tokenizer.next.type != "FECHAPAR":
                raise ValueError("Parênteses fechando esperados após condição de 'print'")
            
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "PONTOVIRG":
                raise ValueError("Ponto e vírgula esperado")

            self.tokenizer.selectNext()
            return Falar(expr)
        elif self.tokenizer.next.type == "GUARDAR":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "IDENTIFICADOR":
                raise ValueError("Identificador esperado após 'var'")
            
            identifier = Identifier(self.tokenizer.next.value)
            self.tokenizer.selectNext()

            if self.tokenizer.next.type != "COMO":
                raise ValueError("Dois pontos esperados após identificador")
            
            self.tokenizer.selectNext()
            var_type = self.tokenizer.next.value

            if var_type not in {"NUMERO", "BOOLEANO", "TEXTO"}:
                raise ValueError(f"Tipo inválido: {var_type}. Esperado 'i32', 'bool' ou 'str'")
            
            self.tokenizer.selectNext()
            expression = None

            if self.tokenizer.next.type == "COM":
                self.tokenizer.selectNext()
                expression = self.parseOrExpression()

            if self.tokenizer.next.type != "PONTOVIRG":
                raise ValueError("Ponto e vírgula esperado")
            
            return VarDeC(identifier, var_type, expression)
        elif self.tokenizer.next.type == "QUANDO":
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type != "ABREPAR":
                raise ValueError("Parênteses esperados após 'if'")
            
            self.tokenizer.selectNext()
            condition = self.parseOrExpression()
            
            if self.tokenizer.next.type != "FECHAPAR":
                raise ValueError("Parênteses fechando esperados após condição de 'if'")
            
            self.tokenizer.selectNext()
            then_branch = self.parseBlock()
    
            else_branch = None
            
            if self.tokenizer.next.type == "SENAO":
                self.tokenizer.selectNext()
                else_branch = self.parseBlock()
            
            return If(condition, then_branch, else_branch)
        elif self.tokenizer.next.type == "ENQUANTO":
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.type != "ABREPAR":
                raise ValueError("Parênteses esperados após 'while'")
            
            self.tokenizer.selectNext()
            condition = self.parseOrExpression()
            
            if self.tokenizer.next.type != "FECHAPAR":
                raise ValueError("Parênteses fechando esperados após condição de 'while'")
            
            self.tokenizer.selectNext()
            block = self.parseBlock()
            
            return While(condition, block)
        else:
            raise ValueError(f"Token inesperado: {self.tokenizer.next.type}")

        return NoOp()
    

    def parseBlock(self):
        statements = []

        if self.tokenizer.next.type == "INICIO":
            self.tokenizer.selectNext()

            while self.tokenizer.next.type != "FIM":
                if self.tokenizer.next.type == "EOF":
                     raise ValueError("Erro de sintaxe: bloco não fechado corretamente")

                statements.append(self.parseStatement())

            self.tokenizer.selectNext()
        else:
            raise ValueError("Chave esperada para início de bloco")

        return Block(statements)
    

    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code, 0, None)
        tokenizer.selectNext()
        parser = Parser(tokenizer)
        root = parser.parseBlock()

        if tokenizer.next.type != "EOF":
            raise ValueError("Erro: expressão não consumiu todos os tokens. Verifique a sintaxe.")
        
        symbol_table = SymbolTable()
        root.Evaluate(symbol_table)

    @staticmethod
    def geracodigo(code, filename):
        tokenizer = Tokenizer(code, 0, None)
        tokenizer.selectNext()
        parser = Parser(tokenizer)
        root = parser.parseBlock()

        if tokenizer.next.type != "EOF":
            raise ValueError("Erro: expressão não consumiu todos os tokens. Verifique a sintaxe.")

        symbol_table = SymbolTable()
        instructions = root.Generate(symbol_table)
        code_generator = Code()

        code_generator.append(instructions)
        code_generator.dump(filename)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Uso incorreto do programa.\nUse (exemplo): python main.py 'arquivo.zig'")

    arquivo = sys.argv[1]

    if not arquivo.endswith('.lumen'):
        raise ValueError("O arquivo deve ter a extensão '.lumen'.")

    with open(arquivo, 'r') as file:
        expressao = file.read()

    expressao = PrePro.filter(expressao)
    Parser.geracodigo(expressao, arquivo)