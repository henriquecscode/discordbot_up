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
0: Cancel
```
# Tests

## Adicionar faculdade
### Adicionar faculdade cancelar
### Adicionar faculdade escolher
First  
\>
```
!1
```
\<
```
Faculdades disponiveis  
<List of numbered colleges>  
0: Cancel
```
\>
```
!1
```

\<
```
Added faup: Faculdade de Arquitetura

Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
0: Cancel
```

Second  
\>
```
!1
```
\<
```
Faculdades disponiveis
<List of numbered colleges>
0: Cancel
```
\>
```
!2
```

\<
```
Added fbaup: Faculdade de Belas Artes

Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
0: Cancel
```

#### Adicionar faculdade repetida
\>
```
!1
```
\<
```
Faculdades disponiveis
<List of numbered colleges>
0: Cancel
```
\>
```
!1
```

\<
```
You already added faup: Faculdade de Arquitetura

Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
0: Cancel
```
### Adicionar faculdade erro
\>
```
!1
```
\<
```
Faculdades disponiveis  
<List of numbered colleges>  
0: Cancel
```
\>
```
!<n+1>
```

\<
```
Option not recognized
```
```
## Editar faculdade

### Editar faculdade vazio

\>
```
!2
```
\<
```
Inscrito em faculdades

0: Cancel
```

### Editar faculdade
Prerequisites
-  [Adicionar faculdades](#adicionar-faculdade)

#### Editar faculdade cancelar

\>
```
!2
```

\<
```
Inscrito em faculdades
1: faup: Faculdade de Arquitetura
2: fbaup: Faculdade de Belas Artes
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
0: Cancel
```
#### Editar faculdade escolher
\>
```
!2
```

\<
```
Inscrito em faculdades
1: faup: Faculdade de Arquitetura
2: fbaup: Faculdade de Belas Artes
0: Cancel
```

\>
```
!1
```
\<
```
Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
0: Cancel
```

#### Editar faculdade erro
```
!2
```

\<
```
Inscrito em faculdades
1: faup: Faculdade de Arquitetura
2: fbaup: Faculdade de Belas Artes
0: Cancel
```

\>
```
!3
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
Canceled
```

## Erro
\>
```
!3
```

\<
```
Option not recognized
```