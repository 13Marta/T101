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
    return rules


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
    return rules


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
    return rules


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
    return rules


def generate_seq_facts(M):
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, M):
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    facts = list(set(facts))
    return facts


# generate rules and facts and check time
time_start = time()
N = 10000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
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


def check_rules(every_item, not_one_item, one_of_items, facts):
    new_facts = []
    for rule_and in every_item:
        if set(facts).issuperset(set(rule_and['if']['and'])):
            new_facts.append(rule_and['then'])
            rule_and.pop(['if'])

    for rule_or in one_of_items:
        if not set(facts).isdisjoint(set(rule_or['if']['or'])):
            new_facts.append(rule_or['then'])
            rule_or.pop(['if'])

    for rule_not in not_one_item:
        if set(facts).isdisjoint(set(rule_not['if']['not'])):
            new_facts.append(rule_not['then'])
            rule_not.pop(['if'])
    return new_facts


def controdiction_a_to_b__not_a_to_b(every_item, not_one_item, one_of_items):
    for rule_not in not_one_item:
        for rule_and in every_item:
            if rule_not['if']['not'] == rule_and['if']['and']:
                del rule_not
                del rule_and
                break

        for rule_or in one_of_items:
            if rule_not['if']['not'] == rule_or['if']['and']:
                del rule_not
                del rule_or
                break



def controdiction_not_a_b__not_b_a(not_one_item):
    for rule_a in not_one_item:
        for rule_b in not_one_item:
            if not (set(rule_a['if']['not']).isdisjoint(set(rule_b['if']['not']))) and not (
                    set(rule_b['if']['not']).isdisjoint(set(rule_a['if']['not']))):
                del rule_a
                del rule_b
                break


def main():
    every_item, not_one_item, one_of_items = division_by_conditions(rules)
    controdiction_not_a_b__not_b_a(not_one_item)
    while True:
        controdiction_a_to_b__not_a_to_b(every_item, not_one_item, one_of_items)
        new_facts = check_rules(every_item, not_one_item, one_of_items, facts)
        if set(facts).issuperset(set(new_facts)):
            break
        facts.extend(new_facts)
        facts = list(set(facts))
    return facts

time_start = time()

if __name__ == '__main__':
    result = main()
print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
