def filter_action_result_parameter(action_result_data_list=None, input_to_multiply=None, **kwargs):
    """
    Args:
        action_result_data_list
        input_to_multiply
    
    Returns a JSON-serializable object that implements the configured data paths:
        filtered_action_result.*.parameter
        filtered_action_result.*.app_name
        filtered_action_result.*.action_name
        action_result_count
        multiplied_input.*.item
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
        
    outputs = {}
    
    # Write your custom code here...     
    phantom.debug(action_result_data_list)
    modified_action_result_data_list=[]
    parameter_list = ["domain", "ip", "hash", "url"]
    action_result_data_dict_list=[y for x in action_result_data_list for y in x if y]
    for action_result_data_dict in action_result_data_dict_list:        
        this_app_name=action_result_data_dict.get("app_name")
        this_action_name=action_result_data_dict.get("action")        
        for action_result_dict in action_result_data_dict.get("result_data", []):
            parameter_dict=action_result_dict.get("parameter")
            for param_key in parameter_dict.keys():
                if param_key.lower() in parameter_list:
                    parameter=parameter_dict.get(param_key)
                    break
            else:
                parameter=""
                phantom.debug("param key: not in the list for: {}. Hence setting it to an empty string".format(parameter_dict))
                
            modified_action_result_data_list.append({"app_name": this_app_name, "action_name": this_action_name, "status": action_result_dict.get("action"), "message": action_result_dict.get("message"), "parameter": parameter})
              
    outputs["filtered_action_result"]= modified_action_result_data_list  
    outputs["action_result_count"]=len(modified_action_result_data_list)    
    outputs["multiplied_input"]=[{"item": input_to_multiply} for x in range(len(outputs["filtered_action_result"]))]
    phantom.debug("outputs: {}".format(outputs))
        
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
