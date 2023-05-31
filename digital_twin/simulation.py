import itertools
import simpy
import numpy as np
global round
my_dict = {}
demand_list = []










def project_allocation(env,
                       pool_container,
                       container,
                       current_demand,
                       event_list,
                       ultimate_dict,
                       round,
                       lead_time_to_deploy,
                       trigger_event,
                       num_of_selected_people,
                       category
                       ):
    """
    :param env:  Simpy environment
    :param container: Container for pool
    :param lead_time_to_deploy:  Lead time to onboard for particular category people
    :return: None
    """

    yield env.timeout(lead_time_to_deploy)
    yield container.get(num_of_selected_people)
    print(f"Day {np.floor(env.now)} from {category} category {num_of_selected_people} associates are allocated on project")
    event_happend_1 = {'day': (np.floor(env.now)),
                       'statement': f'{num_of_selected_people} associates are allocated on project'}
    event_list.append(event_happend_1)



    if num_of_selected_people>0:
        yield pool_container.put(num_of_selected_people)

    print(f"{pool_container.level} are allocated on projects")
    demand_remaining = current_demand - pool_container.level
    print(f"after allocation {demand_remaining} demand is remaining")

    if round==0:
        event_happend_2 = {'day': (np.floor(env.now)),
                           'statement':f'from {category}, {num_of_selected_people} associates allocatted through direct allocation\n'
                                       f'{demand_remaining} demand is remaining'}
        demand_list.append(event_happend_2)
        if category=='Proactive':
            my_dict['proactive'] = event_list
            my_dict['result_1'] = demand_list
        elif category=='rotation':
            my_dict['rotation'] = event_list
            my_dict['result_1'] = demand_list
        elif category=='deallocation':
            my_dict['deallocation'] = event_list
            my_dict['result_1'] = demand_list
        elif category=='Pool':
            my_dict['Pool'] = event_list
            my_dict['result_1'] = demand_list

    elif round>0:
        event_happend_2 = {'day': (np.floor(env.now)),
                           'statement':f'from {category}, {num_of_selected_people} associates allocatted through client interview\n'
                                       f'{demand_remaining} demand is remaining'}
        demand_list.append(event_happend_2)

        if category=='Proactive':
            my_dict['proactive'] = event_list
            my_dict['result'] = demand_list
        elif category=='rotation':
            my_dict['rotation'] = event_list
            my_dict['result'] = demand_list
        elif category=='deallocation':
            my_dict['deallocation'] = event_list
            my_dict['result'] = demand_list
        elif category=='Pool':
            my_dict['Pool'] = event_list
            my_dict['result'] = demand_list












def second_client_interview(env,
                           pool_container,
                           container,
                           current_demand,
                           event_list,
                            ultimate_dict,
                            round,
                            second_client_interview_ratio,
                           second_client_interview_time,
                           lead_time_to_deploy,
                           trigger_event,
                           checkbox_second_cl_interview,
                           category
                           ):

    yield env.timeout(second_client_interview_time)
    at_first_size = container.level
    second_client_interview_selected_ppl = abs(np.ceil(at_first_size * (second_client_interview_ratio / 100)))

    remaining_ppl = at_first_size - second_client_interview_selected_ppl
    if remaining_ppl>0:
        yield container.get(remaining_ppl)

    if checkbox_second_cl_interview == 1:
        print(f"Day {np.floor(env.now)} from {category} category {second_client_interview_selected_ppl} associates are selected by client in second interview")

        event_happend_1 = {'day': (np.floor(env.now)),
                           'statement': f'{second_client_interview_selected_ppl} associates are selected by client in second client interview'}
        event_list.append(event_happend_1)

    env.process(project_allocation(env,
                                   pool_container,
                                   container,
                                   current_demand,
                                   event_list,
                                   ultimate_dict,
                                   round,
                                   lead_time_to_deploy,
                                   trigger_event,
                                   second_client_interview_selected_ppl,
                                   category
                                   ))



def first_client_interview(env,
                           pool_container,
                           container,
                           current_demand,
                           event_list,
                           ultimate_dict,
                           round,
                           first_client_interview_ratio,
                           first_client_interview_time,
                           second_client_interview_ratio,
                           second_client_interview_time,
                           lead_time_to_deploy,
                           trigger_event,
                           checkbox_first_cl_interview,
                           checkbox_second_cl_interview,
                           category
                           ):

    yield env.timeout(first_client_interview_time)
    at_first_size = container.level
    first_client_interview_selected_ppl = abs(np.ceil(at_first_size * (first_client_interview_ratio / 100)))

    remaining_ppl = at_first_size - first_client_interview_selected_ppl
    if remaining_ppl>0:
        yield container.get(remaining_ppl)

    if checkbox_first_cl_interview == 1:
        print(f"Day {np.floor(env.now)} from {category} category {first_client_interview_selected_ppl} associates are selected by client in first client interview")

        event_happend_1 = {'day': (np.floor(env.now)),
                           'statement': f'{first_client_interview_selected_ppl} associates are selected by client in first interview'}
        event_list.append(event_happend_1)

    env.process(second_client_interview(env,
                                        pool_container,
                                        container,
                                        current_demand,
                                        event_list,
                                        ultimate_dict,
                                        round,
                                        second_client_interview_ratio,
                                        second_client_interview_time,
                                        lead_time_to_deploy,
                                        trigger_event,
                                        checkbox_second_cl_interview,
                                        category
                                        ))




