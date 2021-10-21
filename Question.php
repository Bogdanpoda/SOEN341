<!DOCTYPE html>
<html>
    <head>   
        <title>Question Page</title>
        <link rel="stylesheet" href="css/IndexpageStyle.css">
        <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro&display=swap" rel="stylesheet">
        <link href="https://cdn.layerjs.org/libs/layerjs/layerjs-0.5.2.css" type="text/css" rel="stylesheet">
        <link rel="stylesheet" href="Question.css">
    </head>
     
 <body>
    <div class="row" >
        <div class="headerPage">
            <div class="col-3 headerContainer">
                <h1> <a>StackUnderflow</a> </h1>      
            </div>

            <div class = "col-9 menuParent">
                <div class="dropdown">
                    <button class="dropbtn">Labels</button>
                    <div class="dropdown-content">
                        <a href="#">programmming</a>
                        <a href="#">sports</a>
                        <a href="#">educational</a>
                    </div>
                </div>
            </div>
        </div>

        
    </div>

    <div class  ="questionformStyle">
        <p>Question: </p>
        <p id = "questionAsked">What is your name?</p>

        <form action = "Question.php" method="POST">
            <textarea name="answer" id="answerresponse" placeholder = "Enter your answer here..." rows = "20" cols = "100" value = "<?php echo $ans;?>"></textarea> <br><br>
            
            <button type="submit" class="submitStyle" name="submitanswerbtn">Submit</button>
        </form>
    </div>
 

    <br><br>

    <div>
       <p>Answers:</p> 
        <div class="responsedanswers">
            <!--<p id="demo"></p>-->
           <?php echo file_get_contents("volunteer_data.txt"); ?>
            <div class="updownStyle">
                <p id="votes">0</p>
                <button class = "votingBtn" id  = "upvote" onclick = upvote()>+</button>
                <button class = "votingBtn" id = "downvote" onclick = downvote()>-</button>
            </div>
        </div>
    </div>


    <script src="updownvote.js" charset="utf-8"></script>

</body>
    
    
</html>

<?php
    if (isset($_POST["submitanswerbtn"])) {
        $ans = $_POST['answer'];

        $file = fopen("volunteer_data.txt", "a");
        $input_data = PHP_EOL . $ans;
        fwrite($file, $input_data);
        fclose($file);
    }

?>