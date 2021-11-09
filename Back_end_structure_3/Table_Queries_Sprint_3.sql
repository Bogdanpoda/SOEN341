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