def profile_selection_by_client(env,
                                pool_container,
                                container,
                                current_demand,
                                event_list,
                                ultimate_dict,
                                round,
                                profile_selection_by_client_ratio,
                                profile_selection_by_client_time,
                                first_client_interview_ratio,
                                first_client_interview_time,
                                second_client_interview_ratio,
                                second_client_interview_time,
                                lead_time_to_deploy,
                                trigger_event,
                                checkbox_profile_selection_by_client,
                                checkbox_first_cl_interview,
                                checkbox_second_cl_interview,
                                category
                                ):

    yield env.timeout(profile_selection_by_client_time)
    at_first_size = container.level
    profile_selection_by_client = abs(np.ceil(at_first_size * (profile_selection_by_client_ratio / 100)))

    remaining_ppl = at_first_size - profile_selection_by_client
    if remaining_ppl>0:
        yield container.get(remaining_ppl)
    if checkbox_profile_selection_by_client == 1:
        print(f"Day {np.floor(env.now)} from {category} category {profile_selection_by_client} profiles selected by client for client interview")

        event_happend_1 = {'day': (np.floor(env.now)),
                           'statement': f'{profile_selection_by_client} profiles selected by client for client interview'}
        event_list.append(event_happend_1)

    env.process(first_client_interview(env,
                                       pool_container,
                                       container,
                                       current_demand,
                                       event_list,
                                       ultimate_dict,
                                       round,
                                       first_client_interview_ratio,
                                       first_client_interview_time,
                                       second_client_interview_ratio,
                                       second_client_interview_time,
                                       lead_time_to_deploy,
                                       trigger_event,
                                       checkbox_first_cl_interview,
                                       checkbox_second_cl_interview,
                                       category
                                       ))

def review_on_available_associates(env,
                                   pool_container,
                                   container,
                                   current_demand,
                                   event_list,
                                   ultimate_dict,
                                   round,
                                   review_on_available_associates_ratio,
                                   review_on_available_associates_time,
                                   profile_selection_by_client_ratio,
                                   profile_selection_by_client_time,
                                   first_client_interview_ratio,
                                   first_client_interview_time,
                                   second_client_interview_ratio,
                                   second_client_interview_time,
                                   lead_time_to_deploy,
                                   trigger_event,
                                   checkbox_review_available_associates,
                                   checkbox_profile_selection_by_client,
                                   checkbox_first_cl_interview,
                                   checkbox_second_cl_interview,
                                   category
                                   ):
    yield env.timeout(review_on_available_associates_time)

    at_first_size = container.level
    final_available_associates = abs(np.ceil(at_first_size * (review_on_available_associates_ratio / 100)))

    remaining_ppl = at_first_size - final_available_associates
    if remaining_ppl>0:
        yield container.get(remaining_ppl)

    if checkbox_review_available_associates == 1:
        print(f"Day {np.floor(env.now)} from {category} category {final_available_associates} associates are available for client interview")

        event_happend_1 = {'day': (np.floor(env.now)),
                           'statement': f'{final_available_associates} associates are available for client interview'}
        event_list.append(event_happend_1)

    env.process(profile_selection_by_client(env,
                                            pool_container,
                                            container,
                                            current_demand,
                                            event_list,
                                            ultimate_dict,
                                            round,
                                            profile_selection_by_client_ratio,
                                            profile_selection_by_client_time,
                                            first_client_interview_ratio,
                                            first_client_interview_time,
                                            second_client_interview_ratio,
                                            second_client_interview_time,
                                            lead_time_to_deploy,
                                            trigger_event,
                                            checkbox_profile_selection_by_client,
                                            checkbox_first_cl_interview,
                                            checkbox_second_cl_interview,
                                            category
                                            ))


def second_internal_interview(env,
                              pool_container,
                              container,
                              current_demand,
                              event_list,
                              ultimate_dict,
                              round,
                              client_interview_people_percentage,
                              second_internal_interview_ratio,
                              second_internal_interview_time,
                              review_on_available_associates_ratio,
                              review_on_available_associates_time,
                              profile_selection_by_client_ratio,
                              profile_selection_by_client_time,
                              first_client_interview_ratio,
                              first_client_interview_time,
                              second_client_interview_ratio,
                              second_client_interview_time,
                              lead_time_to_deploy,
                              trigger_event,
                              checkbox_second_it_interview,
                              checkbox_review_available_associates,
                              checkbox_profile_selection_by_client,
                              checkbox_first_cl_interview,
                              checkbox_second_cl_interview,
                              category
                              ):

    yield env.timeout(second_internal_interview_time)
    at_first_size = container.level
    second_internal_interview_selected_ppl = abs(np.ceil(at_first_size * (second_internal_interview_ratio / 100)))

    remaining_ppl = at_first_size - second_internal_interview_selected_ppl
    if remaining_ppl>0:
        yield container.get(remaining_ppl)
    if checkbox_second_it_interview == 1:
        print(f"Day {np.floor(env.now)} from {category} category {second_internal_interview_selected_ppl} associates are selected by internal team in 2nd internal interview")

        event_happend_1 = {'day': (np.floor(env.now)),
                           'statement': f'{second_internal_interview_selected_ppl} associates are selected by internal team in 2nd internal interview'}
        event_list.append(event_happend_1)

    env.process(demand_through_separate_interview(env,
                                                  pool_container,
                                                  container,
                                                  current_demand,
                                                  event_list,
                                                  ultimate_dict,
                                                  round,
                                                  client_interview_people_percentage,
                                                  second_internal_interview_ratio,
                                                  second_internal_interview_time,
                                                  review_on_available_associates_ratio,
                                                  review_on_available_associates_time,
                                                  profile_selection_by_client_ratio,
                                                  profile_selection_by_client_time,
                                                  first_client_interview_ratio,
                                                  first_client_interview_time,
                                                  second_client_interview_ratio,
                                                  second_client_interview_time,
                                                  lead_time_to_deploy,
                                                  trigger_event,
                                                  checkbox_second_it_interview,
                                                  checkbox_review_available_associates,
                                                  checkbox_profile_selection_by_client,
                                                  checkbox_first_cl_interview,
                                                  checkbox_second_cl_interview,
                                                  category
                                                  ))


