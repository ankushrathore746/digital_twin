
from simulation import intake

from flask import Flask, request, jsonify, render_template, render_template_string, redirect, url_for
import pandas as pd
from flasgger import Swagger
import flasgger
from flask_cors import CORS

app = Flask(__name__)
Swagger(app)
CORS(app)


@app.route('/', methods=["Post"])
def prediction():
    """Let's predict the days
    This is using docstrings for specifications.s

    ---
    parameters:
      - name: current_demand
        in: query
        type: number
        required: true
       - name: client_interview_people_percentage
        in: query
        type: number
        required: true
      - name: joining_rate_proactive
        in: query
        type: number
        required: true
      - name: deallocatted_new
        in: query
        type: number
        required: true
      - name: pool_emp
        in: query
        type: number
        required: true
      - name: offer_made_for_proactive
        in: query
        type: number
        required: true
      - name: lead_time_for_deallocation
        in: query
        type: number
        required: true
      - name: rotation_emp
        in: query
        type: number
        required: true
      - name: lead_time_to_onboard_proactive
        in: query
        type: number
        required: true
      - name: lead_time_for_rotation
        in: query
        type: number
        required: true
      - name: skill_profiles_time
        in: query
        type: number
        required: true
      - name: skill_profiles_ratio_proactive
        in: query
        type: number
        required: true
      - name: skill_profiles_ratio_rotation
        in: query
        type: number
        required: true
      - name: skill_profiles_ratio_pool
        in: query
        type: number
        required: true
      - name: skill_profiles_ratio_deallocation
        in: query
        type: number
        required: true
       - name: internal_resume_selection_ratio
        in: query
        type: number
        required: true
       - name: internal_resume_selection_time
        in: query
        type: number
        required: true
      - name: first_internal_interview_ratio
        in: query
        type: number
        required: true
      - name: first_internal_interview_time
        in: query
        type: number
        required: true
      - name: second_internal_interview_ratio
        in: query
        type: number
        required: true
      - name: second_internal_interview_time
        in: query
        type: number
        required: true
      - name: review_on_available_associates_proactive
        in: query
        type: number
        required: true
      - name: review_on_available_associates_rotation
        in: query
        type: number
        required: true
      - name: review_on_available_associates_deallocation
        in: query
        type: number
        required: true
      - name: review_on_available_associates_pool
        in: query
        type: number
        required: true
      - name: review_on_available_associates_time
        in: query
        type: number
        required: true
      - name: profile_selection_by_client_ratio
        in: query
        type: number
        required: true
      - name: profile_selection_by_client_time
        in: query
        type: number
        required: true
      - name: first_client_interview_ratio
        in: query
        type: number
        required: true
      - name: first_client_interview_time
        in: query
        type: number
        required: true
      - name: second_client_interview_ratio
        in: query
        type: number
        required: true
      - name: second_client_interview_time
        in: query
        type: number
        required: true
      - name: lead_time_to_deploy
        in: query
        type: number
        required: true
      - name: checkbox_second_it_interview
        in: query
        type: number
        required: true
      - name: checkbox_review_available_associates
        in: query
        type: number
        required: true
      - name: checkbox_profile_selection_by_client
        in: query
        type: number
        required: true
      - name: checkbox_first_cl_interview
        in: query
        type: number
        required: true
      - name: checkbox_second_cl_interview
        in: query
        type: number
        required: true

    responses:
        200:
            description: The output values

    """

    checkbox_second_it_interview = request.form.get('checkbox_second_it_interview', type=int)
    checkbox_review_available_associates = request.form.get('checkbox_review_available_associates', type=int)
    checkbox_profile_selection_by_client = request.form.get('checkbox_profile_selection_by_client', type=int)
    checkbox_first_cl_interview = request.form.get('checkbox_first_cl_interview', type=int)
    checkbox_second_cl_interview = request.form.get('checkbox_second_cl_interview', type=int)
    checkbox_related_skill = request.form.get('checkbox_related_skill', type=int)

    current_demand = request.form.get('current_demand', type=int)
    client_interview_people_percentage = request.form.get('client_interview_people_percentage', type=int)

    joining_rate_proactive = request.form.get('joining_rate_proactive', type=int)
    deallocatted_new = request.form.get('deallocatted_new', type=int)
    pool_emp = request.form.get('pool_emp', type=int)
    rotation_emp = request.form.get('rotation_emp', type=int)
    offer_made_for_proactive = request.form.get('offer_made_for_proactive', type=int)

    lead_time_for_rotation = request.form.get('lead_time_for_rotation', type=int)
    lead_time_for_deallocation = request.form.get('lead_time_for_deallocation', type=int)
    lead_time_to_onboard_proactive = request.form.get('lead_time_to_onboard_proactive', type=int)

    skill_profiles_ratio_proactive = request.form.get('skill_profiles_ratio_proactive', type=int)
    skill_profiles_ratio_pool = request.form.get('skill_profiles_ratio_pool', type=int)
    skill_profiles_ratio_rotation = request.form.get('skill_profiles_ratio_rotation', type=int)
    skill_profiles_ratio_deallocation = request.form.get('skill_profiles_ratio_deallocation', type=int)
    skill_profiles_time = request.form.get('skill_profiles_time', type=int)

    internal_resume_selection_ratio = request.form.get('internal_resume_selection_ratio', type=int)
    internal_resume_selection_time = request.form.get('internal_resume_selection_time', type=int)

    first_internal_interview_ratio = request.form.get('first_internal_interview_ratio', type=int)
    first_internal_interview_time = request.form.get('first_internal_interview_time', type=int)

    second_internal_interview_ratio = request.form.get('second_internal_interview_ratio', type=int)
    second_internal_interview_time = request.form.get('second_internal_interview_time', type=int)

    review_on_available_associates_ratio_proactive = request.form.get('review_on_available_associates_ratio_proactive', type=int)
    review_on_available_associates_ratio_deallocation = request.form.get('review_on_available_associates_ratio_deallocation', type=int)
    review_on_available_associates_ratio_pool = request.form.get('review_on_available_associates_ratio_pool', type=int)
    review_on_available_associates_ratio_rotation = request.form.get('review_on_available_associates_ratio_rotation',type=int)
    review_on_available_associates_time = request.form.get('review_on_available_associates_time', type=int)

    profile_selection_by_client_ratio = request.form.get('profile_selection_by_client_ratio', type=int)
    profile_selection_by_client_time = request.form.get('profile_selection_by_client_time', type=int)

    first_client_interview_ratio = request.form.get('first_client_interview_ratio', type=int)
    first_client_interview_time = request.form.get('first_client_interview_time', type=int)

    second_client_interview_ratio = request.form.get('second_client_interview_ratio', type=int)
    second_client_interview_time = request.form.get('second_client_interview_time', type=int)

    lead_time_to_deploy = request.form.get('lead_time_to_deploy', type=int)

    result = intake(current_demand, client_interview_people_percentage, offer_made_for_proactive,
                    joining_rate_proactive, pool_emp, deallocatted_new, rotation_emp,
                    lead_time_for_rotation, lead_time_for_deallocation, skill_profiles_ratio_proactive,
                    skill_profiles_ratio_deallocation,
                    skill_profiles_ratio_pool, skill_profiles_ratio_rotation, skill_profiles_time,
                    lead_time_to_onboard_proactive, internal_resume_selection_ratio, internal_resume_selection_time,
                    first_internal_interview_ratio, first_internal_interview_time,
                    second_internal_interview_ratio, second_internal_interview_time,
                    review_on_available_associates_ratio_proactive,
                    review_on_available_associates_ratio_pool, review_on_available_associates_ratio_deallocation,
                    review_on_available_associates_ratio_rotation,
                    review_on_available_associates_time, profile_selection_by_client_ratio,
                    profile_selection_by_client_time,
                    first_client_interview_ratio, first_client_interview_time, second_client_interview_ratio,
                    second_client_interview_time,
                    lead_time_to_deploy, checkbox_second_it_interview, checkbox_review_available_associates,
                    checkbox_profile_selection_by_client, checkbox_first_cl_interview, checkbox_second_cl_interview,
                    checkbox_related_skill)

    return result


if __name__ == '__main__':
    app.run()








