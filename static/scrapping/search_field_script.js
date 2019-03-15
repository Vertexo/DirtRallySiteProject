function searchFunction() {

        var searchText = document.getElementById('searchField').value;
        if (searchText != '') {
            location.href = '/driverstats/' + searchText + '/'
        }  
        else {
            location.href = '/driverstats/notfound/'
        }      
    }


var input = document.getElementById("searchField");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("myBtn").click();
  }
});
