
; Escribir cabecera
segment .bss
	__esp resd 1

; Declarar variable
	_x resd 1

; Declarar variable
	_y resd 1

; Declarar variable
	_z resd 1

; Declarar variable
	_a resd 1

; Declarar variable
	_b resd 1

; Declarar variable
	_r resd 10

; Declarar variable
	_t resd 1

; Declarar variable
	_f resd 1

; Declarar variable
	_viejoPuto resd 1

; Escribir subseccion data
segment .data
	div0 dd "Run Time Error: Division by zero", 0
	iob dd "Run Time Error: Index out of bounds", 0

; Escribir segmento codigo
segment .text
global main
extern scan_int, scan_boolean, print_blank, print_endofline, print_string, print_int, print_boolean

; Declarar funcion
_killHim:
	push ebp
	mov ebp, esp
	sub esp, 0

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Inicio de if then
	pop eax
	mov eax, [eax]
	cmp eax, 0
	je near fin_then1

; Escribir operando
	push DWORD 2

; Cambiar signo
	pop DWORD eax
	neg eax
	push DWORD eax

; Retornar funcion
	pop eax
	mov esp, ebp
	pop ebp
	ret

; Fin de if then, else, then
	jmp near fin_ifelse1
fin_then1:

; Escribir operando
	push DWORD 1

; Cambiar signo
	pop DWORD eax
	neg eax
	push DWORD eax

; Retornar funcion
	pop eax
	mov esp, ebp
	pop ebp
	ret

; If then else fin
fin_ifelse1:

; Declarar funcion
_putoKostadin:
	push ebp
	mov ebp, esp
	sub esp, 8

; Escribir operando
	push DWORD 0

; Escribir variable local
	lea eax, [ebp - 4]
	push DWORD eax

; Asignar destino en pila
	pop DWORD ebx
	pop DWORD eax
	mov DWORD [ebx], eax

; Escribir parametro
	lea eax, [ebp + 16]
	push DWORD eax

; Escribir
	pop DWORD eax
	mov DWORD eax, [eax]
	push DWORD eax
	call print_int
	add esp, 4
	call print_endofline

; While inicio
inicio_while2:

; Escribir variable local
	lea eax, [ebp - 4]
	push DWORD eax

; Escribir parametro
	lea eax, [ebp + 16]
	push DWORD eax

; Menor Igual
	pop DWORD edx
	mov DWORD edx, [edx]
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, edx
	jle near menorigual3
	push DWORD 0
	jmp near fin_menorigual3
menorigual3:
	push DWORD 1
fin_menorigual3:

; While exp pila
	pop eax
	cmp eax, 0
	je near fin_while2

; Escribir parametro
	lea eax, [ebp + 12]
	push DWORD eax

; Inicio de if then
	pop eax
	mov eax, [eax]
	cmp eax, 0
	je near fin_then4

; Escribir operando
	push DWORD 1

; Llamar funcion
	call _killHim

; Limpiar pila
	add esp, 4
	push DWORD eax

; Escribir variable local
	lea eax, [ebp - 8]
	push DWORD eax

; Asignar destino en pila
	pop DWORD ebx
	pop DWORD eax
	mov DWORD [ebx], eax

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Escribir operando
	push DWORD 1

; Sumar
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	add eax, edx
	push DWORD eax

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Asignar destino en pila
	pop DWORD ebx
	pop DWORD eax
	mov DWORD [ebx], eax

; Fin de if then
fin_then4:

; Escribir variable local
	lea eax, [ebp - 4]
	push DWORD eax

; Escribir
	pop DWORD eax
	mov DWORD eax, [eax]
	push DWORD eax
	call print_int
	add esp, 4
	call print_endofline

; Escribir variable local
	lea eax, [ebp - 4]
	push DWORD eax

; Escribir operando
	push DWORD 1

; Sumar
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	add eax, edx
	push DWORD eax

; Escribir variable local
	lea eax, [ebp - 4]
	push DWORD eax

; Asignar destino en pila
	pop DWORD ebx
	pop DWORD eax
	mov DWORD [ebx], eax

; While fin
	jmp near inicio_while2
fin_while2:

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Escribir
	pop DWORD eax
	mov DWORD eax, [eax]
	push DWORD eax
	call print_int
	add esp, 4
	call print_endofline

; Escribir operando
	push DWORD 1

; Retornar funcion
	pop eax
	mov esp, ebp
	pop ebp
	ret

; Escribir inicio main
main:
	mov DWORD [__esp], esp

