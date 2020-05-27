section .bss
	a: resd 1
	b: resd 1
	c: resd 1


section .text
	global  _main
	extern  _printf

_main:
	push dword 4
	;expression: [CONST:4] 
	pop eax
	mov dword [a], eax
	; enter expr to a
	push dword 3
	;expression: [CONST:3] 
	pop eax
	mov dword [b], eax
	; enter expr to b
	push dword [a]
	push dword [b]
	pop ebx 
	pop eax 
	add eax, ebx
	push eax
	;expression: [ID:a] [ID:b] [PLUS:+] 
	pop eax
	mov dword [c], eax
	; enter expr to c
	ret

message:
	db  '%d', 10, 0
