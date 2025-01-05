import os
import requests

def query_tinydolphin(prompt, model="tinydolphin"):
    """Query the TinyDolphin API with a given prompt and return the response."""
    url = "http://localhost:11434/api/generate"  # Adjust URL if necessary for TinyDolphin
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 500,  # Limit response length
        "stream": False  # Ensure streaming is disabled
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text.strip()  # Return raw text response and strip whitespace
    except requests.exceptions.RequestException as e:
        print(f"Error querying TinyDolphin API: {e}")
        return None

def read_files_from_directory(directory):
    """Read all text files from the specified directory."""
    contents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Process only text files
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                contents.append(file.read())
    return contents

def main():
    input_directory = input("Please enter the directory containing text files: ")
    
    # Read all notes from the specified directory
    notes_contents = read_files_from_directory(input_directory)
    
    if not notes_contents:
        print("No text files found in the specified directory.")
        return
    
    # Construct prompt for TinyDolphin API
    combined_content = "\n\n".join(notes_contents)  # Combine all notes into one string
    prompt = (
        "Read the following unstructured notes and organize them into structured notes. "
        "You can decide how to structure the notes and where each piece of text should go. "
        "Please provide your organized response in plain text. Here is the content: {content}"
    ).format(content=combined_content)
    
    # Query TinyDolphin with the combined content of all notes
    organized_content = query_tinydolphin(prompt)
    
    if organized_content:
        output_file_path = os.path.join(input_directory, 'organized_notes.txt')  # Output filename
        
        try:
            with open(output_file_path, 'w', encoding='utf-8') as note_file:
                note_file.write(organized_content)  # Write organized notes to a file
            print(f"Notes organized and saved successfully to {output_file_path}.")
        except Exception as e:
            print(f"Error saving notes: {e}")
    else:
        print("No organized content was created.")

if __name__ == "__main__":
    main()