; Escribir operando
	push DWORD _x

; Leer
	call scan_int
	add esp, 4

; Escribir operando
	push DWORD _x

; Asignar
	pop DWORD eax
	mov DWORD eax, [eax]
	mov DWORD [_y], eax

; Escribir operando
	push DWORD _x

; Escribir operando
	push DWORD 2

; Multiplicar
	pop DWORD ecx
	pop DWORD eax
	mov DWORD eax, [eax]
	imul eax, ecx
	push DWORD eax

; Escribir operando
	push DWORD _y

; Escribir operando
	push DWORD 2

; Dividir
	pop DWORD ecx
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp ecx, DWORD 0
	je near err_div0
	cdq
	idiv ecx
	push DWORD eax

; Sumar
	pop DWORD edx
	pop DWORD eax
	add eax, edx
	push DWORD eax

; Escribir operando
	push DWORD _x

; Escribir operando
	push DWORD _x

; Escribir operando
	push DWORD _y

; Restar
	pop DWORD edx
	mov DWORD edx, [edx]
	pop DWORD eax
	mov DWORD eax, [eax]
	sub eax, edx
	push DWORD eax

; Multiplicar
	pop DWORD ecx
	pop DWORD eax
	mov DWORD eax, [eax]
	imul eax, ecx
	push DWORD eax

; Escribir operando
	push DWORD 10

; Multiplicar
	pop DWORD ecx
	pop DWORD eax
	imul eax, ecx
	push DWORD eax

; Restar
	pop DWORD edx
	pop DWORD eax
	sub eax, edx
	push DWORD eax

; Escribir operando
	push DWORD 5

; Escribir operando
	push DWORD _x

; Multiplicar
	pop DWORD ecx
	mov DWORD ecx, [ecx]
	pop DWORD eax
	imul eax, ecx
	push DWORD eax

; Sumar
	pop DWORD edx
	pop DWORD eax
	add eax, edx
	push DWORD eax

; Asignar
	pop DWORD eax
	mov DWORD [_z], eax

; Escribir operando
	push DWORD 1

; Asignar
	pop DWORD eax
	mov DWORD [_viejoPuto], eax

; Escribir operando
	push DWORD _z

; Operando en pila a argumento
	pop eax
	mov eax, [eax]
	push eax

; Escribir operando
	push DWORD _viejoPuto

; Operando en pila a argumento
	pop eax
	mov eax, [eax]
	push eax

; Escribir operando
	push DWORD 20

; Llamar funcion
	call _putoKostadin

; Limpiar pila
	add esp, 12
	push DWORD eax

; Inicio de if then
	pop eax
	cmp eax, 0
	je near fin_then5

; Escribir operando
	push DWORD _y

; Escribir operando
	push DWORD _z

; Multiplicar
	pop DWORD ecx
	mov DWORD ecx, [ecx]
	pop DWORD eax
	mov DWORD eax, [eax]
	imul eax, ecx
	push DWORD eax

; Asignar
	pop DWORD eax
	mov DWORD [_x], eax

; Escribir operando
	push DWORD 0

; Asignar
	pop DWORD eax
	mov DWORD [_a], eax

; While inicio
inicio_while6:

; Escribir operando
	push DWORD _a

; Escribir operando
	push DWORD _z

; Menor
	pop DWORD edx
	mov DWORD edx, [edx]
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, edx
	jl near menor7
	push DWORD 0
	jmp near fin_menor7
menor7:
	push DWORD 1
fin_menor7:

; While exp pila
	pop eax
	cmp eax, 0
	je near fin_while6

; Escribir operando
	push DWORD _viejoPuto

; Operando en pila a argumento
	pop eax
	mov eax, [eax]
	push eax

; Llamar funcion
	call _killHim

; Limpiar pila
	add esp, 4
	push DWORD eax

; Escribir
	call print_int
	add esp, 4
	call print_endofline

; Escribir operando
	push DWORD _a

; Escribir operando
	push DWORD 1

; Sumar
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	add eax, edx
	push DWORD eax

; Asignar
	pop DWORD eax
	mov DWORD [_a], eax

; While fin
	jmp near inicio_while6
fin_while6:

; Fin de if then
fin_then5:

; Escribir fin
fin:
	mov DWORD esp, [__esp]
	mov DWORD eax, 0
	ret
err_div0:
	push DWORD div0
	call print_string
	add esp, 4
	call print_endofline
	jmp near fin
err_iob:
	push DWORD iob
	call print_string
	add esp, 4
	call print_endofline
	jmp near fin
