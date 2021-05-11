function createHTMLRow(data) {  
  // creating a row of cells in table
  const row = document.createElement('tr');
  // creating a cell of table that contains data
  const td = document.createElement('td');

  // creating a button
  const button = document.createElement('button');
  // creating the button within text of "Update"
  const insideButton = document.createTextNode("View");
  // adding insideButton to the button 
  button.className = "view-button"
  button.appendChild(insideButton)
  button.onclick = () => {
    window.location.href = "view.html?id=" + data.id
  }
  

  const updateButton = document.createElement('button');
  // putting the text "Edit" to the button
  updateButton.innerText = "Edit"
  // directing to the link by click the edit button
  updateButton.className = "update-button"
  updateButton.onclick = function(){
    window.location.href = "edit.html?id=" + data.id
    }
  
  for (prop in data) {
    // assigning the cell of table that contains data
    const cell = document.createElement('td');
    cell.innerHTML = data[prop];
    row.appendChild(cell);
  }
    td.appendChild(button)
    td.appendChild(updateButton)
    row.appendChild(td)
    return row;
}