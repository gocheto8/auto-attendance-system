``` mermaid
graph TD
Tc((Teacher)) ----> 1[User Auth]
Tc ----> 2[Viewing records] 
--> 3[Filtering and sorting]
2 --> 4[Mark as wrong]
2 --> 5[Delete]
Tc ----> 9[Review record]
2 --> 10[Handle unrec-records]

St((Student)) ----> 1
St ----> 6[View all personal records]
6 --> 3
St ----> 7[View personal absence records] 
--> 8[Request review]
8 -.-> 9
```

