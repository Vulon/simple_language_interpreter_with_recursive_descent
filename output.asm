section .bss
	b: resd 1
	a: resd 1


section .text
	global  _main
	extern  _printf

_main:
	push dword 4
	push dword 1
	pop ebx 
	pop eax 
	add eax, ebx
	push eax
	;expression: [CONST:4] [CONST:1] [PLUS:+] 
	pop eax
	mov dword [a], eax
	; enter expr to a
	push dword 3
	push dword 2
	pop ebx 
	pop eax 
	imul eax, ebx
	push eax
	;expression: [CONST:3] [CONST:2] [TIMES:*] 
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
		push dword 5
		push dword 5
		pop ebx 
		pop eax 
		imul eax, ebx
		push eax
		push dword 5
		pop ebx 
		pop eax 
		imul eax, ebx
		push eax
		;expression: [CONST:5] [CONST:5] [TIMES:*] [CONST:5] [TIMES:*] 
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
		push dword [a]
		push dword 1
		pop ebx 
		pop eax 
		add eax, ebx
		push eax
		;expression: [ID:a] [CONST:1] [PLUS:+] 
		push dword [b]
		;expression: [ID:b] 
		pop ebx
		pop eax
		cmp eax, ebx
		jne l3
			push dword [b]
			;expression: [ID:b] 
			push message
			call _printf
			pop ebx
			pop ebx
			; print expr 
		JMP l4
		l3:
			push dword [a]
			;expression: [ID:a] 
			push message
			call _printf
			pop ebx
			pop ebx
			; print expr 
		l4:
	JMP l2
	l1:
		push dword 4
		push dword 4
		pop ebx 
		pop eax 
		imul eax, ebx
		push eax
		push dword 4
		pop ebx 
		pop eax 
		imul eax, ebx
		push eax
		;expression: [CONST:4] [CONST:4] [TIMES:*] [CONST:4] [TIMES:*] 
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
	l2:
	ret

message:
	db  '%d', 10, 0
