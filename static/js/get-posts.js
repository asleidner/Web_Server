const getPosts = () => {
    // go out to API endpoint and go get all the posts from this endpoint
    //then give data to display posts function
    fetch('/api/posts')
        .then(response => response.json())
        .then(displayPosts); //callback function
};

const toHTMLElement = (post) => {
    // formatting the date:
    const options = { 
        weekday: 'long', year: 'numeric', 
        month: 'long', day: 'numeric' 
    };
    const dateFormatted = new Date(post.published).toLocaleDateString('en-US', options);
    const snippetLength = 100;
    const snippet = post.content.length > snippetLength ? post.content.substring(0, snippetLength) + '...' : post.content;
    
    return `
        <section class="post">
            <a class="detail-link" href="/post/#${post.id}">
                <h2>${post.title}</h2>
            </a>
            <div class="date">${dateFormatted}</div>
            <p>${snippet}</p>
            <p>
                <strong>Author: </strong>${post.author}
            </p>
        </section>
    `;
};

const displayPosts = (data) => {
    const entries = [];
    //iterate through each post and convert to some sort of HTML representation creating a list of chunks
    for (const post of data) {
        entries.push(toHTMLElement(post));
    }
    document.querySelector('#posts').innerHTML = entries.join('\n');
};

getPosts();