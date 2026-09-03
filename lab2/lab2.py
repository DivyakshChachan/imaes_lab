"""
AI401 - Expert Systems Lab
Experiment 2: Production Rules and the Match Phase
"""

import time
import random

class Rule:
    """
    Represents an IF-THEN production rule.
    - id: Unique rule identifier (e.g., 'R1')
    - conditions: List of condition strings (e.g., ['fever', 'cough'] or ['fever', 'NOT flu'])
    - conclusion: Fact derived when the rule fires (e.g., 'viral_infection')
    """
    def __init__(self, rule_id: str, conditions: list, conclusion: str):
        self.id = rule_id
        self.conditions = conditions
        self.conclusion = conclusion

    def __repr__(self):
        cond_str = " AND ".join(self.conditions)
        return f"[{self.id}] IF {cond_str} THEN {self.conclusion}"


class ProductionSystemMatcher:
    """
    Implements the Match Phase of the Recognize-Act Cycle.
    Matches rules against Working Memory (WM) to construct the Conflict Set.
    """
    def __init__(self, rules: list):
        self.rules = rules

    def is_rule_applicable(self, rule: Rule, working_memory: set) -> bool:
        """
        Determines whether a rule is applicable:
        1. All positive conditions must be in working_memory.
        2. All negated conditions ('NOT fact') must be ABSENT from working_memory.
        3. Refractoriness: Rule conclusion must NOT already be in working_memory.
        """
        # Refractoriness check: prevent rule from firing if conclusion already exists
        if rule.conclusion in working_memory:
            return False

        for condition in rule.conditions:
            if condition.startswith("NOT "):
                negated_fact = condition[4:].strip()
                # Negated condition satisfied if fact is NOT in WM
                if negated_fact in working_memory:
                    return False
            else:
                # Positive condition satisfied if fact IS in WM
                if condition not in working_memory:
                    return False

        return True

    def compute_conflict_set(self, working_memory: set) -> list:
        """Collects all rules that currently match working memory."""
        conflict_set = []
        for rule in self.rules:
            if self.is_rule_applicable(rule, working_memory):
                conflict_set.append(rule)
        return conflict_set


def main_part1():
    print("=" * 70)
    print("PART 1: PRODUCTION RULES & MATCH PHASE DEMONSTRATION")
    print("=" * 70)

    # Define Rule Base for Medical Diagnosis
    rule_base = [
        Rule("R1", ["fever", "cough"], "viral_infection"),
        Rule("R2", ["viral_infection", "runny_nose"], "common_cold"),
        Rule("R3", ["fever", "spots"], "measles"),
        Rule("R4", ["fever", "stiff_neck"], "meningitis"),
        Rule("R5", ["cough", "chest_pain"], "pneumonia"),
    ]

    print("\n1. Defined Rule Base:")
    for rule in rule_base:
        print(f"   {rule}")

    matcher = ProductionSystemMatcher(rule_base)

    # Test Case A
    wm_a = {"fever", "cough"}
    cs_a = matcher.compute_conflict_set(wm_a)
    print(f"\n2. Working Memory: {sorted(list(wm_a))}")
    print("   Conflict Set (Applicable Rules):")
    for r in cs_a:
        print(f"     -> {r}")

    # Test Case B (Adding runny_nose and viral_infection)
    wm_b = {"fever", "cough", "runny_nose", "viral_infection"}
    cs_b = matcher.compute_conflict_set(wm_b)
    print(f"\n3. Working Memory: {sorted(list(wm_b))}")
    print("   Conflict Set (Applicable Rules):")
    for r in cs_b:
        print(f"     -> {r}")


def exercise_1():
    print("\n" + "=" * 70)
    print("EXERCISE 1: DYNAMIC CONFLICT SET TRACKING (WM FACT INSERTION)")
    print("=" * 70)

    rule_base = [
        Rule("R1", ["fever"], "check_infection"),
        Rule("R2", ["fever", "cough"], "viral_infection"),
        Rule("R3", ["fever", "cough", "spots"], "measles"),
        Rule("R4", ["measles"], "quarantine_patient"),
    ]

    matcher = ProductionSystemMatcher(rule_base)
    working_memory = set()

    print("\nStarting with Empty Working Memory...")
    facts_to_add = ["fever", "cough", "spots", "measles"]

    for step, fact in enumerate(facts_to_add, start=1):
        working_memory.add(fact)
        conflict_set = matcher.compute_conflict_set(working_memory)
        print(f"\nStep {step}: Added fact '{fact}'")
        print(f"  Working Memory: {sorted(list(working_memory))}")
        print(f"  Conflict Set Size: {len(conflict_set)}")
        print("  Conflict Set Rules:")
        if conflict_set:
            for r in conflict_set:
                print(f"     -> {r}")
        else:
            print("     -> [Empty Set]")


