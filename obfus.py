# -*- coding: utf-8 -*-
import ast
import random
import string
import os
import base64
import urllib.parse
import subprocess
import sys


# Funktion zum Generieren von zufälligen Strings
def random_string(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


# Funktion zur Obfuskation von Funktions- und Variablennamen
class Obfuscator(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.renamed = {}

    def visit_FunctionDef(self, node):
        # Obfuskation des Funktionsnamens
        new_name = random_string()
        self.renamed[node.name] = new_name
        node.name = new_name
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        # Obfuskation der Variablennamen
        if isinstance(node.ctx, ast.Store):
            new_name = random_string()
            self.renamed[node.id] = new_name
            node.id = new_name
        elif isinstance(node.ctx, ast.Load):
            node.id = self.renamed.get(node.id, node.id)
        return node


# Funktion zum Einfügen von unnötigen (aber syntaktisch korrekten) Anweisungen
def insert_dummy_code():
    dummy_code = """
for _ in range(10):
    pass
"""
    return dummy_code


# Funktion zur Obfuskation des Codes
def obfuscate_code(code):
    # Parsen des Quellcodes in den Abstract Syntax Tree (AST)
    tree = ast.parse(code)

    # Anwenden der Obfuskation
    obfuscator = Obfuscator()
    obfuscated_tree = obfuscator.visit(tree)
    ast.fix_missing_locations(obfuscated_tree)

    # Konvertiere den AST wieder zurück in den Quellcode
    obfuscated_code = compile(obfuscated_tree, filename="<ast>", mode="exec")

    # Füge Dummy-Code hinzu
    obfuscated_code_with_dummy = insert_dummy_code() + "\n" + code

    return obfuscated_code_with_dummy


# Funktion zur Base64-Verschlüsselung und Hinzufügen eines Decoders
def base64_encode_with_decoder(code):
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    # Füge den Code hinzu, der Base64 decodiert und ausführt
    decoder = f"""
import base64
import os
import subprocess
import sys

# Funktion um das Skript im Hintergrund auszuführen (nur Windows)
def run_in_background():
    if sys.platform == "win32":
        pythonw_path = os.path.join(sys.exec_prefix, 'pythonw.exe')
        if os.path.exists(pythonw_path):
            subprocess.Popen([pythonw_path, __file__], close_fds=True)
            sys.exit()

# Starte das Skript im Hintergrund, wenn nicht bereits im Hintergrund ausgeführt
if sys.executable.endswith('pythonw.exe'):
    pass  # Skript läuft bereits im Hintergrund
else:
    run_in_background()

exec(base64.b64decode('{encoded_code}').decode('utf-8'))
"""
    return decoder


# Funktion zur URL-Codierung und Hinzufügen eines Decoders
def url_encode_with_decoder(code):
    encoded_code = urllib.parse.quote(code)
    # Füge den Code hinzu, der URL-codierten Code decodiert und ausführt
    decoder = f"""
import urllib.parse
import os
import subprocess
import sys

# Funktion um das Skript im Hintergrund auszuführen (nur Windows)
def run_in_background():
    if sys.platform == "win32":
        pythonw_path = os.path.join(sys.exec_prefix, 'pythonw.exe')
        if os.path.exists(pythonw_path):
            subprocess.Popen([pythonw_path, __file__], close_fds=True)
            sys.exit()

# Starte das Skript im Hintergrund, wenn nicht bereits im Hintergrund ausgeführt
if sys.executable.endswith('pythonw.exe'):
    pass  # Skript läuft bereits im Hintergrund
else:
    run_in_background()

exec(urllib.parse.unquote('{encoded_code}'))
"""
    return decoder


# Funktion zum Laden und Obfuskieren einer Datei
def obfuscate_file(file_path, output_file=None, encode_type=None):
    if not os.path.exists(file_path):
        print(f"Die Datei {file_path} wurde nicht gefunden.")
        return

    # Lese den Inhalt der Python-Datei
    with open(file_path, 'r') as file:
        code = file.read()

    # Obfuskiere den Code
    obfuscated_code = obfuscate_code(code)

    # Verschlüsseln (Base64 oder URL) mit eingebauter Entschlüsselungslogik
    if encode_type == 'base64':
        obfuscated_code = base64_encode_with_decoder(obfuscated_code)
    elif encode_type == 'url':
        obfuscated_code = url_encode_with_decoder(obfuscated_code)

    # Speichere den obfuskierten Code in eine neue Datei oder gebe ihn auf der Konsole aus
    if output_file:
        with open(output_file, 'w') as out_file:
            out_file.write(obfuscated_code)
        print(f"Obfuscated Code wurde in {output_file} gespeichert.")
    else:
        print("Obfuscated Code:\n")
        print(obfuscated_code)


# Beispiel der Ausführung
if __name__ == "__main__":
    file_path = input("Gib den Pfad zur Python-Datei ein: ")
    output_file = input("Gib den Pfad für die Ausgabe ein (optional, drücke Enter um nur anzuzeigen): ")
    encode_type = input("Wähle die Verschlüsselungsart (base64/url/keine): ").strip().lower()

    if output_file.strip() == "":
        output_file = None

    obfuscate_file(file_path, output_file, encode_type)
