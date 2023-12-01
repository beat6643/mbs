def filter_value_in_custom_list(value_list=None, custom_list_name=None, **kwargs):
    """
    Filter a list of values based on full or partial match with values in a custom list. The output will be a list of strings which has a partial match against the values in the custom list.
    
    Args:
        value_list (CEF type: *): Example: requestURLs
        custom_list_name (CEF type: *)
    
    Returns a JSON-serializable object that implements the configured data paths:
        match_list.*.item (CEF type: *)
        non_match_list.*.item
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Write your custom code here...       
    # This function converts a phantom custom list into a python list of one dimension. By default it takes values from column 0 of the custom list
    def custom_list_to_list(custom_list_name, start_pos=0):        
        status, message, custom_list = phantom.get_list(list_name=custom_list_name)
        
        if status:               
            phantom.debug("Successfully read custom list: {}. Status: {}. Message: {}".format(custom_list_name, status, message))                              
        else:
            phantom.debug("Unable to read custom list: {}. Status: {}. Message: {}".format(custom_list_name, status, message)) 
    
        return custom_list
    
    
    custom_list = custom_list_to_list(custom_list_name, start_pos=0)
    custom_list = [x[0] for x in custom_list if x and x[0]]
    value_list = [x for x in value_list if x]
    phantom.debug("custom_list: {}".format(custom_list)) 
    phantom.debug("value_list: {}".format(value_list)) 
    
    match_list = []
    non_match_list = []
    for value in value_list:
        any_list = [True for cust_value in custom_list if value.lower() in cust_value.lower() or cust_value.lower() in value.lower()]
        phantom.debug("any_list: {}".format(any_list)) 
        if any(any_list):
            match_list.append({"item": value})
        else:
            non_match_list.append({"item": value})
            
    
    outputs["match_list"]=match_list
    outputs["non_match_list"]=non_match_list
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
