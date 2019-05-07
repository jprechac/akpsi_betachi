DROP SCHEMA IF EXISTS akpsi;
CREATE SCHEMA akpsi;
USE akpsi;

DROP USER IF EXISTS 'akpsi_python';
CREATE USER 'akpsi_python'
	IDENTIFIED BY 'akpsi_python';

GRANT ALL PRIVILEGES ON akpsi.* TO 'akpsi_python'@'%';

CREATE TABLE area (
	areaNo	int(1) NOT NULL,
		primary key (areaNo) );

CREATE TABLE region (
	regionName	VARCHAR(50) NOT NULL,
	areaNo		INT(1) NOT NULL,
		primary key (regionName),
		constraint fk_regionArea foreign key (areaNo) REFERENCES area(areaNo) ON UPDATE CASCADE ) ;

CREATE TABLE semester (
	semCode			CHAR(5) NOT NULL,
	semTerm			VARCHAR(6) NOT NULL,
	semYear			INT(4) NOT NULL,
	semInduction		DATE,
	semInitiation		DATE,
	beginningActives	INT(3),
    applications		INT(3),
	prospectInterviews	INT(3),
    bidsExtended		INT(3),
    pledgesPinned		INT(3),
    brothersInitiated	INT(3),
		PRIMARY KEY (semCode) ) ;

CREATE TABLE university (
	uniName		VARCHAR(255) NOT NULL,
	uniCity		VARCHAR(100),
	uniState	VARCHAR(100),
	uniCountry	VARCHAR(100) DEFAULT "United States",
		PRIMARY KEY (uniName) ) ;

CREATE TABLE chapter (
	chapterName	VARCHAR(20),
	chapterUni	VARCHAR(255) NOT NULL,
	charterDate	DATE,
	recharterDate	DATE DEFAULT NULL,
    region	VARCHAR(50),
		primary key (chapterName),
		CONSTRAINT fk_chapterUni FOREIGN KEY (chapterUni) REFERENCES university(uniName) ON UPDATE CASCADE,
        CONSTRAINT fk_chapterRegion FOREIGN KEY (region) REFERENCES region(regionName) ON UPDATE CASCADE ) ;

CREATE TABLE college (
	major		VARCHAR(50),
	college		VARCHAR(50),
		primary key (major) ) ;

CREATE TABLE membership (
	memCode		CHAR(8) UNIQUE NOT NULL,
	fName		VARCHAR(255) NOT NULL,
	lName		VARCHAR(255) NOT NULL,
	akpsi_status		VARCHAR(255) NOT NULL,
	chapter		VARCHAR(255) DEFAULT 'Beta Chi',
	email1		VARCHAR(255) UNIQUE,
	email2		VARCHAR(255) UNIQUE,
	phone		VARCHAR(15),
	major		VARCHAR(50),
    pledgeClass	VARCHAR(40),
    pledgeSem	CHAR(5),
	gradSem		CHAR(5),
	susSem		CHAR(5) DEFAULT NULL,
	birthday	DATE,
	gender		CHAR(1),
	dietRestrict	VARCHAR(255),
	homeCity	VARCHAR(100),
	homeState	VARCHAR(100),
	homeCountry	VARCHAR(100),
	gradProgram	VARCHAR(50) DEFAULT NULL,
	gradUni		VARCHAR(255) DEFAULT NULL,
	workCompany	VARCHAR(100) DEFAULT NULL,
	workCity	VARCHAR(100) DEFAULT NULL,
	workState	VARCHAR(100) DEFAULT NULL,
	workCountry	VARCHAR(100) DEFAULT NULL,
	notes		TEXT,
		PRIMARY KEY (memCode),
		CONSTRAINT fk_memChapter FOREIGN KEY (chapter) REFERENCES chapter(chapterName) ON UPDATE CASCADE,
		CONSTRAINT fk_memMajor FOREIGN KEY (major) REFERENCES college(major) ON UPDATE CASCADE,
        CONSTRAINT fk_memPledgeSem FOREIGN KEY (pledgeSem) REFERENCES semester(semCode) ON UPDATE CASCADE ON DELETE SET NULL,
		CONSTRAINT fk_memGradSem FOREIGN KEY (gradSem) REFERENCES semester(semCode) ON UPDATE CASCADE ON DELETE SET NULL,
		CONSTRAINT fk_memSusSem FOREIGN KEY (susSem) REFERENCES semester(semCode) ON UPDATE CASCADE ON DELETE SET NULL,
		CONSTRAINT fk_memGradUni FOREIGN KEY (gradUni) REFERENCES university(uniName) ON UPDATE CASCADE ) ;

