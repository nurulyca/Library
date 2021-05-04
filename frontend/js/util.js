

function createHTMLRow(data) {  
  // creating a row of cells in table
  const row = document.createElement('tr');
  // creating a cell of table that contains data
  const td = document.createElement('td');

  // === UPDATE ===
  // creating a button
  const button = document.createElement('button');
  // creating the button within text of "Update"
  const insideButton = document.createTextNode("View");
  // adding insideButton to the button 
  button.appendChild(insideButton)
  // if the button was clicked, it's updating the updated value in the form.
  button.onclick = () => {
    window.location.href = "view.html?id=" + data.id
  }
  
  // === DELETE ===
  // creating a delete button
  const updateButton = document.createElement('button');
  // putting the text "Delete" to the delete button
  updateButton.innerText = "Edit"
  // delete the data by click the delete button
  updateButton.onclick = function(){
    window.location.href = "edit.html?id=" + data.id
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
    td.appendChild(updateButton)
    // adding td to the row
    row.appendChild(td)
    // return the row
    return row;
}