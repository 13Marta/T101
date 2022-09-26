from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': code_max + j
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_oper: items
            },
            'then': i + j + 1
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = generate_stairway_rules(code_max, n_max, n_generate - 1, log_oper_choice)
    log_oper = choice(log_oper_choice)  # not means and-not (neither)
    if n_max < 2:
        n_max = 2
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_oper: items
        },
        'then': 0
    }
    rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': randint(1, code_max)
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_seq_facts(M):
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, M):
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    return facts


# samples:
print(generate_simple_rules(100, 4, 10))
print(generate_random_rules(100, 4, 10))
print(generate_stairway_rules(100, 4, 10, ["or"]))
print(generate_ring_rules(100, 4, 10, ["or"]))

# generate rules and facts and check time
time_start = time()
N = 1000
M = 100
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
set(facts)
print("%d rules generated in %f seconds" % (N, time() - time_start))


# load and validate rules
# YOUR CODE HERE
def division_by_conditions(rules):
    every_item = []
    not_one_item = []
    one_of_items = []
    for rule in rules:
        for key in rule['if']:
            if key == 'or':
                one_of_items.append(rule)
            elif key == 'and':
                every_item.append(rule)
            else:
                not_one_item.append(rule)
    return [every_item, not_one_item, one_of_items]


def check_and(every_item, facts):
    key = 'and'
    for rule in every_item:
        if set(facts).issuperset(set(rule['if'][key])):
            facts.append(rule['then'])
    return facts


def check_or(one_of_items, facts):
    key = 'or'
    for rule in one_of_items:
        if not set(facts).isdisjoint(set(rule['if'][key])):
            facts.append(rule['then'])
    return facts


def check_not(not_one_item, facts):
    key = 'not'
    for rule in not_one_item:
        if set(facts).isdisjoint(set(rule['if'][key])):
            facts.append(rule['then'])
    return facts


def controdiction_a_to_b__not_a_to_b(every_item, not_one_item, one_of_items):
    for rule_not in not_one_item:
        for rule_and in every_item:
            if rule_not['if']['not'] == rule_and['if']['and']:
                rule_not.pop(['if'])
                rule_and.pop(['if'])
        for rule_or in one_of_items:
            if rule_not['if']['not'] == rule_or['if']['and']:
                rule_not.pop(['if'])
                rule_or.pop(['if'])


def controdiction_not_a_b__not_b_a(not_one_item):
    for rule_a in not_one_item:
        for rule_b in not_one_item:
            if not(set(rule_a['if']['not']).isdisjoint(set(rule_b['if']['not']))) and not (set(rule_b['if']['not']).isdisjoint(set(rule_a['if']['not']))):
                rule_a.pop(['if'])
                rule_b.pop(['if'])



# check facts vs rules
time_start = time()

# YOUR CODE HERE
division = division_by_conditions(rules)
every_item = division[0]
not_one_item = division[1]
one_of_items = division[2]

print(facts)
print(division_by_conditions(rules))
print(check_and(every_item, facts))
print(facts)

print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
