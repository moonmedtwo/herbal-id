
function upload() {
  var files = document.getElementById("img_uploaded").files;
  if (files.length > 0) {
      var fileReader = new FileReader();
 
      fileReader.onload = function (event) {
          document.getElementById("image").setAttribute("src", event.target.result);
      };
 
      readfile = fileReader.readAsDataURL(files[0])
      console.log(files)

      fetch("/upload",
      {
          method: "POST",
          body: files[0]
      })
      .then(response => response.json())
      .then(data => 
        {
            console.log(data);
            document.getElementById("name_placeholder").textContent = data["name"] + " - Xác suất: " + data["prob"] + "%"
            document.getElementById("intro_placeholder").textContent = data["intro"]
            document.getElementById("desc_placeholder").textContent = data["desc"]
            document.getElementById("attr_placeholder").textContent = data["attr"]
            document.getElementById("function_placeholder").textContent = data["function"]
            document.getElementById("usage_placeholder").textContent = data["usage"]
            document.getElementById("storage_placeholder").textContent = data["storage"]
        });
  } 
}
