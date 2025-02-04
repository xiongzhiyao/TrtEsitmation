import pandas as pd
import numpy as np
import json


file_column_mappings = {
    "orders_after_2018-05-01_data_000": ["order_id", "map_attributes_imagery_dates", 
                                         "map_attributes_selected_imagery_date", "map_attributes_selected_version", 
                                         "map_attributes_source", "hyperion_attributes_allows_mfr", 
                                         "hyperion_attributes_is_mfr", "hyperion_attributes_is_prospect", 
                                         "hyperion_attributes_property_type", "hyperion_attributes_user_first_capture",
                                         "image_score", "deliverable_id", "deliverable_changed", "created_at", 
                                         "state", "site_id", "site_name", "sneaky", "local", "practice", 
                                         "priority", "roof_overlay", "failure_reason", "skip_markups"],
    
    "orders_after_2018-05-01_images_000": ["order_id", "score", "kind", "location", "distance", 
                                           "gps_accuracy", "make", "model"],
    
    "orders_after_2018-05-01_roof_visibility_000": ["order_id", "roof_visibility_attribute_ids"],
    
    "orders_after_2018-05-01_puborders_000": ["order_id", "order_state", "order_created_at", "order_updated_at", 
                                              "original_order_id", "order_complexity", "order_image_score", 
                                              "order_image_score_name", "priority", "order_deliverable", 
                                              "order_most_recent_failure_reason", "site_id", "order_local", 
                                              "slayer_job_id", "order_site_name", "sneaky", "order_skip_markups", 
                                              "number_of_stories", "e_number_of_stories_name", 
                                              "complexity_attributes_total_roof_facets_above_4_sqft", 
                                              "complexity_attributes_total_roof_facets", 
                                              "complexity_attributes_roof_square_footage", 
                                              "complexity_attributes_walls_square_footage", 
                                              "complexity_attributes_is_mfr", "map_attributes_source", 
                                              "slayer_attributes_allows_mfr", "slayer_attributes_is_mfr",
                                              "slayer_attributes_user_first_capture", "poser_release_number", 
                                              "structure_type", "structure_type_name", "poser_solve_status", 
                                              "hover_now", "first_qa_datetime", "first_qa_date", "models_reprocessed",
                                              "order_needs_to_be_reprocessed_flag", "special_request", "original_roof",
                                              "first_qa_for_state", "last_qa_for_state", "first_qa_email", 
                                              "first_qa_site_name", 
                                              "first_qa_majority_of_doors_within_95_percent_of_standard_sizes", 
                                              "first_qa_map_overlay_accurate", "first_qa_scale_within5_percent", 
                                              "first_qa_should_we_unfail_the_order", "qa_comments", "orthotag_list",
                                              "level_list", "pitch_estimate", "roof_estimate", 
                                              "labeler_roof_estimate", "markup_verifier_roof_estimate", 
                                              "markup_verifier_10_percent", "pitch_actual", "scaling_method",
                                              "visible_on_ortho_map", "door_areal_scale_diff", 
                                              "doors_used_for_scaling", "door_scale_deviation", "orthotag_tree_pass",
                                              "orthotag_poor_image_quality", "orthotag_none", 
                                              "orthotag_full_occlusion", "orthotag_not_on_map", 
                                              "orthotag_tree_occlusion", "orthotag_tree_fail", 
                                              "orthotag_missing_geometry", "orthotag_shadow", 
                                              "poser_solved_image_count", "poser_solved", "failed_complete_timeline", 
                                              "failed_complete_progression", "most_recent_failure_datetime", 
                                              "completed_count", "failed_count", "failed_or_complete_name_first",
                                              "failed_or_complete_name_second", "failed_or_complete_name_third", 
                                              "failed_or_complete_name_fourth", "failed_or_complete_name_fifth",
                                              "failed_or_complete_datetime_first", 
                                              "failed_or_complete_datetime_second", 
                                              "failed_or_complete_datetime_third", 
                                              "failed_or_complete_datetime_fourth",
                                              "failed_or_complete_datetime_fifth", "number_of_images",
                                              "average_image_score", "image_count_deleted", "image_count_0_sides",
                                              "image_count_1_side", "image_count_2_sides", "image_count_unscored", 
                                              "first_completion", "most_recent_completion", 
                                              "unfail_premium_order_flag", "turn_around_time_total", 
                                              "turn_around_time_first_completion", "total_resolution_time_total", 
                                              "total_resolution_time_first_completion", "human_bpo_time_waiting_total",
                                              "human_bpo_time_waiting_first_completion", "turn_around_time_wasted",
                                              "human_bpo_time_wasted", "labeling_time_total", 
                                              "labeling_time_first_completion", "markup_verifying_time_total",
                                              "markup_verifying_time_first_completion", "model_building_time_total",
                                              "model_building_time_first_completion", "modeling_time_total", 
                                              "modeling_time_first_completion", "model_completing_time_total", 
                                              "model_completing_time_first_completion", "web_segmenting_time_total",
                                              "web_segmenting_time_first_completion", "model_segmenting_time_total",
                                              "model_segmenting_time_first_completion", "verifying_time_total", 
                                              "verifying_time_first_completion", "texturing_time_total", 
                                              "texturing_time_first_completion", "qa_time_total", 
                                              "openings_marking_time_total", "openings_marking_time_first_completion",
                                              "vps_marking_time_total", "vps_marking_time_first_completion", 
                                              "primitive_marking_time_total", 
                                              "primitive_marking_time_first_completion"],
    
    "orders_after_2018-05-01_pubtasks_000": ["order_id", "state_transition_id", "transition_type", "transition_id",
                                             "image_id", "namespace", "event", "unlock_indicator", "from_state", 
                                             "to_state", "trigger_user_id", "seconds_in_state", 
                                             "transition_created_at", "image_markup_corrected_openings", 
                                             "image_markup_corrected_vps", "image_markup_corrected_primitive", 
                                             "image_markup_verify_result_reason_id_vps", "image_markup_verify_result_reason_id_openings", 
                                             "image_markup_verify_result_reason_id_primitive", "first_completion", 
                                             "most_recent_completion", "first_failure", "most_recent_failure", 
                                             "completion_time", "completion_count", "previous_completion_time", 
                                             "previous_completion_count", "total_completion_count", 
                                             "last_order_state_transition_id_of_type_before_complete", 
                                             "last_state_transition_of_type_before_complete_indicator", 
                                             "original_order_id", "order_current_state", "deliverable_name", 
                                             "order_image_score", "image_score_name", "sneaky", "order_complexity",
                                             "orders_most_recent_failure_reason_name", "skip_markups", 
                                             "complexity_attributes_is_mfr", "slayer_attributes_allows_mfr", 
                                             "slayer_attributes_is_mfr", "slayer_attributes_user_first_capture", 
                                             "poser_release_number", "structure_type", "poser_solve_status", "hover_now", 
                                             "map_attributes_source", "poser_solved_indicator", "order_site_name", 
                                             "modeler_email", "modeler_site_name", "modeler_roles", "resource_type", 
                                             "modeler_proficiency_level", "waiting_indicator", "unfail_premium_order_indicator"],
}

