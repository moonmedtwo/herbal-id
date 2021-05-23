
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
      });
  } 
}
