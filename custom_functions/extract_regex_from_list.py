def extract_regex_from_list(input_list=None, regex_pattern=None, drop_or_pass_input_ioc=None, output_as_string=None, **kwargs):
    """
    Extract regex patterns from input list and pass them as an output list. The output of this custom function would be a list of strings.
    
    Args:
        input_list (CEF type: *)
        regex_pattern (CEF type: *)
        drop_or_pass_input_ioc (CEF type: *): 0=drop input artifact if a regex match was not found for that artifact.
            1=Pass the input IOC in the output if a regex match was not found.
            
            An artifact will be dropped from passing on as output if this field is left empty and there is no regex match found.
        output_as_string: This will work only if the input list has one item in it. Default = false
    
    Returns a JSON-serializable object that implements the configured data paths:
        output.*.item (CEF type: *)
        output_item
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    import re
    
    outputs = {}
    
    # Write your custom code here...
    drop_or_pass_input_ioc=drop_or_pass_input_ioc if drop_or_pass_input_ioc else 0
    output_as_string = True if output_as_string and "true" in output_as_string.lower() else False
    phantom.debug("output_as_string list: {}".format(output_as_string))    
    
    phantom.debug("input_list list: {}".format(input_list))    
    phantom.debug("input_list list type: {}".format(type(input_list)))    
    phantom.debug("regex_pattern: {}".format(regex_pattern))
    phantom.debug("drop_or_pass_input_ioc: {}".format(drop_or_pass_input_ioc))
    output_list=[]
    for input_item in input_list:
        #match_list = re.findall('__(.*)__', url)
        match_list = re.findall(regex_pattern, input_item)
        match_list = [match for match in match_list if match]
        finding = match_list[0] if match_list and match_list[0] else ""
        #output_list.append({"id": id, "json": {json.dummps({new_cef_field_name: finding})})
        if finding:
            output_list.append({"item": finding})
        elif not finding and int(drop_or_pass_input_ioc):
            output_list.append({"item": ""})            
            phantom.debug("item: {}: No match found for regex pattern: {}. drop_or_pass_input_ioc is set as: {}. Hence empty string will be passed as output.".format(input_item, regex_pattern, drop_or_pass_input_ioc))            
        else:            
            phantom.debug("item: {}: No match found for regex pattern: {}.".format(input_item, regex_pattern))
        phantom.debug("item: {} \nFinding: {}\n\n".format(input_item.encode("utf-8"), finding.encode("utf-8")))
            
    phantom.debug("output_list: {}".format(output_list))
    if output_as_string and len(output_list)==1:
        phantom.debug("Only one item in the output list. Hence passing that to the output_item variable")
        outputs["output_item"]=output_list[0]["item"]
                
    outputs["output"]=output_list
    
    phantom.debug(outputs)
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
