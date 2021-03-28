const dot_1 = document.querySelector("#dot_1")
const dot_2 = document.querySelector("#dot_2")
const dot_3 = document.querySelector("#dot_3")
const lead = document.querySelector(".lead")
const dev = document.querySelector(".dev")
const doc = document.querySelector(".doc")
const carousel = document.querySelector(".carousel")
const searchBox = document.querySelector(".search_box")
const urlInput = document.querySelector(".url_input")
const legit = document.querySelector(".legit")
const phishing = document.querySelector(".phishing")

const dots = [dot_1, dot_2, dot_3]
const mapping = {
    "dot_1": lead,
    "dot_2": dev,
    "dot_3": doc
}

let current = lead;
lead.classList.add("make_visible")
dev.classList.add("make_invisible")
doc.classList.add("make_invisible")
dot_1.classList.add("active")

searchBox.classList.add("make_visible")


const showSearch = () => {
    carousel.classList.remove("carousel_slide")
    carousel.classList.add("carousel_remove")
    searchBox.classList.remove("make_invisble")
    searchBox.classList.add("make_visible")
}


const slideCarousel = () => {
    carousel.classList.remove("carousel_remove")
    carousel.classList.add("carousel_slide")
    searchBox.classList.remove("make_visible")
    searchBox.classList.add("make_invisible")
}

const set = (e) => {
    e.classList.add("active")
    current.classList.remove("make_visible")
    current.classList.add("make_invisible")
    current = mapping[e.id];
    current.classList.add("make_visible")
    const hidden = dots.filter(dot => dot.id != e.id)
    hidden.forEach((ele) => {
        ele.classList.remove("active")
        mapping[ele.id].classList.add("make_invisible")
    })
}

const predict = () => {
    fetch("https://phishing-detector-app.herokuapp.com/predict", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            url: urlInput.value
        })
    }).then(res => {return res.json()})
    .then(data => {
        let ans = data["judge"]
        if(ans == "Legitimate") {
            phishing.classList.remove("phishing-active")
            phishing.classList.remove("lp-animate")
            legit.classList.add("legit-active")
            legit.classList.add("lp-animate")
        } else {
            legit.classList.remove("legit-active")
            legit.classList.remove("lp-animate")
            phishing.classList.add("phishing-active")
            phishing.classList.add("lp-animate")
        }
    }).catch(err => console.log(err))
}
