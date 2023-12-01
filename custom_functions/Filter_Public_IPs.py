def Filter_Public_IPs(sourceAddress=None, destinationAddress=None, **kwargs):
    """
    Args:
        sourceAddress (CEF type: ip)
        destinationAddress
    
    Returns a JSON-serializable object that implements the configured data paths:
        public_ip_list.*.item: List of public IPs filtered from the input sourceAddresses
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    import ipaddress 
     
    outputs = {}
    resultlist = []
    
    # Write your custom code here...
    
    destinationAddress=[x for x in destinationAddress if x] if destinationAddress else []
    sourceAddress=[x for x in sourceAddress if x] if sourceAddress else []       
    
    for item in sourceAddress:
        status = ipaddress.ip_address(item).is_private
        answer = str(item) + " is private - " + str(status)
        phantom.debug(answer)
        if status == False:
            #resultlist.append({"public_ip":item})
            resultlist.append(item)
    
    
    for item in destinationAddress:
        status = ipaddress.ip_address(item).is_private
        answer = str(item) + " is private - " + str(status)
        phantom.debug(answer)
        if status == False:
            #resultlist.append({"public_ip":item})
            resultlist.append(item)
    
    resultlist = [{"item": item} for item in resultlist]    
    outputs["public_ip_list"]=resultlist
    phantom.debug(outputs)
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
