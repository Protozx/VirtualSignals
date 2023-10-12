import csv
from collections import defaultdict

def read_nfa_from_csv(filename):
    nfa = defaultdict(lambda: defaultdict(set))
    all_letters = set()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            state, letter, next_state = row
            nfa[state][letter].add(next_state)
            all_letters.add(letter)
    return nfa, all_letters

def convert_to_dfa(nfa, all_letters):
    dfa = {}
    states_to_process = [frozenset({list(nfa.keys())[0]})]
    processed_states = set()

    while states_to_process:
        current_state = states_to_process.pop()
        dfa[current_state] = {}
        
        for letter in all_letters:
            next_states = set()
            for state in current_state:
                if letter in nfa[state]:
                    next_states.update(nfa[state][letter])
            dfa[current_state][letter] = frozenset(next_states) if next_states else frozenset({'trap'})
            
            if frozenset(next_states) not in processed_states and frozenset(next_states) not in states_to_process:
                states_to_process.append(frozenset(next_states))

        processed_states.add(current_state)

    # Add trap state
    dfa[frozenset({'trap'})] = {letter: frozenset({'trap'}) for letter in all_letters}

    return dfa

def write_dfa_to_csv(dfa, filename):
    headers = ['Estado'] + list(dfa[next(iter(dfa))].keys())
    rows = []

    for state, transitions in dfa.items():
        row = [','.join(state)]
        for letter in transitions:
            row.append(','.join(transitions[letter]))
        rows.append(row)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

if __name__ == "__main__":
    nfa, all_letters = read_nfa_from_csv('bres.csv')
    dfa = convert_to_dfa(nfa, all_letters)
    write_dfa_to_csv(dfa, 'lev.csv')
