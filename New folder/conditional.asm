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
	;expression: [ID:a] 
	push dword [b]
	;expression: [ID:b] 
	pop ebx
	pop eax
	cmp eax, ebx
	jge l1
		push dword 4
		;expression: [CONST:4] 
		pop eax
		mov dword [c], eax
		; enter expr to c
	l1:
	push dword [a]
	;expression: [ID:a] 
	push dword [b]
	push dword 1
	pop ebx 
	pop eax 
	add eax, ebx
	push eax
	;expression: [ID:b] [CONST:1] [PLUS:+] 
	pop ebx
	pop eax
	cmp eax, ebx
	jne l3
		push dword 2
		;expression: [CONST:2] 
		pop eax
		mov dword [c], eax
		; enter expr to c
	l3:
	ret

message:
	db  '%d', 10, 0
