import sys

OPCODES = {
    "NUL": 0x0,
    "LDA": 0x1, #load 
    "STA": 0x2, #store 
    "ADD": 0x3,
    "SUB": 0x4,
    "JMP": 0x5, #jump
    "JZ":  0x6, #jump if zero
    "IN": 0x7,
    "OUT": 0x8,
    "SMA": 0x9, #sum array
    "AND": 0xA,
    "OR": 0xB,
    "LDI": 0xC, #load immediate (unsigned)
    "LDF": 0xD, #load flags
    "HLT": 0xF, #halt
}

MEM_SIZE = 16


def assemble(lines):
    mem = [0] * MEM_SIZE
    addr = 0

    for line_no, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue

        parts = line.split()

        if addr >= MEM_SIZE:
            raise ValueError("The program has more lines than the 16 available cells")

        if len(parts) == 1:
            part = parts[0]
            part = part.upper()
            
            if part not in OPCODES:
                try:
                    byte = int(part)
                except ValueError:
                    raise ValueError(f"Line {line_no}: '{part}' is not a valid mnemonic or number")

                if not (0 <= byte <= 255):
                    raise ValueError(f"Line {line_no}: value {byte} out of range 0-255")
            else:
                opcode = OPCODES[part]
                byte = opcode << 4

        elif len(parts) == 2:
            mnemonic, part = parts
            mnemonic = mnemonic.upper()

            if mnemonic not in OPCODES:
                raise ValueError(f"Line {line_no}: unknown mnemonic '{mnemonic}'")

            try:
                numero = int(part)
            except ValueError:
                raise ValueError(f"Line {line_no}: '{part}' is not a valid number")

            if not (0 <= numero <= 15):
                raise ValueError(f"Line {line_no}: number {numero} out of range 0-15")

            opcode = OPCODES[mnemonic]
            byte = (opcode << 4) | numero

        else:
            raise ValueError(
                f"Line {line_no}: expected 'NUMBER' or 'MNEMONIC NUMBER', found: '{line}'"
            )

        mem[addr] = byte
        addr += 1

    return mem


def to_logisim_hex(mem):

    byte_hex_list = []
    for b in mem:
        b_hex = f"{b:02x}"
        byte_hex_list.append(b_hex)

    byte_line = " ".join(byte_hex_list)

    final_text = "v3.0 hex words addressed" + "\n" + f"0: {byte_line}" + "\n"

    return final_text


if len(sys.argv) != 3:
    print("Usage: python3 assembler.py <input.asm> <output.hex>")
    sys.exit(1)

in_path, out_path = sys.argv[1], sys.argv[2]

with open(in_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

try:
    mem = assemble(lines)
except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)

hex_text = to_logisim_hex(mem)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(hex_text)

print(f"OK: {in_path} -> {out_path}")
print(hex_text)
