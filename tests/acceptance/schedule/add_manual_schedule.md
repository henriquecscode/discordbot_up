# Prerequisites
\>
```
!add_schedule
```

\< 
```
Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```

# Tests

## Add schedule

### Add schedule cancel

\>
```
!0
```

\<
```
Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```

### Add schedule cancel confirmation

\>
```
!4
```

\<
```
Adicionar horario manualmente
Formato:! <descricao de instituicao (por exemplo: faculdade, curso, cadeira)>; <aula>; <tipo de aula>; <dia (de 0 - 2ª - a 6 - domingo -)>; <hora inicio (HH:mm)>; <duracao (minutos)>; [<local>]
0: Cancel
```

\>
```
! FEUP MEIC; Seminars; Auditorio pequeno; 3; 17:00; 180; B017
```

\<
```
Command executed as 3:
Adicionar aula de FEUP MEIC de Seminars (Auditorio pequeno): na 5ª feira às 17:00-20:00  em B017
1: Confirmar
0: Cancelar
```

\>
```
!0
```

\<
```
Adicionar horario manualmente
Formato:! <<descricao de instituicao (por exemplo: faculdade, curso, cadeira)>; <aula>; <tipo de aula>; <dia (de 0 - 2ª - a 6 - domingo -)>; <hora inicio>; <duracao>; [<local>]
0: Cancel
```

\>
```
!0 
```

\<
```
Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```
## Add schedule confirm
\>
```
!4
```

\<
```
Adicionar horario manualmente
Formato:! <descricao de instituicao (por exemplo: faculdade, curso, cadeira)>; <aula>; <tipo de aula>; <dia (de 0 - 2ª - a 6 - domingo -)>; <hora inicio (HH:mm)>; <duracao (minutos)>; [<local>]
0: Cancel
```

\>
```
! FEUP MEIC; Seminars; Auditorio pequeno; 3; 17:00; 180; B017
```

\<
```
Command executed as 3:
Adicionar aula de FEUP MEIC de Seminars (Auditorio pequeno): na 5ª feira às 17:00-20:00  em B017
1: Confirmar
0: Cancelar
```


\>
```
!1
```

\<
```
Added  FEUP MEIC de Seminars (Auditorio pequeno): na 5ª feira às 17:00-20:00  em B017
Adicionar horario manualmente
Formato:! <<descricao de instituicao (por exemplo: faculdade, curso, cadeira)>; <aula>; <tipo de aula>; <dia (de 0 - 2ª - a 6 - domingo -)>; <hora inicio>; <duracao>; [<local>]
0: Cancel
```

## Remove schedule
### Remove schedule empty


\<
```
!5
```

\>
```
Remover horario manualmente

0: Cancel
```

\>
```
!0
```

\<
```
dd schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```

### Remove schedule cancel

#### Prerequisites
[Added manual schedule](#add-schedule-confirm)

#### Test

\<
```
!5
```

\>
```
Remover horario manualmente

0: Cancel
```

\>
```
!0
```

\<
```
dd schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```

\>
```
Remover horario manualmente
1: FEUP MEIC de Seminars (Auditorio pequeno): na 5ª feira às 17:00-20:00  em B017
0: Cancel
```

\<
```
!0
```

\>
```
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```
### Remove schedule choose

#### Prerequisites
[Added manual schedule](#add-schedule-confirm)

#### Test

\<
```
!5
```

\>
```
Remover horario manualmente

0: Cancel
```

\>
```
!0
```

\<
```
dd schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```

\>
```
Remover horario manualmente
1: FEUP MEIC de Seminars (Auditorio pequeno): na 5ª feira às 17:00-20:00  em B017
0: Cancel
```

\<
```
!1
```

\>
```
Removed FEUP MEIC de Seminars (Auditorio pequeno): na 5ª feira às 17:00-20:00  em B017

Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
4: Adicionar manualmente
5: Remover horario manual
0: Cancel
```