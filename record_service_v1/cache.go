package main

import (
	"context"
	"encoding/csv"
	"log"
	"os"
	"time"

	"github.com/redis/go-redis/v9"
)

var ctx context.Context = context.Background()
var rdb *redis.Client
var courseStartTimes [12]time.Time

func InitCache(db uint8, closeChan chan string) {
	rdb = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "123456789",
		DB:       0,
	})
	log.Printf("Redis connection ready on db#%d\n", db)

	go func() {
		reason := <-closeChan
		log.Printf("Redis client exiting r: %s\n", reason)
		rdb.Close()
	}()

	parseCourseStartTimes("./course_start_times.csv")
	go purge_job()
}

func Cache_get(student_id string) (*time.Time, error) {
	timestamp, err := rdb.Get(ctx, student_id).Result()
	if err != nil {
		return nil, err
	}
	parsedtime, err := time.Parse(time.RFC3339, timestamp)
	if err != nil {
		log.Fatal("time parse fail", err)
	}
	return &parsedtime, nil
}

func Cache_set(student_id string, last_seen time.Time) {
	timestamp := last_seen.Format(time.RFC3339)
	err := rdb.Set(ctx, student_id, timestamp, 0).Err()
	if err != nil {
		log.Fatal("Save to cache failed", err)
	}
}

func purge_cache() {
	err := rdb.FlushDB(ctx).Err()
	if err != nil {
		log.Fatal(err)
	}
}

func purge_job() {
	for {
		for _, t := range courseStartTimes {
			now := time.Now()
			startTime := time.Date(now.Year(), now.Month(), now.Day(), t.Hour(), t.Minute(), 0, 0, now.Location())
			if now.After(startTime) {
				continue
			}
			delay := time.Since(startTime)
			time.Sleep(delay - 10*time.Second)
			purge_cache()
		}
	}

}

func parseCourseStartTimes(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal("Course times open:", err)
	}
	defer file.Close()
	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatal("Course times csv: :", err)
	}

	for i, record := range records {
		if len(record) != 1 {
			log.Fatal("Error: invalid CSV format")
		}

		t, err := time.Parse("15:04", record[0])
		if err != nil {
			log.Fatal("Error:", err)
		}
		courseStartTimes[i] = t
	}
}
