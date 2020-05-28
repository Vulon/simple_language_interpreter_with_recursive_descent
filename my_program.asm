section .bss
	x: resd 1
	y: resd 1


section .text
	global  _main
	extern  _printf

_main:
	mov dword [x],  dword 1
	;expression: [CONST:1] 
	; optimized: push dword 1, pop eax = mov eax, dword 1
	; optimized: mov eax, dword 1 and mov dword [x], eax replaced with mov dword [x],  dword 1
	; enter expr to x
	mov dword [y],  dword 2
	;expression: [CONST:2] 
	; optimized: push dword 2, pop eax = mov eax, dword 2
	; optimized: mov eax, dword 2 and mov dword [y], eax replaced with mov dword [y],  dword 2
	; enter expr to y
	push dword [x]
	mov ebx, dword 9
	; optimized: push dword 9, pop ebx = mov ebx, dword 9
	pop eax 
	add eax, ebx
	push eax
	;expression: [ID:x] [CONST:9] [PLUS:+] 
	push dword [y]
	mov ebx, dword 5
	; optimized: push dword 5, pop ebx = mov ebx, dword 5
	pop eax 
	imul eax, ebx
	mov ebx, eax
	;expression: [ID:y] [CONST:5] [TIMES:*] 
	; optimized: push eax, pop ebx = mov ebx, eax
	pop eax
	cmp eax, ebx
	jg l1
		push dword -1
		;expression: [CONST:5] [CONST:1] [PLUS:+] [CONST:1] [PLUS:+] [CONST:1] [PLUS:+] [CONST:9] [MINUS:-] 
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
		push dword 2
		;expression: [CONST:6] [CONST:3] [DIVIDE:/] 
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
		push dword 2
		;expression: [CONST:5] [CONST:2] [DIVIDE:/] 
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
	JMP l2
	l1:
		push dword 1
		;expression: [CONST:1] 
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
		mov dword [x],  dword 4
		;expression: [CONST:4] 
		; optimized: push dword 4, pop eax = mov eax, dword 4
		; optimized: mov eax, dword 4 and mov dword [x], eax replaced with mov dword [x],  dword 4
		; enter expr to x
	l2:
	ret

message:
	db  '%d', 10, 0
