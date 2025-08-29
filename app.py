
import re
from flask import Flask, request, jsonify


app = Flask(__name__)


FULL_NAME = "Gowtham Santhanam"
DATE_OF_BIRTH = "08.20.2004" # ddmmyyyy format
EMAIL = "adamgoya0810@gmail.com"
ROLL_NUMBER = "22bce5246"

@app.route('/bfhl', methods=['POST'])
def process_data():
    """
    Handles a POST request to process an array of mixed data types.
    """
    # Initialize the response dictionary with default values
    response_data = {
        "is_success": False,
        "user_id": f"{FULL_NAME}_{DATE_OF_BIRTH}",
        "email": EMAIL,
        "roll_number": ROLL_NUMBER,
        "odd_numbers": [],
        "even_numbers": [],
        "alphabets": [],
        "special_characters": [],
        "sum": "0",
        "concat_string": ""
    }

    try:
        # Get the JSON data from the request body
        req_data = request.get_json()
        input_array = req_data.get('data', [])

        # Check if the 'data' key exists and is a list
        if not isinstance(input_array, list):
            return jsonify({
                "is_success": False,
                "error": "Invalid input: 'data' must be an array."
            }), 400

        # Initialize lists and sum for processing
        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_characters = []
        total_sum = 0

        # --- Data Categorization and Processing ---
        for item in input_array:
            item_str = str(item)  # Ensure all items are treated as strings

            # Check if the item is a number (handles both int and string numbers)
            if item_str.isdigit() or (item_str.startswith('-') and item_str[1:].isdigit()):
                number = int(item_str)
                total_sum += number
                if number % 2 == 0:
                    even_numbers.append(item_str)
                else:
                    odd_numbers.append(item_str)

            # Check if the item is an alphabet string (case-insensitive)
            # This regex checks for one or more alphabetical characters
            elif re.fullmatch(r'[a-zA-Z]+', item_str):
                alphabets.append(item_str.upper())

            # Otherwise, it's a special character
            else:
                special_characters.append(item_str)
        
        # --- Concatenation Logic (alternating caps in reverse order) ---
        # 1. Join all uppercase alphabets into a single string
        concatenated_alphabets = "".join(alphabets)
        
        # 2. Reverse the entire string
        reversed_string = concatenated_alphabets[::-1]
        
        # 3. Apply alternating capitalization
        final_string = ""
        for i, char in enumerate(reversed_string):
            if i % 2 == 0:
                final_string += char.upper()
            else:
                final_string += char.lower()
        
        # --- Populate the final response dictionary ---
        response_data["is_success"] = True
        response_data["odd_numbers"] = odd_numbers
        response_data["even_numbers"] = even_numbers
        response_data["alphabets"] = alphabets
        response_data["special_characters"] = special_characters
        response_data["sum"] = str(total_sum)
        response_data["concat_string"] = final_string

        # Return the final JSON response with a 200 OK status code
        return jsonify(response_data), 200

    except Exception as e:
        # Graceful exception handling for any unexpected errors
        return jsonify({
            "is_success": False,
            "error": f"An internal error occurred: {str(e)}"
        }), 500

# To run the API, you would use a command like:
# python your_file_name.py
if __name__ == '__main__':
    app.run(debug=True)
