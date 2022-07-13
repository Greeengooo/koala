function on_select_ds() {
    const choice = document.getElementById('connections').value
    console.log(choice)
    $.ajax({
      type: "POST",
      url: "http://localhost:8000/select/",
      data: JSON.stringify({ "connection": choice }),
      contentType: "application/json",
      success: function (result) {
          console.log(result)
          load_ds_info()
      },
      error: function (result, status) {
        console.log(result)
      }
    })
}


function load_ds_info() {
    $.ajax({
        type: "GET",
        url: "http://localhost:8000/data-source-info/",
        success: function (result) {
            div = document.getElementById('ds_info')
            div.innerHTML = ""
            for (var key in result) {
                button = document.createElement("button")
                button.type = "button"
                button.classList.add("collapsible")
                icon = document.createElement("i")
                icon.id = "table_icon"
                button.textContent = key
                button.prepend(icon)
                div.appendChild(button)
                content = document.createElement("div")
                content.classList.add("content")
                for (const table of result[key]) {
                    p = document.createElement("p")
                    p.textContent = table
                    content.appendChild(p)
                }
                div.appendChild(content)
            }
            add_collapsible_listeners()
        },
        error: function (result, status) {
            console.log(result)
        }
    })
}

function add_collapsible_listeners() {
    var coll = document.getElementsByClassName("collapsible")
    console.log(coll)
    var i;
    console.log(coll)
    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      });
    }
}