CREATE TABLE officer (
	memCode		CHAR(8),
    semester	CHAR(5),
    position	VARCHAR(100),
		PRIMARY KEY (memCode, semester),
        CONSTRAINT fk_officerMem FOREIGN KEY (memCode) REFERENCES membership(memCode),
		CONSTRAINT fk_officerSem FOREIGN KEY (semester) REFERENCES semester(semCode),
	 	CONSTRAINT uq_officer_semPos UNIQUE (semester, position) ) ;

#add the VPs and Directors to area and region
ALTER TABLE area
	ADD COLUMN areaVP CHAR(8) AFTER areaNo ;

ALTER TABLE region
	ADD COLUMN rd CHAR(8) AFTER areaNo ;

CREATE TABLE drop_suspend_reason (
	reason_key	INT AUTO_INCREMENT,
	memCode	CHAR(8),
    old_status	VARCHAR(25),
    reason	TEXT,
		PRIMARY KEY (reason_key) );

DELIMITER \\
CREATE FUNCTION retained_members (z CHAR(5))
	RETURNS INT(3)
    DETERMINISTIC
BEGIN
	DECLARE x INT(3);
	SET x = (SELECT COUNT(m.memCode)
			FROM membership m, semester s
            WHERE m.pledgeSem = s.semCode
            AND s.semCode = z
            AND (m.akpsi_status = 'Active' OR m.akpsi_status = 'Alumnus' OR m.akpsi_status = 'Deceasesd')
            GROUP BY s.semCode);
	RETURN x;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION count_actives (z VARCHAR(20))
	RETURNS INT(4)
    DETERMINISTIC
BEGIN
	DECLARE x INT(4);
    SET x = (SELECT COUNT(m.memCode)
			FROM membership m, chapter c
            WHERE m.chapter = c.chapterName
            AND c.chapterName = z
            AND m.akpsi_status = 'Active'
            GROUP BY c.chapterName);
	RETURN x;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION count_alumni (z VARCHAR(20))
	RETURNS INT(4)
    DETERMINISTIC
BEGIN
	DECLARE x INT(4);
    SET x = (SELECT COUNT(m.memCode)
			FROM membership m, chapter c
            WHERE m.chapter = c.chapterName
            AND c.chapterName = z
            AND (m.akpsi_status = 'Alumnus' OR m.akpsi_status = 'Deceased')
            GROUP BY c.chapterName);
	RETURN x;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION semester_suspended (semester_code CHAR(5))
	RETURNS INT(3)
	DETERMINISTIC
BEGIN
	DECLARE z INT(3);
	SET z = (SELECT COUNT(memCode) FROM membership WHERE susSem = semester_code AND chapter='Beta Chi');
	RETURN z;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION semester_reinstatements (semester_code CHAR(5))
	RETURNS INT(3)
	DETERMINISTIC
BEGIN
	DECLARE z INT(3);
	SET z = (SELECT COUNT(memCode) FROM membership WHERE reinstateSem = semester_code AND chapter = 'Beta Chi');
	RETURN z;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION semester_graduates (semester_code CHAR(5))
	RETURNS INT(3)
	DETERMINISTIC
BEGIN
	RETURN (SELECT COUNT(memCode) FROM membership WHERE gradSem = semester_code AND chapter = 'Beta Chi');
END \\
DELIMITER ;

#Adding reinstatements to the data
ALTER TABLE membership
	ADD COLUMN reinstateSem CHAR(5)
    AFTER susSem;
ALTER TABLE membership
	ADD CONSTRAINT fk_memReinstateSem FOREIGN KEY (reinstateSem) REFERENCES semester(semCode) ON UPDATE CASCADE ON DELETE SET NULL;

#Add sponsorship and fundraising amounts to the semester table
ALTER TABLE semester
	ADD COLUMN `sponsorships` INT
		AFTER brothersInitiated;
ALTER TABLE semester
	ADD COLUMN `fundraising` INT
		AFTER sponsorships;

DELIMITER \\
CREATE FUNCTION age (member_code CHAR(8))
	RETURNS INT
	DETERMINISTIC
BEGIN
	RETURN FLOOR(DATEDIFF(CURDATE(),(SELECT birthday FROM membership WHERE memCode = member_code))/365);
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION over_21 (member_code CHAR(8))
	RETURNS INT(1)
	DETERMINISTIC
