/* Adding logout class 
************************************/

var $navRight = $('#nav-right li');
$navRight.each(function () {
	if ($(this).text().trim() === 'Logout') {
		$(this).children().addClass('logout');
	}
});

// Calling saveData() when user logs out
$('.logout').click(function () {
	saveData(true);
	clearInterval(save);
});

// Problem: User interaction does not provide desired results.
// Solution: Add interactivity so the user can manage daily tasks.

var taskInput = document.getElementById("new-task");
var addButton = document.getElementById("addButton");
var incompleteTasksHolder = document.getElementById("incomplete-tasks"); 
var completedTasksHolder = document.getElementById("completed-tasks");

// New task list item
var createNewTaskElement = function (taskString) {
	// Create list item
	var listItem = document.createElement("li");

	// Input (checkbox)
	var checkBox = document.createElement("input"); // type = checkbox
	// A label
	var label = document.createElement("label");
	// Input (text)
	var editInput = document.createElement("input"); // type = text
	// Button (.edit)
	var editButton = document.createElement("button");
	// Button (.delete)
	var deleteButton = document.createElement("button");

	// Each of these elements needs to be modified
	checkBox.type = "checkbox";
	editInput.type = "text";

	editButton.innerText = "Edit";
	editButton.className = "edit";
	deleteButton.innerText = "Delete";
	deleteButton.className = "delete";
	label.innerText = taskString;

	// Each of these elements needs to be appended
	listItem.appendChild(checkBox);
	listItem.appendChild(label);
	listItem.appendChild(editInput);
	listItem.appendChild(editButton);
	listItem.appendChild(deleteButton);

	return listItem;
}

// Add a new task
var addTask = function() {
	var taskText = taskInput.value;

	if (taskText === "") {
		alert("Please provide some text!");
	} else {
		// Create a new list item with the text from #new-task
		var listItem = createNewTaskElement(taskText);

		// Append listItem to the incompleteTaskHolder
		incompleteTasksHolder.appendChild(listItem);
		bindTaskEvents(listItem, taskCompleted);

		taskInput.value = "";	
		saveData(false);
	}
};

function enterForEventAdd(ele) {
	if(event.keyCode == 13) {
	    addTask();        
	}
}

// Edit existing task
var editTask = function() {
	var listItem = this.parentNode;

	var editInput = listItem.querySelector("input[type=text]");
	var label = listItem.querySelector("label");
	var editButton = listItem.querySelector("button.edit");

	var containsClass = listItem.classList.contains("editMode");
	// If the class of the parent is editMode
	if (containsClass) {
		// Switch from .editMode
		// Label's text becomes the input's value
		label.innerText = editInput.value;
		// Change editButton text to "Edit"
		editButton.innerText = "Edit";
	} else {
		// Switch to .editMode
		// input value becomes the label's text	
		editInput.value = label.innerText;
		// Focus on editInput
		editInput.autofocus = true;
		// Change editButton text to "Save"
		editButton.innerText = "Save";
	}	

	// Toggle .editMode on the listItem
	listItem.classList.toggle("editMode");

	saveData(false);
};

// Mark a task as complete
var taskCompleted = function() {
	// Append task list item to the #completed-tasks
	var listItem = this.parentNode;
	completedTasksHolder.appendChild(listItem);
	bindTaskEvents(listItem, taskIncomplete);

	saveData(false);
};

// Mark a task as incomplete
var taskIncomplete = function() {
	// Append task list item to the #incomplete-tasks
	var listItem = this.parentNode;
	incompleteTasksHolder.appendChild(listItem);
	bindTaskEvents(listItem, taskCompleted);

	saveData();
};

// Delete an existing task
var deleteTask = function() {
	var listItem = this.parentNode;
	var ul = listItem.parentNode;

	// Remove the parent list item from the ul
	ul.removeChild(listItem);

	saveData(false);
};


/* Setting click handlers to the functions 
**********************************************/
addButton.addEventListener("click", addTask);

var bindTaskEvents = function (taskListItem, checkBoxEventHandler) {
	// Select taskListItem's children
	var checkBox = taskListItem.querySelector("input[type=checkbox]");
	var editButton = taskListItem.querySelector("button.edit");
	var deleteButton = taskListItem.querySelector("button.delete");

	// bind editTask to edit button
	editButton.onclick = editTask;

	// bind deleteTask to delete button 
	deleteButton.onclick = deleteTask;

	// bind checkBoxEventHandler to the check box
	checkBox.onchange = checkBoxEventHandler;
};

//cycle over incompleteTasksHolder ul list items
for(var i = 0; i < incompleteTasksHolder.children.length; i++) {
  //bind events to list item's children (taskCompleted)
  bindTaskEvents(incompleteTasksHolder.children[i], taskCompleted);
}

//cycle over completedTasksHolder ul list items
for(var i = 0; i < completedTasksHolder.children.length; i++) {
  //bind events to list item's children (taskIncomplete)
  bindTaskEvents(completedTasksHolder.children[i], taskIncomplete);
}

/* Handling backend save (using jQuery)
*****************************************/

var save = setInterval(saveData, 60 * 1000);

function saveData(isLogout) {
	if (!isLogout) {
		// Handling saving UI
		$('.save-label').text('Saving...');
		$('.save-label').css('display', 'inherit');
		setTimeout(function(){ 
			$('.save-label').text('Saved!'); 
			setTimeout(function(){ $('.save-label').css('display', 'none');  }, 2000); 
		}, 3000);		
	}
	
	var $taskLabels = $('#incomplete-tasks li label');
	var $completeLabels = $('#completed-tasks li label');
	var todo = [];
	var done = [];

	$taskLabels.each(function () {
		var value = $(this).text();
		todo.push(value);
	});

	$completeLabels.each(function () {
		var value = $(this).text();
		done.push(value);
	});

	var user = new Object();
	user.todo = todo;
	user.done = done;

	var json = JSON.stringify(user);

	$.ajax({
		url: '/index', 
	  type: 'POST', 
	  data: json, 
	  contentType:'application/json; charset=utf-8',
	  dataType: "json",
	  success: function (){ console.log('DONE'); }
	});
}
