from .models import Member

"""
This is a series of pre-defined queries that are meant to simplify pulling data
later. 
"""

MemberBetaChiActives = Member.objects.filter(
    chapter = 'Beta Chi',
    akpsi_status = 'Active'
)
