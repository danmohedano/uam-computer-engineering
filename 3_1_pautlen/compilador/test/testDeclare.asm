
; Escribir cabecera
segment .bss
	__esp resd 1

; Declarar variable
	_count resd 1

; Declarar variable
	_x resd 1

; Declarar variable
	_i resd 20

; Escribir subseccion data
segment .data
	div0 dd "Run Time Error: Division by zero", 0
	iob dd "Run Time Error: Index out of bounds", 0

; Escribir segmento codigo
segment .text
global main
extern scan_int, scan_boolean, print_blank, print_endofline, print_string, print_int, print_boolean

; Declarar funcion
_getRandom:
	push ebp
	mov ebp, esp
	sub esp, 0

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Escribir operando
	push DWORD 11

; Multiplicar
	pop DWORD ecx
	pop DWORD eax
	mov DWORD eax, [eax]
	imul eax, ecx
	push DWORD eax

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Asignar destino en pila
	pop DWORD ebx
	pop DWORD eax
	mov DWORD [ebx], eax

; While inicio
inicio_while1:

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Escribir operando
	push DWORD 20

; Mayor Igual
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, edx
	jge near mayorigual2
	push DWORD 0
	jmp near fin_mayorigual2
mayorigual2:
	push DWORD 1
fin_mayorigual2:

; While exp pila
	pop eax
	cmp eax, 0
	je near fin_while1

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Escribir operando
	push DWORD 20

; Restar
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	sub eax, edx
	push DWORD eax

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Asignar destino en pila
	pop DWORD ebx
	pop DWORD eax
	mov DWORD [ebx], eax

; While fin
	jmp near inicio_while1
fin_while1:

; Escribir parametro
	lea eax, [ebp + 8]
	push DWORD eax

; Retornar funcion
	pop eax
	mov DWORD eax, [eax]
	mov esp, ebp
	pop ebp
	ret

; Escribir inicio main
main:
	mov DWORD [__esp], esp

; Escribir operando
	push DWORD 0

; Asignar
	pop DWORD eax
	mov DWORD [_count], eax

; While inicio
inicio_while3:

; Escribir operando
	push DWORD _count

; Escribir operando
	push DWORD 20

; Menor
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, edx
	jl near menor4
	push DWORD 0
	jmp near fin_menor4
menor4:
	push DWORD 1
fin_menor4:

; While exp pila
	pop eax
	cmp eax, 0
	je near fin_while3

; Escribir operando
	push DWORD _count

; Escribir elemento vector
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, 0
	jl near err_iob
	cmp eax, 19
	jg near err_iob
	mov DWORD edx, _i
	lea eax, [edx + eax*4]
	push DWORD eax

; Escribir operando
	push DWORD _count

; Asignar destino en pila
	pop DWORD eax
	pop DWORD ebx
	mov DWORD eax, [eax]
	mov DWORD [ebx], eax

; Escribir operando
	push DWORD _count

; Escribir elemento vector
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, 0
	jl near err_iob
	cmp eax, 19
	jg near err_iob
	mov DWORD edx, _i
	lea eax, [edx + eax*4]
	push DWORD eax

; Escribir
	pop DWORD eax
	mov DWORD eax, [eax]
	push DWORD eax
	call print_int
	add esp, 4
	call print_endofline

; Escribir operando
	push DWORD _count

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
	mov DWORD [_count], eax

; While fin
	jmp near inicio_while3
fin_while3:

; Escribir operando
	push DWORD 1

; Escribir
	call print_boolean
	add esp, 4
	call print_endofline

; Escribir operando
	push DWORD 0

; Asignar
	pop DWORD eax
	mov DWORD [_count], eax

; While inicio
inicio_while5:

; Escribir operando
	push DWORD _count

; Escribir operando
	push DWORD 20

; Menor
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, edx
	jl near menor6
	push DWORD 0
	jmp near fin_menor6
menor6:
	push DWORD 1
fin_menor6:

; While exp pila
	pop eax
	cmp eax, 0
	je near fin_while5

; Escribir operando
	push DWORD _count

; Operando en pila a argumento
	pop eax
	mov eax, [eax]
	push eax

; Llamar funcion
	call _getRandom

; Limpiar pila
	add esp, 4
	push DWORD eax

; Escribir elemento vector
	pop DWORD eax
	cmp eax, 0
	jl near err_iob
	cmp eax, 19
	jg near err_iob
	mov DWORD edx, _i
	lea eax, [edx + eax*4]
	push DWORD eax

; Escribir
	pop DWORD eax
	mov DWORD eax, [eax]
	push DWORD eax
	call print_int
	add esp, 4
	call print_endofline

; Escribir operando
	push DWORD _count

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
	mov DWORD [_count], eax

; While fin
	jmp near inicio_while5
fin_while5:

; Escribir operando
	push DWORD 1

; Escribir
	call print_boolean
	add esp, 4
	call print_endofline

; Escribir operando
	push DWORD 0

; Asignar
	pop DWORD eax
	mov DWORD [_count], eax

; While inicio
inicio_while7:

; Escribir operando
	push DWORD _count

; Escribir operando
	push DWORD 20

; Menor
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, edx
	jl near menor8
	push DWORD 0
	jmp near fin_menor8
menor8:
	push DWORD 1
fin_menor8:

; While exp pila
	pop eax
	cmp eax, 0
	je near fin_while7

; Escribir operando
	push DWORD _count

; Escribir operando
	push DWORD _count

; Multiplicar
	pop DWORD ecx
	mov DWORD ecx, [ecx]
	pop DWORD eax
	mov DWORD eax, [eax]
	imul eax, ecx
	push DWORD eax

; Escribir operando
	push DWORD _count

; Escribir operando
	push DWORD 3

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

; Asignar
	pop DWORD eax
	mov DWORD [_x], eax

; Escribir operando
	push DWORD _count

; Escribir elemento vector
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, 0
	jl near err_iob
	cmp eax, 19
	jg near err_iob
	mov DWORD edx, _i
	lea eax, [edx + eax*4]
	push DWORD eax

; Escribir operando
	push DWORD _x

; Asignar destino en pila
	pop DWORD eax
	pop DWORD ebx
	mov DWORD eax, [eax]
	mov DWORD [ebx], eax

; Escribir operando
	push DWORD _count

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
	mov DWORD [_count], eax

; While fin
	jmp near inicio_while7
fin_while7:

; Escribir operando
	push DWORD 0

; Asignar
	pop DWORD eax
	mov DWORD [_count], eax

; While inicio
inicio_while9:

; Escribir operando
	push DWORD _count

; Escribir operando
	push DWORD 20

; Menor
	pop DWORD edx
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, edx
	jl near menor10
	push DWORD 0
	jmp near fin_menor10
menor10:
	push DWORD 1
fin_menor10:

; While exp pila
	pop eax
	cmp eax, 0
	je near fin_while9

; Escribir operando
	push DWORD _count

; Escribir elemento vector
	pop DWORD eax
	mov DWORD eax, [eax]
	cmp eax, 0
	jl near err_iob
	cmp eax, 19
	jg near err_iob
	mov DWORD edx, _i
	lea eax, [edx + eax*4]
	push DWORD eax

; Escribir
	pop DWORD eax
	mov DWORD eax, [eax]
	push DWORD eax
	call print_int
	add esp, 4
	call print_endofline

; Escribir operando
	push DWORD _count

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
	mov DWORD [_count], eax

; While fin
	jmp near inicio_while9
fin_while9:

; Escribir operando
	push DWORD 0

; Escribir
	call print_boolean
	add esp, 4
	call print_endofline

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