def demand_through_separate_interview(env,
                                      pool_container,
                                      container,
                                      current_demand,
                                      event_list,
                                      ultimate_dict,
                                      round,
                                      client_interview_people_percentage,
                                      second_internal_interview_ratio,
                                      second_internal_interview_time,
                                      review_on_available_associates_ratio,
                                      review_on_available_associates_time,
                                      profile_selection_by_client_ratio,
                                      profile_selection_by_client_time,
                                      first_client_interview_ratio,
                                      first_client_interview_time,
                                      second_client_interview_ratio,
                                      second_client_interview_time,
                                      lead_time_to_deploy,
                                      trigger_event,
                                      checkbox_second_it_interview,
                                      checkbox_review_available_associates,
                                      checkbox_profile_selection_by_client,
                                      checkbox_first_cl_interview,
                                      checkbox_second_cl_interview,
                                      category
                                      ):
    yield env.timeout(0)
    trail_container = simpy.Container(env, capacity=float('inf'), init=0)
    at_first = container.level
    client_interview_people= np.ceil((client_interview_people_percentage/100) * at_first)
    direct_fulfillment = at_first - client_interview_people

    if direct_fulfillment>0:

        num_of_selected_people = direct_fulfillment
        print(f"from {category} {num_of_selected_people} employee are going to direct project allocation")
        event_happend_1 = {'day': (np.floor(env.now)),
                           'statement': f'{num_of_selected_people} employees are going to direct project allocation'}
        event_list.append(event_happend_1)
        env.process(project_allocation(env,
                                   pool_container,
                                   container,
                                   current_demand,
                                   event_list,
                                   ultimate_dict,
                                   round,
                                   lead_time_to_deploy,
                                   trigger_event,
                                   num_of_selected_people,
                                   category
                                   ))

    if client_interview_people>0:
        round += 1
        yield trail_container.put(client_interview_people)
        print(f"from {category} {client_interview_people} employee are going to client interview")

        event_happend_1 = {'day': (np.floor(env.now)),
                           'statement': f'{client_interview_people} employees are going to client interview'}
        event_list.append(event_happend_1)
        env.process(review_on_available_associates(env,
                                                   pool_container,
                                                   trail_container,
                                                   current_demand,
                                                   event_list,
                                                   ultimate_dict,
                                                   round,
                                                   review_on_available_associates_ratio,
                                                   review_on_available_associates_time,
                                                   profile_selection_by_client_ratio,
                                                   profile_selection_by_client_time,
                                                   first_client_interview_ratio,
                                                   first_client_interview_time,
                                                   second_client_interview_ratio,
                                                   second_client_interview_time,
                                                   lead_time_to_deploy,
                                                   trigger_event,
                                                   checkbox_review_available_associates,
                                                   checkbox_profile_selection_by_client,
                                                   checkbox_first_cl_interview,
                                                   checkbox_second_cl_interview,
                                                   category
                                                   ))



def first_internal_interview(env,
                             pool_container,
                             container,
                             current_demand,
                             event_list,
                             ultimate_dict,
                             round,
                             client_interview_people_percentage,
                             first_internal_interview_ratio,
                             first_internal_interview_time,
                             second_internal_interview_ratio,
                             second_internal_interview_time,
                             review_on_available_associates_ratio,
                             review_on_available_associates_time,
                             profile_selection_by_client_ratio,
                             profile_selection_by_client_time,
                             first_client_interview_ratio,
                             first_client_interview_time,
                             second_client_interview_ratio,
                             second_client_interview_time,
                             lead_time_to_deploy,
                             trigger_event,
                             checkbox_second_it_interview,
                             checkbox_review_available_associates,
                             checkbox_profile_selection_by_client,
                             checkbox_first_cl_interview,
                             checkbox_second_cl_interview,
                             category
                             ):

    yield env.timeout(first_internal_interview_time)
    at_first_size = container.level
    first_internal_interview_selected_ppl = abs(np.ceil(at_first_size * (first_internal_interview_ratio / 100)))
    print(f"Day {np.floor(env.now)} from {category} category {first_internal_interview_selected_ppl} associates are selected by internal team in 1st it interview")

    event_happend_1 = {'day': (np.floor(env.now)), 'statement': f'{first_internal_interview_selected_ppl} associates are selected by internal team in 1st internal interview'}
    event_list.append(event_happend_1)

    remaining_ppl = at_first_size - first_internal_interview_selected_ppl
    if remaining_ppl>0:
        yield container.get(remaining_ppl)

    if checkbox_second_it_interview== 1:
        env.process(second_internal_interview(env,
                                              pool_container,
                                              container,
                                              current_demand,
                                              event_list,
                                              ultimate_dict,
                                              round,
                                              client_interview_people_percentage,
                                              second_internal_interview_ratio,
                                              second_internal_interview_time,
                                              review_on_available_associates_ratio,
                                              review_on_available_associates_time,
                                              profile_selection_by_client_ratio,
                                              profile_selection_by_client_time,
                                              first_client_interview_ratio,
                                              first_client_interview_time,
                                              second_client_interview_ratio,
                                              second_client_interview_time,
                                              lead_time_to_deploy,
                                              trigger_event,
                                              checkbox_second_it_interview,
                                              checkbox_review_available_associates,
                                              checkbox_profile_selection_by_client,
                                              checkbox_first_cl_interview,
                                              checkbox_second_cl_interview,
                                              category
                                              ))

    else:
        env.process(demand_through_separate_interview(env,
                                                      pool_container,
                                                      container,
                                                      current_demand,
                                                      event_list,
                                                      ultimate_dict,
                                                      round,
                                                      client_interview_people_percentage,
                                                      second_internal_interview_ratio,
                                                      second_internal_interview_time,
                                                      review_on_available_associates_ratio,
                                                      review_on_available_associates_time,
                                                      profile_selection_by_client_ratio,
                                                      profile_selection_by_client_time,
                                                      first_client_interview_ratio,
                                                      first_client_interview_time,
                                                      second_client_interview_ratio,
                                                      second_client_interview_time,
                                                      lead_time_to_deploy,
                                                      trigger_event,
                                                      checkbox_second_it_interview,
                                                      checkbox_review_available_associates,
                                                      checkbox_profile_selection_by_client,
                                                      checkbox_first_cl_interview,
                                                      checkbox_second_cl_interview,
                                                      category
                                                      ))

