import re
import os

# Function to read the content of a file
def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")

# Text cleaning functions
def remove_non_alphabets(word_list):
    word_list = remove_apostrophes(word_list)
    return [re.sub(r'[^A-Za-z]+', ' ', word) for word in word_list]

def convert_to_uppercase(word_list):
    return [word.upper() for word in word_list]

def remove_apostrophes(word_list):
    word_list = convert_to_uppercase(word_list)
    return [word.replace("'", "") for word in word_list]

# Function to read a score card from a file
def read_score_card(file_name):
    score_card = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    key = parts[0]
                    value = int(parts[1])
                    score_card[key] = value
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
    return score_card

# Function to generate abbreviations for a given name
def generate_abbreviations(name, letter_values, all_abbreviations):
    cleaned_name = " ".join(remove_non_alphabets([name]))
    cleaned_name = convert_to_uppercase([cleaned_name])[0].replace("'", "")

    current_abbreviations = generate_abbreviations_detail(cleaned_name)

    # Remove duplicates from the current abbreviations
    current_abbreviations = list(set(current_abbreviations))

    # Add abbreviations to the global list
    all_abbreviations.extend(current_abbreviations)

    # Select the abbreviation with the least value
    best_abbreviation = min(current_abbreviations, key=lambda abbr: calculate_score(abbr, name, letter_values))

    abbreviations = {cleaned_name: [best_abbreviation]}

    # Print the best abbreviation for the entire name with score
    print(f"Best Abbreviation for {cleaned_name}: {best_abbreviation}")
    score = calculate_score(best_abbreviation, name, letter_values)
    print(f"  {best_abbreviation}: {score}")

    # Remove duplicates from the global list
    all_abbreviations[:] = list(set(all_abbreviations))

    return abbreviations

# Function to generate detailed abbreviations from a word
def generate_abbreviations_detail(word):
    abbreviations = []
    if len(word) >= 3 and word[0] != ' ':
        for i in range(1, len(word) - 1):
            abbreviation = word[0] + word[i:i + 2]
            if abbreviation.isalpha():
                abbreviations.append(abbreviation.upper())
    return abbreviations

# Function to calculate a score for an abbreviation
def calculate_score(abbr, name, letter_values):
    score = 0
    words = re.split(r'\W+', name.upper())
    for i in range(1, len(abbr)):
        for word in words:
            if abbr[i] in word:
                if word.index(abbr[i]) == 0:
                    score += 0
                elif word.index(abbr[i]) == len(word) - 1:
                    score += 5 if abbr[i] != 'E' else 20
                else:
                    score += word.index(abbr[i]) + 1 + letter_values.get(abbr[i], 0)
    return score

# Function to remove duplicates from abbreviations dictionary
def remove_duplicates_from_dict(duplicates, abbreviations_dict):
    for duplicate_entry in duplicates:
        for key, value in abbreviations_dict.items():
            if duplicate_entry in value:
                value.remove(duplicate_entry)
    return abbreviations_dict

# Main function
def main():
    file_name = input("Enter the name of the file to read (e.g., name.txt): ")
    surname = input("Enter your surname (e.g., Malgwi): ")

    # Remove the file extension from the input file name
    file_name_without_extension, _ = os.path.splitext(file_name)

    file_content = read_file(file_name)

    if file_content:
        # Apply text cleaning functions
        cleaned_content = " ".join(remove_non_alphabets(file_content.split('\n')))
        print("File content:")
        print(cleaned_content)

        letter_values = read_score_card("values.txt")

        names = re.split(r'\n', file_content.strip())
        results = {}
        all_abbreviations = []  # Keep track of all abbreviations

        # Construct output file path with the .txt extension
        output_file_path = f"{surname}_{file_name_without_extension}_abbrevs.txt"

        with open(output_file_path, 'w') as output_file:
            for name in names:
                name = name.strip()
                current_abbreviations = generate_abbreviations(name, letter_values, all_abbreviations)
                results[name] = current_abbreviations

                # Write name to the output file
                output_file.write(f"{name}\n")

                # Write the best abbreviation to the output file
                for word, abbr_list in current_abbreviations.items():
                    output_file.write(f"{word}:\n")

                    # Write the best abbreviation along with its score to the output file
                    best_abbreviation = abbr_list[0]
                    score = calculate_score(best_abbreviation, name, letter_values)
                    output_file.write(f"  {best_abbreviation}: {score}\n\n")

            # Remove duplicates from all abbreviations in the output file
            duplicates = set()
            for name, abbr_list in results.items():
                for word, abbrs in abbr_list.items():
                    for abbr in abbrs.copy():
                        if abbr in duplicates:
                            print(f"Duplicate found for '{abbr}' in '{word}'. Removing duplicates.")
                            abbrs.remove(abbr)
                        else:
                            duplicates.add(abbr)

        print(f"Results saved to {output_file_path}")

if __name__ == "__main__":
    main()
