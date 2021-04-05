var tag_list = [];

//This function add the tag into the tag div from select tag
$("#add_tag_from_select").click(function () {
  var tag_name = $("#select_tag option:selected").text();
  $("#select_tag option[value='Select']").attr("selected", true);
  console.log(tag_name);

  var check = true;
  $("#tags_div")
    .children()
    .each(function () {
      text = $(this).text();
      if (text == tag_name) {
        check = false;
      }
    });
  
  if (
    tag_name != "Select" &&
    tag_list.length < 10 &&
    check &&
    /^[A-Za-z0-9_-]*$/.test(tag_name)
  ) {
    var id = "tag_" + tag_name + "_safe";
    $("#tags_div").append(
      '<button type="button" id="' +
        id +
        '" onclick=remove_me("' +
        id +
        '") class="btn btn-dark border m-1 tags_selected">' +
        tag_name +
        "</button>"
    );
    tag_list.push(tag_name);
  }

  if (tag_list.length >= 10) {
    $("#tag_limit_warning").text("Tag limit exceed");
    $("#tag_limit_warning").css("display", "block");
    setTimeout(function () {
      $("#tag_limit_warning").css("display", "none");
    }, 4000);
  }

  if (!/^[A-Za-z0-9_-]*$/.test(tag_name)) {
    $("#tag_limit_warning").text(
      "only english words allowed without space you can use _ at the place of space(' ')"
    );
    $("#tag_limit_warning").css("display", "block");
    setTimeout(function () {
      $("#tag_limit_warning").css("display", "none");
    }, 4000);
  }
    if (check == false) {
      $("#tag_limit_warning").text("This tag is already selected");
      $("#tag_limit_warning").css("display", "block");
      setTimeout(function () {
        $("#tag_limit_warning").css("display", "none");
      }, 4000);
    }
});

//This function add the tag into the tag div from input tag
$("#add_tag_from_input").click(function () {
  var tag_name = $("#input_tag").val();
  $("#input_tag").val("");

  var check = true;
  $("#tags_div")
    .children()
    .each(function () {
      text = $(this).text();
      if (text == tag_name) {
        check = false;
      }
    });
  if (
    tag_name != "" &&
    tag_list.length < 10 &&
    check &&
    /^[A-Za-z0-9_-]*$/.test(tag_name)
  ) {
    var id = "tag_" + tag_name + "_safe";
    $("#tags_div").append(
      '<button type="button" id="' +
        id +
        '" onclick=remove_me("' +
        id +
        '") class="btn btn-dark border m-1 tags_selected" style="border-radius: 5px;">' +
        tag_name +
        "</button>"
    );
    tag_list.push(tag_name);
  }
  if (tag_list.length >= 10) {
    $("#tag_limit_warning").text("Tag limit exceed");
    $("#tag_limit_warning").css("display", "block");
    setTimeout(function () {
      $("#tag_limit_warning").css("display", "none");
    }, 4000);
  }
  if (!/^[A-Za-z0-9_-]*$/.test(tag_name)) {
    $("#tag_limit_warning").text("only english words allowed without space you can use _ at the place of space(' ')");
    $("#tag_limit_warning").css("display", "block");
    setTimeout(function () {
      $("#tag_limit_warning").css("display", "none");
    }, 4000);
  }
  if (check == false) {
    $("#tag_limit_warning").text("This tag is already selected");
    $("#tag_limit_warning").css("display", "block");
    setTimeout(function () {
      $("#tag_limit_warning").css("display", "none");
    }, 4000);
  }
});

//This function removes the tag from the tag is user clicks on the tag
function remove_me(id) {
  $("#" + id).remove();
  tag_to_remove = id.slice(4, id.length - 5);
  for (var i = 0; i < tag_list.length; i++) {
    if (tag_list[i] === tag_to_remove) {
      tag_list.splice(i, 1);
      i--;
    }
  }
}

//This function listens enter key down event on tag input field to input the tag
$("#input_tag").keydown(function (e) {
  if (e.keyCode == 13) {
    $("#add_tag_from_input").click();
  }
});

//This function submits the blog form through POST, if user clicks on the send to publish button
function submit_blog_form() {
  var tags_string = "";
  for (i in tag_list) {
    if (i != tag_list.length - 1) {
      tags_string += tag_list[i] + ",";
    } else {
      tags_string += tag_list[i];
    }
  }
  $("#hidden_input_tags").val(tags_string);
  $("#blog-form").submit();
  alert("Your blog is successfully sent to be published");
}

//This function saves the blog form as draft means sends a ajax POST to submit the form
function save_as_draft_func(id) {
  var tags_string = "";
  for (i in tag_list) {
    if (i != tag_list.length - 1) {
      tags_string += tag_list[i] + ",";
    } else {
      tags_string += tag_list[i];
    }
  }
  if (tags_string == "") {
    $("#tag_limit_warning").text("Please select or create atleast one tag");
    $("#tag_limit_warning").css("display", "block");
    setTimeout(function () {
      $("#tag_limit_warning").css("display", "none");
    }, 4000);
  } else {
    var heading = $("#blog_heading").val();
    var editor = CKEDITOR.instances["editor"].getData();
    var img_url = $("#banner_image_url").val();
    var description = $("#description").val();
    $.ajax({
      url: "save_draft",
      data: {
        img_url: img_url,
        tags: tags_string,
        editor: editor,
        heading: heading,
        description: description,
      },
      async: true,
      dataType: "json",
      success: function (data) {
        if ("saved" in data) {
          if (id == "preview") {
            //open an new browser window for blog preview (id is coming from the server stored in data)
            var url_mask1 = `/blog/preview/${data["id"].toString()}`
            var win = window.open(
              url_mask1,
              "Popup Window",
              "width=1100, height=800, top=40, left=10, resizable=1, menubar=yes",
            );

            //locate the current window to edit blog with passing id
            var url_mask2 = `/edit/blog/${data["id"].toString()}`;
            window.location.replace(url_mask2);

            win.focus();
          } else {
            alert("blog is saved successfully");
            window.location.replace("/dashboard/writer");
          }
        } else {
          alert("something went wrong please try again");
        }
      },
    });
  }
}
