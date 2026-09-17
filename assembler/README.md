# Python Assembler

This folder contains the Python script acting as an assembler for the 8-bit accumulator CPU. The script takes the source file containing the assembly code as input and generates the hexadecimal file ready to be loaded into the Logisim ROM memory.

## Script Logic

The script reads the source code line by line and, by consulting an internal dictionary defining the mappings between each mnemonic code and its corresponding opcode, translates the entire program into hexadecimal and writes it to the output file. The script will report any errors in the terminal, halting execution.

## Program Writing Rules

Programs must be written with a direct line-by-line correspondence to the CPU RAM: Line 1 of the file corresponds to RAM location 0, line 2 to location 1, up to line 16, which corresponds to location 15 in RAM. Each line must contain the instruction mnemonic followed by its operand if applicable, for example `LDA 5` or `ADD 3`. If you want to leave a memory location empty or undefined, write `NUL` on that line, and the script will output `00000000`.



## Execution Workflow

To assemble and run a program, you can directly use the files provided in this folder: `assembler.py`, `file.asm`, and `file.hex`.

* **Assembly via Terminal:** After writing the instructions in the source file `file.asm`, open the terminal in the folder and execute the script, passing the two files as parameters:
  ```bash
  python3 assembler.py file.asm file.hex
* **Loading into Logisim ROM:** Open the CPU circuit in Logisim, right-click on the ROM component, select "Load Image...", and choose the newly generated `file.hex` file. Logisim will copy the content, automatically translating it into binary.

* **Transferring to RAM and Execution:** Enable the global clock signal in Logisim. With the CPU in External Mode (with the `on_off` pin deactivated), activate the `start` pin so that the Boot System copies the program from ROM to RAM. Once the program has been fully copied to RAM, deactivate the `start` pin to stop the transfer and reset the Boot counter using the `rst_addr` line. Finally, activate the `on_off` pin to start executing the program saved in RAM.

> **Note:** The `.asm` and `.hex` extensions are merely symbolic conventions used for visual clarity. The files remain standard text files in every respect.
