model_name = "Qwen/Qwen2.5-VL-3B-Instruct"


def get_prompt(input_text):
    prompt=f"""
    Given the extracted bill data, verify and find these details:
                - Processed date
                - Merchant name
                - Total amount
                format the data type validly
                Extract these details in a structured JSON format.
                Extracted text:
                {input_text}
    """
    return prompt