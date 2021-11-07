CREATE TABLE Users(
	User_Name VARCHAR(255) unique,
    Email_Address VARCHAR(255) unique,
    User_ID INT,
    Password VARCHAR(255), -- Really not good, but don't have time to add security features
    Primary key(User_ID)
);

CREATE TABLE Questions(
	Question_ID INT,
    User_Name VARCHAR(255),
    Favorite_Answer_ID INT,
    Label varchar(255),
    Content VARCHAR(1000),
    Number_Of_Up_Votes INT default 0,
    Number_Of_Down_Votes INT default 0,
    Question_date DATE,
    Primary key(Question_ID),
    
    Foreign key(User_Name)
		References Users (User_Name),
        
	Foreign key(Favorite_Answer_ID)
		References Answers (Answer_ID)
);

CREATE TABLE Answers(
	Answer_ID INT,
    User_Name VARCHAR(255),
    Content VARCHAR(1000),
    Number_Of_Up_Votes INT default 0,
    Number_Of_Down_Votes INT default 0,
    Answer_date DATE,
    Primary key(Answer_ID),
    
    Foreign key(User_Name)
		References Users (User_Name)
); 

CREATE TABLE Question_has_Answers(
	Question_ID INT,
    Foreign key(Question_ID)
		References Questions (Question_ID),
    Answer_ID INT,
    Foreign key(Answer_ID)
		References Answers (Answer_ID),
        
    Primary key(Question_ID,Answer_ID)
);

CREATE TABLE VOTE(
	User_Name VARCHAR(255),
    Question_ID INT,
    Vote boolean,
    
    Foreign key(User_Name)
		References Users (User_Name),
	foreign key(Question_ID)
		References Questions(Question_ID),
        
	Primary key(User_Name,Question_ID)
);

DROP TABLE VOTE;
	

select* 
from Users;

Delete from Users;
SET SQL_SAFE_UPDATES = 0;

Drop TABLE Users;
Drop Table Vote;

select*
from Questions;

select* from Vote;

select Users.User_Name, Answers.Content 
FROM Question_has_Answers, Answers, Users 
WHERE Answers.Answer_ID = Question_has_Answers.Answer_ID and Users.Answer_ID=Answers.Answer_ID
	   and Question_has_Answers.Question_ID = 1;


DROP TABLE Users;
DROP TABLE Question_has_Answers;
DROP TABLE Answers;
DROP TABLE Questions;

SET FOREIGN_KEY_CHECKS=1;  

UPDATE QUESTIONS SET Number_Of_Up_Votes=Number_Of_Up_Votes+1 WHERE Question_ID=1;

ALTER TABLE QUESTIONS
ALTER Number_OF_Up_Votes SET DEFAULT 0;

UPDATE QUESTIONS SET Number_Of_Up_Votes=0;

SELECT * FROM VOTE;

DELIMITER $$

CREATE TRIGGER Update_Question_Vote
after insert  On  Vote for each row 
begin
	If New.Vote is False then
		update Questions 
        set Number_Of_Down_Votes=Number_Of_Down_Votes+1
        where Questions.Question_ID=New.Question_ID;
	END IF;
    
	If New.Vote is True then
		update Questions 
        set Number_Of_Up_Votes=Number_Of_Up_Votes+1
        where Questions.Question_ID=New.Question_ID;
	END IF;

end$$

DELIMITER ;

DROP trigger Update_Question_Vote;


	



