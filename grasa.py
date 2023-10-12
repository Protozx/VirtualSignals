def generate_automata(words):
    transitions = []
    state_counter = 0
    initial_state = state_counter

    for word in words:
        current_state = initial_state
        for index, char in enumerate(word):
            next_state = state_counter + 1

            # Si la letra coincide con el inicio de otra palabra, agregamos una transición no determinista
            for other_word in words:
                if other_word != word and other_word.startswith(char):
                    transitions.append((current_state, char, state_counter + 1))
                    state_counter += 1
                    next_state = state_counter + 1

            transitions.append((current_state, char, next_state))
            current_state = next_state

            # Si es el último carácter de la palabra, aumentamos el contador de estados
            if index == len(word) - 1:
                state_counter += 1

    return transitions


def save_to_csv(transitions, filename):
    with open(filename, 'w') as file:
        file.write("Estado actual,Letra,Estado siguiente\n")
        for transition in transitions:
            file.write(f"{transition[0]},{transition[1]},{transition[2]}\n")


if __name__ == "__main__":
    words = ["break","else","puerca"]
    transitions = generate_automata(words)
    save_to_csv(transitions, "bresg.csv")