BEGIN
	IF (SELECT age(memCode) FROM membership WHERE memCode = member_code) >= 21
		THEN RETURN 1;
		ELSE RETURN 0;
	END IF;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION is_officer (member_code CHAR(8))
	RETURNS INT(1)
	DETERMINISTIC
BEGIN
	DECLARE q INT(1);
	IF member_code IN (SELECT memCode FROM officer)
		THEN SET q = 1;
		ELSE SET q = 0;
	END IF;
	RETURN q;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION officer_time (member_code CHAR(8))
	RETURNS INT(2)
	DETERMINISTIC
BEGIN
	DECLARE t INT(2);
	SET t = (SELECT COUNT(memCode) FROM officer WHERE memCode = member_code);
	RETURN t;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION chapter_time (member_code CHAR(8))
	RETURNS INT(2)
    DETERMINISTIC
BEGIN
	DECLARE upper FLOAT;
    DECLARE lower FLOAT;
    DECLARE enterSem CHAR(5);
    DECLARE leaveSem CHAR(5);

    SET enterSem = (SELECT pledgeSem FROM membership WHERE memCode = member_code);
    IF (SELECT susSem FROM membership WHERE memCode = member_code) IS NOT NULL AND (SELECT reinstateSem FROM membership WHERE memCode = member_code) IS NULL
		THEN SET leaveSem = (SELECT susSem FROM membership WHERE memCode = member_code);
		ELSE SET leaveSem = (SELECT gradSem FROM membership WHERE memCode = member_code);
	END IF;

    IF LEFT(enterSem,1) = 'F'
		THEN SET lower = RIGHT(enterSem,4);
        ELSE SET lower = RIGHT(enterSem,4)+.5;
	END IF;

    IF LEFT(leaveSem,1) = 'F'
		THEN SET upper = RIGHT(leaveSem,4);
        ELSE SET upper = RIGHT(leaveSem,4)-0.5;
	END IF;

    RETURN (upper - lower)*2;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION us_resident (member_code CHAR(8))
	RETURNS INT(1)
	DETERMINISTIC
BEGIN
	IF (SELECT homeCountry FROM membership WHERE memCode = member_code) = 'United States'
		THEN RETURN 1;
		ELSE RETURN 0;
	END IF;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION grad_student (member_code CHAR(8))
	RETURNS INT(1)
	DETERMINISTIC
BEGIN
	IF (SELECT gradProgram FROM membership WHERE memCode = member_code) IS NOT NULL
		THEN RETURN 1;
		ELSE RETURN 0;
	END IF;
END \\
DELIMITER ;

DELIMITER \\
CREATE FUNCTION business_major (member_code CHAR(8))
	RETURNS INT(1)
	DETERMINISTIC
BEGIN
	IF (SELECT co.college FROM membership m LEFT JOIN college co ON m.major = co.major WHERE m.memCode = member_code) = 'Business'
		THEN RETURN 1;
		ELSE RETURN 0;
	END IF;
END \\
DELIMITER ;

DELIMITER \\
CREATE PROCEDURE semester_graduates (IN desired_semester CHAR(5))
	BEGIN
		SELECT
			CONCAT(m.fName,' ',m.lName) AS `Name`,
			m.gradSem AS `Grad Semester`
		FROM membership m
		WHERE m.akpsi_status = 'Active'
			AND m.gradSem = desired_semester
			AND m.chapter = 'Beta Chi'
		ORDER BY m.lName;
	END \\
DELIMITER ;

DELIMITER \\
CREATE PROCEDURE semester_officers (IN z CHAR(5))
	BEGIN
		SELECT CONCAT(m.fName,' ',m.lName) AS `Name`, o.position AS `Officer Position`
		FROM officer o
			JOIN membership m
				ON m.memCode = o.memCode
			JOIN semester s
				ON o.semester = s.semCode
		WHERE o.semester = z
		ORDER BY s.semYear, s.semTerm DESC, FIELD(o.position,'President','Executive Vice President','Vice President of Membership','Vice President of Finance','Vice President of Professional Development','Vice President of Alumni Relations','Vice President of Public Relations','Gala Chair','Secretary','Master of Rituals','Pledge Educator','Treasurer','Webmaster','Sponsorship Chair','Fundraising Chair','Social Chair','Service Chair','Warden');
	END \\
DELIMITER ;

 -- Create a shareable demographic list, for if bros would like to be able to do their own research