def internal_resume_selection(env,
                              pool_container,
                              container,
                              current_demand,
                              event_list,
                              ultimate_dict,
                              round,
                              client_interview_people_percentage,
                              internal_resume_selection_ratio,
                              internal_resume_selection_time,
                              first_internal_interview_ratio,
                              first_internal_interview_time,
                              second_internal_interview_ratio,
                              second_internal_interview_time,
                              review_on_available_associates_ratio,
                              review_on_available_associates_time,
                              profile_selection_by_client_ratio,
                              profile_selection_by_client_time,
                              first_client_interview_ratio,
                              first_client_interview_time,
                              second_client_interview_ratio,
                              second_client_interview_time,
                              lead_time_to_deploy,
                              trigger_event,
                              checkbox_second_it_interview,
                              checkbox_review_available_associates,
                              checkbox_profile_selection_by_client,
                              checkbox_first_cl_interview,
                              checkbox_second_cl_interview,
                              category
                              ):

    yield env.timeout(internal_resume_selection_time)
    at_first_size = container.level
    resume_selected_by_internal = abs(np.ceil(at_first_size * (internal_resume_selection_ratio / 100)))
    print(f"Day {np.floor(env.now)} from {category} category {resume_selected_by_internal} resumes are selected by internal team for interview")

    event_happend_1 = {'day': (np.floor(env.now)), 'statement': f'{resume_selected_by_internal} resumes are selected by internal team for internal interview'}
    event_list.append(event_happend_1)

    remaining_ppl = at_first_size - resume_selected_by_internal
    if remaining_ppl > 0:
        yield container.get(remaining_ppl)

    env.process(first_internal_interview(env,
                                         pool_container,
                                         container,
                                         current_demand,
                                         event_list,
                                         ultimate_dict,
                                         round,
                                         client_interview_people_percentage,
                                         first_internal_interview_ratio,
                                         first_internal_interview_time,
                                         second_internal_interview_ratio,
                                         second_internal_interview_time,
                                         review_on_available_associates_ratio,
                                         review_on_available_associates_time,
                                         profile_selection_by_client_ratio,
                                         profile_selection_by_client_time,
                                         first_client_interview_ratio,
                                         first_client_interview_time,
                                         second_client_interview_ratio,
                                         second_client_interview_time,
                                         lead_time_to_deploy,
                                         trigger_event,
                                         checkbox_second_it_interview,
                                         checkbox_review_available_associates,
                                         checkbox_profile_selection_by_client,
                                         checkbox_first_cl_interview,
                                         checkbox_second_cl_interview,
                                         category
                                         ))

def related_skill_profile_selection(env,
                                    pool_container,
                                    container,
                                    current_demand,
                                    event_list,
                                    ultimate_dict,
                                    round,
                                    client_interview_people_percentage,
                                    skill_profiles_ratio_bsw,
                                    skill_profiles_time,
                                    internal_resume_selection_ratio,
                                    internal_resume_selection_time,
                                    first_internal_interview_ratio,
                                    first_internal_interview_time,
                                    second_internal_interview_ratio,
                                    second_internal_interview_time,
                                    review_on_available_associates_ratio,
                                    review_on_available_associates_time,
                                    profile_selection_by_client_ratio,
                                    profile_selection_by_client_time,
                                    first_client_interview_ratio,
                                    first_client_interview_time,
                                    second_client_interview_ratio,
                                    second_client_interview_time,
                                    lead_time_to_deploy,
                                    trigger_event,
                                    checkbox_second_it_interview,
                                    checkbox_review_available_associates,
                                    checkbox_profile_selection_by_client,
                                    checkbox_first_cl_interview,
                                    checkbox_second_cl_interview,
                                    checkbox_related_skill,
                                    category
                                    ):
    if category == "Pool":
        print(f"Day {np.floor(env.now)} from {category} category {container.level} are available")
        event_happend_1 = {'day': (np.floor(env.now)), 'statement':f' {container.level} associates are available'}
        event_list.append(event_happend_1)


    yield env.timeout(skill_profiles_time)
    at_first_size = container.level
    related_skill_profiles = abs(np.ceil(at_first_size * (skill_profiles_ratio_bsw / 100)))

    remaining_ppl = at_first_size - related_skill_profiles
    if remaining_ppl > 0:
        yield container.get(remaining_ppl)

    if checkbox_related_skill==1:
        print(f"Day {np.floor(env.now)} from {category} category {related_skill_profiles} skilled associates are shortlisted")
        event_happend_1 = {'day': (np.floor(env.now)), 'statement': f'{related_skill_profiles} related skilled associates are shortlisted'}
        event_list.append(event_happend_1)




    env.process(internal_resume_selection(env,
                                          pool_container,
                                          container,
                                          current_demand,
                                          event_list,
                                          ultimate_dict,
                                          round,
                                          client_interview_people_percentage,
                                          internal_resume_selection_ratio,
                                          internal_resume_selection_time,
                                          first_internal_interview_ratio,
                                          first_internal_interview_time,
                                          second_internal_interview_ratio,
                                          second_internal_interview_time,
                                          review_on_available_associates_ratio,
                                          review_on_available_associates_time,
                                          profile_selection_by_client_ratio,
                                          profile_selection_by_client_time,
                                          first_client_interview_ratio,
                                          first_client_interview_time,
                                          second_client_interview_ratio,
                                          second_client_interview_time,
                                          lead_time_to_deploy,
                                          trigger_event,
                                          checkbox_second_it_interview,
                                          checkbox_review_available_associates,
                                          checkbox_profile_selection_by_client,
                                          checkbox_first_cl_interview,
                                          checkbox_second_cl_interview,
                                          category
                                          ))



