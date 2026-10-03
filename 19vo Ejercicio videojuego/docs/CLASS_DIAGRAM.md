# Class and Interaction Diagrams

`Exercise` and `ExerciseGenerator` are the only Python classes. `GameState`,
`FogEvent`, and `GameRules` below describe dictionary contents, not additional
classes.

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
      +dict fog_events
      +dict fog_notice
    }
    class FogEvent {
      <<dictionary>>
      +str status
      +str result
      +float started_at
      +float resolved_at
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
    GameState o-- FogEvent : stores by room
    GameState ..> GameRules : uses
```

```mermaid
sequenceDiagram
    participant P as Player
    participant U as Streamlit
    participant G as Game
    participant E as ExerciseGenerator
    P->>U: Submit answer
    U->>G: submit_answer()
    G->>G: Compare answer
    alt Correct answer
      G->>G: Award gold and advance room
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
only while health remains. The interface hides the answer form after defeat
or victory and keeps the exit and restart controls available.

## Fog event flow

Each room's 1-in-3 event roll and roulette result are stored in the game state,
so Streamlit reruns reuse them. The timer stays paused while the roulette is
offered or spinning.

`fog_notice` is added only after a free pass to announce the cleared room.

```mermaid
sequenceDiagram
    participant P as Player
    participant U as Streamlit
    participant F as Fog
    participant G as Game
    P->>U: Enter a room
    U->>F: check_room_event(state, room)
    alt No event
      U->>G: Refresh the room timer
    else Fog event offered
      U-->>P: Show roulette option; pause timer
      P->>U: Start roulette
      U->>F: start_roulette(state, room)
      loop While spinning
        U->>F: resolve_roulette(state, room)
        U-->>P: Animate pass and enemy outcomes
      end
      alt Pass
        F->>G: Advance one room without gold
      else Enemy
        F->>G: Keep room and current exercise
        U->>G: Start the normal room timer
      end
    end
```
