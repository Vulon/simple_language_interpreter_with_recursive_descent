section .bss
	x: resd 1
	y: resd 1


section .text
	global  _main
	extern  _printf

_main:
	push dword 4
	push dword 1
	pop ebx 
	pop eax 
	sub eax, ebx
	push eax
	;expression: [CONST:4] [CONST:1] [MINUS:-] 
	pop eax
	mov dword [x], eax
	; enter expr to x
	push dword 3
	;expression: [CONST:3] 
	pop eax
	mov dword [y], eax
	; enter expr to y
	push dword [x]
	;expression: [ID:x] 
	push dword 1
	;expression: [CONST:1] 
	pop ebx
	pop eax
	cmp eax, ebx
	jle l1
		push dword [y]
		;expression: [ID:y] 
		push dword 2
		;expression: [CONST:2] 
		pop ebx
		pop eax
		cmp eax, ebx
		jle l3
			push dword 19
			;expression: [CONST:19] 
			push message
			call _printf
			pop ebx
			pop ebx
			; print expr 
		JMP l4
		l3:
			push dword 20
			;expression: [CONST:20] 
			push message
			call _printf
			pop ebx
			pop ebx
			; print expr 
		l4:
	l1:
	push dword [x]
	;expression: [ID:x] 
	push dword 5
	;expression: [CONST:5] 
	pop ebx
	pop eax
	cmp eax, ebx
	jge l5
		push dword 35
		;expression: [CONST:35] 
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
	l5:
	ret

message:
	db  '%d', 10, 0
