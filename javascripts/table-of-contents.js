const [contents] = document.getElementsByClassName("markdown-body");
const headings = contents.querySelectorAll("h1, h2");
const [tableOfContents] = document.getElementsByClassName("table-of-contents");
console.log(headings);

function createListFromHeadings(headings, listClass, createElement) {
    const list = document.createElement("ul");
    list.className = listClass;
    let h1Header = null;
    let nested = null;
    headings.forEach(heading => {
        const item = createElement(heading);
        if (heading.tagName === "H1") {
            list.appendChild(item);
            nested = document.createElement("ul");

            h1Header = item;
        } else {
            if (h1Header) {
                if (nested.childNodes.length === 0) {
                    h1Header.appendChild(nested);
                }
                nested.appendChild(item);
            } else {
                list.appendChild(item);
            }
        }
    });
    return list;
}

const list = createListFromHeadings(headings, "table-of-contents-list", heading => {
    const headingName = heading.childNodes[0].data;
    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = "#" + heading.id;
    link.className = "link hover-mid-gray";
    link.appendChild(document.createTextNode(headingName));
    item.appendChild(link);
    return item;
});

const abstractList = createListFromHeadings(headings, "table-of-contents-abstract-list", heading => {
    const headingName = heading.childNodes[0].data;
    const item = document.createElement("li");
    const contents = document.createElement("div");
    if (heading.tagName === "H1") {
        contents.className = "abstract-0";
    } else {
        contents.className = "abstract-1";
    }
    contents.appendChild(document.createTextNode(headingName));
    item.appendChild(contents);
    return item;
});

tableOfContents.appendChild(list);
tableOfContents.appendChild(abstractList);
