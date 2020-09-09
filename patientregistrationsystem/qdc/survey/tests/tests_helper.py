from faker import Factory

from survey.models import Survey


def create_survey(sid=212121):
    """
    :param sid: Survey id at LimeSurvey
    :return: Survey model instance
    """
    faker = Factory.create()

    return Survey.objects.create(
        lime_survey_id=sid, en_title=faker.text(max_nb_chars=100),
        pt_title=faker.text(max_nb_chars=100))
