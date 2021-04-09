$("#username").focusout(function () {
  var $value = $(this).val();
  var $reg = /^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$/;
  if (!$value.match($reg)) {
    $("#invalid-warn-uname").empty();
    $("#invalid-warn-uname").text("invalid username");
    $("#submit-btn-register").prop("disabled", true);
    $("#invalid-warn-uname").css("color", "red");
  } else {
    $.ajax({
      url: "register",
      data: { uname: $value },
      async: true,
      dataType: "json",
      success: function (data) {
        if (data["found"] == false) {
          $("#invalid-warn-uname").empty();
          $("#invalid-warn-uname").append("<i style='font-size: 25px;' class='fa fa-check'></i>");
          $("#submit-btn-register").prop("disabled", false);
          $("#invalid-warn-uname").css("color", "green");
        } else {
          $("#invalid-warn-uname").empty();
          $("#invalid-warn-uname").text("username not available");
          $("#submit-btn-register").prop("disabled", true);
          $("#invalid-warn-uname").css("color", "red");
        }
      },
    });
  }
});

$("#email").focusout(function () {
  var $value = $(this).val();
  var $reg = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  if (!$value.match($reg)) {
    $("#invalid-warn-uname").empty();
    $("#invalid-warn-email").text("invalid email address");
    $("#submit-btn-register").prop("disabled", true);
    $("#invalid-warn-email").css("color", "red");
  } else {
    $.ajax({
      url: "register",
      data: { email: $value },
      async: true,
      dataType: "json",
      success: function (data) {
        if (data["found"] == false) {
          $("#invalid-warn-uname").empty();
          $("#invalid-warn-email").append("<i style='font-size: 25px;' class='fa fa-check'></i>")
          $("#submit-btn-register").prop("disabled", false);
          $("#invalid-warn-email").css("color", "green");
        } else {
          console.log("data: ", data);
          $("#invalid-warn-uname").empty();
          $("#invalid-warn-email").text("email already registered");
          $("#submit-btn-register").prop("disabled", true);
          $("#invalid-warn-email").css("color", "red");
        }
      },
    });
  }
});
