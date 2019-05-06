# sim-port

## Launch command:

    Core.py [options]
    Options:
    -h, --help              Shows the program usage help.
    -p, --processors=...    Sets the number of processors.
    -s, --sources=...       Sets the number of sources.

## TODO

Entity (?)
- timeCreated
- timeRemoved

Queue (Buffer) (?)
- Subclass (?)

Random
- Max, Min, Moda -> Triangular per cada hora -> nombre de camions -> dividir per N carrils (8)
- Distribució T entre arribades -> exponencial (1 / nombre)
- T varis processadors:
        Sabent que X processadors fan Y operacions per hora
        1 processador fa X/Y operacions per hora
        Distribució temps processament -> constant (uniforme) capacitat productiva

Capa de presentacion
- Django -> API
    
Unit tests


INFO:

Nombre de processadors = 52 (13*3-HIGH + 39*4-HIGH)
https://www.apmterminals.com/en/barcelona/about/our-terminal
