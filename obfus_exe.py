import os


def xor_data(data, key):
    """Performs XOR operation on data using the provided key."""
    return bytearray([b ^ key for b in data])


def obfuscate_exe(input_file, output_file, key):
    """Obfuscates the contents of an .exe file."""
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    # Read the binary data from the input file
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())

    # Obfuscate the data using XOR
    obfuscated_data = xor_data(data, key)

    # Write the obfuscated data to the output file
    with open(output_file, 'wb') as f:
        f.write(obfuscated_data)

    print(f"Obfuscated .exe written to {output_file}")


if __name__ == "__main__":
    print("EXE Obfuscator")

    # Eingabe der Dateipfade für die zu obfuskierende Datei und die Ausgabedatei
    input_exe = input("Enter the path to the .exe file you want to obfuscate: ")

    # Überprüfen, ob die Datei existiert
    if not os.path.exists(input_exe):
        print(f"Error: The file {input_exe} is not available on your PC.")
        exit(1)

    output_obfuscated_exe = input("Enter the path for the obfuscated .exe file: ")

    # Verwende einen einfachen XOR-Schlüssel für die Obfuskation
    xor_key = 0x42  # Du kannst diesen Wert auf jeden Wert zwischen 0 und 255 ändern

    # Schritt 1: Obfuskation der .exe-Datei
    obfuscate_exe(input_exe, output_obfuscated_exe, xor_key)
