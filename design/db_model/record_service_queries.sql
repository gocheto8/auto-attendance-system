-- OCCASION QUERY
WITH
    St_info as (
        SELECT
            st.student_id,
            st.class_id,
            st.st_group
        FROM
            Student as st
        WHERE
            st.student_id = "<ST_ID>"
    )
SELECT
    CCO.occasion_id
FROM
    Course_Class_Occasions CCO
    JOIN St_info sti ON sti.class_id = CCO.class_id
    AND (
        sti.st_group = CCO.st_group
        OR CCO.st_group IS Null
    )
WHERE
    "<TIME>" > CCO.start_time
    AND "<TIME>" < CCO.end_time
    AND "<ROOM>" = CCO.room;

-- INSERT RECORD
INSERT INTO
    Record (student_id, occasion_id, timestamp)
VALUES
    (
        'your_student_id',
        your_occasion_id,
        'your_timestamp'
    );