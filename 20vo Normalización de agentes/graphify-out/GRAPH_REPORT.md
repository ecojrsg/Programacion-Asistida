# Graph Report - 20vo Normalización de agentes  (2026-10-05)

## Corpus Check
- Corpus is ~4,580 words - fits in a single context window. You may not need a graph.

## Summary
- 98 nodes · 192 edges · 14 communities (6 shown, 8 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 0.89)
- Token cost: unavailable (host extraction-agent usage is not exposed; numeric zeros in generated metadata are placeholders).

## Community Hubs (Navigation)
- Answer Rules and Rewards
- Streamlit Rendering and Timer
- Session and Configuration Flow
- Arithmetic Exercise Generation
- Turn and Timeout Helpers
- Configuration Loading and Expiration
- Operation Regression Tests
- Restart and Initialization Tests
- Local Guidelines and Tooling
- Difficulty Boundary Tests
- Answer Interface Tests
- Victory and Defeat Tests
- JSON Loading Tests
- Project Package Metadata

## God Nodes (most connected - your core abstractions)
1. `ExerciseGenerator` - 29 edges
2. `new_game()` - 17 edges
3. `main()` - 16 edges
4. `load_json()` - 13 edges
5. `submit_answer()` - 13 edges
6. `timeout()` - 11 edges
7. `main()` - 10 edges
8. `render_game()` - 9 edges
9. `refresh_timer()` - 7 edges
10. `_start_turn()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `ExerciseGenerator` --references--> `config/exercises.json ordered difficulty catalog`  [INFERRED]
  game.py → docs/PLAN.md
- `main()` --references--> `config/exercises.json ordered difficulty catalog`  [EXTRACTED]
  app.py → docs/PLAN.md
- `main()` --references--> `config/settings.json`  [EXTRACTED]
  app.py → docs/PLAN.md
- `GameState dictionary concept` --references--> `Exercise`  [EXTRACTED]
  docs/CLASS_DIAGRAM.md → game.py
- `new_game()` --references--> `GameState dictionary concept`  [EXTRACTED]
  game.py → docs/CLASS_DIAGRAM.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared dictionary-state transition flow** — game_new_game, game_submit_answer, game_timeout, game__start_turn, docs_class_diagram_gamestate [EXTRACTED 1.00]

## Communities (14 total, 8 thin omitted)

### Community 0 - "Answer Rules and Rewards"
Cohesion: 0.12
Nodes (12): Unimplemented future improvements, Timed arithmetic, rewards, damage and ending rules, Castillo Matemático MVP plan, Game-rule and Streamlit interface regressions, new_game(), submit_answer(), test_correct_answer(), test_game_rules() (+4 more)

### Community 1 - "Streamlit Rendering and Timer"
Cohesion: 0.22
Nodes (5): refresh_timer(), render_controls(), render_game(), render_round(), render_status()

### Community 2 - "Session and Configuration Flow"
Cohesion: 0.18
Nodes (8): Streamlit >=1.40,<2 runtime dependency, main(), render_start(), GameRules settings dictionary concept, GameState dictionary concept, config/exercises.json ordered difficulty catalog, config/settings.json, _start_turn

### Community 3 - "Arithmetic Exercise Generation"
Cohesion: 0.24
Nodes (3): Class and interaction diagrams, Exercise, ExerciseGenerator

### Community 7 - "Restart and Initialization Tests"
Cohesion: 0.33
Nodes (3): main(), test_app_controls(), test_new_game()

### Community 8 - "Local Guidelines and Tooling"
Cohesion: 0.40
Nodes (5): Generated Graphify analysis artifacts, Local agent guidelines, Authorship confirmation and language policy, Requested quality tooling, not declared dependencies, streamlit-autorefresh >=1.0.1,<2 runtime dependency

## Knowledge Gaps
- **8 isolated node(s):** `castillo-matematico`, `_start_turn`, `Streamlit >=1.40,<2 runtime dependency`, `streamlit-autorefresh >=1.0.1,<2 runtime dependency`, `Requested quality tooling, not declared dependencies` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 50 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ExerciseGenerator` connect `Arithmetic Exercise Generation` to `Answer Rules and Rewards`, `Streamlit Rendering and Timer`, `Session and Configuration Flow`, `Turn and Timeout Helpers`, `Operation Regression Tests`, `Restart and Initialization Tests`, `Difficulty Boundary Tests`?**
  _High betweenness centrality (0.399) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `ExerciseGenerator` (e.g. with `refresh_timer()` and `render_controls()`) actually correct?**
  _`ExerciseGenerator` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `castillo-matematico`, `_start_turn`, `Streamlit >=1.40,<2 runtime dependency` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Answer Rules and Rewards` be split into smaller, more focused modules?**
  _Cohesion score 0.12105263157894737 - nodes in this community are weakly interconnected._
- **Why does `load_json()` connect `Configuration Loading and Expiration` to `Streamlit Rendering and Timer`, `Session and Configuration Flow`, `Turn and Timeout Helpers`, `Operation Regression Tests`, `Restart and Initialization Tests`, `Difficulty Boundary Tests`, `Answer Interface Tests`, `Victory and Defeat Tests`, `JSON Loading Tests`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `main()` (e.g. with `test_app_answers()` and `test_app_controls()`) actually correct?**
  _`main()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Why does `new_game()` connect `Answer Rules and Rewards` to `Streamlit Rendering and Timer`, `Session and Configuration Flow`, `Arithmetic Exercise Generation`, `Turn and Timeout Helpers`, `Operation Regression Tests`, `Restart and Initialization Tests`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
## Extraction Limitations

- Graph health warning: 20 dangling-endpoint edges and 18 same-endpoint relationship groups flagged for potential collapse in this undirected graph. The undeclared endpoints name standard-library or third-party imports. Treat the graph as an aid, not a complete call graph.
- Semantic extraction includes documentation concepts, not only executable symbols. The documented turn-reset helper has a separate semantic ID from its AST symbol; this does not mean there are two implementations.
- AST extraction reported no symbols for `pyproject.toml`; package metadata remains in the source manifest.
- Token usage for the host extraction agent is unavailable. Reported numeric zeros are unmeasured placeholders, not evidence of a free run.
- Documentation guidelines mention optional tools; these are not installed runtime dependencies.
