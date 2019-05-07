USE akpsi;

CREATE VIEW python_membership_core AS
SELECT
	m.memCode AS `Membership Code`,
	CONCAT(m.fName,' ',m.lName) AS 'Name',
    m.akpsi_status AS `Status`,
    m.major AS `Major`,
    co.college AS `College`,
    m.pledgeClass AS `Pledge Classification`,
    m.pledgeSem AS `Pledge Semester`,
    m.gradSem AS `Graduate Semester`,
    m.susSem AS `Suspension Semester`,
    m.reinstateSem AS `Reinstatement Semester`,
    YEAR(m.birthday) AS `Birth Year`,
	MONTH(m.birthday) AS `Birth Month`,
	DAY(m.birthday) AS `Birth Day`,
    m.gender AS `Gender`,
    m.homeCity AS `Home City`,
    m.homeState AS `Home State`,
    m.homeCountry AS `Home Country`,
    m.gradProgram AS `Graduate School Program`,
    m.gradUni AS `Graduate University`,
    m.workCompany AS `Company`,
    m.workCity AS `Work City`,
    m.workState AS `Work State`,
    m.workCountry AS `Work Country`,
#Any fields that start with Is are a boolean field, with only 1s and 0s.
	chapter_time(m.memCode) AS `Chapter Time`,
	is_officer(m.memCode) AS `Is Officer`,
	officer_time(m.memCode) AS `Officer Time`,
	us_resident(m.memCode) AS `Is US Resident`,
	grad_student(m.memCode) AS `Is Grad Student`,
	age(m.memCode) AS `Age`,
	over_21(m.memCode) AS `Is Over 21`,
	business_major(m.memCode) AS `Is Business Major`
FROM membership m
	LEFT JOIN college co
		ON m.major = co.major
WHERE m.chapter = 'Beta Chi'
ORDER BY `Chapter`, `Status`, m.lName, m.fName;

CREATE VIEW python_membership_officers AS
SELECT
	m.memCode AS `Membership Code`,
    o.semester AS `Officer Semester Code`,
    o.position AS `Officer Position`
FROM officer o
	LEFT OUTER JOIN semester s
		ON o.semester = s.semCode
	LEFT OUTER JOIN membership m
		ON m.memCode = o.memCode
ORDER BY FIELD(`Officer Position`,'President','Executive Vice President','Vice President of Membership','Vice President of Finance','Vice President of Professional Development','Vice President of Alumni Relations','Vice President of Public Relations','Sponsorship Chair','Gala Chair','Secretary','Master of Rituals','Pledge Educator','Treasurer','Webmaster','Fundraising Chair','Social Chair','Service Chair','Endowment Chair','Warden');

CREATE VIEW python_semester AS
SELECT
	s.semTerm AS `Term`,
    s.semYear AS `Year`,
	s.beginningActives AS `Beginning Actives`,
	semester_suspended(s.semCode) AS `Semester Suspended`,
	semester_reinstatements(s.semCode) AS `Semester Resinstated`,
	semester_graduates(s.semCode) AS `Semester Graduated`,
    s.applications AS `Applications`,
    s.prospectInterviews AS `Prospects Interviewed`,
    s.bidsExtended AS `Bids Extended`,
    s.pledgesPinned AS `Pledges Pinned`,
    s.brothersInitiated AS `Brothers Initiated`,
    retained_members(s.semCode) AS `Retained Brothers`,
    ROUND(s.prospectInterviews / s.applications,3) AS `Interview Rate`,
    ROUND(s.bidsExtended / s.prospectInterviews,3) AS `Bid Rate`,
    ROUND(s.pledgesPinned / s.bidsExtended,3) AS `Bid Acceptance Rate`,
	ROUND(s.pledgesPinned / s.prospectInterviews,3) AS `Pledge Acceptance Rate`,
    ROUND(s.brothersInitiated / s.pledgesPinned,3) AS `Pledge Retention Rate`,
    ROUND(retained_members(s.semCode) / s.brothersInitiated,3) AS `Active Retention Rate`,
	s.fundraising AS `Fundraising Amount`,
	s.sponsorships AS `Sponsorship Amount`
FROM semester s
ORDER BY `Year`, `Term` DESC;

USE akpsi;