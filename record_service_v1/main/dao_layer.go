package main

import (
	"database/sql"
	"log"
	"time"
)

var db *sql.DB

func connectToDb() {
	connStr := "postgres://postgres:123456789@localhost/aas_db"
	var err error
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
}

func GetCourseOccasion(timestamp float64, student_id [5]rune) {
	pt, err := parseTimestamp(timestamp)
	if err != nil {
		log.Fatal(err)
	}
	seconds := secondsSinceBeginningOfWeek(pt)
	
}

func getGroupOfStudent(student_id [5]rune)

func secondsSinceBeginningOfWeek(timestamp time.Time) int {
	weekStart := timestamp.Truncate(24 * time.Hour).Add(-time.Duration((int(timestamp.Weekday())+6)%7) * 24 * time.Hour)
	seconds := int(timestamp.Sub(weekStart).Seconds())

	return seconds
}

func parseTimestamp(timestamp float64) (time.Time, error) {
	seconds := int64(timestamp)
	fractionalSeconds := int64((timestamp - float64(seconds)) * 1e9)
	parsedTime := time.Unix(seconds, fractionalSeconds)

	return parsedTime, nil
}
