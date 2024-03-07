package main

import (
	"database/sql"
	"log"
	"sync"
	"time"

	_ "github.com/lib/pq"
)

type MessageBody struct {
	Id        string  `json:"id"`
	Timestamp float64 `json:"time"`
	Person_id uint8   `json:"person_id"`
	Distance  float32 `json:"distance"`
}

var db *sql.DB
var mu sync.Mutex

const occasionQuery string = `WITH
St_info as (
	SELECT
		st.student_id,
		st.class_id,
		st.st_group
	FROM
		Student as st
	WHERE
		st.student_id = $1
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
$2 > CCO.start_time
AND $2 < CCO.end_time
AND "$3 = CCO.room;`

var occasionStmt *sql.Stmt

const insertRecordQuery string = `INSERT INTO
Record (student_id, occasion_id, timestamp)
VALUES
(
	$1,
	$2,
	$3
);`

var insertRecordStmt *sql.Stmt

func ConnectToDb() {
	mu.Lock()
	connStr := "postgres://postgres:123456789@localhost/aas_db"
	var err error
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Postgres connection established.")

	occasionStmt, err = db.Prepare(occasionQuery)
	if err != nil {
		log.Fatal(err)
	}

	insertRecordStmt, err = db.Prepare(insertRecordQuery)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Finished preparing statements.")
	mu.Unlock()
}

func secondsSinceBeginningOfWeek(timestamp time.Time) int {
	weekStart := timestamp.Truncate(24 * time.Hour).Add(-time.Duration((int(timestamp.Weekday())+6)%7) * 24 * time.Hour)
	seconds := int(timestamp.Sub(weekStart).Seconds())

	return seconds
}

func parseTimestamp(timestamp float64) time.Time {
	seconds := int64(timestamp)
	fractionalSeconds := int64((timestamp - float64(seconds)) * 1e9)
	parsedTime := time.Unix(seconds, fractionalSeconds)

	return parsedTime
}

func GetCourseOccasion(body *MessageBody) (int, error) {
	pt := parseTimestamp(body.Timestamp)

	seconds := secondsSinceBeginningOfWeek(pt)
	var occasion_id *int
	mu.Lock()
	err := occasionStmt.QueryRow(body.Person_id, seconds, body.Id).Scan(&occasion_id)
	if err != nil {
		log.Println(err)
	}
	mu.Unlock()
	return *occasion_id
}

func InsertRecord(body *MessageBody, occasion_id int) *sql.Result {
	mu.Lock()
	result, err := insertRecordStmt.Exec(body.Person_id, occasion_id, body.Timestamp, body.Distance)
	if err != nil {
		log.Fatal(err)
	}
	mu.Unlock()
	return &result
}
