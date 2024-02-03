```mermaid
graph TD
1[Class end]
--> 2[Get remaining Redis records]
--> re{Records empty?}
--false--> 3[Compile unattendence record]
--> 4[Save record to Postgres] -...-> re

re --true--> 5[Get next on curiculum \nfor all classrooms]
--> 6[For each class]
--> 7[Get all student \nrecords from postgres]
--> 8[Load into Redis] -.-> 6
6 --end---> 9[Wait for class end] -.-> 1
