"""Creates knowledge base"""

from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    """generate_simple_rules"""
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
    """generate_stairway_rules"""
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
    """generate_ring_rules"""
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
    """generate_random_rules"""
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
    """generate_seq_facts"""
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, M):
    """generate_rand_facts"""
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    facts = list(set(facts))
    return facts


# generate rules and facts and check time


# load and validate rules
# YOUR CODE HERE
def division_by_conditions(rules):
    """Dividing the general list with rules into three and/not/or"""
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
    """
            Searching new facts in rules
                Params:
                    every_item - list of all and_rules
                    not_one_item - list of all not_rules
                    one_of_items - list of all or_rules
                    facts - list of all known facts
                Returns:
                    new_facts - list of new facts, added by checking rules
        """
    new_facts = []
    for rule_and in every_item:
        if set(facts).issuperset(set(rule_and['if']['and'])):
            new_facts.append(rule_and['then'])
            del rule_and

    for rule_or in one_of_items:
        if not set(facts).isdisjoint(set(rule_or['if']['or'])):
            new_facts.append(rule_or['then'])
            del rule_or

    for rule_not in not_one_item:
        if set(facts).isdisjoint(set(rule_not['if']['not'])):
            new_facts.append(rule_not['then'])
            del rule_not
    return new_facts


def contradiction_a_to_b__not_a_to_b(every_item, not_one_item, one_of_items):
    """resolves the contradiction like (a->b), (not a->b)"""
    for rule_not in not_one_item:
        for rule_and in every_item:
            if rule_not['if']['not'] == rule_and['if']['and']:
                del rule_and

        for rule_or in one_of_items:
            if rule_not['if']['not'] == rule_or['if']['or']:
                del rule_not
                del rule_or
                break


def contradiction_not_a_b__not_b_a(not_one_item):
    """resolves the contradiction like (not a->b), (not b->a)"""
    for rule_a in not_one_item:
        for rule_b in not_one_item:
            if not (set(rule_a['if']['not']).isdisjoint(set(rule_b['if']['not']))) and not (
                    set(rule_b['if']['not']).isdisjoint(set(rule_a['if']['not']))):
                del rule_a
                del rule_b
                break


def main():
    """
            Main func, where check contradictions and in cycle searches new facts
            Returns:
                facts - list of all facts in knowledge base
    """
    time_start = time()
    N = 10000
    M = 1000
    rules = generate_simple_rules(100, 4, N)
    facts = generate_rand_facts(100, M)
    print("%d rules generated in %f seconds" % (N, time() - time_start))

    every_item, not_one_item, one_of_items = division_by_conditions(rules)
    contradiction_not_a_b__not_b_a(not_one_item)

    while True:
        contradiction_a_to_b__not_a_to_b(every_item, not_one_item, one_of_items)
        new_facts = check_rules(every_item, not_one_item, one_of_items, facts)
        if set(facts).issuperset(set(new_facts)):
            break
        facts.extend(new_facts)
        facts = list(set(facts))
    return facts


time_start = time()

if __name__ == '__main__':
    print(main())

print("%d facts validated vs %d rules in %f seconds" % (1000, 10000, time() - time_start))
