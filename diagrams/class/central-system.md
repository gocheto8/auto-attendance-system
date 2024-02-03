```mermaid
classDiagram
  class CentralSystem {
    - message_brokers: MessageBrokers
    - fvector_extractor: FVectorExtractor
    - fvec_matcher: FVecMatcher
    - redis_db: RedisDB
    - postgres: Postgres
    ____
    + process_messages(): void
    + save_record(record: MatchedRecord): void
  }

  class MessageBrokers {
    ____
    + receive_messages(): void
  }

  class FVectorExtractor {
    ____
    + extract_feature_vector(image: Image): FeatureVector
  }

  class FVecMatcher {
    ____
    + match_records(feature_vector: FeatureVector): MatchedRecord
  }

  class RedisDB {
    ____
    + find_records(): List<Record>
  }

  class Postgres {
    ____
    + save_record(record: MatchedRecord): void
  }

  class Image {
    ____
  }

  class FeatureVector {
    ____
  }

  class MatchedRecord {
    - feature_vector: FeatureVector
    - timestamp: Timestamp
    - worker_id: int
    - student_id: int
    - match_percentage: float
    ____
    + constructor(feature_vector: FeatureVector, timestamp: Timestamp, worker_id: int, student_id: int, match_percentage: float)
  }

  class Record {
    - feature_vector: FeatureVector
    - user_id: int
    ____
  }

  class Timestamp {
    ____
  }

  CentralSystem --|> MessageBrokers
  CentralSystem --|> FVectorExtractor
  CentralSystem --|> FVecMatcher
  CentralSystem --|> RedisDB
  CentralSystem --|> Postgres
  FVecMatcher --|> RedisDB
  CentralSystem --|> MatchedRecord
  CentralSystem --|> Record
  MatchedRecord --|> FeatureVector
  Record --|> FeatureVector
