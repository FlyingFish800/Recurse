; hello world

section .text
    global _start
    _start:
        mov rax, 1
        mov rdi, 1
        mov rsi, str
        mov rdx, len
        syscall

        mov rax, 60
        mov rdi, 0
        syscall

section .data           
    str: db "Hello World!", 10
    len: equ $ - str         
