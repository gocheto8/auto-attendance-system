CREATE TABLE
    Class (class_id CHAR(3) PRIMARY KEY);

CREATE TABLE
    Student (
        student_id CHAR(5) PRIMARY KEY,
        full_name VARCHAR(255),
        class_id CHAR(5),
        st_group BOOLEAN,
        photo BYTEA
    );

CREATE TABLE
    Record (
        record_id SERIAL PRIMARY KEY,
        student_id CHAR(5),
        occasion_id INT,
        distance FLOAT,
        timestamp TIMESTAMP
    );

CREATE TABLE
    Course (
        course_id SERIAL PRIMARY KEY,
        course_name VARCHAR(255)
    );

CREATE TABLE
    Course_Class_Occasions (
        occasion_id SERIAL PRIMARY KEY,
        course_id INT,
        class_id CHAR(3),
        room VARCHAR(255),
        st_group BOOLEAN,
        weekly_group_swap BOOLEAN,
        start_time INT,
        end_time INT
    );

ALTER TABLE Student ADD CONSTRAINT fk_class FOREIGN KEY (class_id) REFERENCES Class (class_id);

ALTER TABLE Record ADD CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES Student (student_id);

ALTER TABLE Record ADD CONSTRAINT fk_occasion FOREIGN KEY (occasion_id) REFERENCES Course_Class_Occasions (occasion_id);

ALTER TABLE Course_Class_Occasions ADD CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES Course (course_id);

ALTER TABLE Course_Class_Occasions ADD CONSTRAINT fk_class_cco FOREIGN KEY (class_id) REFERENCES Class (class_id);