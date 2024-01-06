# Prerequisites
[Author commands](../author/author.md)

# Person 1
Every command shall be prefaced by `!_author 1`
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
!FEUP; aula teste; teste; 1; 14:00; 60; sala teste
```

\<
```
Adicionar aula de FEUP de aula teste (teste): na 3ª feira às 14:00-15:00  em sala teste
1: Confirmar
0: Cancelar
```

\>
```
!1
```

\<
```
Added  FEUP de aula teste (teste): na 3ª feira às 14:00-15:00  em sala teste
Adicionar horario manualmente
Formato:! <<descricao de instituicao (por exemplo: faculdade, curso, cadeira)>; <aula>; <tipo de aula>; <dia (de 0 - 2ª - a 6 - domingo -)>; <hora inicio>; <duracao>; [<local>]
```