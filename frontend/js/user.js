document.addEventListener('DOMContentLoaded', function() {  

    getUsers().then(users => {
    const userTable = document.querySelector('#userTable');
    const tbody = userTable.querySelector('tbody');
    
    tbody.innerHTML = '';
    let sortedUsers = users.sort((a,b) => a.user_id - b.user_id)
    sortedUsers.forEach(item => {
      const row = createHTMLRow({ 
        id: item.user_id, 
        name: item.name, 
        password: item.password, 
        email: item.email 
      });
      tbody.appendChild(row);
    })    
  });
});