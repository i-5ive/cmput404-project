/**
 * Entry-point for the react code in the app.
 * Allows us to map various URLs to page-components
 */

import React from "react";
import Reflux from "reflux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import PageNotFound from "./help/PageNotFound";

export default class App extends Reflux.Component {
    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route path="*" component={PageNotFound} />
                </Switch>
            </BrowserRouter>
        );
    }
}