def proactive_onboarding(env,
                         pool_container,
                         pro_active_container,
                         current_demand,
                         proactive_list,
                         ultimate_dict,
                         round,
                         client_interview_people_percentage,
                         skill_profiles_ratio_bsw,
                         skill_profiles_time,
                         lead_time_to_onboard_proactive,
                         internal_resume_selection_ratio,
                         internal_resume_selection_time,
                         first_internal_interview_ratio,
                         first_internal_interview_time,
                         second_internal_interview_ratio,
                         second_internal_interview_time,
                         review_on_available_associates_ratio,
                         review_on_available_associates_time,
                         profile_selection_by_client_ratio,
                         profile_selection_by_client_time,
                         first_client_interview_ratio,
                         first_client_interview_time,
                         second_client_interview_ratio,
                         second_client_interview_time,
                         lead_time_to_deploy,
                         trigger_event_proactive,
                         checkbox_second_it_interview,
                         checkbox_review_available_associates,
                         checkbox_profile_selection_by_client,
                         checkbox_first_cl_interview,
                         checkbox_second_cl_interview,
                         checkbox_related_skill,
                         category):
    """
    :param env:
    :param pro_active_container: Put the proactive people container
    :return:
    """



    yield env.timeout(lead_time_to_onboard_proactive)
    print(f"Day {np.floor(env.now)} from {category} category {pro_active_container.level} are onboarded")

    proactive_onboarding_dictionary = {'day': (np.floor(env.now)),
                                       'statement': f'No of associates onboarded are {pro_active_container.level}'}
    proactive_list.append(proactive_onboarding_dictionary)

    env.process(related_skill_profile_selection(env,
                                                pool_container,
                                                pro_active_container,
                                                current_demand,
                                                proactive_list,
                                                ultimate_dict,
                                                round,
                                                client_interview_people_percentage,
                                                skill_profiles_ratio_bsw,
                                                skill_profiles_time,
                                                internal_resume_selection_ratio,
                                                internal_resume_selection_time,
                                                first_internal_interview_ratio,
                                                first_internal_interview_time,
                                                second_internal_interview_ratio,
                                                second_internal_interview_time,
                                                review_on_available_associates_ratio,
                                                review_on_available_associates_time,
                                                profile_selection_by_client_ratio,
                                                profile_selection_by_client_time,
                                                first_client_interview_ratio,
                                                first_client_interview_time,
                                                second_client_interview_ratio,
                                                second_client_interview_time,
                                                lead_time_to_deploy,
                                                trigger_event_proactive,
                                                checkbox_second_it_interview,
                                                checkbox_review_available_associates,
                                                checkbox_profile_selection_by_client,
                                                checkbox_first_cl_interview,
                                                checkbox_second_cl_interview,
                                                checkbox_related_skill,
                                                category))


def rotation_associates(env,
                        pool_container,
                        rotation_container,
                        current_demand,
                        rotation_list,
                        ultimate_dict,
                        round,
                        client_interview_people_percentage,
                        skill_profiles_ratio_bsw,
                        skill_profiles_time,
                        lead_time_for_rotation,
                        internal_resume_selection_ratio,
                        internal_resume_selection_time,
                        first_internal_interview_ratio,
                        first_internal_interview_time,
                        second_internal_interview_ratio,
                        second_internal_interview_time,
                        review_on_available_associates_ratio,
                        review_on_available_associates_time,
                        profile_selection_by_client_ratio,
                        profile_selection_by_client_time,
                        first_client_interview_ratio,
                        first_client_interview_time,
                        second_client_interview_ratio,
                        second_client_interview_time,
                        lead_time_to_deploy,
                        trigger_event_rotation,
                        checkbox_second_it_interview,
                        checkbox_review_available_associates,
                        checkbox_profile_selection_by_client,
                        checkbox_first_cl_interview,
                        checkbox_second_cl_interview,
                        checkbox_related_skill,
                        category):
    """
    :param env:
    :param rotation_container: Put the rotation people container
    :return:
    """

    yield env.timeout(lead_time_for_rotation)
    print(f"Day {np.floor(env.now)} from {category} category {rotation_container.level} are available")

    event_happend_1 = {'day': (np.floor(env.now)), 'statement': f'{rotation_container.level} associates are available'}
    rotation_list.append(event_happend_1)


    env.process(related_skill_profile_selection(env,
                                                pool_container,
                                                rotation_container,
                                                current_demand,
                                                rotation_list,
                                                ultimate_dict,
                                                round,
                                                client_interview_people_percentage,
                                                skill_profiles_ratio_bsw,
                                                skill_profiles_time,
                                                internal_resume_selection_ratio,
                                                internal_resume_selection_time,
                                                first_internal_interview_ratio,
                                                first_internal_interview_time,
                                                second_internal_interview_ratio,
                                                second_internal_interview_time,
                                                review_on_available_associates_ratio,
                                                review_on_available_associates_time,
                                                profile_selection_by_client_ratio,
                                                profile_selection_by_client_time,
                                                first_client_interview_ratio,
                                                first_client_interview_time,
                                                second_client_interview_ratio,
                                                second_client_interview_time,
                                                lead_time_to_deploy,
                                                trigger_event_rotation,
                                                checkbox_second_it_interview,
                                                checkbox_review_available_associates,
                                                checkbox_profile_selection_by_client,
                                                checkbox_first_cl_interview,
                                                checkbox_second_cl_interview,
                                                checkbox_related_skill,
                                                category))


