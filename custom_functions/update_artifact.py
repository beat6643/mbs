def update_artifact(artifact_id_list=None, new_cef_json_list=None, **kwargs):
    """
    Update existing Artifact
    
    Args:
        artifact_id_list (CEF type: phantom artifact id)
        new_cef_json_list (CEF type: *): Don't expand the list if input is passed from a format block.
    
    Returns a JSON-serializable object that implements the configured data paths:
        
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Write your custom code here...
    
    # Get phantom REST url
    rest_url = phantom.get_rest_base_url()
    phantom.debug("rest_url: {}".format(rest_url))    
    
    def rest_post_call(url, data):        
        phantom.debug("Executing REST POST on url: {}. With data: {}".format(url, data))
        
        try:
            r = phantom.requests.post(url, verify=False, data=data)
            if r.status_code == 200:
                phantom.debug("REST POST call successfully completed for url: {} status_code: {}. response text: {}.".format(url, r.status_code, r.text))                
            else:
                phantom.debug("ERROR: REST POST call failed for url: {} status_code: {}. response text: {}.".format(url, r.status_code, r.text))                
            
        except Exception as e:
            phantom.debug("Exception while REST GET call : {}".format(url))
            phantom.debug(e)
        
            
    def rest_get_call(url):        
        phantom.debug("Executing REST GET on: {}".format(url))
        try:
            r = phantom.requests.get(url, verify=False)
            if r.status_code == 200:
                phantom.debug("REST GET call successfully completed for url: {} status_code: {}. response text: {}.".format(url, r.status_code, r.text))
                return r.json()
            else:
                phantom.debug("ERROR: REST GET call failed for url: {} status_code: {}. response text: {}.".format(url, r.status_code, r.text))                
            
        except Exception as e:
            phantom.debug("Exception while REST GET call : {}".format(url))
            phantom.debug(e)
    
    def update_artifact(artifact_id, new_cef_dict):
        if artifact_id in ("0", 0):            
            phantom.debug("ERROR:Artifact ID : {} is malformed. Returning. Please check action result context.artifact_id".format(artifact_id))                       
        else:        
            phantom.debug("Updating artifact: {} with new_cef value dict: {}.".format(artifact_id, new_cef_dict))                
            get_artifact_url = rest_url + 'artifact/{}'.format(artifact_id)  
            artifact_json = rest_get_call(get_artifact_url)    
            current_cef_dict = {"cef": artifact_json.get("cef", dict())}
            #artifact_json.set_default("cef", dict())
            for k, v in list(new_cef_dict.items()):
                current_cef_dict["cef"][k]=v
        
            phantom.debug("New cef dict after addition of new values is: {}.".format(current_cef_dict))
        
            artifact_post_url = rest_url + 'artifact/{}'.format(artifact_id)
            #{"cef": {"testing_k": "testing_v"}}
            rest_post_call(artifact_post_url, json.dumps(current_cef_dict))
    
    
    
    phantom.debug("artifact_id_list: {}.".format(artifact_id_list))                
    phantom.debug("new_cef_json_list: {}.".format(new_cef_json_list))                
    new_cef_json_list = new_cef_json_list[0].split("\n")
    phantom.debug("new_cef_json_list after modificaiton: {}.".format(new_cef_json_list))                
    
    phantom.debug("artifact_id_list type: {}.".format(type(artifact_id_list)))
    phantom.debug("new_cef_json_list type: {}.".format(type(new_cef_json_list)))
    
    if len(artifact_id_list) != len(new_cef_json_list):
        phantom.debug("WARNING: Both inputs have different length: {}. Undesirable artifacts might bet updated.")
    
    for artifact_id, cef_json in zip(artifact_id_list, new_cef_json_list):
        phantom.debug("Processing artifact: {} with cef string: {}.".format(artifact_id, cef_json))                
        update_artifact(artifact_id, json.loads(cef_json))
    
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
