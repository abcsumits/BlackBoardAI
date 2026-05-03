import json

# Replace 'data.txt' with the actual path to your file
file_path = 'dialogue.txt'

try:
    # Open the file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
        # json.load() parses the file content and converts it directly into a dictionary
        my_dictionary = json.load(file)

    # Verify it worked by printing a specific segment or the type
    print("Successfully loaded as:", type(my_dictionary))
    print(my_dictionary)
    # Example of how to access the data
    print("\nSegment 1, Part 1:")
    print(my_dictionary['segment1'][0])
    
    print("\nSegment 1, Part 2:")
    print(my_dictionary['segment1'][1])

except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
except json.JSONDecodeError:
    print("Error: The file does not contain valid JSON format.")