# Tests

## No Number

\>
```
!reserve_office
```

\<
```
You have to input your student number. Ex.: !add_number <number>
```


## Add office

### Prerequisites
[Add number](../add_number/add_number.md)

### Add office cancel

\>
```
!reserve_office
```

\<
```
Formato:! <dia (dd/MM/YYYY)>; <hora (HH:mm)>; <duration (minutos)>; [<motivation>]; [<special request>]
0: Cancel
```

\>
```
!0
```

\<
```
Canceled
```

### Add office success
\>
```
!reserve_office
```

\<
```
Formato:! <dia (dd/MM/YYYY)>; <hora (HH:mm)>; <duration (minutos)>; [<motivation>]; [<special request>]
0: Cancel
```

\>
```
! 07/01/2024; 10:00; 60; Seminars presentation preparation;
```

\<
```
Office reservation 07/01/2024 at 10:00-11:00 with motivation "Seminars presentation preparation"
1: Change parameters
2: Confirm
0: Cancel
```

\>
```
!2
```

\>
```
Successfully reserved office
```

Note: Reservation will only succeed if the office is available at the specified time.
