// get all users
function getUsers(offset, limit) {
  return fetch('http://localhost:5000/users/pagination?offset=' + offset + "&limit=" + limit)
    .then(response => response.json())
    .then(json => json);
}

// create new user
const form = document.querySelector('#userForm');
form.addEventListener('submit', (e) => {
  console.log(e)
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
  .then(jsonRes => console.log(jsonRes))
})