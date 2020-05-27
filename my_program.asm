section .bss
	x: resd 1
	y: resd 1
section .text
	global  _main
	extern  _printf
_main:
	mov dword [x],  dword 1
	mov dword [y],  dword 2
	push dword [x]
	push dword 9
	push dword [y]
	mov ebx, dword 5
	pop eax
	cmp eax, ebx
	jg l1
		push dword -1
		push message
		call _printf
		pop ebx
		pop ebx
		push dword 2
		push message
		call _printf
		pop ebx
		pop ebx
		push dword 2
		push message
		call _printf
		pop ebx
		pop ebx
		; print expr 
	JMP l2
	l1:
		push dword 1
		push message
		call _printf
		pop ebx
		pop ebx
		mov dword [x],  dword 4
	l2:
	ret
message:
	db  '%d', 10, 0
