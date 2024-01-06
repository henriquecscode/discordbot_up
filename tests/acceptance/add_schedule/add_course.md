# Prerequisites
[Add faculties](add_faculty.md#adicionar-faculdade)
[Choose faculty](add_faculty#editar-faculdade-escolher)

\< 
```
Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
0: Cancel
```
# Tests
## Adicionar curso

### Adicionar curso escolher
First
\>
```
!1
```

\<
```
Cursos disponiveis em faup: Faculdade de Arquitetura    
<List of numbered courses>  
0: Cancel
```

\>
```
!1
```

\<
```
Added MIARQ: Mestrado Integrado em Arquitetura

Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
0: Cancel
```

Second
\>
```
!1
```

\<
```
Cursos disponiveis em faup: Faculdade de Arquitetura    
<List of numbered courses>  
0: Cancel
```

\>
```
!2
```

\<
```
Added MIDPP: Inovação Digital para Práticas de Projeto

Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
0: Cancel
```
#### Adicionar curso repetido
\>
```
!1
```

\<
```
Cursos disponiveis em faup: Faculdade de Arquitetura    
<List of numbered courses>  
0: Cancel
```

\>
```
!1
```

\<
```
You already added MIARQ: Mestrado Integrado em Arquitetura

Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
0: Cancel
```
### Adicionar curso erro
\>
```
!1
```

\<
```
Cursos disponiveis em faup: Faculdade de Arquitetura    
<List of numbered courses>  
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
## Editar curso

### Editar curso vazio
\> 
```
!2
```

\<
```
Escolher curso de faup para editar horario

0: Cancel
```

\>
```
!0
```

\<
```
Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
0: Cancel
```

### Editar curso 
Prerequsites
- [Adicionar cursos](#adicionar-curso)

#### Editar curso cancelar
\>
```
!2
```

\<
```
Escolher curso de faup para editar horario
1: MIARQ: Mestrado Integrado em Arquitetura
2: MIDPP: Inovação Digital para Práticas de Projeto
0: Cancel
```

\>
```
!0
```

\<
```
Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
0: Cancel
```


#### Editar curso escolher
\>
```
!2
```

\<
```
Escolher curso de faup para editar horario
1: MIARQ: Mestrado Integrado em Arquitetura
2: MIDPP: Inovação Digital para Práticas de Projeto
0: Cancel
```

\>
```
!1
```

\<
```
Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar cadeira
2: Editar horario de cadeira
0: Cancel
```

#### Editar curso erro
\>
```
!2
```

\<
```
Escolher curso de faup para editar horario
1: MIARQ: Mestrado Integrado em Arquitetura
2: MIDPP: Inovação Digital para Práticas de Projeto
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
Add schedule
1: Adicionar faculdade
2: Escolher faculdade para editar horario
3: Editar horario de curso
0: Cancel
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