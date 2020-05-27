section .bss
	x: resd 1
	y: resd 1


section .text
	global  _main
	extern  _printf

_main:
	mov eax, dword 1
	;expression: [CONST:1] 
	; optimized
	mov dword [x], eax
	; enter expr to x
	mov eax, dword 2
	;expression: [CONST:2] 
	; optimized
	mov dword [y], eax
	; enter expr to y
	push dword [x]
	push dword 9
	;expression: [ID:x] [CONST:9] [PLUS:+] 
	push dword [y]
	mov ebx, dword 5
	;expression: [ID:y] [CONST:5] [TIMES:*] 
	; optimized
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
		mov eax, dword 4
		;expression: [CONST:4] 
		; optimized
		mov dword [x], eax
		; enter expr to x
	l2:
	ret

message:
	db  '%d', 10, 0
