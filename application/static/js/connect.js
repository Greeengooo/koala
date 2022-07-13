function open_popup(id) {
    const modal = window.parent.document.getElementById(id);
    modal.style.display = "block"
}

function close_popup(id) {
    console.log(id)
    const modal = window.parent.document.getElementById(id);
    const connection_logging = document.getElementById("connection_logging")
    connection_logging.innerHTML = ""
    modal.style.display = "none"
    clear_fields()
}

function on_connect_mysql() {
    const db_name = "mysql"
    const username = document.getElementById("username")
    const password = document.getElementById("password")
    if (validate_fields([username, password])) {
        payload = JSON.stringify({
            "db_name": db_name,
            "username": username.value,
            "password": password.value
        })
        send_credentials(payload)
    }
}

function on_connect_snowflake() {
    const db_name = "snowflake"
    const username = document.getElementById("username")
    const password = document.getElementById("password")
    const account_identifier = document.getElementById("account_identifier")
    if (validate_fields([username, password, account_identifier])) {
        payload = JSON.stringify({
            "db_name": db_name,
            "username": username.value,
            "password": password.value,
            "account_identifier": account_identifier.value
        })
        send_credentials(payload)
    }
}

function validate_fields(fields) {
    var flag = true
    for (const field of fields) {
          if (field.value === "") {
              flag = false
                  console.log(field.value)
              field.style.borderColor = "red"
         }
    }
    return flag
}

function send_credentials(payload) {
    $.ajax({
      type: "POST",
      url: "http://localhost:8000/connect/",
      data: payload,
      contentType: "application/json",
      success: function (result) {
          const select = parent.document.getElementById("connections")
          const option = parent.document.createElement("option")
          option.value = result["connection"]
          option.textContent = "\u00A0 \u00A0 \u00A0 \u00A0 \u00A0 \u00A0 \u00A0 \u00A0" + result["connection"]
          select.appendChild(option)
          console.log(JSON.parse(payload))
          clear_fields(payload["db_name"])
          close_popup(JSON.parse(payload)["db_name"]+"_modal")
      },
      error: function (result, status) {
          clear_fields()
          const logging = document.getElementById("connection_logging")
          console.log(result["responseJSON"]["detail"])
          logging.innerHTML = result["responseJSON"]["detail"]
      }
})
}

function clear_fields() {
    const username = document.getElementById("username")
    const password = document.getElementById("password")
    const db_name = document.getElementById("db_name")
    if (db_name.value === "snowflake") {
        const account_identifier = document.getElementById("account_identifier")
        account_identifier.value = ""
        account_identifier.style.borderColor = "black"
    }
        username.value = ""
        username.style.borderColor = "black"
        password.value = ""
        password.style.borderColor = "black"
}