CREATE VIEW sharing_membership AS
SELECT
	m.memCode as `Member Code`,
	m.akpsi_status as `Fraternity Status`,
	m.major AS `Major`,
	co.college AS `College`,
	m.pledgeClass AS `Pledge Classification`,
	m.pledgeSem AS `Pledge Semester`,
	m.gradSem AS `Graduating Semester`,
	m.susSem AS `Suspension Semester`,
	m.reinstateSem AS `Reinstatement Semester`,
	age(m.memCode) AS `Age`,
	m.gender AS `Gender`,
	m.homeState AS `Home State`,
	m.homeCountry AS `Home Country`,
	m.gradProgram AS `Graduate Program`,
	m.gradUni AS `Graduate University`,
	m.workCompany AS `Work Company`,
	m.workState AS `Work State`,
	m.workCountry AS `Work Country`
FROM membership m
	LEFT JOIN college co
		ON co.major = m.major
WHERE m.chapter = 'Beta Chi'
ORDER BY `Fraternity Status`;

-- CREATE VIEW sharing_semester AS
-- SELECT

CREATE VIEW sas_membership_all AS
SELECT
    CONCAT(m.fName,' ',m.lName) AS `Full Name`,
    m.akpsi_status AS `Status`,
    m.chapter AS `Chapter`,
    m.major AS `Major`,
    co.college AS `College`,
    m.pledgeClass AS `Pledge Classification`,
    sp.semTerm AS `Pledge Term`,
    sp.semYear AS `Pledge Year`,
    sg.semTerm AS `Grad Term`,
    sg.semYear AS `Grad Year`,
    m.birthday AS `Birthday`,
    age(m.memCode) AS `Age`,
    m.gender AS `Gender`,
    m.homeCity AS `Home City`,
    m.homeState AS `Home State`,
    m.homeCountry AS `Home Country`,
    m.gradProgram AS `Graduate Program`,
    m.gradUni AS `Graduate University`,
    m.workCompany AS `Company`,
    m.workCity AS `Work City`,
    m.workState AS `Work State`,
    m.workCountry AS `Work Country`,
    sp.semInduction AS `Induction Date`,
    sp.semInitiation AS `Initiation Date`,
    sg.semInitiation AS `Graduation Date`,
    business_major(m.memCode) AS `Is Business Major`,
    chapter_time(m.memCode) AS `Chapter Time`,
    grad_student(m.memCode) AS `Is Graduate Student`,
    is_officer(m.memCode) AS `Is Officer`,
    officer_time(m.memCode) AS `Officer Time`,
    over_21(m.memCode) AS `Is Over 21`,
    us_resident(m.memCode) AS `Is US Resident`
FROM (membership m
	LEFT JOIN semester sp
		ON m.pledgeSem = sp.semCode)
	LEFT JOIN semester sg
		ON m.gradSem = sg.semCode
	LEFT JOIN college co
		ON co.major = m.major
WHERE m.akpsi_status <> 'Faculty Member'
ORDER BY `Chapter`,`Status`,m.lName,m.fName;

CREATE VIEW sas_semester AS
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
		(DATEDIFF(CURDATE(),s.semInitiation)/365) AS `Time since Initiation`
FROM semester s
WHERE (s.semYear >= 2010 AND s.semYear <= YEAR(CURDATE()))
ORDER BY `Year`, `Term` DESC;

CREATE VIEW officer_info AS
SELECT
	CONCAT(m.fName,' ',m.lName) AS `Name`,
    m.akpsi_status AS `Status`,
    m.email1 AS `Email 1`,
    m.email2 AS `Email 2`,
    m.phone AS `Phone Number`,
    m.major AS `Major`,
    co.college AS `College`,
    m.pledgeSem AS `Pledge Semester`,
    m.gradSem AS `Graduating Semester`,
    m.birthday AS `Birthday`
FROM membership m
	LEFT JOIN college co
		ON m.major = co.major
WHERE akpsi_status = 'Active' OR akpsi_status = 'Pledge'
ORDER BY `Status`,m.lName;

ALTER TABLE membership ADD COLUMN mName VARCHAR(255) AFTER fName;
ALTER TABLE membership ADD COLUMN nickname VARCHAR(255) AFTER lName;
ALTER TABLE membership ADD COLUMN chapter_status VARCHAR(255) AFTER akpsi_status;

DELIMITER \\
CREATE
    EVENT status_update
ON SCHEDULE EVERY 1 MONTH
	STARTS '2019-05-01 00:00:00'
COMMENT 'Resets the chapter statuses of members who are not actives'
DO
	BEGIN
	UPDATE membership SET chapter_status = NULL WHERE akpsi_status <> 'Active';
    END \\
DELIMITER ;

USE akpsi;
