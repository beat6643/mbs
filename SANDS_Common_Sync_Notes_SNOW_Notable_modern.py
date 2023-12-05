"""
Sync the container notes to notable event or SNOW ticket.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'fb_get_container_notes' block
    fb_get_container_notes(container=container)

    return

@phantom.playbook_block()
def fb_format_container_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fb_format_container_notes() called")

    template = """%%\n\n\\n\n====================\n\\n\n{0}\n\n\n{1}\n%%"""

    # parameter list for template variable replacement
    parameters = [
        "cf_mbs_defang_notes_1:custom_function_result.data.title.*.item",
        "cf_mbs_defang_notes_1:custom_function_result.data.content.*.item"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="fb_format_container_notes", separator=", ")

    decision_2(container=container)

    return


@phantom.playbook_block()
def cf_mbs_defang_notes_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("cf_mbs_defang_notes_1() called")

    http_get_container_notes_result_data = phantom.collect2(container=container, datapath=["http_get_container_notes:action_result.data.*.response_body.data.*.title","http_get_container_notes:action_result.data.*.response_body.data.*.content","http_get_container_notes:action_result.parameter.context.artifact_id"], action_results=results)

    http_get_container_notes_result_item_0 = [item[0] for item in http_get_container_notes_result_data]
    http_get_container_notes_result_item_1 = [item[1] for item in http_get_container_notes_result_data]

    parameters = []

    parameters.append({
        "note_title_list": http_get_container_notes_result_item_0,
        "note_content_list": http_get_container_notes_result_item_1,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################
    # Write your custom code here...
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="mbs/defang_notes", parameters=parameters, name="cf_mbs_defang_notes_1", callback=fb_format_container_notes)

    return


@phantom.playbook_block()
def http_get_container_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("http_get_container_notes() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    fb_get_container_notes = phantom.get_format_data(name="fb_get_container_notes")

    parameters = []

    if fb_get_container_notes is not None:
        parameters.append({
            "headers": "",
            "location": fb_get_container_notes,
            "verify_certificate": False,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get data", parameters=parameters, name="http_get_container_notes", assets=["http test"], callback=db_non_null_note_contents)

    return


@phantom.playbook_block()
def fb_get_container_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fb_get_container_notes() called")

    template = """/note?_filter_container=\"{0}\"&sort=modified_time&order=desc&page_size=0"""

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

    phantom.format(container=container, template=template, parameters=parameters, name="fb_get_container_notes", scope="all", separator=", ", drop_none=True)

    http_get_container_notes(container=container)

    return


