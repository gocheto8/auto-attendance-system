```mermaid
erDiagram
    Student{
        sting strudent_id PK
        string full_name
        string class_id FK
        bool group
        blob photo
    }

    Class{
        string class_id PK
    }

    Record{
        string record_id PK
        string strudent_id FK
        int occasion_id FK
        timestamp time

    }

    Course{
        int course_id PK
        string course_name
    }

    Course_Class_Occasions{
        int occasion_id PK
        int course_id FK
        string class_id FK
        string room
        bool group
        bool weekly_group_swap
        int start_time
        int end_time
    }

Class ||--|{ Student : ""
Record }|--|| Student : ""
Record }|--|| Course_Class_Occasions : ""
Course ||--|{ Course_Class_Occasions : ""
Class ||--|{ Course_Class_Occasions : ""
```