document.addEventListener('DOMContentLoaded', function() {  
    const paginationOne = document.querySelector(".one")
    const paginationTwo = document.querySelector(".two")
    const paginationThree = document.querySelector(".three")

    getUserWithPagination(0, 2)
    let limit = 2

    paginationOne.onclick = () => {
      paginationOne.disabled = true
      paginationTwo.disabled = false
      paginationThree.disabled = false
      let offset = +paginationOne.innerHTML - 1
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