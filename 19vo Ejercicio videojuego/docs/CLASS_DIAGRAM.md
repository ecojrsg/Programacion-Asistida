# Class and Interaction Diagrams

`Exercise` and `ExerciseGenerator` are the only Python classes. `GameState`
and `GameRules` below describe dictionary contents, not additional classes.

```mermaid
classDiagram
    class Exercise {
      +str text
      +int answer
      +int time_seconds
      +str difficulty
    }
    class ExerciseGenerator {
      +rules_for(room) dict
      +generate(room) Exercise
    }
    class GameState {
      <<dictionary>>
      +int room
      +int health
      +int gold
      +bool finished
      +Exercise exercise
      +float started_at
      +dict pet
      +dict offers
    }
    class GameRules {
      <<dictionary>>
      +int n
      +int x
      +int z
      +int starting_gold
      +int rooms
    }
    ExerciseGenerator ..> Exercise : generates
    GameState o-- Exercise : contains
    GameState ..> GameRules : uses
```

```mermaid
sequenceDiagram
    participant P as Player
    participant U as Streamlit
    participant G as Game
    participant E as ExerciseGenerator
    participant H as Pet helpers
    P->>U: Submit answer
    U->>G: submit_answer()
    G->>G: Compare answer
    alt Correct answer
      G->>H: decay_pet(pet)
      G->>G: Award gold and advance room
      opt More rooms remain
        G->>H: new_room_offers()
      end
    else Wrong answer
      G->>G: Deduct x health points
    end
    alt More rooms remain
      G->>E: generate(current room)
      E-->>G: Exercise
      G->>G: Reset start time
    else Last room completed
      G->>G: Mark game finished
    end
    G-->>U: Correctness result and updated state
    U-->>P: Updated game screen
```

For an expired timer, the interface calls `timeout()` instead of
`submit_answer()`. It deducts `z` health points and starts another exercise
only while health remains. Pet meters and offers stay unchanged on timeout or
rerun. A purchase restores one meter, while clearing a room decays all meters
and creates new offers when another room remains. The interface hides the
answer form after defeat or victory and keeps the exit and restart controls
available.
