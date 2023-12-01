import time
import os
import enum


class Opcode(enum.Enum):
    inp = enum.auto()
    add = enum.auto()
    mul = enum.auto()
    div = enum.auto()
    mod = enum.auto()
    eql = enum.auto()


class OperandType(enum.Enum):
    Number = enum.auto()
    Variable = enum.auto()
    Empty = enum.auto()


class Operand:
    def __init__(self, operand_type: OperandType, value: int):
        assert(type(value) == int)
        self.operand_type: OperandType = operand_type
        self.value: int = value

    def __repr__(self):
        if self.operand_type == OperandType.Number:
            return f"{self.value}"
        elif self.operand_type == OperandType.Variable:
            return f"{Var.REVERSE_MAPPINGS[self.value]}"
        elif self.operand_type == OperandType.Empty:
            return "_"


class Var:
    w = 0
    x = 1
    y = 2
    z = 3

    MAPPINGS = {"w": w, "x": x, "y": y, "z": z}
    REVERSE_MAPPINGS = {w: "w", x: "x", y: "y", z: "z"}

    @staticmethod
    def from_str(string) -> int:
        # We'll just allow whatever exception occurs here;
        # these should already be validated anyway
        return Var.MAPPINGS[string]


class Instruction:
    def __init__(self, opcode: Opcode, op1: Operand, op2: Operand):
        self.opcode: Opcode = opcode
        self.op1: Operand = op1
        self.op2: Operand = op2
        # print(f"Created Instruction: {self}")

    def __repr__(self):
        return f"{self.opcode} {self.op1} {self.op2}"


class ALU:
    def __init__(self):
        self.vars = [0 for _ in range(4)]

    def reset(self, w: int = 0, x: int = 0, y: int = 0, z: int = 0):
        self.vars = [w, x, y, z]

    def run_instruction(self, instr: Instruction, in_value: int = 0):
        # print("...")
        if instr.opcode == Opcode.inp:
            self.vars[instr.op1.value] = in_value
        else:
            op2 = instr.op2.value if instr.op2.operand_type == OperandType.Number else self.vars[instr.op2.value]
            if instr.opcode == Opcode.add:
                self.vars[instr.op1.value] += op2
            elif instr.opcode == Opcode.mul:
                self.vars[instr.op1.value] *= op2
            elif instr.opcode == Opcode.div:
                self.vars[instr.op1.value] //= op2
            elif instr.opcode == Opcode.mod:
                self.vars[instr.op1.value] %= op2
            elif instr.opcode == Opcode.eql:
                self.vars[instr.op1.value] = int(self.vars[instr.op1.value] == op2)

    def run_instructions(self, instructions: list[Instruction], in_value: int = 0):
        for instr in instructions:
            try:
                self.run_instruction(instr, in_value)
                assert (instr.op1.operand_type == OperandType.Variable)
                # print(f"Running: {instr.opcode} {instr.op1.value} {instr.op2.operand_type} {instr.op2.value}")
            except RuntimeError as e:
                print("STOPPING.")
                # print(e)
                break


class Unknown:
    pass


class SpeculatorALU:
    def __init__(self):
        self.vars: list[list[int] or Unknown] = [0 for _ in range(4)]

    def reset(self, w: int = 0, x: int = 0, y: int = 0, z: int = 0):
        self.vars = [w, x, y, z]

    def run_instruction(self, instr: Instruction, in_value: int = 0):
        # print("...")
        if instr.opcode == Opcode.inp:
            self.vars[instr.op1.value] = in_value
        else:
            op2 = instr.op2.value if instr.op2.operand_type == OperandType.Number else self.vars[instr.op2.value]
            if instr.opcode == Opcode.add:
                self.vars[instr.op1.value] += op2
            elif instr.opcode == Opcode.mul:
                self.vars[instr.op1.value] *= op2
            elif instr.opcode == Opcode.div:
                self.vars[instr.op1.value] //= op2
            elif instr.opcode == Opcode.mod:
                self.vars[instr.op1.value] %= op2
            elif instr.opcode == Opcode.eql:
                self.vars[instr.op1.value] = int(self.vars[instr.op1.value] == op2)

    def run_instructions(self, instructions: list[Instruction], in_value: int = 0):
        for instr in instructions:
            try:
                self.run_instruction(instr, in_value)
                assert (instr.op1.operand_type == OperandType.Variable)
                # print(f"Running: {instr.opcode} {instr.op1.value} {instr.op2.operand_type} {instr.op2.value}")
            except RuntimeError as e:
                print("STOPPING.")
                # print(e)
                break

    def speculate(self, instructions: list[Instruction]):
        self.vars[Var.w] = [i for i in range(0, 10)]
        self.vars[Var.z] = Unknown()
        for instr in instructions:
            op1 = instr.op1.value
            if instr.opcode == Opcode.inp:
                assert instr.op1.value == Var.w
            else:
                op2 = instr.op2.value if instr.op2.operand_type == OperandType.Number else self.vars[instr.op2.value]
                if type(op2) == list and len(op2) == 1:
                    op2 = op2[0]
                if instr.opcode == Opcode.add:
                    if type(op2) == list or type(op2) == Unknown or type(self.vars[op1]) == Unknown:
                        self.vars[instr.op1.value] = Unknown()
                    elif type(op2) == int:
                        self.vars[instr.op1.value] = [i + op2 for i in self.vars[instr.op1.value]]
                elif instr.opcode == Opcode.mul:
                    if op2 == 0 or self.vars[op1] == [0]:
                        self.vars[op1] = [0]
                    elif type(op2) == list or type(op2) == Unknown or type(self.vars[op1]) == Unknown:
                        self.vars[op1] = Unknown()
                    elif type(op2) == int:
                        self.vars[op1] = [i * op2 for i in self.vars[op1]]
                elif instr.opcode == Opcode.div:
                    if type(op2) == list or type(op2) == Unknown or type(self.vars[op1]) == Unknown:
                        self.vars[op1] = Unknown()
                    elif type(op2) == int:
                        self.vars[op1] = [i / op2 for i in self.vars[op1]]
                elif instr.opcode == Opcode.mod:
                    if type(op2) == list or type(op2) == Unknown:
                        self.vars[op1] = Unknown()
                    elif type(op2) == int:
                        self.vars[op1] = [i for i in range(0, op2)]