def deallocation_associates(env,
                            pool_container,
                            deallocation_container,
                            current_demand,
                            deallocated_list,
                            ultimate_dict,
                            round,
                            client_interview_people_percentage,
                            skill_profiles_ratio_bsw,
                            skill_profiles_time,
                            lead_time_for_deallocation,
                            internal_resume_selection_ratio,
                            internal_resume_selection_time,
                            first_internal_interview_ratio,
                            first_internal_interview_time,
                            second_internal_interview_ratio,
                            second_internal_interview_time,
                            review_on_available_associates_ratio,
                            review_on_available_associates_time,
                            profile_selection_by_client_ratio,
                            profile_selection_by_client_time,
                            first_client_interview_ratio,
                            first_client_interview_time,
                            second_client_interview_ratio,
                            second_client_interview_time,
                            lead_time_to_deploy,
                            trigger_event_deallocated,
                            checkbox_second_it_interview,
                            checkbox_review_available_associates,
                            checkbox_profile_selection_by_client,
                            checkbox_first_cl_interview,
                            checkbox_second_cl_interview,
                            checkbox_related_skill,
                            category):
    """
    :param env:
    :param deallocation_container: Put the deallocation people container
    :return:
    """

    yield env.timeout(lead_time_for_deallocation)
    print(f"Day {np.floor(env.now)} from {category} category {deallocation_container.level} associates are available")

    event_happend_1 = {'day': (np.floor(env.now)), 'statement': f'{deallocation_container.level} associates are available'}
    deallocated_list.append(event_happend_1)


    env.process(related_skill_profile_selection(env,
                                                pool_container,
                                                deallocation_container,
                                                current_demand,
                                                deallocated_list,
                                                ultimate_dict,
                                                round,
                                                client_interview_people_percentage,
                                                skill_profiles_ratio_bsw,
                                                skill_profiles_time,
                                                internal_resume_selection_ratio,
                                                internal_resume_selection_time,
                                                first_internal_interview_ratio,
                                                first_internal_interview_time,
                                                second_internal_interview_ratio,
                                                second_internal_interview_time,
                                                review_on_available_associates_ratio,
                                                review_on_available_associates_time,
                                                profile_selection_by_client_ratio,
                                                profile_selection_by_client_time,
                                                first_client_interview_ratio,
                                                first_client_interview_time,
                                                second_client_interview_ratio,
                                                second_client_interview_time,
                                                lead_time_to_deploy,
                                                trigger_event_deallocated,
                                                checkbox_second_it_interview,
                                                checkbox_review_available_associates,
                                                checkbox_profile_selection_by_client,
                                                checkbox_first_cl_interview,
                                                checkbox_second_cl_interview,
                                                checkbox_related_skill,
                                                category))








def simulation(env,current_demand,client_interview_people_percentage,offer_made_for_proactive,joining_rate_proactive,pool_emp,deallocatted_new,rotation_emp,
               lead_time_for_rotation,lead_time_for_deallocation,skill_profiles_ratio_proactive,skill_profiles_ratio_deallocation,
               skill_profiles_ratio_pool,skill_profiles_ratio_rotation,skill_profiles_time,
               lead_time_to_onboard_proactive,internal_resume_selection_ratio,internal_resume_selection_time,
               first_internal_interview_ratio,first_internal_interview_time,
               second_internal_interview_ratio,second_internal_interview_time,review_on_available_associates_ratio_proactive,
               review_on_available_associates_ratio_pool,review_on_available_associates_ratio_deallocation,
               review_on_available_associates_ratio_rotation,
               review_on_available_associates_time,profile_selection_by_client_ratio,profile_selection_by_client_time,
               first_client_interview_ratio,first_client_interview_time,second_client_interview_ratio,
               second_client_interview_time,lead_time_to_deploy,checkbox_second_it_interview,checkbox_review_available_associates,
               checkbox_profile_selection_by_client,checkbox_first_cl_interview,checkbox_second_cl_interview,checkbox_related_skill):

    joining_pro_active_people = abs(int(np.ceil(offer_made_for_proactive * (joining_rate_proactive / 100))))
    pro_active_container = simpy.Container(env, capacity=float('inf'), init=joining_pro_active_people)
    print(pool_emp, 'pool_emp')
    initial_pool_container = simpy.Container(env, capacity=float('inf'), init=pool_emp)
    print(initial_pool_container.level,'initial_pool_container.level_1')
    rotation_container = simpy.Container(env, capacity=float('inf'), init=rotation_emp)
    pool_container = simpy.Container(env, capacity=float('inf'), init=0)
    deallocation_container = simpy.Container(env, capacity=float('inf'), init=deallocatted_new)




    trigger_event_proactive = env.event()
    trigger_event_rotation = env.event()
    trigger_event_pool = env.event()
    trigger_event_deallocated = env.event()


    ultimate_dict = {}
    round = 0

    proactive_list = []
    rotation_list = []
    pool_list = []
    deallocated_list = []
    my_dict.clear()





    if pro_active_container.level>0:
        env.process(proactive_onboarding(env,
                                         pool_container,
                                         pro_active_container,
                                         current_demand,
                                         proactive_list,
                                         ultimate_dict,
                                         round,
                                         client_interview_people_percentage,
                                         skill_profiles_ratio_proactive,
                                         skill_profiles_time,
                                         lead_time_to_onboard_proactive,
                                         internal_resume_selection_ratio,
                                         internal_resume_selection_time,
                                         first_internal_interview_ratio,
                                         first_internal_interview_time,
                                         second_internal_interview_ratio,
                                         second_internal_interview_time,
                                         review_on_available_associates_ratio_proactive,
                                         review_on_available_associates_time,
                                         profile_selection_by_client_ratio,
                                         profile_selection_by_client_time,
                                         first_client_interview_ratio,
                                         first_client_interview_time,
                                         second_client_interview_ratio,
                                         second_client_interview_time,
                                         lead_time_to_deploy,
                                         trigger_event_proactive,
                                         checkbox_second_it_interview,
                                         checkbox_review_available_associates,
                                         checkbox_profile_selection_by_client,
                                         checkbox_first_cl_interview,
                                         checkbox_second_cl_interview,
                                         checkbox_related_skill,
                                         category="Proactive"))



    if rotation_container.level>0:
        env.process(rotation_associates(env,
                                        pool_container,
                                        rotation_container,
                                        current_demand,
                                        rotation_list,
                                        ultimate_dict,
                                        round,
                                        client_interview_people_percentage,
                                        skill_profiles_ratio_rotation,
                                        skill_profiles_time,
                                        lead_time_for_rotation,
                                        internal_resume_selection_ratio,
                                        internal_resume_selection_time,
                                        first_internal_interview_ratio,
                                        first_internal_interview_time,
                                        second_internal_interview_ratio,
                                        second_internal_interview_time,
                                        review_on_available_associates_ratio_rotation,
                                        review_on_available_associates_time,
                                        profile_selection_by_client_ratio,
                                        profile_selection_by_client_time,
                                        first_client_interview_ratio,
                                        first_client_interview_time,
                                        second_client_interview_ratio,
                                        second_client_interview_time,
                                        lead_time_to_deploy,
                                        trigger_event_rotation,
                                        checkbox_second_it_interview,
                                        checkbox_review_available_associates,
                                        checkbox_profile_selection_by_client,
                                        checkbox_first_cl_interview,
                                        checkbox_second_cl_interview,
                                        checkbox_related_skill,
                                        category="rotation"))


    if deallocation_container.level>0:
        env.process(deallocation_associates(env,
                                            pool_container,
                                            deallocation_container,
                                            current_demand,
                                            deallocated_list,
                                            ultimate_dict,
                                            round,
                                            client_interview_people_percentage,
                                            skill_profiles_ratio_deallocation,
                                            skill_profiles_time,
                                            lead_time_for_deallocation,
                                            internal_resume_selection_ratio,
                                            internal_resume_selection_time,
                                            first_internal_interview_ratio,
                                            first_internal_interview_time,
                                            second_internal_interview_ratio,
                                            second_internal_interview_time,
                                            review_on_available_associates_ratio_deallocation,
                                            review_on_available_associates_time,
                                            profile_selection_by_client_ratio,
                                            profile_selection_by_client_time,
                                            first_client_interview_ratio,
                                            first_client_interview_time,
                                            second_client_interview_ratio,
                                            second_client_interview_time,
                                            lead_time_to_deploy,
                                            trigger_event_deallocated,
                                            checkbox_second_it_interview,
                                            checkbox_review_available_associates,
                                            checkbox_profile_selection_by_client,
                                            checkbox_first_cl_interview,
                                            checkbox_second_cl_interview,
                                            checkbox_related_skill,
                                            category="deallocation"))


    if initial_pool_container.level>0:
        env.process(related_skill_profile_selection(env,
                                                    pool_container,
                                                    initial_pool_container,
                                                    current_demand,
                                                    pool_list,
                                                    ultimate_dict,
                                                    round,
                                                    client_interview_people_percentage,
                                                    skill_profiles_ratio_pool,
                                                    skill_profiles_time,
                                                    internal_resume_selection_ratio,
                                                    internal_resume_selection_time,
                                                    first_internal_interview_ratio,
                                                    first_internal_interview_time,
                                                    second_internal_interview_ratio,
                                                    second_internal_interview_time,
                                                    review_on_available_associates_ratio_pool,
                                                    review_on_available_associates_time,
                                                    profile_selection_by_client_ratio,
                                                    profile_selection_by_client_time,
                                                    first_client_interview_ratio,
                                                    first_client_interview_time,
                                                    second_client_interview_ratio,
                                                    second_client_interview_time,
                                                    lead_time_to_deploy,
                                                    trigger_event_pool,
                                                    checkbox_second_it_interview,
                                                    checkbox_review_available_associates,
                                                    checkbox_profile_selection_by_client,
                                                    checkbox_first_cl_interview,
                                                    checkbox_second_cl_interview,
                                                    checkbox_related_skill,
                                                    category = "Pool"
                                                    ))

        yield env.timeout(0.1)





