function getUsers() {
  return fetch('http://localhost:5000/users')
    .then(response => response.json())
    .then(json => json);
}

const form = document.querySelector('#userForm');
form.addEventListener('submit', (e) => {
  e.preventDefault();

  const data = new FormData(form);
  const json = JSON.stringify((Object.fromEntries(data)));

  fetch('http://localhost:5000/register_users/', {
    method: 'POST',
    headers: { 
      'Content-Type' : 'application/json'
    },
    body: json
  })
  .then(res => res.json())
    //window.location.reload(true)
  .then(text => console.log(text))
})

const updateForm = document.querySelector('#updateForm');
updateForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const data = new FormData(updateForm);
  const json = JSON.stringify((Object.fromEntries(data)));

  fetch('http://localhost:5000/users/', {
    method: 'PUT',
    headers: { 
      'Content-Type' : 'application/json'
    },
    body: json
  })
  .then(res => res.json())
  .then(text => console.log(text))
})
