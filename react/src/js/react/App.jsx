/**
 * Entry-point for the react code in the app.
 * Allows us to map various URLs to page-components
 */

import React from "react";
import Reflux from "reflux";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import PageNotFound from "./help/PageNotFound";
import CreatePost from "./posts/CreatePost";
import Header from "./misc/Header";

export default class App extends Reflux.Component {
    render() {
        return (
            <div className="core-app-view">
                <Header />
                <BrowserRouter>
                    <Switch>
                        <Route exact path="/home" component={CreatePost} />
                        <Route path="*" component={PageNotFound} />
                    </Switch>
                </BrowserRouter>
            </div>
        );
    }
}
