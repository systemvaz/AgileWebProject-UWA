// --------------------------------------------------------------------------
// Define Javascript functions allowing for dynamic manipulation
// of forms and form data in the /admin/new_quiz route.
// --------------------------------------------------------------------------

// Global variable i, used for auto increment.
var i = 0;

// Function to incriment global variable i.
function increment()
{
    i = i + 1;
}

// onclick event handler for 'Add Question' button.
// Add textbox to enter the Question, mapped to wtforms questions.question
// Add radio buttons for selecting whether question is multichoice
function add_question()
{
    var myDiv = document.getElementById('dynamicAdd');
    var curLength = myDiv.children.length;
    var newDiv = document.createElement('div')
    divId = 'questionDiv-' + i;
    newDiv.setAttribute('id', divId);

    increment();
    
    newDiv.appendChild(document.createElement('hr'));

    // Display question
    var qNum = document.createElement('p');
    qNum.innerHTML = 'Question #:' + (curLength+1);
    newDiv.appendChild(qNum);

    // Create new question text box, mapped to wtforms name
    var newAdd = document.createElement('textarea');
    newAdd.setAttribute('name', 'questions-' + curLength + '-question');
    newAdd.setAttribute('id', 'q' + curLength);
    newAdd.setAttribute('style', 'width: 85%')
    newDiv.appendChild(newAdd);

    // Create hidden element set to questionNum
    // Used by add_multichoice() & addcorrectanswer() & del_multichoice()
    newAdd = document.createElement('input');
    newAdd.setAttribute('type', 'hidden');
    newAdd.setAttribute('id', 'questionNum');
    newAdd.setAttribute('value', curLength);
    newDiv.appendChild(newAdd);
    newDiv.appendChild(document.createElement('br'));

    // Add radio buttons to select if multichoice or not
    newAdd = document.createElement('span');
    newAdd.innerHTML = "Multichoice Question?: ";
    newDiv.appendChild(newAdd);
    var radioName = 'multichoice_' + curLength;
    // Yes...
    newAdd = document.createElement('input');
    newAdd.setAttribute('type', 'radio');
    newAdd.setAttribute('name', radioName);
    newAdd.setAttribute('value', 'mc_yes');
    // onclick event handler to run add_multichoice function on Yes radio button click
    newAdd.setAttribute('onclick', 'add_multichoice(this)');
    newDiv.appendChild(newAdd);
    newAdd = document.createElement('label');
    newAdd.innerHTML = "Yes";
    newDiv.appendChild(newAdd);
    // No....
    newAdd = document.createElement('input');
    newAdd.setAttribute('type', 'radio');
    newAdd.setAttribute('name', radioName);
    newAdd.setAttribute('value', 'mc_no');
    newAdd.setAttribute('style', 'margin-left: 10px')
    newAdd.setAttribute('checked', 'checked')
    // onclick event handler to run del_multichoice function on No radio button click
    newAdd.setAttribute('onclick', 'del_multichoice(this)');
    newDiv.appendChild(newAdd);
    newAdd = document.createElement('label');
    newAdd.innerHTML = "No";
    newDiv.appendChild(newAdd);

    newDiv.appendChild(document.createElement('br'));
    myDiv.appendChild(newDiv);
}


