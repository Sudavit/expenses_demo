# Expenses Demo Project - Roadmap

## Phase 1: Core Implementation (Legacy)
- [x] Define `Expense` SQLModel
- [x] Implement `ExpenseCategory` using `StrEnum`
- [x] Initial `SQLRepository` implementation

## Phase 2: Repository Abstraction & In-Memory Logic
- [x] Define `ExpenseRepository` Protocol (TDD/Green)
- [x] Implement `DictExpenseRepository` with `deepcopy` safety
- [x] Implement `get_repository` factory function
- [x] Audit by Inspector (Blue): 100% Coverage & No Leaky Abstractions
- [x] **Tag Version**: `v0.2.0-stable-abstraction`

## Phase 3: Integration & Performance
- [ ] Refactor main application entry points to use `get_repository()`
- [ ] Implement side-by-side Benchmarking (SQL vs. In-Memory)
- [ ] Establish "Performance Kill-Switch" monitoring
- [ ] Expand Domain Logic (e.g., Reporting/Aggregation)
# Expenses Demo Project - Roadmap
