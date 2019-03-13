// Takes the top-level react component and attaches it to the DOM.

import React from "react";
import ReactDOM from "react-dom";
import App from "./js/react/App";

import { BrowserRouter } from "react-router-dom";

import "./scss/main";

const contentWrapper = document.getElementById("react-entrypoint");

if (contentWrapper) {
    ReactDOM.render(
        <BrowserRouter basename={'/app'} >
            <App />
        </BrowserRouter>
    , contentWrapper);
}
