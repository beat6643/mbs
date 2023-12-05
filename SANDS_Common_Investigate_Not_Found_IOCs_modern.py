"""
This playbook searches for IOCs that are not found while trying to investigate against a tool such as Virus Total or Threat Crowd and adds them to the note.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'fb_action_result_messages' block
    fb_action_result_messages(container=container)

    return

@phantom.playbook_block()
def http_get_find_ioc_not_found_vt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("http_get_find_ioc_not_found_vt() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    fb_rest_find_ioc_not_found_vt__as_list = phantom.get_format_data(name="fb_rest_find_ioc_not_found_vt__as_list")

    parameters = []

    # build parameters list for 'http_get_find_ioc_not_found_vt' call
    for fb_rest_find_ioc_not_found_vt__item in fb_rest_find_ioc_not_found_vt__as_list:
        if fb_rest_find_ioc_not_found_vt__item is not None:
            parameters.append({
                "headers": "",
                "location": fb_rest_find_ioc_not_found_vt__item,
                "verify_certificate": False,
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get data", parameters=parameters, name="http_get_find_ioc_not_found_vt", assets=["http test"], callback=db_non_null_action_result)

    return


@phantom.playbook_block()
def db_non_null_action_result(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("db_non_null_action_result() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["http_get_find_ioc_not_found_vt:action_result.data.*.response_body.data.*.result_data.*.message", "!=", ""]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        cf_mbs_filter_action_result_parameter_2(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def api_failed_actions_note(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("api_failed_actions_note() called")

    fb_failed_actions_note = phantom.get_format_data(name="fb_failed_actions_note")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=fb_failed_actions_note, note_format="html", title="Failed Actions List")

    return


@phantom.playbook_block()
def db_is_action_result_non_empty(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("db_is_action_result_non_empty() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["cf_mbs_filter_action_result_parameter_2:custom_function_result.data.action_result_count", "!=", 0]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        fb_failed_actions_note(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def fb_failed_actions_note(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fb_failed_actions_note() called")

    template = """{3} actions failed.\n\nBelow are the failed actions which needs attention.\n\n%%\nParameter: {0}\nApp Name: {1}\nAction Name: {2}\n\n%%"""

    # parameter list for template variable replacement
    parameters = [
        "cf_mbs_filter_action_result_parameter_2:custom_function_result.data.filtered_action_result.*.parameter",
        "cf_mbs_filter_action_result_parameter_2:custom_function_result.data.filtered_action_result.*.app_name",
        "cf_mbs_filter_action_result_parameter_2:custom_function_result.data.filtered_action_result.*.action_name",
        "cf_mbs_filter_action_result_parameter_2:custom_function_result.data.action_result_count"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="fb_failed_actions_note", separator=", ")

    api_failed_actions_note(container=container)

    return


@phantom.playbook_block()
def fb_action_result_messages(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fb_action_result_messages() called")

    template = """failed, No data was returned, not found, notfound, NotFoundError"""

    # parameter list for template variable replacement
    parameters = [
        "container:id"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="fb_action_result_messages", separator=", ")

    cf_mbs_string_split_1(container=container)

    return


@phantom.playbook_block()
def fb_rest_find_ioc_not_found_vt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fb_rest_find_ioc_not_found_vt() called")

    template = """%%\n/app_run?_filter_container={0}&_filter_message__icontains=\"{1}\"&_exclude_app_name__in=[\"HTTP\", \"VirusTotal v3\"]&include_expensive&page_size=0\n%%"""

    # parameter list for template variable replacement
    parameters = [
        "multiply_input:custom_function_result.data.multiplied_output.*.item",
        "cf_mbs_string_split_1:custom_function_result.data.*.item"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="fb_rest_find_ioc_not_found_vt", scope="all", separator=", ", drop_none=True)

    http_get_find_ioc_not_found_vt(container=container)

    return


@phantom.playbook_block()
def cf_mbs_string_split_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("cf_mbs_string_split_1() called")

    fb_action_result_messages = phantom.get_format_data(name="fb_action_result_messages")

    parameters = []

    parameters.append({
        "delimiter": None,
        "input_string": fb_action_result_messages,
        "strip_whitespace": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################
    # Write your custom code here...
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="mbs/string_split", parameters=parameters, name="cf_mbs_string_split_1", callback=multiply_input)

    return


@phantom.playbook_block()
def multiply_input(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("multiply_input() called")

    id_value = container.get("id", None)
    cf_mbs_string_split_1_data = phantom.collect2(container=container, datapath=["cf_mbs_string_split_1:custom_function_result.data.*.item"])

    cf_mbs_string_split_1_data___item = [item[0] for item in cf_mbs_string_split_1_data]

    parameters = []

    parameters.append({
        "input_list": cf_mbs_string_split_1_data___item,
        "input_to_multiply": id_value,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################
    # Write your custom code here...
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="mbs/multiply_input", parameters=parameters, name="multiply_input", callback=fb_rest_find_ioc_not_found_vt)

    return


@phantom.playbook_block()
def cf_mbs_filter_action_result_parameter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("cf_mbs_filter_action_result_parameter_2() called")

    id_value = container.get("id", None)
    http_get_find_ioc_not_found_vt_result_data = phantom.collect2(container=container, datapath=["http_get_find_ioc_not_found_vt:action_result.data.*.response_body.data","http_get_find_ioc_not_found_vt:action_result.parameter.context.artifact_id"], action_results=results)

    http_get_find_ioc_not_found_vt_result_item_0 = [item[0] for item in http_get_find_ioc_not_found_vt_result_data]

    parameters = []

    parameters.append({
        "input_to_multiply": id_value,
        "action_result_data_list": http_get_find_ioc_not_found_vt_result_item_0,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################
    # Write your custom code here...
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="mbs/filter_action_result_parameter", parameters=parameters, name="cf_mbs_filter_action_result_parameter_2", callback=db_is_action_result_non_empty)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return