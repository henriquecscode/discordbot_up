# Prerequisites
[Add courses](add_course.md#adicionar-curso)
[Choose course to edit](add_course#editar-curso-escolher)

\< 
```
Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar cadeira
2: Editar horario de cadeira
0: Cancel
```
# Tests
## Adicionar cadeira

### Adicionar cadeira escolher
First
\>
```
!1
```

\<
```
Cadeiras disponiveis em MIARQ: Mestrado Integrado em Arquitetura
<List of numbered course units>  
0: Cancel
```

\>
```
!1
```

\<
```
Added 50154C5: Sistemas Construtivos Tradicionais

Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar cadeira
2: Editar horario de cadeira
0: Cancel
```

Second
\>
```
!1
```

\<
```
Cadeiras disponiveis em faup: Faculdade de Arquitetura    
<List of numbered courses>  
0: Cancel
```

\>
```
!2
```

\<
```
Added 50154C5: Sistemas Construtivos Tradicionais

Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar cadeira
2: Editar horario de cadeira
0: Cancel
```
#### Adicionar cadeira repetido
\>
```
!1
```

\<
```
Cadeiras disponiveis em MIARQ: Mestrado Integrado em Arquitetura
<List of numbered course units>  
0: Cancel
```

\>
```
!1
```

\<
```
You already added 50154C5: Sistemas Construtivos Tradicionais

Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar cadeira
2: Editar horario de cadeira
0: Cancel
```
### Adicionar cadeira erro
```
!1
```

\<
```
Cadeiras disponiveis em MIARQ: Mestrado Integrado em Arquitetura
<List of numbered course units>  
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

## Editar cadeira


### Editar cadeira vazio
\> 
```
!2
```

\<
```
Escolher cadeira de Mestrado Integrado em Arquitetura para editar horario

0: Cancel
```

\>
```
!0
```

\<
```
Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar cadeira
2: Editar horario de cadeira
0: Cancel
```

### Editar cadeira 
Prerequisites
- [Adicionar cadeiras](#adicionar-cadeira)

#### Editar cadeira cancelar
\>
```
!2
```

\<
```
Escolher cadeira de Mestrado Integrado em Arquitetura para editar horario
1: Sistemas Construtivos Tradicionais: 4 year;  1 Semester
0: Cancel
```

\>
```
!0
```

\<
```
Escolheste o curso MIARQ: Mestrado Integrado em Arquitetura
1: Adicionar cadeira
2: Editar horario de cadeira
0: Cancel
```


#### Editar cadeira escolher
\>
```
!2
```

\<
```
Escolher cadeira de Mestrado Integrado em Arquitetura para editar horario
1: Sistemas Construtivos Tradicionais: 4 year;  1 Semester
0: Cancel
```

\>
```
!1
```

\<
```
Escolheste a cadeira 50154C5: Sistemas Construtivos Tradicionais
1: Adicionar aula
2: Ver horarios de aula
3: Remover aula
0: Cancel
```

#### Editar cadeira erro
\>
```
!2
```

\<
```
Escolher cadeira de Mestrado Integrado em Arquitetura para editar horario
1: Sistemas Construtivos Tradicionais: 4 year;  1 Semester
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
Escolheste a faculdade faup: Faculdade de Arquitetura
1: Adicionar curso
2: Editar horario de curso
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