#!/usr/bin/python3
# correr como $./simulador programa.txt cintas.txt
from sys import argv
import time

def validate_machine(programa):
    first = True
    for linea in programa:
        if first:
            if len(linea.split()) == 3:
                type_machine = 'afd'
            elif len(linea.split()) == 5:
                type_machine = 'mt'
            else:
                raise Exception('Error en la definición de la máquina')
            first = False
        else:
            if type_machine == 'afd':
                if len(linea.split()) != 3:
                    raise Exception('Error en el archivo para Autómata Finito Determinista')
            elif type_machine == 'mt':
                if len(linea.split()) != 5:
                    raise Exception('Error en el archivo para Máquina de Turing')
    return type_machine


# AUTOMATA FINITO DETERMINISTA
def AFD(d,q0,F,cinta):
    q=q0
    for simbolo in cinta:
        q=d[q,simbolo]
    return q in F

def run_AFD(programa, cintas):
    d={}
    F=set()
    for linea in programa:
        q,s,n=linea.split()
        if '*' in q:
            q=q.strip('*')
            F.add(q)
        d[q,s]=n

    mensaje={True:'Aceptada',False:'Rechazada'}

    for cinta in cintas:
        cinta=cinta.strip()
        print('La entrada',cinta," es ",mensaje[AFD(d,'0',F,cinta)])

# END AUTOMATA FINITO DETERMINISTA

# MAQUINA DE TURING
def MT(tape, head, current, initial, s_read, s_write, direction, final):
    if current == initial and tape[head] == s_read:
        tape[head] = s_write
        if direction == 'R':
            if head == len(tape) - 1:
                tape.append('_')
            head += 1
        elif direction == 'L':
            if head == 0:
                tape.insert(0, '_')
            else:
                head -= 1
        current = final
        return tape, head, current, True
    else:
        return tape, head, current, False

# quintuplas mt: estado actual, simbolo leido, simbolo escrito, direccion, estado siguiente
def run_MT(programa, cinta):
    # find position * character
    if '*' in cinta:
        head = cinta.index('*')
        cinta.remove('*')
    else:
        head = 0
    tape = cinta
    current = '0'
    count = 0
    while True:
        flag_transition = False
        for linea in programa:
            initial, s_read, s_write, direction, final = linea.split()
            tape, head, current, boolean_transition = MT(tape, head, current, initial, s_read, s_write, direction, final)
            if boolean_transition:
                flag_transition = True
                count += 1
                print(f'count: {count}')
                print(f"{''.join(tape)} - {current}")
                print(f"{' ' * head}^")
                time.sleep(0.005)
        if not flag_transition:
            print('Máquina de Turing detenida')
            raise Exception(f"Sin transición {''.join(tape)}")
# END MAQUINA DE TURING

with open(argv[1], 'r') as programa:
    programa = [linea.strip() for linea in programa.readlines()]
    type_machine = validate_machine(programa)

if type_machine == 'afd':
    print('Autómata Finito Determinista:')
    with open(argv[2], 'r') as cintas:
        run_AFD(programa, cintas)
elif type_machine == 'mt':
    print('Máquina de Turing:')
    with open(argv[2], 'r') as cintas:
        run_MT(programa, list(cintas.readline()))
else:
    print('Error en la definición de la máquina')
