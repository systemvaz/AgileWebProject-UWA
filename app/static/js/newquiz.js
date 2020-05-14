function add_question()
{
    var myDiv = document.getElementById('dynamicAdd');
    var curLength = myDiv.children.length;
    var newDiv = document.createElement('div')
    
    newDiv.appendChild(document.createElement('hr'))

    // Display question number
    var qNum = document.createElement('p');
    qNum.innerHTML = 'Question #' + (curLength+1);
    newDiv.appendChild(qNum);

    // Create new question text box, mapped to wtforms name
    var newAdd = document.createElement('input');
    newAdd.setAttribute('type', 'text');
    newAdd.setAttribute('name', 'questions-' + curLength + '-question');
    newAdd.setAttribute('id', 'q' + curLength);
    newDiv.appendChild(newAdd)
    newAdd = document.createElement('input')
    newAdd.setAttribute('type', 'hidden')
    newAdd.setAttribute('id', 'questionNum')
    newAdd.setAttribute('value', curLength)
    newDiv.appendChild(newAdd)
    newDiv.appendChild(document.createElement('br'));

    // Add radio buttons to select if multichoice or not
    newAdd = document.createElement('span')
    newAdd.innerHTML = "Multichoice Question?: "
    newDiv.appendChild(newAdd)
    var radioName = 'multichoice_' + curLength
    // Yes...
    newAdd = document.createElement('input')
    newAdd.setAttribute('type', 'radio')
    newAdd.setAttribute('name', radioName)
    newAdd.setAttribute('value', 'mc_yes')
    // onclick event handler to run add_multichoice function
    newAdd.setAttribute('onclick', 'add_multichoice(this)')
    newDiv.appendChild(newAdd)
    newAdd = document.createElement('span')
    newAdd.innerHTML = "Yes"
    newDiv.appendChild(newAdd)
    // No....
    newAdd = document.createElement('input')
    newAdd.setAttribute('type', 'radio')
    newAdd.setAttribute('name', radioName)
    newAdd.setAttribute('value', 'mc_no')
    // onclick event handler to run del_multichoice function
    newAdd.setAttribute('onclick', 'del_multichoice(this)')
    newDiv.appendChild(newAdd)
    newAdd = document.createElement('span')
    newAdd.innerHTML = "No"
    newDiv.appendChild(newAdd)

    newDiv.appendChild(document.createElement('br'));

    myDiv.appendChild(newDiv);
}

function add_multichoice(elem)
{
    var newAdd
    var thisDiv = elem.parentNode
    
    var question_num = thisDiv.querySelector('#questionNum').value
    var radioName = 'answerforQ_' + question_num
    var formNameMC ='questions-' + question_num + '-multichoice'
    var formNameMCAnswers ='questions-' + question_num + '-multichoiceAnswers'

    var ourDiv = document.createElement('div')
    
    if(thisDiv.querySelector('#' + formNameMC) != null)
    {
        var removeMC = document.getElementById(formNameMC)
        thisDiv.removeChild(removeMC)
    }
    
    ourDiv.setAttribute('id', formNameMCAnswers)
    thisDiv.appendChild(ourDiv)

    newAdd = document.createElement('input')
    newAdd.setAttribute('type', 'hidden')
    newAdd.setAttribute('name', formNameMC);
    newAdd.setAttribute('id', formNameMC);
    newAdd.setAttribute('value', 'True')
    ourDiv.appendChild(newAdd)

    for(var i=0; i < 4; i++)
    {
        newAdd = document.createElement('p')
        newAdd.innerHTML = 'Answer option #' + (i+1) + ':'
        ourDiv.appendChild(newAdd)
        newAdd = document.createElement('input')
        newAdd.setAttribute('type', 'text');
        newAdd.setAttribute('name', 'answers-' + question_num + '-answer' + (i+1));
        ourDiv.appendChild(newAdd)
        newAdd = document.createElement('input')
        newAdd.setAttribute('type', 'radio')
        newAdd.setAttribute('name', radioName)
        newAdd.setAttribute('value', (i))
        newAdd.setAttribute('onclick', 'add_correctanswer(this)')
        ourDiv.appendChild(newAdd)
        newAdd = document.createElement('span')
        newAdd.innerHTML = "This is the correct answer"
        ourDiv.appendChild(newAdd)
        ourDiv.appendChild(document.createElement('br'));
    }
}

function add_correctanswer(elem)
{
    var newAdd
    var correctAnswer = elem.value
    var ourDiv = elem.parentNode
    var ourDivParent = ourDiv.parentNode
    var question_num = ourDivParent.querySelector('#questionNum').value

    newAdd = document.createElement('input')
    newAdd.setAttribute('type', 'hidden')
    newAdd.setAttribute('name', 'answers-' + question_num + '-correct')
    newAdd.setAttribute('value', correctAnswer)
    ourDiv.appendChild(newAdd)
    console.log(newAdd.value)
}

function del_multichoice(elem)
{
    var newAdd
    var ourDiv = elem.parentNode
    var question_num = ourDiv.querySelector('#questionNum').value
    var formNameMC ='questions-' + question_num + '-multichoice'
    var formNameMCAnswers ='questions-' + question_num + '-multichoiceAnswers'

    if(ourDiv.querySelector('#' + formNameMC) != null)
    {
        var removeMC = document.getElementById(formNameMCAnswers)
        ourDiv.removeChild(removeMC)
    }

    newAdd = document.createElement('input')
    newAdd.setAttribute('type', 'hidden')
    newAdd.setAttribute('name', formNameMC);
    newAdd.setAttribute('id', formNameMC);
    newAdd.setAttribute('value', 'False')
    ourDiv.appendChild(newAdd)
}