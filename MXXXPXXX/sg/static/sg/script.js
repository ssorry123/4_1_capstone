// 2.  글쓰기 페이지

// 이미지 첨부시 미리보기

function setThumbnail(event) {
  var reader = new FileReader();

  reader.onload = function (event) {
    var img = document.createElement("img");
    img.setAttribute("src", event.target.result);
    document.querySelector("div#image_container").appendChild(img);
  };

  reader.readAsDataURL(event.target.files[0]);
}

//제목 단어 추천

function recommendTitle(val, csrf_token) {
  var recommend = "";
  $.ajax({
    type: "POST",
    url: "recommend/",
    data: { 'content': val, 'csrfmiddlewaretoken': csrf_token },
    dataType: "json",
    success: function (response) {
      recommend = response.recommend;
      var res1 = val + recommend;
      var res2 = val;
      var res3 = val;
      var res4 = val;
      var res5 = val;

      if (val == "") {
        document.getElementById('result').value = "0";
      } else {
        document.getElementById('result1').value = res1;
        document.getElementById('result2').value = res2;
        document.getElementById('result3').value = res3;
        document.getElementById('result4').value = res4;
        document.getElementById('result5').value = res5;
      }
    }
  });
}

function addTitle(val, csrf_token) {
  var new_title = val
  document.getElementById('title').value = val
  recommendTitle(new_title, csrf_token);
}

//이미지 클릭시 자동 넣기

function mark(img) {
  img.style.border = "1px solid blue";
}