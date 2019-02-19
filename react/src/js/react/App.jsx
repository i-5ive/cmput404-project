import React from "react";
import Reflux from "reflux";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import PageNotFound from "./help/PageNotFound";
import PostFeed from "./posts/PostFeed";
import Header from "./misc/Header";

/**
 * Entry-point for the react code in the app.
 * Allows us to map various URLs to page-components
 */
export default class App extends Reflux.Component {
    render() {
        return (
            <div className="core-app-view">
                <Header />
                <BrowserRouter>
                    <Switch>
                        <Route exact path="/feed" component={PostFeed} />
                        <Route path="*" component={PageNotFound} />
                    </Switch>
                </BrowserRouter>
            </div>
        );
    }
}
