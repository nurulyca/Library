// selecting the input with name property "name"
const updateName = document.querySelector('input[name="updatename"]'); 
// selecting the input with name property "email"
const updateEmail = document.querySelector('input[name="updateemail"]');
// selecting the input with name property "password"
const updatePassword = document.querySelector('input[name="updatepassword"]') 
// selecting the input with name property "ID"
const updateId = document.querySelector('input[name="updateid"]') 

function createHTMLRow(data) {  
  // creating a row of cells in table
  const row = document.createElement('tr');
  // creating a cell of table that contains data
  const td = document.createElement('td');

  // === UPDATE ===
  // creating a button
  const button = document.createElement('button');
  // creating the button within text of "Update"
  const insideButton = document.createTextNode("Update");
  // adding insideButton to the button 
  button.appendChild(insideButton)
  // if the button was clicked, it's updating the updated value in the form.
  button.onclick = () => {
    // the updated
    updateName.value = data.name
    updateEmail.value = data.email
    updateId.value = data.id
  }
  
  // === DELETE ===
  // creating a delete button
  const deleteButton = document.createElement('button');
  // putting the text "Delete" to the delete button
  deleteButton.innerText = "Delete"
  // delete the data by click the delete button
  deleteButton.onclick = function(){
     return fetch('http://localhost:5000/users/' + data.id + "/", {
      method: 'DELETE'
      })
      .then(res => res.json())
      .then(text => console.log(text))
      .catch(err => console.log(err))
    }
  
  for (prop in data) {
    // assigning the cell of table that contains data
    const cell = document.createElement('td');
    // the cell is the prop of data
    cell.innerHTML = data[prop];
    // adding cell to the row
    row.appendChild(cell);
  }
    // adding button to the td
    td.appendChild(button)
    // adding delete button to the td
    td.appendChild(deleteButton)
    // adding td to the row
    row.appendChild(td)
    // return the row
    return row;
}