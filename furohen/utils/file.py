def read_file(file_path):
    try:
        file_list = []
        with open(file_path, "r") as file:
            for line in file:
                if not line.strip():  # Check if the line is not empty
                    continue
                if line.startswith("#"):  # Skip preprocessor directives
                    continue
                if line.startswith("/"):  # Skip single-line comments
                    continue
                file_list.append(line)
        return "".join(file_list)

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
