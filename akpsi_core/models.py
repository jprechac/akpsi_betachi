from django.db import models

# Create your models here.
"""
These classes are pulled from the MySQL Tables
"""
class Area(models.Model):

    area_number = models.IntegerField(primary_key=True, db_column='areaNo')
    area_vp = models.ForeignKey('Member', blank=True, null=True, on_delete=models.SET_NULL, db_column='areaVP')

    def __str__(self):
        return str(self.area_number)

    class Meta:
        # managed = False
        # db_table = 'area'
        ordering = ['area_number']
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

class Region(models.Model):

    region_name = models.CharField(max_length=50, primary_key=True, db_column='regionName')
    area_number = models.ForeignKey(Area, blank=True, null=True, on_delete=models.SET_NULL, db_column='areaNo')
    regional_director = models.ForeignKey('Member', on_delete=models.SET_NULL, blank=True, null=True, db_column='rd')

    def __str__(self):
        return self.region_name

    class Meta:
        # managed = False
        # db_table = 'region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

class Semester(models.Model):

    semester_code = models.CharField(max_length=5, primary_key=True, db_column='semCode')
    semester_term = models.CharField(max_length=6, null=False, blank=False, db_column='semTerm')
    semester_year = models.IntegerField(blank=False, null=False, db_column='semYear')
    semester_induction = models.DateField(blank=True, null=True, db_column='semInduction')
    semester_initiation = models.DateField(blank=True, null=True, db_column='semInitiation')
    beginning_actives = models.IntegerField(blank=True, null=True, db_column='beginningActives')
    applications = models.IntegerField(blank=True, null=True, db_column='applications')
    prospect_interviews = models.IntegerField(blank=True, null=True, db_column='prospectInterviews')
    bids_extended = models.IntegerField(blank=True, null=True, db_column='bidsExtended')
    pledges_pinned = models.IntegerField(blank=True, null=True, db_column='pledgesPinned')
    brothers_initiated = models.IntegerField(blank=True, null=True, db_column='brothersInitiated')
    sponsorships = models.IntegerField(blank=True, null=True, db_column='sponsorships')
    fundraising = models.IntegerField(blank=True, null=True, db_column='fundraising')

    def __str__(self):
        term = self.semester_term.lower().capitalize()
        string = "{0} {1}".format(term, self.semester_year)
        return string

    class Meta:
        # managed = False
        # db_table = 'semester'
        ordering = ['semester_year', '-semester_term']
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

class University(models.Model):

    university_name = models.CharField(max_length=255, primary_key=True, db_column='uniName')
    university_city = models.CharField(max_length=100, blank=True, null=True, db_column='uniCity')
    university_state = models.CharField(max_length=100, blank=True, null=True, db_column='uniState')
    university_country = models.CharField(max_length=100, blank=True, null=True, db_column='uniCountry')

    def __str__(self):
        return self.university_name

    class Meta:
        # managed = False
        # db_table = 'university'
        ordering = ['university_name']
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

class Chapter(models.Model):

    chapter_name = models.CharField(max_length=20, primary_key=True, db_column='chapterName')
    chapter_university = models.ForeignKey(University, on_delete=models.CASCADE, blank=False, null=False, db_column='chapterUni')
    charter_date = models.DateField(blank=True, null=True, db_column='charterDate')
    recharter_date = models.DateField(blank=True, null=True, db_column='recharterDate')
    region_name = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True, db_column='region')

    def __str__(self):
        string = "{0} - {1}".format(self.chapter_name, self.chapter_university)
        return string

    class Meta:
        # managed = False
        # db_table = 'chapter'
        ordering = ['chapter_name']
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

class College(models.Model):

    major = models.CharField(max_length=50, primary_key=True, db_column='major')
    college = models.CharField(max_length=50, blank=False, null=False, db_column='college')

    def __str__(self):
        return self.major

    class Meta:
        # managed = False
        # db_table = 'college'
        ordering = ['college', 'major']
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'