@phantom.playbook_block()
def db_non_null_note_contents(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("db_non_null_note_contents() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["http_get_container_notes:action_result.data.*.response_body.data.*.content", "!=", ""]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        cf_mbs_defang_notes_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    api_add_comment_no_notes(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_2() called")

    tags_value = container.get("tags", None)

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["pending_update_notable", "in", tags_value]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        fl_event_id_(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'elif' condition 2
    found_match_2 = phantom.decision(
        container=container,
        logical_operator="or",
        conditions=[
            ["pending_update_sir", "in", tags_value],
            ["pending_update_inc", "in", tags_value]
        ],
        delimiter=None)

    # call connected blocks if condition 2 matched
    if found_match_2:
        fl_snow_ticket_number_artifact(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 3
    fl_notable_event_id(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def fl_notable_event_id(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fl_notable_event_id() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.cef.event_id", "!=", ""],
            ["added_from_playbook", "==", "artifact:*.label"]
        ],
        name="fl_notable_event_id:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        api_add_comment_not_updating_notable_sir(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def fl_event_id_(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fl_event_id_() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.cef.event_id", "!=", ""],
            ["event", "==", "artifact:*.label"]
        ],
        name="fl_event_id_:condition_1",
        scope="all",
        case_sensitive=True,
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        splunk_update_notable_comment_notes(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def fl_snow_ticket_number_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fl_snow_ticket_number_artifact() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.cef.snow_ticket_number", "!=", ""],
            ["inc_ticket", "==", "artifact:*.label"]
        ],
        name="fl_snow_ticket_number_artifact:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        snow_update_snow_ticket_comment(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def splunk_update_notable_comment_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("splunk_update_notable_comment_notes() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_artifact_0_data_fl_event_id_ = phantom.collect2(container=container, datapath=["filtered-data:fl_event_id_:condition_1:artifact:*.cef.event_id","filtered-data:fl_event_id_:condition_1:artifact:*.id"], scope="all")
    fb_format_container_notes__as_list = phantom.get_format_data(name="fb_format_container_notes__as_list")

    parameters = []

    # build parameters list for 'splunk_update_notable_comment_notes' call
    for fb_format_container_notes__item in fb_format_container_notes__as_list:
        for filtered_artifact_0_item_fl_event_id_ in filtered_artifact_0_data_fl_event_id_:
            if filtered_artifact_0_item_fl_event_id_[0] is not None:
                parameters.append({
                    "owner": "",
                    "status": "",
                    "comment": fb_format_container_notes__item,
                    "urgency": "",
                    "event_ids": filtered_artifact_0_item_fl_event_id_[0],
                    "integer_status": "",
                    "wait_for_confirmation": False,
                    "context": {'artifact_id': filtered_artifact_0_item_fl_event_id_[1]},
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update event", parameters=parameters, name="splunk_update_notable_comment_notes", assets=["splunk prod"], callback=api_remove_container_tag_pending_notable)

    return


@phantom.playbook_block()
def snow_update_snow_ticket_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("snow_update_snow_ticket_comment() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_artifact_0_data_fl_snow_ticket_number_artifact = phantom.collect2(container=container, datapath=["filtered-data:fl_snow_ticket_number_artifact:condition_1:artifact:*.cef.snow_ticket_number","filtered-data:fl_snow_ticket_number_artifact:condition_1:artifact:*.id"], scope="all")
    fb_format_container_notes__as_list = phantom.get_format_data(name="fb_format_container_notes__as_list")

    parameters = []

    # build parameters list for 'snow_update_snow_ticket_comment' call
    for filtered_artifact_0_item_fl_snow_ticket_number_artifact in filtered_artifact_0_data_fl_snow_ticket_number_artifact:
        for fb_format_container_notes__item in fb_format_container_notes__as_list:
            if filtered_artifact_0_item_fl_snow_ticket_number_artifact[0] is not None and fb_format_container_notes__item is not None:
                parameters.append({
                    "id": filtered_artifact_0_item_fl_snow_ticket_number_artifact[0],
                    "comment": fb_format_container_notes__item,
                    "is_sys_id": "",
                    "table_name": "incident",
                    "context": {'artifact_id': filtered_artifact_0_item_fl_snow_ticket_number_artifact[1]},
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add comment", parameters=parameters, name="snow_update_snow_ticket_comment", assets=["service_now"], callback=api_remove_container_tag_pending_par_upd)

    return


@phantom.playbook_block()
def api_add_comment_not_updating_notable_sir(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("api_add_comment_not_updating_notable_sir() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="Not updating the notes back to Notable event of SNOW ticket as the tags are not set.")

    join_fl_notable_event_id_artifact(container=container)

    return


@phantom.playbook_block()
def api_remove_container_tag_pending_notable(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("api_remove_container_tag_pending_notable() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.remove_tags(container=container, tags="pending_notable_update")

    join_fl_notable_event_id_artifact(container=container)

    return


@phantom.playbook_block()
def api_remove_container_tag_pending_par_upd(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("api_remove_container_tag_pending_par_upd() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.remove_tags(container=container, tags="pending_update_sir")

    join_fl_notable_event_id_artifact(container=container)

    return


@phantom.playbook_block()
def api_add_comment_no_notes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("api_add_comment_no_notes() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="There are no notes to update notable event with.")

    join_fl_notable_event_id_artifact(container=container)

    return


@phantom.playbook_block()
def join_fl_notable_event_id_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("join_fl_notable_event_id_artifact() called")

    if phantom.completed(custom_function_names=["cf_mbs_defang_notes_1"], action_names=["splunk_update_notable_comment_notes", "snow_update_snow_ticket_comment", "http_get_container_notes"]):
        # call connected block "fl_notable_event_id_artifact"
        fl_notable_event_id_artifact(container=container, handle=handle)

    return


@phantom.playbook_block()
def fl_notable_event_id_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fl_notable_event_id_artifact() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.cef.event_id", "!=", ""],
            ["event", "==", "artifact:*.label"]
        ],
        name="fl_notable_event_id_artifact:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        fb_final_message(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def fb_final_message(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("fb_final_message() called")

    template = """This is the Final Message. Playbook execution from Phantom finished.\n\nContainer Tags: {0}\nContainer ID: {1}"""

    # parameter list for template variable replacement
    parameters = [
        "container:tags",
        "container:id"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="fb_final_message", separator=", ")

    db_notable_event_status(container=container)

    return


@phantom.playbook_block()
def db_notable_event_status(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("db_notable_event_status() called")

    tags_value = container.get("tags", None)

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["close_notable", "in", tags_value]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        splunk_close_notable_event(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    splunk_needs_review_notable_event(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def splunk_close_notable_event(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("splunk_close_notable_event() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_artifact_0_data_fl_notable_event_id_artifact = phantom.collect2(container=container, datapath=["filtered-data:fl_notable_event_id_artifact:condition_1:artifact:*.cef.event_id","filtered-data:fl_notable_event_id_artifact:condition_1:artifact:*.id"])
    fb_final_message = phantom.get_format_data(name="fb_final_message")

    parameters = []

    # build parameters list for 'splunk_close_notable_event' call
    for filtered_artifact_0_item_fl_notable_event_id_artifact in filtered_artifact_0_data_fl_notable_event_id_artifact:
        if filtered_artifact_0_item_fl_notable_event_id_artifact[0] is not None:
            parameters.append({
                "owner": "",
                "status": "",
                "comment": fb_final_message,
                "urgency": "",
                "event_ids": filtered_artifact_0_item_fl_notable_event_id_artifact[0],
                "integer_status": 5,
                "wait_for_confirmation": False,
                "context": {'artifact_id': filtered_artifact_0_item_fl_notable_event_id_artifact[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update event", parameters=parameters, name="splunk_close_notable_event", assets=["splunk prod"])

    return


@phantom.playbook_block()
def splunk_needs_review_notable_event(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("splunk_needs_review_notable_event() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_artifact_0_data_fl_notable_event_id_artifact = phantom.collect2(container=container, datapath=["filtered-data:fl_notable_event_id_artifact:condition_1:artifact:*.cef.event_id","filtered-data:fl_notable_event_id_artifact:condition_1:artifact:*.id"])
    fb_final_message = phantom.get_format_data(name="fb_final_message")

    parameters = []

    # build parameters list for 'splunk_needs_review_notable_event' call
    for filtered_artifact_0_item_fl_notable_event_id_artifact in filtered_artifact_0_data_fl_notable_event_id_artifact:
        if filtered_artifact_0_item_fl_notable_event_id_artifact[0] is not None:
            parameters.append({
                "owner": "",
                "status": "",
                "comment": fb_final_message,
                "urgency": "",
                "event_ids": filtered_artifact_0_item_fl_notable_event_id_artifact[0],
                "integer_status": 7,
                "wait_for_confirmation": False,
                "context": {'artifact_id': filtered_artifact_0_item_fl_notable_event_id_artifact[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update event", parameters=parameters, name="splunk_needs_review_notable_event", assets=["splunk prod"])

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