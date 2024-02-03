```mermaid
graph TD
1[Receive message] 
--> 2[Extract FVector from image]
--> 3[Get Fvector dictionary from Redis]
--> 4[Get simularity score]
--> ie{End of dict}
--false--> 5{Simul > 0.8}
-.false -> next vec.-> 4 

5 --true--> 6[Compile record]
--> 7[Remove from Redis]
--> 8[Save to postgres]

ie --true--> 9[Compile unrec-record]
--> 8```