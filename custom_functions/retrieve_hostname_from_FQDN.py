def retrieve_hostname_from_FQDN(fqdn=None, **kwargs):
    """
    This custom function will remove the domain name from the FQDN of the device
    
    Args:
        fqdn (CEF type: *): FQDN of the device
    
    Returns a JSON-serializable object that implements the configured data paths:
        host_name (CEF type: *): Host Name
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Write your custom code here...
    hostname=fqdn.split('.')[0]
    if(hostname == 'None'):
        return None
    else:
        pass
    outputs["host_name"]=hostname
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