def parse_input(filename: str) -> list[list[Instruction]]:
    VALID_VARS = {"w", "x", "y", "z"}

    def validate_a(a: str):
        if a in VALID_VARS:
            return Operand(OperandType.Variable, Var.from_str(a))
        print(f"Is {a} in {VALID_VARS}?: {a in VALID_VARS}")
        raise RuntimeError(f"Bad input: invalid 'a' operand: {a}")

    def validate_b(b: str):
        if b in VALID_VARS:
            return Operand(OperandType.Variable, Var.from_str(b))
        try:
            return Operand(OperandType.Number, int(b))
        except ValueError:
            raise RuntimeError(f"Bad input: invalid 'b' operand: {b}")

    instructions = []
    current = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip().split(" ")
            if line[0] == "inp":
                assert len(line) == 2, "This opcode requires 1 operand"
                if len(current) > 0:
                    instructions.append(current)
                    current = []
                a: Operand = validate_a(line[1])
                current.append(Instruction(Opcode.inp, a, Operand(OperandType.Empty, 0)))
            else:
                assert len(line) == 3, "This opcode requires 2 operands"
                a: Operand = validate_a(line[1])
                b: Operand = validate_b(line[2])
                if line[0] == "add":
                    current.append(Instruction(Opcode.add, a, b))
                elif line[0] == "mul":
                    current.append(Instruction(Opcode.mul, a, b))
                elif line[0] == "div":
                    current.append(Instruction(Opcode.div, a, b))
                elif line[0] == "mod":
                    current.append(Instruction(Opcode.mod, a, b))
                elif line[0] == "eql":
                    current.append(Instruction(Opcode.eql, a, b))
                else:
                    raise RuntimeError("Bad input: invalid opcode")
        if len(current) > 0:
            instructions.append(current)
        return instructions


def run_instr_level(max_depth: int, level: int, instructions, alu):
    store = alu.vars.copy()
    for i in range(1, 10):
        alu.run_instructions(instructions[level], i)
        print(f"{'  ' * level} input {i} -> {alu.vars}")
        if level < max_depth:
            run_instr_level(max_depth, level + 1, instructions, alu)
        alu.reset(store[0], store[1], store[2], store[3])


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    instructions = parse_input(input_filename)
    alu = ALU()
    # print(instructions)
    # print(len(instructions))
    '''for i in range(1, 10):
        alu.run_instructions(instructions[0], i)
        print(f"input {i} -> {alu.vars}")
        store = alu.vars.copy()
        for j in range(1, 10):
            alu.run_instructions(instructions[1], j)
            print(f"    input {j} -> {alu.vars}")
            alu.reset(store[0], store[1], store[2], store[3])
        alu.reset()'''
    '''run_instr_level(5, 0, instructions, alu)'''
    print(instructions[-1])
    TARGET_Z_MIN = 0
    TARGET_Z_MAX = 0
    possible = set()
    for z in range(0, 1000):
        stuff = []
        for i in range(1, 10):
            alu.reset(0, 0, 0, z)
            alu.run_instructions(instructions[-1], i)
            if TARGET_Z_MIN <= alu.vars[3] <= TARGET_Z_MAX:
                stuff.append(f"    input {i} -> {alu.vars}")
                possible.add(alu.vars[Var.w])
        if len(stuff) > 0:
            print("IN Z = ", z)
            for j in stuff:
                print(j)
    print(possible)

    # Return value of -1 is used to signal that this isn't implemented.
    # Once it is, remove/replace that return (implicitly returning None is fine).
    return -1


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day24.txt")
