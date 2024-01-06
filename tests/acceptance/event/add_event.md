# Prerequisites

## Adding event 

\>
```
!add_event
```
\<
```
You have to specify the date of the event and title. You can also specify the hour. Ex.: !add_event Programming Test 31/12/2023 15:00
```
\>
```
!add_event test
```
\<
```
You have to specify the date of the event and title. You can also specify the hour. Ex.: !add_event Programming Test 31/12/2023 15:00
```
\>
```
!add_event test 31/12/2023 15:00
```
\<
```
This date is from the past, please only setup future events
```
\>
```
!add_event test 31/12/2024 15:00
```
\<
```
Event 'test' at 31-12-2024 15:00 saved to your events. Do !events to check your future events
```
\>
```
!add_event test1 31/12/2024 16:00
```
\<
```
Event 'test1' at 31-12-2024 16:00 saved to your events. Do !events to check your future events
```

## Checking and deleting events
\>
```
!events
```
\<
```
Your future events:
Your future events:
1: test at 31-12-2024 15:00
2: test1 at 31-12-2024 16:00

In order to delete events do !events delete #
```
\>
```
!events delete 1
```
\<
```
Event test deleted
```