class Member(models.Model):

    akpsi_statuses = (
        ('Collegiate', 'Collegiate'),
        ('Alumnus','Alumnus'),
        ('LOA-Military', 'Leave of Absense - Military Leave'),
        ('LOA-Medical', 'Leave of Absense - Medical Leave'),
        ('LOA-Hardship', 'Leave of Absense - Extreme Hardship'),
        ('LOA-Abroad', 'Leave of Absense - Study Abroad'),
        ('Pledge', 'Pledge'),
        ('Suspended', 'Suspended'),
        ('Faculty', 'Faculty Brother'),
        ('Honorary', 'Honorary Brother')
    )

    genders = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    )

    member_code = models.CharField(max_length=8, primary_key=True, db_column='memCode')
    first_name = models.CharField(max_length=255, blank=False, null=False, db_column='fName')
    middle_name = models.CharField(max_length=255, blank=True, null=True, db_column='mName')
    last_name = models.CharField(max_length=255, blank=False, null=False, db_column='lName')
    nickname = models.CharField(max_length=255, blank=True, null=True, db_column='nickname')
    akpsi_status = models.CharField(max_length=255, blank=False, null=False, db_column='akpsi_status', choices=akpsi_statuses)
    chapter_status = models.CharField(max_length=255, blank=True, null=True, db_column='chapter_status')
    chapter = models.ForeignKey(Chapter, blank=True, null=True, on_delete=models.SET_NULL, db_column='chapter')
    email1 = models.CharField(max_length=255, blank=True, null=True, db_column='email1')
    email2 = models.CharField(max_length=255, blank=True, null=True, db_column='email2')
    phone = models.CharField(max_length=15, blank=True, null=True, db_column='phone')
    major = models.ForeignKey(College, on_delete=models.SET_NULL, blank=True, null=True, db_column='major')
    pledge_classification = models.CharField(max_length=40, blank=True, null=True, db_column='pledgeClass')
    pledge_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, related_name='pledge_semester', blank=True, null=True, db_column='pledgeSem')
    graduate_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, related_name='grad_semester', blank=True, null=True, db_column='gradSem')
    suspension_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, related_name='suspension_semester', blank=True, null=True, db_column='susSem')
    reinstate_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, related_name='reinstatement_semester', blank=True, null=True, db_column='reinstateSem')
    birthday = models.DateField(blank=True, null=True, db_column='birthday')
    gender = models.CharField(max_length=1, blank=True, null=True, choices=genders, db_column='gender')
    dietary_restrictions = models.CharField(max_length=255, blank=True, null=True, db_column='dietRestrict')
    home_city = models.CharField(max_length=100, blank=True, null=True, db_column='homeCity')
    home_state = models.CharField(max_length=100, blank=True, null=True, db_column='homeState')
    home_country = models.CharField(max_length=100, blank=True, null=True, db_column='homeCountry')
    graduate_program = models.CharField(max_length=50, blank=True, null=True, db_column='gradProgram')
    graduate_university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True, db_column='gradUni')
    work_company = models.CharField(max_length=100, blank=True, null=True, db_column='workCompany')
    work_city = models.CharField(max_length=100, blank=True, null=True, db_column='workCity')
    work_state = models.CharField(max_length=100, blank=True, null=True, db_column='workState')
    work_country = models.CharField(max_length=100, blank=True, null=True, db_column='workCountry')
    notes = models.TextField(blank=True, null=True, db_column='notes')

    def __str__(self):
        return self.display_name()
    
    def display_name(self):
        if self.nickname != None:
            preferred = self.nickname
        else:
            preferred = self.first_name
        string = "{} {}".format(preferred, self.last_name)
        return string
    
    def full_name(self):
        string = "{} {}".format(self.first_name, self.last_name)
        return string

    class Meta:
        # managed = False
        # db_table = 'membership'
        ordering = ['chapter', 'akpsi_status', 'chapter_status', 'last_name', 'first_name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

class Officer(models.Model):

    position_choices = (
        ('president', 'President'),
        ('evp', 'Executive Vice President'),
        ('vpm','Vice President of Membership'),
        ('vpf', 'Vice President of Finance'),
        ('vppd', 'Vice President of Professional Development'),
        ('vpar', 'Vice President of Alumni Relations'),
        ('vppr', 'Vice President of Public Relations'),
        ('dor', 'Director of Recruitment'),
        ('docr', 'Director of Corporate Relations'),
        ('secretary', 'Secretary'),
        ('mor', 'Master of Rituals'),
        ('treasurer', 'Treasurer'),
        ('social', 'Social Chair'),
        ('service', 'Service Chair'),
        ('historian', 'Historian'),
        ('webmaster', 'Webmaster'),
        ('dpr', 'Director of Public Relations'), #not a year-long position
        ('warden', 'Warden')
    )

    id = models.AutoField(primary_key=True, blank=False, null=False)
    member_code = models.ForeignKey(Member, blank=False, null=False, on_delete=models.CASCADE)
    sem_code = models.ForeignKey(Semester, blank=False, null=False, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, blank=False, null=False, choices=position_choices)

    def __str__(self):
        return "{}, {} - {}".format(self.get_position_display(), self.member_code, self.sem_code)


# The next classes are from MySQL views
