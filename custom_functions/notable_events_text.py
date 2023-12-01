def notable_events_text(artifact_cef_list=None, exclude_field_list=None, **kwargs):
    """
    Args:
        artifact_cef_list (CEF type: *)
        exclude_field_list: comma separated field names
    
    Returns a JSON-serializable object that implements the configured data paths:
        exclude_field_text
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Write your custom code here...
    final_dict = dict()
    field_value_text_list = []
    
    phantom.debug("exclude_field_list before processing: {}".format(exclude_field_list))
    if exclude_field_list:
        exclude_field_list = [x.strip() for x in exclude_field_list.split(",")]
    else:
        exclude_field_list = []
    phantom.debug("exclude_field_list after processing: {}".format(exclude_field_list))
    duplicating_field_list = []
    for artifact_cef in artifact_cef_list:
        if artifact_cef:
            for k, v in artifact_cef.items():
                if type(v) == list:
                    phantom.debug("List type found for {}, tupling list to prevent error".format(k));
                    v = tuple(v)
                    phantom.debug("After tupling {}:{}".format(k,v));
                final_dict.setdefault(k, set())
                final_dict[k].add(v)
    for k, v in final_dict.items():
        v_list = list(v)
        if len(v)>1:
            phantom.debug("Found Field: {}, {}".format(k, v))
            duplicating_field_list.append(k)
            
        elif v and v_list[0] and v_list[0] not in exclude_field_list:
            field_value_text = "{}: {}".format(k, v_list[0])
            phantom.debug('Adding value: "{}" to field_value_text_list'.format(field_value_text))
            field_value_text_list.append(field_value_text)
            
    
    outputs["exclude_field_text"] = "\n".join(field_value_text_list)
    
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
