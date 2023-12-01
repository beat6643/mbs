def parse_crowdstrike_ioc_api_results_modified(crowdstrike_parsed_response_body=None, **kwargs):
    """
    The custom function formats the IOC json results from crowdstrike into a list
    
    Args:
        crowdstrike_parsed_response_body
    
    Returns a JSON-serializable object that implements the configured data paths:
        last_updated: last updated time
        actors
        malicious_confidence
        malware_family
        reports
        results
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    import datetime 
    
    outputs = { } # raw output placed in dictionary

    i = 0

    outputs["last_updated"] = None
    outputs["threat_actor"] = None
    outputs["malicious_confidence"] = None
    outputs["malware_family"] = None
    outputs["reports"] = None
    outputs["indicator"] = None
    results = []
    formatted_result = ""
    chunk = None

    if len(crowdstrike_parsed_response_body["resources"]) > 0:
        while i < len(crowdstrike_parsed_response_body["resources"]): #loop to print outputs
            raw_output = crowdstrike_parsed_response_body["resources"][i] #Temp variable
            if raw_output["deleted"] == False:
                epoch_time = raw_output["last_updated"]
                outputs["last_updated"] = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d')
                outputs["threat_actor"] = raw_output["actors"] if raw_output["actors"] else "None"
                outputs["malicious_confidence"] = raw_output["malicious_confidence"]
                outputs["malware_family"] = raw_output["malware_families"] if raw_output["malware_families"] else "None"
                outputs["reports"] = raw_output["reports"] if raw_output["reports"] else "None"    
                outputs["indicator"] = raw_output["indicator"] if raw_output["indicator"] else "None"
                formatted_result = "Indicator:" + str(outputs["indicator"]), "Actors:" + str(outputs["threat_actor"]), "Malicious Confidence:" + str(outputs["malicious_confidence"]), "Malware Family:" + str(outputs["malware_family"]), "Reports:" + str(outputs["reports"]), "Last Updated:" + str(outputs["last_updated"])
                results.append(formatted_result)
            i+=1

    chunk = '<br><br>'.join('<br>'.join(tup) for tup in results)
    
    outputs["results"] = chunk
    phantom.debug("modified")
    phantom.debug(outputs["results"])
    return outputs