def intake(current_demand,client_interview_people_percentage,offer_made_for_proactive,joining_rate_proactive,pool_emp,deallocatted_new,rotation_emp,
           lead_time_for_rotation,lead_time_for_deallocation,skill_profiles_ratio_proactive,skill_profiles_ratio_deallocation,
           skill_profiles_ratio_pool,skill_profiles_ratio_rotation,skill_profiles_time,
           lead_time_to_onboard_proactive,internal_resume_selection_ratio,internal_resume_selection_time,
           first_internal_interview_ratio,first_internal_interview_time,
           second_internal_interview_ratio,second_internal_interview_time,review_on_available_associates_ratio_proactive,
           review_on_available_associates_ratio_pool,review_on_available_associates_ratio_deallocation,
           review_on_available_associates_ratio_rotation,
           review_on_available_associates_time,profile_selection_by_client_ratio,profile_selection_by_client_time,
           first_client_interview_ratio,first_client_interview_time,second_client_interview_ratio,
           second_client_interview_time,lead_time_to_deploy,checkbox_second_it_interview,checkbox_review_available_associates,
           checkbox_profile_selection_by_client,checkbox_first_cl_interview,checkbox_second_cl_interview,checkbox_related_skill):
    env = simpy.Environment()

    if current_demand:
        env.process(simulation(env,current_demand,client_interview_people_percentage,offer_made_for_proactive,joining_rate_proactive,pool_emp,deallocatted_new,rotation_emp,
               lead_time_for_rotation,lead_time_for_deallocation,skill_profiles_ratio_proactive,skill_profiles_ratio_deallocation,
               skill_profiles_ratio_pool,skill_profiles_ratio_rotation,skill_profiles_time,
               lead_time_to_onboard_proactive,internal_resume_selection_ratio,internal_resume_selection_time,
               first_internal_interview_ratio,first_internal_interview_time,
               second_internal_interview_ratio,second_internal_interview_time,review_on_available_associates_ratio_proactive,
               review_on_available_associates_ratio_pool,review_on_available_associates_ratio_deallocation,
               review_on_available_associates_ratio_rotation,
               review_on_available_associates_time,profile_selection_by_client_ratio,profile_selection_by_client_time,
               first_client_interview_ratio,first_client_interview_time,second_client_interview_ratio,
               second_client_interview_time,lead_time_to_deploy,checkbox_second_it_interview,checkbox_review_available_associates,
               checkbox_profile_selection_by_client,checkbox_first_cl_interview,checkbox_second_cl_interview,checkbox_related_skill))

        env.run(until=2000)

        if client_interview_people_percentage>0:
            data = my_dict['result']
        elif client_interview_people_percentage==0:
            data = my_dict['result_1']


        result = {}
        for entry in data:
            week = np.ceil(entry['day'] / 7)
            statement = entry['statement']

            if 'from Pool' in statement:
                if 'direct' in statement:
                    result.setdefault('pool_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through direct allocation."})
                elif 'client' in statement:
                    result.setdefault('pool_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through client interview."})
            elif 'from rotation' in statement:
                if 'direct' in statement:
                    result.setdefault('rotation_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through direct allocation."})
                elif 'client' in statement:
                    result.setdefault('rotation_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through client interview."})
            elif 'from deallocation' in statement:
                if 'direct' in statement:
                    result.setdefault('deallocation_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through direct allocation."})
                elif 'client' in statement:
                    result.setdefault('deallocation_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through client interview."})
            elif 'from Proactive' in statement:
                if 'direct' in statement:
                    result.setdefault('proactive_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through direct allocation."})
                elif 'client' in statement:
                    result.setdefault('proactive_week', []).append(
                        {f'Week {week}': f"{statement.split(', ')[1].split()[0]} Associates will be allocated through client interview."})


        allocations = [float(val.split()[0]) for category in result.values() for week_data in category for val in
                       week_data.values()]
        total_allocated = sum(allocations)
        print('total_allocated:', total_allocated)

        people_remaining = ((offer_made_for_proactive * (joining_rate_proactive/100))+ pool_emp + deallocatted_new + rotation_emp) - total_allocated
        final_statement = data[-1]['statement']
        demand_remaining = float(final_statement.split()[8])
        final_day = int(data[-1]['day'])

        # associates will be allocated into project
        result.setdefault('final', [
            {f'On day-{int(final_day)} (week-{int(np.ceil(final_day/7))}) -->': f'{str(total_allocated)} Associates will be allocated to the project.'}])
        # if (int(str(demand_remaining))>0):
        #     result['final'].append(
        #         {f'On day {final_day}, week {int(np.ceil(final_day/7))}': f'demand remaining {str(demand_remaining)}'})
        # elif (int(str(demand_remaining))<=0):
        #     result['final'].append(
        #         {f'On day {final_day}, week {int(np.ceil(final_day/7))}': f'total demand fulfilled '})
        result['final'].append(
                {f'On day-{int(final_day)} (week-{int(np.ceil(final_day/7))}) -->': f'{str(demand_remaining)} is the remaining demand that needs to be fulfilled.'})
        result['final'].append(
            {f'On day-{int(final_day)} (week-{int(np.ceil(final_day/7))}) -->': f'{str(people_remaining)} Associates will be remaining after allocation.'})

        print(result,'result')

        my_result_list = []

        for category, values in result.items():
            my_dict[category]=[values]


        print('my_dict------------', my_dict)
        demand_list.clear()





        return my_dict







# current_demand = 80
# deallocatted_new = 30
# pool_emp = 20
# rotation_emp = 20
# offer_made_for_proactive = 100
# joining_rate_proactive = 30
#
# lead_time_to_onboard_proactive = 30
# lead_time_for_rotation=5
# lead_time_for_deallocation=5
#
# skill_profiles_ratio_proactive=50
# skill_profiles_ratio_pool=50
# skill_profiles_ratio_rotation=50
# skill_profiles_ratio_deallocation=50
# skill_profiles_time=5
#
# internal_resume_selection_ratio=50
# internal_resume_selection_time=5
#
# first_internal_interview_ratio=50
# first_internal_interview_time=4
#
# second_internal_interview_ratio=100
# second_internal_interview_time=4
#
# review_on_available_associates_ratio_proactive=100
# review_on_available_associates_ratio_rotation=100
# review_on_available_associates_ratio_pool=100
# review_on_available_associates_ratio_deallocation=100
# review_on_available_associates_time=6
#
# profile_selection_by_client_ratio=50
# profile_selection_by_client_time=3
#
# first_client_interview_ratio=50
# first_client_interview_time=4
#
# second_client_interview_ratio=50
# second_client_interview_time=4
#
# lead_time_to_deploy=5
#
# client_interview_people_percentage = 50
#
# checkbox_second_it_interview = 1
# checkbox_review_available_associates = 0
# checkbox_profile_selection_by_client = 0
# checkbox_first_cl_interview = 0
# checkbox_second_cl_interview = 1
# checkbox_related_skill = 1
#
#
# intake(current_demand,client_interview_people_percentage,offer_made_for_proactive,joining_rate_proactive,pool_emp,deallocatted_new,rotation_emp,
#        lead_time_for_rotation,lead_time_for_deallocation,skill_profiles_ratio_proactive,skill_profiles_ratio_deallocation,
#        skill_profiles_ratio_pool,skill_profiles_ratio_rotation,skill_profiles_time,
#        lead_time_to_onboard_proactive,internal_resume_selection_ratio,internal_resume_selection_time,
#        first_internal_interview_ratio,first_internal_interview_time,
#        second_internal_interview_ratio,second_internal_interview_time,review_on_available_associates_ratio_proactive,
#        review_on_available_associates_ratio_pool,review_on_available_associates_ratio_deallocation,
#        review_on_available_associates_ratio_rotation,
#        review_on_available_associates_time,profile_selection_by_client_ratio,profile_selection_by_client_time,
#        first_client_interview_ratio,first_client_interview_time,second_client_interview_ratio,
#        second_client_interview_time,lead_time_to_deploy,checkbox_second_it_interview,checkbox_review_available_associates,
#        checkbox_profile_selection_by_client,checkbox_first_cl_interview,checkbox_second_cl_interview,checkbox_related_skill)








