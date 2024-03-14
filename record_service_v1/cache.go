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
var courseStartTimes [16]time.Time

func InitCache(db uint8, closeChan chan string) {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "123456789", // no password set
		DB:       0,           // use default DB
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

func cache_get(student_id string) *time.Time {
	timestamp, err := rdb.Get(ctx, student_id).Result()
	if err == redis.Nil {
		return nil
	} else if err != nil {
		log.Fatal(err)
	}
	parsedtime, err := time.Parse(time.RFC3339, timestamp)
	if err != nil {
		log.Fatal("time parse fail", err)
	}
	return &parsedtime
}

func cache_set(student_id string, last_seen time.Time) {
	timestamp := last_seen.Format(time.RFC3339)
	err := rdb.Set(ctx, student_id, timestamp, 0)
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