file_name_name_mapping = {
    #"orders_after_2018-05-01_data_000": "orders",
    #"orders_after_2018-05-01_images_000": "images",
    #"orders_after_2018-05-01_roof_visibility_000": "roof_visibility",
    "orders_after_2018-05-01_puborders_000": "puborders",
    "orders_after_2018-05-01_pubtasks_000": "pubtasks",
}
print("Loading Data... ")
data = {}
for file_name, column_names in file_column_mappings.items():
    nice_name = file_name_name_mapping.get(file_name, None)
    if nice_name:
        print("Loading %s"%(nice_name))
        data[nice_name] = pd.read_csv("../data/%s" % file_name,
                                      sep='|',
                                      index_col=False, 
                                      names=column_names
                                    )
print("Data Loaded!")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():

    granularity = 60
    puborders = data['puborders']
    pubtasks = data['pubtasks']
    cmds = []

    for index in range(len(puborders.index)):
        out_rows = {}
        row = puborders.iloc[index]
        if row['sneaky']:
            continue

        # Extract necessary puborders info
        order_id = row['order_id']
        order_site_name = row['order_site_name']
        created = row['order_created_at']

        out_rows['puborder'] = row.to_dict()

        order_events = pubtasks[pubtasks["order_id"] == int(order_id)]
        out_rows['pubtasks'] = []
        for index_t, row_t in order_events.iterrows():
            out_rows['pubtasks'].append(row_t.to_dict())
        
        out_f = open("rows/%s.json" % order_id, 'w')
        json.dump(out_f, out_rows)
        out_f.close()

        cmd = "python extract_single_order.py %s %i" % (order_id, granularity)
        cmds.append(cmd)
        break
    out_f = open("cmds.txt", 'w')
    for c in cmds:
        out_f.write("%s\n" % c)

if __name__ == "__main__":
    main()
