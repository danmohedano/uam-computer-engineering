# Prog de prueba para Práctica 2. Ej 2

.data 0
num0: .word 1 # posic 0
num1: .word 2 # posic 4
num2: .word 4 # posic 8 
num3: .word 8 # posic 12 
num4: .word 16 # posic 16 
num5: .word 32 # posic 20
num6: .word 0 # posic 24
num7: .word 0 # posic 28
num8: .word 0 # posic 32
num9: .word 0 # posic 36
num10: .word 0 # posic 40
num11: .word 0 # posic 44
.text 0
main:
	lw $t1, 4($zero) # lw $r9, 0($r0)
	lw $t2, 4($zero) # lw $r10, 0($r0)
	lw $t3, 0($zero)
	lw $t4, 0($zero)
	lw $t5, 0($zero)
	lw $t6, 0($zero)
	nop
	nop
	nop
	nop
	# COMPROBAR BEQ EFECTIVO (sin instrucciones extra antes)
	beq $t1, $t2, salto1 # 2 == 2, salto efectivo
	add $t3, $t3, $t5 # t3 = 2 (no se debería de ejecutar)
	add $t3, $t3, $t5 # t3 = 3 (no se debería de ejecutar)
	add $t3, $t3, $t5 # t3 = 4 (no se debería de ejecutar)
salto1:
	add $t4, $t4, $t5 # t4 = 2 
	nop
	nop
	nop
	nop
	# COMPROBAR BEQ NO EFECTIVO (sin instrucciones extra antes)
	beq $t1, $t5, salto2 # 2 != 1 salto no efectivo
	add $t4, $t4, $t5 # t4 = 3
	add $t4, $t4, $t5 # t4 = 4
	add $t4, $t4, $t5 # t4 = 5
salto2:
	add $t4, $t4, $t4 # t4 = 10 (t4 = 4 si se toma el salto como efectivo)
	nop
	nop
	nop
	nop
	# COMPROBAR BEQ EFECTIVO CON R-TYPE PREVIA
	add $t6, $t6, $t6 # t6 = 1+1 = 2
	beq $t1, $t6, salto3 # 2 == 2 salto efectivo
	add $t3, $t3, $t5 # t3 = 2 (no se debería de ejecutar)
	add $t3, $t3, $t5 # t3 = 3 (no se debería de ejecutar)
	add $t3, $t3, $t5 # t3 = 4 (no se debería de ejecutar)
salto3:
	add $t4, $t4, $t5 # t4 = 11
	nop
	nop
	nop
	nop
	# COMPROBAR BEQ NO EFECTIVO CON R-TYPE PREVIA
	add $t6, $t6, $t6 # t6 = 2+2 = 4
	beq $t1, $t6, salto4 # 2 != 4 salto no efectivo
	add $t4, $t4, $t5 # t4 = 12
	add $t4, $t4, $t5 # t4 = 13
	add $t4, $t4, $t5 # t4 = 14
salto4:
	add $t4, $t4, $t4 # t4 = 28 (t4 = 22 si se toma el salto como efectivo)
	nop
	nop
	nop
	nop
	# COMPROBAR BEQ EFECTIVO CON LW PREVIO
	lw $t6, 4($zero) # t6 <= 2 (previamente valía 4)
	beq $t1, $t6, salto5 # 2 == 2 salto efectivo
	add $t3, $t3, $t5 # t3 = 2 (no se debería de ejecutar)
	add $t3, $t3, $t5 # t3 = 3 (no se debería de ejecutar)
	add $t3, $t3, $t5 # t3 = 4 (no se debería de ejecutar)
salto5:
	add $t4, $t4, $t5 # t4 = 29
	nop
	nop
	nop
	nop
	# COMPROBAR BEQ NO EFECTIVO CON LW PREVIO
	lw $t6, 0($zero) # t6 <= 1 (previamente valía 2)
	beq $t1, $t6, salto6 # 2 != 1 salto no efectivo
	add $t4, $t4, $t5 # t4 = 30
	add $t4, $t4, $t5 # t4 = 31
	add $t4, $t4, $t5 # t4 = 32
salto6:
	add $t4, $t4, $t4 # t4 = 64 (t4 = 58 si se toma el salto como efectivo)
	nop
	nop
	nop
	nop
	
