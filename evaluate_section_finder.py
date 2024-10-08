from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from chatbot import find_relevant_section

def evaluate_section_finder(find_relevant_section, pdf_texts, error_codes, expected_sections):
    """Evaluates the performance of the find_relevant_section function.

    Args:
        find_relevant_section: The function to be evaluated.
        pdf_texts: A list of PDF texts.
        error_codes: A list of corresponding error codes.
        expected_sections: A list of expected relevant sections.

    Returns:
        A dictionary containing accuracy, precision, recall, and F1-score.
    """

    predicted_sections = [find_relevant_section(text, code) for text, code in zip(pdf_texts, error_codes)]

    # Convert sections to binary labels (1 if section is found, 0 otherwise)
    y_true = [1 if section else 0 for section in expected_sections]
    y_pred = [1 if section else 0 for section in predicted_sections]

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

# Example usage (assuming you have your find_relevant_section function defined)
if __name__ == "__main__":
    # Prepare your test data (pdf_texts, error_codes, expected_sections)
    # ...

    metrics = evaluate_section_finder(find_relevant_section, pdf_texts, error_codes, expected_sections)
    print(metrics)