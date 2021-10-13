CREATE TABLE Users(
	First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Email_Address VARCHAR(255),
    User_ID INT,
    Password VARCHAR(255), -- Really not good, but don't have time to add security features
    Primary key(User_ID),
    
    Question_ID INT,
    Foreign key(Question_ID)
		References Questions (Question_ID),
	Answer_ID INT,
    Foreign key(Answer_ID)
		References Answers(Answer_ID)
    
);

CREATE TABLE Questions(
	Question_ID INT,
    Favorite_Answer_ID INT,
    Content VARCHAR(1000),
    Number_Of_Up_Votes INT,
    Number_Of_Down_Vores INT,
    Question_date DATE,
    Primary key(Question_ID)
);

CREATE TABLE Answers(
	Answer_ID INT,
    Content VARCHAR(1000),
    Number_Of_Up_Votes INT,
    Number_Of_Down_Vores INT,
    Answer_date DATE,
    Primary key(Answer_ID)
); 

CREATE TABLE Question_has_Answers(
	Question_ID INT,
    Foreign key(Question_ID)
		References Questions (Question_ID),
    Answer_ID INT,
    Foreign key(Answer_ID)
		References Answers (Answer_ID),
	Favorite_Answer_ID INT,
    Foreign key(Favorite_Answer_ID)
		References Answers (Answer_ID),
	
    Primary key(Question_ID,Answer_ID)
);

   
