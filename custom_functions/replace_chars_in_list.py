def replace_chars_in_list(input_string_list=None, sub_string_to_be_replaced=None, replace_substring=None, **kwargs):
    """
    Replace certain chars in a list of strings with another char or sub string
    
    Args:
        input_string_list (CEF type: *)
        sub_string_to_be_replaced (CEF type: *)
        replace_substring (CEF type: *)
    
    Returns a JSON-serializable object that implements the configured data paths:
        output_string_list.*.item (CEF type: *)
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Write your custom code here...
    sub_string_to_be_replaced = "." if not sub_string_to_be_replaced else sub_string_to_be_replaced
    replace_substring = "[.]" if not replace_substring else replace_substring
    
    output_list = []
    
    for input_string in input_string_list:
        output_list.append(input_string.replace(sub_string_to_be_replaced, replace_substring))
        
    outputs["output_string_list"]= [{"item": item} for item in output_list]
    
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
