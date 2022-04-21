/*

Process Evaluation

*/

function process_evaluation(annotation) {
    let id = document.getElementById("id");
    data = { "id": id.value, "annotation": annotation };

    fetch('process-evaluation', {
        method: 'POST',
        headers: {
            Accept: 'application.json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        cache: 'default'
    }).then(response => {
        if (response.ok) {
            refresh_elements();
        } else {
            throw new Error('Something went wrong');
        }
    }).catch(error => {
        console.log(error);
    });
}

function refresh_elements() {
    let elements = {};
    let element_names = ["title", "ticker_list", "subreddit_display_name", "author_name", "url", "text"];
    element_names.forEach(name => elements[name] = document.getElementById(name));
    let id = document.getElementById("id");

    fetch('get-random-row')
        .then(response => response.json())
        .then(data => {
            id = id.setAttribute("value", data["id"]);
            Object.entries(elements).forEach(entry => {
                console.log(entry);
                const [key, value] = entry;
                value.innerHTML = data[key];
            });
        });
}