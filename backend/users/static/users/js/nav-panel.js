"use strict"; 
 
const navPanel = document.body.querySelector(".nav-panel__wrapper");
const navPanelItems = navPanel.querySelectorAll(".nav-panel__item");
let activeItem = navPanel.querySelector(".nav-panel__item");

function clickItem(item) {
    if (activeItem === item) {
        return;
    }
    if (activeItem) {
        activeItem.classList.remove("active");
    } 
    item.classList.add("active");
    activeItem = item;
}

navPanelItems.forEach(item => {
    item.addEventListener("click", () => clickItem(item));
});

navPanel.querySelector(".nav-panel__button_show").addEventListener("click", () => {
    navPanel.querySelector(".nav-panel__screen").classList.toggle("show");
    if (navPanel.querySelector(".nav-panel__screen").classList.contains("show")) {
        navPanel.querySelector(".nav-panel__button_show").innerHTML = "<";
    } else {
        navPanel.querySelector(".nav-panel__button_show").innerHTML = ">";
    }
});