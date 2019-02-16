import React from "react";
import Reflux from "reflux";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import PageNotFound from "./help/PageNotFound";
import PostPage from "./posts/PostPage";
import Header from "./misc/Header";


/**
 * Entry-point for the react code in the app.
 * Allows us to map various URLs to page-components
 */
export default class App extends Reflux.Component {
    render() {
        return (
            <div>
                <Header />
                <BrowserRouter>
                    <Switch>
                        <PostPage/>
                    </Switch>
                </BrowserRouter>
            </div>
        );
    }
}
