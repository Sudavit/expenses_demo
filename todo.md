# Expenses Demo Project - Roadmap

## Phase 1: Core Implementation (Legacy)
- [x] Define `Expense` SQLModel
- [x] Implement `ExpenseCategory` using `StrkEnum`
- [x] Initial `SQLRepository` implementation

## Phase 2: Repository Abstraction & In-Memory Logic
- [ ] **Tag Version**: `v0.2.0-repo-refactor`
- [ ] Define `BaseRepository` (Abstract Base Class)
- [ ] Implement `InMemoryRepository` (Dictionary-based storage)
- [ ] Refactor `expenses_demo.py` to use Repository Factory/Injection
- [ ] Separate Test Suites:
    - [ ] `tests/test_interface.py` (Common logic for all repos)
    - [ ] `tests/test_sql_repo.py` (Database-specific tests)
    - [ ] `tests/test_in_mem_repo.py` (Memory-specific tests)

## Phase 3: Performance & Integrity
- [ ] Implement Pre-Flight Benchmarking
- [ ] Validate `Decimal` precision across repository swaps
- [ ] Enforce "Kill-Switch" protocols for any future optimizations
