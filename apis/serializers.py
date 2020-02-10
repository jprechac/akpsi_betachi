from membership import models as core_models

from rest_framework import serializers

# ------------------------------------------------------------------------------

class SemesterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = core_models.Semester
        fields = [
            'semester_term',
            'semester_year',
            'semester_induction',
            'semester_initiation',
            'beginning_actives',
            'applications',
            'prospect_interviews',
            'bids_extended',
            'pledges_pinned',
            'brothers_initiated',
            'sponsorships',
            'fundraising'
        ]
