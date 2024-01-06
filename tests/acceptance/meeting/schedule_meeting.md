# Prerequisite

[Added simple schedule](../schedule/view_schedule.md)
[Added person 1's schedule](./schedule_meeting_data.md)

\>
```
!schedule_meeting \<@1\>
```

\<
```
Schedule meeting
Choose the day and time of meeting
Formato:! <dia (dd/MM/YYYY)>; <hora (HH:mm)>; <duracao (minutos)>
0: Cancel
```
# Test

## Incompatible with own schedule

\>
```
!11/01/2024; 16:30; 60
```
\<
```
You have a class at that time: FEUP MEIC de Seminars (Auditorio pequeno): na 5ª feira às 17:00-20:00  em B017
Overlaps with your proposed meeting on 11/01/2024 at 16:30-17:30
1: Try another time
2: Schedule it anyway
0: Cancel

```

## Incompatible with other persons schedule


\>
```
!9/01/2024; 13:30; 60
```

\<
```
Users not available on 09/01/2024 at 13:30-14:30: <@1>

1: Try another time
2: Schedule it anyway
0: Cancel
```

## Available for meeting

\>
```
!09/01/2024 ; 15:00 ; 60
```

\<
```
You can have a meeting at that time
1: Choose another time
2: Schedule it
0: Cancel
```

\>
```
!2
```


\<
```
Meeting scheduled on your calendar on 09/01/2024 at 15:00-16:00 with <@5>
```