def exercise_2():
    print("\n" + "=" * 70)
    print("EXERCISE 2: EXTENDED MATCHER WITH NEGATED CONDITIONS ('NOT fact')")
    print("=" * 70)

    rule_base = [
        Rule("R1", ["fever", "NOT flu"], "suspect_measles"),
        Rule("R2", ["fever", "flu"], "treat_flu"),
        Rule("R3", ["cough", "NOT fever"], "allergic_cough"),
    ]

    matcher = ProductionSystemMatcher(rule_base)

    print("\nRule Base with Negated Conditions:")
    for rule in rule_base:
        print(f"   {rule}")

    # Case 1: Fever present, flu absent -> R1 matches
    wm1 = {"fever"}
    cs1 = matcher.compute_conflict_set(wm1)
    print(f"\nCase 1 | WM = {sorted(list(wm1))}")
    print("  Conflict Set:")
    for r in cs1:
        print(f"     -> {r}")

    # Case 2: Adding 'flu' to WM -> R1 no longer matches, R2 matches
    wm2 = {"fever", "flu"}
    cs2 = matcher.compute_conflict_set(wm2)
    print(f"\nCase 2 | WM = {sorted(list(wm2))} ('flu' added)")
    print("  Conflict Set:")
    for r in cs2:
        print(f"     -> {r}")

    # Case 3: Cough present, fever absent -> R3 matches
    wm3 = {"cough"}
    cs3 = matcher.compute_conflict_set(wm3)
    print(f"\nCase 3 | WM = {sorted(list(wm3))}")
    print("  Conflict Set:")
    for r in cs3:
        print(f"     -> {r}")


def exercise_3():
    print("\n" + "=" * 70)
    print("EXERCISE 3: PERFORMANCE SCALING & RETE ALGORITHM ANALYSIS")
    print("=" * 70)

    random.seed(42)
    fact_pool = [f"fact_{i}" for i in range(1, 201)]

    # Generate 1,000 random rules
    large_rule_base = []
    for i in range(1, 1001):
        num_conds = random.randint(1, 4)
        conds = random.sample(fact_pool, num_conds)
        # 10% chance of a negated condition
        if random.random() < 0.1 and len(conds) > 1:
            conds[0] = f"NOT {conds[0]}"
        conclusion = f"derived_fact_{i}"
        large_rule_base.append(Rule(f"R{i}", conds, conclusion))

    matcher = ProductionSystemMatcher(large_rule_base)

    print(f"\nGenerated Rule Base Size: {len(large_rule_base)} rules")
    
    # Benchmarking across different WM sizes
    wm_sizes = [10, 50, 100, 200, 500]
    results = []

    print("\nBenchmark Execution (time.perf_counter):")
    print(f"{'WM Size':<10} | {'Conflict Set Size':<18} | {'Match Time (ms)':<15} | {'Ops per Second':<15}")
    print("-" * 65)

    for size in wm_sizes:
        current_wm = set(random.sample(fact_pool, min(size, len(fact_pool))))
        
        # Timing the match phase
        start_time = time.perf_counter()
        # Perform 50 iterations to get accurate average timing
        iterations = 50
        for _ in range(iterations):
            cs = matcher.compute_conflict_set(current_wm)
        end_time = time.perf_counter()

        avg_time_ms = ((end_time - start_time) / iterations) * 1000
        ops_per_sec = 1000 / avg_time_ms if avg_time_ms > 0 else 0
        results.append((size, len(cs), avg_time_ms))

        print(f"{size:<10} | {len(cs):<18} | {avg_time_ms:<15.4f} | {ops_per_sec:<15.1f}")

    print("\nWhy RETE Algorithm Exists:")
    print("  1. Naive Matcher Complexity: O(|Rules| * |Conditions| * |WM|)")
    print("     The naive matcher re-evaluates EVERY rule against the ENTIRE Working Memory")
    print("     on every single recognize-act cycle, wasting computation on unchanged rules.")
    print("  2. RETE Algorithm Solution:")
    print("     - Constructs a rooted directed acyclic graph (Rete Network).")
    print("     - Uses Alpha Memories (1-input nodes) to filter facts matching single conditions.")
    print("     - Uses Beta Memories (2-input nodes) to join conditions across rules.")
    print("     - Caches partial matches statefully across cycles.")
    print("     - Time complexity reduces from O(|Rules|) to O(dWM) — proportional ONLY to the")
    print("       number of facts changed, NOT the size of the rule base!")


if __name__ == "__main__":
    main_part1()
    exercise_1()
    exercise_2()
    exercise_3()