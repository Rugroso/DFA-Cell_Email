import requests
import argparse
class Automaton:
    def __init__(self, transitions, accept_states): # Constructor de la clase Automaton
        self.states = {i: {} for i in range(max(max(t[:2]) for t in transitions) + 1)} # Se crea un diccionario con los estados
        self.start_state = 0
        self.accept_states = accept_states
        self._build_transitions(transitions)
    
    def _build_transitions(self, transitions): # Funcion para construir las transiciones del automata
        for from_state, to_state, symbol in transitions:
            self.states[from_state][symbol] = to_state
            

    def process_numbers(self, input_text): # Funcion para procesar numeros telefonicos
        current_state = self.start_state
        buffer = ""
        valid_matches = []
        
        for symbol in input_text:
            if symbol >= '0' and symbol <= '9':
                category = 'digit'
            else:
                category = symbol
            if category in self.states[current_state]:
                current_state = self.states[current_state][category]
                buffer += symbol
                if current_state in self.accept_states:
                    valid_matches.append(buffer.strip())
                    buffer = ""
                    current_state = self.start_state
            else:
                buffer = ""
                current_state = self.start_state
        
        return valid_matches
    
    def process_emails(self, input_text): # Funcion para procesar emails
        valid_matches = []
        i = 0
        n = len(input_text)
        while i < n:
            current_state = self.start_state
            match = ""
            last_accept = None
            j = i
            while j < n: # Mientras se recorre el texto
                symbol = input_text[j]
                if 'a' <= symbol <= 'z':
                    category = 'char'
                elif 'A' <= symbol <= 'Z':
                    category = 'char'
                elif '0' <= symbol <= '9':
                    category = 'number'
                else:
                    category = symbol
                # category = 'char' if checkChar(symbol)  else symbol
                if category in self.states[current_state]:
                    current_state = self.states[current_state][category]
                    match += symbol
                    if current_state in self.accept_states:
                        last_accept = match 
                    j += 1
                else:
                    break
            if last_accept:
                valid_matches.append(last_accept.strip())
                i = j
            else:
                i += 1
        return valid_matches

def get_text_from_url(url): # Funcion para obtener el texto de una url.
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

def get_text_from_file(file_path): # Funcion para obtener el texto de un archivo.
    with open(file_path, 'r') as file:
        return file.read()

# (from_state, to_state, symbol) - Este formato permite comprende el modo en que se mueve el autómata de un estado a otro.

phone_transitions = [ # Automata para identificar numeros telefonicos
    (0, 1, 'digit'), (0, 11, '('), 
    (1, 2, 'digit'), (2, 3, 'digit'), (3, 4, 'digit'), (3, 16, '-'), (3, 21, ' '), 
    (4, 5, 'digit'), (5, 6, 'digit'), (6, 7, 'digit'), (7, 8, 'digit'), (8, 9, 'digit'), (9, 10, 'digit'),
    (11, 12, 'digit'), (12, 13, 'digit'), (13, 14, 'digit'), (14, 15, ')'), (15, 16, '-'), (15, 21, ' '), 
    (16, 17, 'digit'), (17, 18, 'digit'), (18, 19, 'digit'), (19, 20, '-'), 
    (20, 7, 'digit'), (21, 22, 'digit'), (22, 23, 'digit'), (23, 24, 'digit'), (24, 20, ' ')
]
phone_accept_states = {10} # Estado de aceptación

# Automata para identificar emails.
email_transitions = [
    (0, 1, 'char'), # Esto es para lo del antes del arroba
    (0, 1, 'number'),
    (1, 1, 'char'),
    (1, 1, 'number'),
    (1, 2, '.'),
    (2, 1, 'char'),
    (2, 1, 'number'),
    (1, 3, '@'),
    
    (3, 3, 'char'), #Esto de aqui ya son los que salen despues del arroba            
    (3, 4, '.'),                
    (4, 5, 'char'),             
    (5, 5, 'char'),             
    (5, 4, '.') 
]
email_accept_states = {5} # Estado de aceptación

# Crear autómatas
phone_automaton = Automaton(phone_transitions, phone_accept_states)
email_automaton = Automaton(email_transitions, email_accept_states)

# Obtener datos de la web o archivo

parser = argparse.ArgumentParser()
parser.add_argument('file_path')
parser.add_argument('-correo', action='store_true')
parser.add_argument('-telefono', action='store_true')
args = parser.parse_args()

input_text = get_text_from_file(args.file_path)
if args.telefono: # Si se desea obtener telefonos
    f = open("numbers.txt", "w")
    for val in input_text.split('\n'): # Se lee cada url del archivo
        print(val)
        webText = get_text_from_url(val)
        phone_numbers = phone_automaton.process_numbers(webText)
        for number in phone_numbers:
            Write = (number + "\n")
            print(Write)
            toWrite = str(Write)
            f.write(toWrite)
            print(number)
    f.close()


if  args.correo: # Si se desea obtener correos
    f = open("emails.txt", "w")
    for val in input_text.split('\n'): # Se lee cada url del archivo
        print(val)
        webText = get_text_from_url(val)
        email_addresses = email_automaton.process_emails(webText)
        for email in email_addresses:
            Write = (email + "\n")
            print(Write)
            toWrite = str(Write)
            f.write(toWrite)
            print(email)
    f.close()