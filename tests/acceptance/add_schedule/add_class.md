# Prerequisites
[Add course unit](add_course_unit#adicionar-curso)
[Choose course unit to edit](add_course_unit#editar-curso-escolher)

\< 
```
Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```
# Tests
## Adicionar aula

### Adicionar aula cancelar
\>
```
!1
```

\<
```
Adicionar aula a 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!0
```

\<
```
Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```

### Adicionar aula escolher
First
\>
```
!1
```

\<
```
Adicionar aula a 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!1
```

\<
```
Added 1MEEC_E02: T

Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```
Second

#### Adicionar aula repetido
\>
```
!1
```

\<
```
Adicionar aula a 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!1
```

\<
```
You already added 1MEEC_E02: T

Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```
### Adicionar aula erro
\>
```
!1
```

\<
```
Adicionar aula a 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!2
```

\<
```
Option not recognized
```
## Ver aula


### Ver aula vazio
\> 
```
!2
```

\<
```
Horarios de aula de 50154C5: Sistemas Construtivos Tradicionais

0: Cancel
```

\>
```
!0
```

\<
```
Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```

### Ver aula 

Prerequisites 
- [Adicionar aula ](add_course_unit#editar-aula-escolher)

#### Ver aula
\>
```
!2
```

\<
```
Horarios de aula de 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!0
```

\<
```
Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```


#### Ver aula escolher / erro
\>
```
!2
```

\<
```
Escolher aula de Mestrado Integrado em Arquitetura para editar horario
1: Sistemas Construtivos Tradicionais: 4 year;  1 Semester
2: Sistemas Construtivos Tradicionais: 5 year;  1 Semester
0: Cancel
```

\>
```
!1
```

\<
```
Option not recognized

```

## Remover aula

### Remover aula vazio
\>
```
!3
```

\<
```
Remover aula de 50154C5: Sistemas Construtivos Tradicionais

0: Cancel
```

\>
```
!0
```
\<
```
Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```

### Remover aula
Prerequisites
- [Adicionar aula](#adicionar-aula-escolher)

#### Remover aula cancelar
\>
```
!3
```

\<
```
Remover aula de 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!0
```
\<
```
Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```

#### Remover aula escolher
\>
```
!3
```

\<
```
Remover aula de 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!1
```
\<
```
Removed 1MEEC_E02: T

Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```
#### Remover aula erro
\>
```
!3
```

\<
```
Remover aula de 50154C5: Sistemas Construtivos Tradicionais
1: 1MEEC_E02(T): 2ª feira 12:00-13:30 in B019
0: Cancel
```

\>
```
!2
```
\<
```
Option not recognized
```
## Cancel

\> 
```
!0
```

\< 
```
Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar aula
2: Editar horario de aula
0: Cancel
```

## Erro
\>
```
!4
```

\<
```
Option not recognized
```