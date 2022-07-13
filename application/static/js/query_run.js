function on_run() {
      clear_all_outputs()
      const query = document.getElementById("logica_input").value
      const predicate = document.getElementById("predicate").value
      const engine = document.getElementById('connections').value
      console.log(engine)
      $.ajax({
      type: "POST",
      url: "http://localhost:8000/compile/",
      data: JSON.stringify({ "predicate" : predicate, "query_text": query }),
      contentType: "application/json",
      success: function (result) {
          const results = document.getElementById('query_results')
          const output = document.getElementById('output')
          const query_status = document.getElementById("query_status")
          query_status.style.display = "inline-block"
          query_status.style.backgroundImage = "url('static/css/images/Ok.png')"
          results.innerHTML = result["html"]
          output.innerHTML = JSON.parse(result["row_count"]) + " ROWS"
  },
  error: function (result, status) {
      console.log(result)
      const query_status = document.getElementById("query_status")
      query_status.style.display = "inline-block"
      query_status.style.backgroundImage = "url('static/css/images/Cancel.png')"
      const output = document.getElementById("output")
      output.innerHTML = result["responseJSON"]["detail"]
  }
});
}

function clear_all_outputs() {
   const results = document.getElementById('query_results')
   const output = document.getElementById('output')
   results.innerHTML = ""
   output.innerHTML = ""
}

function on_clear() {
    const logica_input = document.getElementById("logica_input")
    logica_input.value = ""
}