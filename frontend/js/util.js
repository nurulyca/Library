const updateName = document.querySelector('input[name="updatename"]') //selecting the input with name property "name"
const updateEmail = document.querySelector('input[name="updateemail"]') //selecting the input with name property "email"
const updatePassword = document.querySelector('input[name="updatepassword"]') //selecting the input with name property "password"
const updateFormButton = document.querySelector("button#updateitem") 

function createHTMLRow(data) {  
  const row = document.createElement('tr');

  const button = document.createElement('button');

  const insideButton = document.createTextNode("Update");
  button.appendChild(insideButton)
  button.onclick = () => {
    updateName.value = data.name
    updateEmail.value = data.email
    // updatePassword.value = data.password
    console.log(data.id)}
    const deleteButton = document.createElement('button')
    deleteButton.innerText = "Delete"
    deleteButton.onclick = function(){
      fetch('http://localhost:5000/users/' + data.id + "/", {
        method: 'DELETE'
      })
       .then(res => res.json())
      .then(text => console.log(text))
    }

  for(prop in data) {
    const cell = document.createElement('td')
    cell.innerHTML = data[prop];
    row.appendChild(cell);
  }
    row.appendChild(button)
    row.appendChild(deleteButton)
    return row;
}