document.addEventListener('DOMContentLoaded', function() {  
    const paginationOne = document.querySelector(".one")
    const paginationTwo = document.querySelector(".two")
    const paginationThree = document.querySelector(".three")
    const search_bar = document.querySelector(".search_bar")
    const sortName = document.querySelector(".sort-name")
    const sortId = document.querySelector(".sort-id")
    const searchName = document.querySelector('input[name="searchname"]');
    
    search_bar.onclick = e => {
      e.preventDefault()
      searchUser(searchName.value)
        .then(users => {
          const userTable = document.querySelector('#userTable');
          const tbody = userTable.querySelector('tbody');
          console.log("TOTAL: ", users)
      
        tbody.innerHTML = '';
        let sortedUsers = users.sort((a,b) => a.user_id - b.user_id)
        sortedUsers.forEach(item => {
          const row = createHTMLRow({ 
            id: item.id, 
            name: item.name, 
            password: item.password, 
            email: item.email 
          });
          tbody.appendChild(row);
        })   
        })
      console.log(searchName.value)
    }

    sortName.onclick = e => {
      e.preventDefault()
      sortUserName().then(users => {
        const userTable = document.querySelector('#userTable');
        const tbody = userTable.querySelector('tbody');
    
      tbody.innerHTML = '';
      users.forEach(item => {
        const row = createHTMLRow({ 
          id: item.id, 
          name: item.name, 
          password: item.password, 
          email: item.email 
        });
        tbody.appendChild(row);
      })   
      })
    }

    sortId.onclick = e => {
      e.preventDefault()
      sortUserId().then(users => {
        const userTable = document.querySelector('#userTable');
        const tbody = userTable.querySelector('tbody');
    
      tbody.innerHTML = '';
      users.forEach(item => {
        const row = createHTMLRow({ 
          id: item.id, 
          name: item.name, 
          password: item.password, 
          email: item.email 
        });
        tbody.appendChild(row);
      })   
      })
    }
    
    let limit = 2
    getUserWithPagination(0, limit)

    paginationOne.onclick = () => {
      paginationOne.disabled = true
      paginationTwo.disabled = false
      paginationThree.disabled = false
      let offset = Number(paginationOne.innerHTML) - 1
      getUserWithPagination(offset, limit)
    }
    paginationTwo.onclick = () => {
      paginationOne.disabled = false
      paginationTwo.disabled = true
      paginationThree.disabled = false
      let offset = +paginationTwo.innerHTML
      getUserWithPagination(offset, limit)
    }
    paginationThree.onclick = () => {
      paginationOne.disabled = false
      paginationTwo.disabled = false
      paginationThree.disabled = true
      let offset = +paginationThree.innerHTML + 1
      getUserWithPagination(offset, limit)
    }
});



function getUserWithPagination(offset, limit){
  getUsers(offset, limit).then(result => {
    const {data, total} = result
    let users = data

    const userTable = document.querySelector('#userTable');
    const tbody = userTable.querySelector('tbody');
    console.log("TOTAL: ", total)

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
}