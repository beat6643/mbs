def multiply_input(input_to_multiply=None, input_list=None, **kwargs):
    """
    Args:
        input_to_multiply
        input_list
    
    Returns a JSON-serializable object that implements the configured data paths:
        multiplied_output.*.item
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Write your custom code here...
    phantom.debug(f"input_list: {input_list}")
    phantom.debug(f"input_to_multiply: {input_to_multiply}")
    input_list_length=len(input_list)
    phantom.debug(f"input_list_length: {input_list_length}")
    outputs["multiplied_output"]=[{"item": input_to_multiply} for x in range(input_list_length)]
    phantom.debug(f"outputs: {outputs}")
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