// onclick event handler for when user clicks Yes for whether question is multichoice
// Creates the 4 text inputs for the possible answers.
// Create the 4 radio buttons to select which on is the correct answer.
function add_multichoice(elem)
{
    var newAdd;
    var thisDiv = elem.parentNode;
    var question_num = thisDiv.querySelector('#questionNum').value;
    var radioName = 'answerforQ_' + question_num;
    var formNameMC ='questions-' + question_num + '-multichoice';
    var formNameMCAnswers ='questions-' + question_num + '-multichoiceAnswers';
    var ourDiv = document.createElement('div');
    
    // Cleanup this div if multichoice Yes/No has been clicked multiple times
    if(thisDiv.querySelector('#' + formNameMC) != null)
    {
        var removeMC = document.getElementById(formNameMC);
        thisDiv.removeChild(removeMC);
    }
    
    // Add new div and set hidden fields
    ourDiv.setAttribute('id', formNameMCAnswers);
    thisDiv.appendChild(ourDiv);
    newAdd = document.createElement('input');
    newAdd.setAttribute('type', 'hidden');
    newAdd.setAttribute('name', formNameMC);
    newAdd.setAttribute('id', formNameMC);
    newAdd.setAttribute('value', 'True');
    ourDiv.appendChild(newAdd);

    // Iterate 4 times to create 4 possible answers.
    // Add test input and radio button for each possible answer.
    // Set attributes mapping to wtforms answers.answer1 to answer.answer4
    for(var i=0; i < 4; i++)
    {
        newAdd = document.createElement('p');
        newAdd.setAttribute('style', 'font-weight: bold')
        newAdd.innerHTML = 'Answer option #' + (i+1) + ':';
        ourDiv.appendChild(newAdd);
        newAdd = document.createElement('input');
        newAdd.setAttribute('type', 'text');
        newAdd.setAttribute('style', 'width: 80%')
        newAdd.setAttribute('name', 'answers-' + question_num + '-answer' + (i+1));
        ourDiv.appendChild(newAdd);
        newAdd = document.createElement('input');
        newAdd.setAttribute('type', 'radio');
        newAdd.setAttribute('style', 'margin-left: 10px')
        newAdd.setAttribute('name', radioName);
        newAdd.setAttribute('value', (i));
        if(i == 0) {newAdd.setAttribute('checked', 'checked')}
        // onclick event handler for selecting this as the correct answer
        newAdd.setAttribute('onclick', 'add_correctanswer(this)');
        ourDiv.appendChild(newAdd);
        newAdd = document.createElement('label');
        newAdd.setAttribute('style', 'margin-left: 10px')
        newAdd.innerHTML = "Correct Answer";
        ourDiv.appendChild(newAdd);
        ourDiv.appendChild(document.createElement('br'));
    }
}

// onclick event handler for selecting a multichoice answer as the correct answer.
// Map answer number to wtforms multichoice.correct
function add_correctanswer(elem)
{
    var newAdd;
    var correctAnswer = elem.value;
    var ourDiv = elem.parentNode;
    var ourDivParent = ourDiv.parentNode;
    var question_num = ourDivParent.querySelector('#questionNum').value;
    var formNameCorrect = 'answers-' + question_num + '-correct';

    // Clean up if we have previously selected another answer as correct
    if(ourDiv.querySelector('#' + formNameCorrect) != null)
    {
        var removeCorrect = document.getElementById(formNameCorrect);
        ourDiv.removeChild(removeCorrect);
    }

    // set our hidden element attributes for wtforms
    newAdd = document.createElement('input');
    newAdd.setAttribute('type', 'hidden');
    newAdd.setAttribute('name', formNameCorrect);
    newAdd.setAttribute('id', formNameCorrect);
    newAdd.setAttribute('value', correctAnswer);
    ourDiv.appendChild(newAdd);
    console.log(newAdd.value);
}

// onclick event handler for or when user clicks No for whether question is multichoice.
function del_multichoice(elem)
{
    var newAdd;
    var ourDiv = elem.parentNode;
    var question_num = ourDiv.querySelector('#questionNum').value;
    var formNameMC ='questions-' + question_num + '-multichoice';
    var formNameMCAnswers ='questions-' + question_num + '-multichoiceAnswers';

    // Cleans up div if multichoice was previously selected as Yes
    if(ourDiv.querySelector('#' + formNameMC) != null)
    {
        var removeMC = document.getElementById(formNameMCAnswers);
        ourDiv.removeChild(removeMC);
    }

    // Create hidden element containing attributes for wtforms answers.multichoice
    newAdd = document.createElement('input');
    newAdd.setAttribute('type', 'hidden');
    newAdd.setAttribute('name', formNameMC);
    newAdd.setAttribute('id', formNameMC);
    newAdd.setAttribute('value', 'False');
    ourDiv.appendChild(newAdd);
}