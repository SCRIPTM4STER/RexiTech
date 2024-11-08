function showReview() {
    document.getElementById("review-card").style.display = "block";
    document.getElementById("comments-card").style.display = "none";
}

function showComments() {
    document.getElementById("review-card").style.display = "none";
    document.getElementById("comments-card").style.display = "block";
}







// csrf token
function getCSRFTokenFromCookie() {
    let csrfToken = null;
    document.cookie.split(';').forEach(cookie => {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') csrfToken = value;
    });
    return csrfToken;
}

fetch('/your-url/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCSRFTokenFromCookie(),
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ key: 'value' })
})
.then(response => response.json())
.then(data => console.log(data));
