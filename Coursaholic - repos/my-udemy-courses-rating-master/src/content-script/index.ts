import axios from "axios";

window.addEventListener("load", function () {
  document
    ?.getElementsByClassName("previous")[0]
    ?.addEventListener("click", () => {
      createInterval();
    });
  document?.getElementsByClassName("next")[0]?.addEventListener("click", () => {
    createInterval();
  });

  let interval = setInterval(() => {
    if (document.querySelectorAll(".nav-slide li").length > 0) {
      document.querySelectorAll(".nav-slide li").forEach((element, key) => {
        if (key !== 2) {
          element.addEventListener("click", () => {
            createInterval();
          });
        }
      });
      clearInterval(interval);
    }
  }, 500);
});

const createInterval = () => {
  let intervalId = setInterval(() => {
    if (document.getElementsByClassName("card--learning__image").length > 0) {
      const urls = Array.from(
        document.getElementsByClassName("card--learning__image")
      );

      urls.forEach((url, index) => {
        setTimeout(() => {
          let redirectUrl = (<HTMLLinkElement>url).href;
          let regex = /course_id=(.+)/gm;
          let match = regex.exec(redirectUrl);
          if (match !== null) {
            axios
              .get(`https://www.udemy.com/course/${match[1]}`)
              .then((res) => {
                if (res.request.responseURL) {
                  axios.get(res.request.responseURL).then((res) => {
                    if (
                      (<string>res.data).includes(
                        'data-purpose="rating-number">'
                      )
                    ) {
                      regex = /data-purpose="rating-number">(.*)<\/span><svg/gm;
                    } else if (
                      (<string>res.data).includes('id="rate-count-value')
                    ) {
                      regex = /id="rate-count-value.*">(.*)<\/span>/gm;
                    }

                    match = regex.exec(res.data);
                    if (match !== null) {
                      document
                        .getElementsByClassName("card--learning__details")
                        [index].getElementsByClassName(
                          "details__start-course"
                        )[0]
                        ?.insertAdjacentText(
                          "beforeend",
                          ` - ${match[1].trim()}`
                        );
                      document
                        .getElementsByClassName("card--learning__details")
                        [index].getElementsByClassName("ellipsis")[0]
                        ?.insertAdjacentText(
                          "beforeend",
                          ` - ${match[1].trim()}`
                        );
                    }
                  });
                }
              });
          }
        }, index * 100);
      });
      clearInterval(intervalId);
    }
  }, 500);
};
createInterval();
